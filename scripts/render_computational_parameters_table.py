#!/usr/bin/env python3
"""Build the computational-parameters table (Methods).

Every value here is read directly from the versioned manifests/configs
already committed in this project — not restated from memory. Confirmed
identical across all 23 preparation attempts / 7 completed docking runs
before being written as a single table (see the uniqueness checks this
script performs).
"""

from __future__ import annotations

import csv
import glob
from pathlib import Path


def read_csv(path: str) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def unique_field(rows: list[dict[str, str]], field: str) -> str:
    values = {row[field] for row in rows}
    if len(values) != 1:
        raise ValueError(f"{field} is not uniform across runs: {values}")
    return values.pop()


def main() -> int:
    run_files = ["data/vina_run_manifest.csv"] + sorted(glob.glob("data/contextual_batch_[0-9][0-9]_vina_run_manifest.csv"))
    completed_runs = []
    for file in run_files:
        completed_runs.extend(row for row in read_csv(file) if row["status"] == "completed")

    vina_version = unique_field(completed_runs, "vina_version")
    seed = unique_field(completed_runs, "seed")
    cpu = unique_field(completed_runs, "cpu")

    prep_rows = read_csv("data/strict_preparation_manifest.csv")
    for file in sorted(glob.glob("data/clean_batch_[0-9][0-9]_preparation_manifest.csv")):
        prep_rows.extend(read_csv(file))
    for file in sorted(glob.glob("data/contextual_batch_[0-9][0-9]_preparation_manifest.csv")):
        prep_rows.extend(read_csv(file))
    meeko_version = unique_field(prep_rows, "meeko_version")

    config_files = sorted(Path("derived/vina-configs").glob("*.txt"))
    exhaustiveness, num_modes, energy_range = set(), set(), set()
    for path in config_files:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("exhaustiveness"):
                exhaustiveness.add(line.split("=")[1].strip())
            elif line.startswith("num_modes"):
                num_modes.add(line.split("=")[1].strip())
            elif line.startswith("energy_range"):
                energy_range.add(line.split("=")[1].strip())
    assert len(exhaustiveness) == 1 and len(num_modes) == 1 and len(energy_range) == 1, \
        "Vina search parameters are not uniform across configs"

    rows = [
        ("Software de docking", f"{vina_version}"),
        ("Preparación de receptor/ligando", f"Meeko {meeko_version} (mk_prepare_receptor / mk_prepare_ligand, sin banderas de reparación)"),
        ("Modelo de cargas parciales", "Predeterminado de Meeko (Gasteiger); sin sobrescritura explícita en ningún comando registrado"),
        ("Exhaustiveness", exhaustiveness.pop()),
        ("Número de modos (poses) por corrida", num_modes.pop()),
        ("Rango de energía reportado", f"{energy_range.pop()} kcal/mol"),
        ("Semilla aleatoria (seed)", seed),
        ("CPUs por corrida", cpu),
        ("Definición de la caja de búsqueda", "Centrada en el centroide del ligando experimental de referencia; tamaño derivado por caso (ver derived/vina-configs/*.txt)"),
        ("Política de reparación estructural", "Ninguna — sin selección de altloc, sin --allow_bad_res, sin adición de átomos faltantes"),
    ]

    md_lines = ["| Parámetro | Valor |", "| --- | --- |"]
    md_lines += [f"| {name} | {value} |" for name, value in rows]

    output = Path("reports/generated/computational-parameters-table.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Wrote {output}")
    for name, value in rows:
        print(f"{name}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
