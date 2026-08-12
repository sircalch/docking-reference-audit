#!/usr/bin/env python3
"""Run the frozen, eligible reference-pose Vina subpilot through WSL.

Only rows with both strict receptor and ideal-ligand preparation marked as
prepared are eligible.  The runner uses a fixed seed, one CPU and the frozen
box configuration; it neither retries failed cases with changed settings nor
selects a preferred pose.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


SEED = 20260812
CPU = 1
FIELDS = (
    "case_id", "pdb_id", "receptor_path", "receptor_sha256", "ligand_path", "ligand_sha256",
    "config_path", "config_sha256", "output_path", "output_sha256", "log_path", "log_sha256",
    "vina_version", "seed", "cpu", "command", "exit_code", "status", "completed_at_utc",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def windows_to_wsl(path: Path) -> str:
    absolute = path.resolve()
    drive = absolute.drive.rstrip(":").lower()
    return "/mnt/" + drive + absolute.as_posix()[2:]


def wsl_vina_version() -> str:
    run = subprocess.run(["wsl.exe", "-e", "vina", "--version"], capture_output=True, text=True, check=True)
    return run.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receptors", type=Path, default=Path("data/strict_preparation_manifest.csv"))
    parser.add_argument("--ligands", type=Path, default=Path("data/ligand_preparation_manifest.csv"))
    parser.add_argument("--boxes", type=Path, default=Path("data/vina_box_manifest.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("derived/vina-runs"))
    parser.add_argument("--log-dir", type=Path, default=Path("reports/generated/vina-runs"))
    parser.add_argument("--manifest", type=Path, default=Path("data/vina_run_manifest.csv"))
    args = parser.parse_args()
    receptors = {row["case_id"]: row for row in read_csv(args.receptors) if row["status"] == "prepared"}
    ligands = {row["case_id"]: row for row in read_csv(args.ligands) if row["status"] == "prepared"}
    boxes = {row["case_id"]: row for row in read_csv(args.boxes)}
    eligible = sorted(set(receptors) & set(ligands) & set(boxes))
    if not eligible:
        raise SystemExit("No cases have prepared receptor, ligand and frozen box")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.log_dir.mkdir(parents=True, exist_ok=True)
    vina_version = wsl_vina_version()
    rows: list[dict[str, str]] = []
    for case_id in eligible:
        receptor, ligand, box = receptors[case_id], ligands[case_id], boxes[case_id]
        output = args.output_dir / f"{case_id}_{receptor['pdb_id']}_out.pdbqt"
        log = args.log_dir / f"{case_id}_{receptor['pdb_id']}.log"
        command = [
            "vina", "--receptor", windows_to_wsl(Path(receptor["output_path"])),
            "--ligand", windows_to_wsl(Path(ligand["pdbqt_path"])),
            "--config", windows_to_wsl(Path(box["config_path"])),
            "--out", windows_to_wsl(output),
            "--seed", str(SEED), "--cpu", str(CPU),
        ]
        complete = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        run = subprocess.run(["wsl.exe", "-e", *command], capture_output=True, text=True, check=False)
        # Vina 1.2.5 lacks a --log option. Store both streams ourselves, which
        # also keeps the recorded command identical across supported versions.
        log.write_text(
            "command: " + json.dumps(command) + "\n"
            + f"exit_code: {run.returncode}\n\nstdout:\n{run.stdout}\n\nstderr:\n{run.stderr}\n",
            encoding="utf-8",
        )
        succeeded = run.returncode == 0 and output.exists() and log.exists()
        rows.append({
            "case_id": case_id, "pdb_id": receptor["pdb_id"],
            "receptor_path": receptor["output_path"], "receptor_sha256": receptor["output_sha256"],
            "ligand_path": ligand["pdbqt_path"], "ligand_sha256": ligand["pdbqt_sha256"],
            "config_path": box["config_path"], "config_sha256": box["config_sha256"],
            "output_path": output.as_posix(), "output_sha256": sha256(output) if succeeded else "",
            "log_path": log.as_posix(), "log_sha256": sha256(log) if succeeded else "",
            "vina_version": vina_version, "seed": str(SEED), "cpu": str(CPU), "command": json.dumps(command),
            "exit_code": str(run.returncode), "status": "completed" if succeeded else "failed", "completed_at_utc": complete,
        })
        print(f"{case_id}: {'completed' if succeeded else 'failed'}")
    with args.manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return 0 if all(row["status"] == "completed" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
