#!/usr/bin/env python3
"""Build the full 30-candidate inventory table (supplementary Table).

Joins data/candidates.csv (registration), data/eligibility_register.csv
(structural classification), and every strict-preparation manifest (all
clean_batch_*/contextual_batch_* files) to produce one row per registered
candidate: PDB ID, ligand, classification stratum, and preparation/docking
outcome. No new measurement — every field is copied from data already
committed and verified elsewhere in this project.
"""

from __future__ import annotations

import csv
from pathlib import Path

DATA = Path("data")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    candidates = {row["case_id"]: row for row in read_csv(DATA / "candidates.csv")}
    eligibility = {row["case_id"]: row for row in read_csv(DATA / "eligibility_register.csv")}

    prep_status: dict[str, tuple[str, str]] = {}
    # Legacy manifest for the original 2-case subpilot (pilot-001, pilot-007)
    # plus pilot-004 — predates the clean/contextual batch split. Read first
    # so any later batch re-run of the same case_id takes precedence.
    for row in read_csv(DATA / "strict_preparation_manifest.csv"):
        prep_status[row["case_id"]] = (row["status"], row.get("normalized_error_class", ""))
    for manifest in sorted(DATA.glob("clean_batch_[0-9][0-9]_preparation_manifest.csv")):
        for row in read_csv(manifest):
            prep_status[row["case_id"]] = (row["status"], row.get("normalized_error_class", ""))
    for manifest in sorted(DATA.glob("contextual_batch_[0-9][0-9]_preparation_manifest.csv")):
        for row in read_csv(manifest):
            prep_status[row["case_id"]] = (row["status"], row.get("normalized_error_class", ""))

    docking_status: dict[str, str] = {}
    for row in read_csv(DATA / "vina_run_manifest.csv"):
        if row["status"] == "completed":
            docking_status[row["case_id"]] = "completado"
    for manifest in sorted(DATA.glob("contextual_batch_[0-9][0-9]_vina_run_manifest.csv")):
        for row in read_csv(manifest):
            if row["status"] == "completed":
                docking_status[row["case_id"]] = "completado"

    rows = []
    for case_id in sorted(candidates, key=lambda c: (0 if c.startswith("pilot") else 1, c)):
        cand = candidates[case_id]
        elig = eligibility.get(case_id, {})
        status, error_class = prep_status.get(case_id, ("no intentado", ""))
        outcome = {
            "prepared": "preparado",
            "failed": f"fallido ({error_class})" if error_class else "fallido",
        }.get(status, status)
        docking = docking_status.get(case_id, "—")
        rows.append({
            "case_id": case_id,
            "pdb_id": cand["pdb_id"],
            "ligand": cand["ligand_component_id"],
            "stratum": elig.get("stratum", "no clasificado"),
            "preparation_outcome": outcome,
            "docking_outcome": docking,
        })

    output = DATA / "candidate_inventory_table.csv"
    fieldnames = ["case_id", "pdb_id", "ligand", "stratum", "preparation_outcome", "docking_outcome"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {output}")

    # Markdown table for direct inclusion in reports
    md_lines = [
        "| Case | PDB | Ligando | Estrato | Preparación | Docking |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        md_lines.append(
            f"| {row['case_id']} | {row['pdb_id']} | {row['ligand']} | {row['stratum']} | "
            f"{row['preparation_outcome']} | {row['docking_outcome']} |"
        )
    Path("reports/generated/candidate-inventory-table.md").parent.mkdir(parents=True, exist_ok=True)
    Path("reports/generated/candidate-inventory-table.md").write_text("\n".join(md_lines), encoding="utf-8")
    print("Wrote reports/generated/candidate-inventory-table.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
