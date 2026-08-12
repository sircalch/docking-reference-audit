#!/usr/bin/env python3
"""Retrieve RCSB ideal ligand SDFs and prepare them for frozen subpilot docking."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import meeko


RCSB_LIGAND_ROOT = "https://files.rcsb.org/ligands/download"
FIELDS = (
    "case_id", "pdb_id", "component_id", "source_url", "sdf_path", "sdf_sha256",
    "pdbqt_path", "pdbqt_sha256", "pdbqt_bytes", "meeko_version", "command",
    "exit_code", "status", "log_path", "completed_at_utc",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def ligand_executable() -> Path:
    executable = Path(sys.executable).parent / "Scripts" / "mk_prepare_ligand.exe"
    if not executable.exists():
        raise FileNotFoundError(f"Meeko ligand executable not found at {executable}")
    return executable


def retrieve_sdf(component: str, destination: Path) -> str:
    source_url = f"{RCSB_LIGAND_ROOT}/{component}_ideal.sdf"
    request = Request(source_url, headers={"User-Agent": "docking-reference-audit/0.1", "Accept": "chemical/x-mdl-sdfile"})
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed HTTPS archive root
        payload = response.read()
    if b"V2000" not in payload and b"V3000" not in payload:
        raise ValueError(f"{component}: response is not an SDF molecule")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    return source_url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=Path("data/candidates.csv"))
    parser.add_argument("--preparation", type=Path, default=Path("data/strict_preparation_manifest.csv"))
    parser.add_argument("--raw-dir", type=Path, default=Path("raw/ligands"))
    parser.add_argument("--output-dir", type=Path, default=Path("derived/strict-ligands"))
    parser.add_argument("--log-dir", type=Path, default=Path("reports/generated/ligand-preparation"))
    parser.add_argument("--manifest", type=Path, default=Path("data/ligand_preparation_manifest.csv"))
    args = parser.parse_args()
    candidates = {row["case_id"]: row for row in read_csv(args.candidates)}
    eligible = [row for row in read_csv(args.preparation) if row["status"] == "prepared"]
    executable = ligand_executable()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.log_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for receptor in eligible:
        candidate = candidates[receptor["case_id"]]
        component = candidate["ligand_component_id"].upper()
        sdf = args.raw_dir / f"{receptor['case_id']}_{component}_ideal.sdf"
        output = args.output_dir / f"{receptor['case_id']}_{component}.pdbqt"
        log = args.log_dir / f"{receptor['case_id']}_{component}.log"
        source_url = retrieve_sdf(component, sdf)
        command = [str(executable), "--mol", str(sdf), "--out", str(output)]
        completed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        run = subprocess.run(command, capture_output=True, text=True, check=False)
        log.write_text(
            "command: " + json.dumps(command) + "\n"
            + f"exit_code: {run.returncode}\n\nstdout:\n{run.stdout}\n\nstderr:\n{run.stderr}\n",
            encoding="utf-8",
        )
        succeeded = run.returncode == 0 and output.exists()
        rows.append({
            "case_id": receptor["case_id"],
            "pdb_id": receptor["pdb_id"],
            "component_id": component,
            "source_url": source_url,
            "sdf_path": sdf.as_posix(),
            "sdf_sha256": sha256(sdf),
            "pdbqt_path": output.as_posix(),
            "pdbqt_sha256": sha256(output) if succeeded else "",
            "pdbqt_bytes": str(output.stat().st_size) if succeeded else "",
            "meeko_version": getattr(meeko, "__version__", "unknown"),
            "command": json.dumps(command),
            "exit_code": str(run.returncode),
            "status": "prepared" if succeeded else "failed",
            "log_path": log.as_posix(),
            "completed_at_utc": completed_at,
        })
        print(f"{receptor['case_id']} {component}: {'prepared' if succeeded else 'failed'}")

    with args.manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return 0 if all(row["status"] == "prepared" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
