#!/usr/bin/env python3
"""Verify hashes and cross-manifest consistency for the docking subpilot."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_hash(label: str, raw_path: str, expected: str, failures: list[str]) -> None:
    path = Path(raw_path)
    if not path.exists():
        failures.append(f"{label}: missing file {path}")
    elif digest(path) != expected:
        failures.append(f"{label}: SHA-256 mismatch for {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receptors", type=Path, default=Path("data/strict_preparation_manifest.csv"))
    parser.add_argument("--ligands", type=Path, default=Path("data/ligand_preparation_manifest.csv"))
    parser.add_argument("--boxes", type=Path, default=Path("data/vina_box_manifest.csv"))
    parser.add_argument("--runs", type=Path, default=Path("data/vina_run_manifest.csv"))
    parser.add_argument("--scores", type=Path, default=Path("data/vina_pose_scores.csv"))
    parser.add_argument("--rmsd", type=Path, default=Path("data/reference_pose_rmsd.csv"))
    args = parser.parse_args()
    failures: list[str] = []
    receptor = {row["case_id"]: row for row in rows(args.receptors) if row["status"] == "prepared"}
    ligand = {row["case_id"]: row for row in rows(args.ligands) if row["status"] == "prepared"}
    box = {row["case_id"]: row for row in rows(args.boxes)}
    runs = [row for row in rows(args.runs) if row["status"] == "completed"]
    scores = rows(args.scores)
    rmsd = rows(args.rmsd)

    for item in receptor.values():
        verify_hash(f"receptor {item['case_id']}", item["output_path"], item["output_sha256"], failures)
    for item in ligand.values():
        verify_hash(f"ligand {item['case_id']}", item["pdbqt_path"], item["pdbqt_sha256"], failures)
    for item in box.values():
        verify_hash(f"box {item['case_id']}", item["config_path"], item["config_sha256"], failures)
    for run in runs:
        case_id = run["case_id"]
        if case_id not in receptor or case_id not in ligand or case_id not in box:
            failures.append(f"run {case_id}: missing prepared dependency")
            continue
        for label, path_key, hash_key in (("output", "output_path", "output_sha256"), ("log", "log_path", "log_sha256")):
            verify_hash(f"run {case_id} {label}", run[path_key], run[hash_key], failures)
        if run["receptor_sha256"] != receptor[case_id]["output_sha256"]:
            failures.append(f"run {case_id}: receptor hash does not match receptor manifest")
        if run["ligand_sha256"] != ligand[case_id]["pdbqt_sha256"]:
            failures.append(f"run {case_id}: ligand hash does not match ligand manifest")
        if run["config_sha256"] != box[case_id]["config_sha256"]:
            failures.append(f"run {case_id}: box hash does not match box manifest")
        if len([row for row in scores if row["case_id"] == case_id]) != 9:
            failures.append(f"run {case_id}: expected nine retained score rows")
        verified_rmsd = [row for row in rmsd if row["case_id"] == case_id and row["mapping_status"] == "verified"]
        if len(verified_rmsd) != 9:
            failures.append(f"run {case_id}: expected nine verified reference-RMSD rows")

    if failures:
        print("EVIDENCE VERIFICATION FAILED")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print(f"EVIDENCE VERIFIED: {len(runs)} completed runs; {len(scores)} score rows; {len(rmsd)} RMSD rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
