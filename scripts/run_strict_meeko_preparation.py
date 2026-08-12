#!/usr/bin/env python3
"""Run the frozen strict Meeko receptor preparation subpilot.

No repair, alternate-location choice, template addition or residue deletion is
requested.  A non-zero exit code is retained in the manifest as an outcome.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import meeko


FIELDS = (
    "case_id", "pdb_id", "receptor_chain", "input_path", "input_sha256",
    "output_path", "output_sha256", "output_bytes", "meeko_version", "command",
    "exit_code", "status", "normalized_error_class", "log_path", "completed_at_utc",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_subpilot(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get("status") == "accepted"]


def meeko_executable() -> Path:
    candidate = Path(sys.executable).parent / "Scripts" / "mk_prepare_receptor.exe"
    if not candidate.exists():
        raise FileNotFoundError(f"Meeko receptor executable not found at {candidate}")
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subpilot", type=Path, default=Path("data/strict_subpilot.csv"))
    parser.add_argument("--input-dir", type=Path, default=Path("derived/strict-receptors"))
    parser.add_argument("--output-dir", type=Path, default=Path("derived/strict-prepared"))
    parser.add_argument("--log-dir", type=Path, default=Path("reports/generated/strict-preparation"))
    parser.add_argument("--manifest", type=Path, default=Path("data/strict_preparation_manifest.csv"))
    args = parser.parse_args()
    executable = meeko_executable()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.log_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for case in load_subpilot(args.subpilot):
        pdb_id = case["pdb_id"].upper()
        chain = case["receptor_chain"]
        stem = f"{case['case_id']}_{pdb_id}_chain-{chain}"
        source = args.input_dir / f"{stem}_strict.pdb"
        output = args.output_dir / f"{stem}.pdbqt"
        log_path = args.log_dir / f"{stem}.log"
        command = [str(executable), "--read_pdb", str(source), "--output_basename", str(args.output_dir / stem), "--write_pdbqt", str(output)]
        completed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        run = subprocess.run(command, capture_output=True, text=True, check=False)
        log_path.write_text(
            "command: " + json.dumps(command) + "\n"
            + f"exit_code: {run.returncode}\n\nstdout:\n{run.stdout}\n\nstderr:\n{run.stderr}\n",
            encoding="utf-8",
        )
        succeeded = run.returncode == 0 and output.exists()
        combined_output = f"{run.stdout}\n{run.stderr}"
        error_class = ""
        has_altloc = "Residues with alternate location" in combined_output
        has_template_failure = "Template matching failed" in combined_output
        if not succeeded and has_altloc and has_template_failure:
            error_class = "meeko_alternate_location_and_template_matching_failed"
        elif not succeeded and has_altloc:
            error_class = "meeko_alternate_location_requires_choice"
        elif not succeeded and has_template_failure:
            error_class = "meeko_template_matching_failed"
        elif not succeeded:
            error_class = "meeko_preparation_failed"
        rows.append({
            "case_id": case["case_id"],
            "pdb_id": pdb_id,
            "receptor_chain": chain,
            "input_path": source.as_posix(),
            "input_sha256": sha256(source),
            "output_path": output.as_posix(),
            "output_sha256": sha256(output) if succeeded else "",
            "output_bytes": str(output.stat().st_size) if succeeded else "",
            "meeko_version": getattr(meeko, "__version__", "unknown"),
            "command": json.dumps(command),
            "exit_code": str(run.returncode),
            "status": "prepared" if succeeded else "failed",
            "normalized_error_class": error_class,
            "log_path": log_path.as_posix(),
            "completed_at_utc": completed_at,
        })
        print(f"{case['case_id']} {pdb_id}: {'prepared' if succeeded else 'failed'}")
    with args.manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return 0 if all(row["status"] == "prepared" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
