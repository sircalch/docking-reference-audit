#!/usr/bin/env python3
"""Download original RCSB mmCIF files and create a checksummed retrieval manifest.

No structural preparation, repair or docking is performed here.  The script
stores the original coordinate files separately from the versioned manifest so
their provenance is retained without treating downloaded archive content as
project-authored source code.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


FILES_ROOT = "https://files.rcsb.org/download"
USER_AGENT = "docking-reference-audit/0.1 (structure collection)"
MANIFEST_FIELDS = (
    "case_id",
    "pdb_id",
    "format",
    "source_url",
    "retrieved_at_utc",
    "local_path",
    "bytes",
    "sha256",
    "status",
    "error",
)


def load_candidates(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get("status") == "candidate"]


def load_existing_manifest(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["case_id"]: row for row in csv.DictReader(handle)}


def verified_cached_row(
    candidate: dict[str, str], destination: Path, existing: dict[str, str] | None
) -> dict[str, str] | None:
    """Return an unchanged prior record only when its local bytes still match."""
    if not existing or existing.get("status") != "retrieved" or not destination.exists():
        return None
    if existing.get("pdb_id", "").upper() != candidate["pdb_id"].upper():
        return None
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    if digest != existing.get("sha256"):
        return None
    return {field: existing.get(field, "") for field in MANIFEST_FIELDS}


def download_mmcif(pdb_id: str, timeout: int) -> bytes:
    source_url = f"{FILES_ROOT}/{pdb_id.upper()}.cif"
    request = Request(source_url, headers={"User-Agent": USER_AGENT, "Accept": "chemical/x-cif,text/plain"})
    with urlopen(request, timeout=timeout) as response:  # nosec B310: fixed HTTPS archive root
        content = response.read()
    if not content.startswith(b"data_"):
        raise ValueError(f"{pdb_id}: response is not an mmCIF data block")
    return content


def write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=Path("data/candidates.csv"))
    parser.add_argument("--raw-dir", type=Path, default=Path("raw/structures"))
    parser.add_argument("--manifest", type=Path, default=Path("data/retrieval_manifest.csv"))
    parser.add_argument("--timeout", type=int, default=60, help="per-download HTTPS timeout in seconds")
    args = parser.parse_args()

    existing_rows = load_existing_manifest(args.manifest)
    rows: list[dict[str, str]] = []
    for candidate in load_candidates(args.candidates):
        pdb_id = candidate["pdb_id"].upper()
        destination = args.raw_dir / f"{candidate['case_id']}_{pdb_id}.cif"
        source_url = f"{FILES_ROOT}/{pdb_id}.cif"
        cached = verified_cached_row(candidate, destination, existing_rows.get(candidate["case_id"]))
        if cached:
            rows.append(cached)
            print(f"{candidate['case_id']} {pdb_id} -> verified cached {destination}")
            continue
        retrieved_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        row = {
            "case_id": candidate["case_id"],
            "pdb_id": pdb_id,
            "format": "mmCIF",
            "source_url": source_url,
            "retrieved_at_utc": retrieved_at,
            "local_path": destination.as_posix(),
            "bytes": "",
            "sha256": "",
            "status": "failed",
            "error": "",
        }
        try:
            content = download_mmcif(pdb_id, args.timeout)
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix(".cif.part")
            temporary.write_bytes(content)
            temporary.replace(destination)
            row.update(
                bytes=str(len(content)),
                sha256=hashlib.sha256(content).hexdigest(),
                status="retrieved",
            )
            print(f"{candidate['case_id']} {pdb_id} -> {destination}")
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            row["error"] = str(error)
            print(f"{candidate['case_id']} {pdb_id} -> FAILED: {error}")
        rows.append(row)
    write_manifest(args.manifest, rows)
    return 0 if all(row["status"] == "retrieved" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
