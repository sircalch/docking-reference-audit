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


def download_mmcif(pdb_id: str) -> bytes:
    source_url = f"{FILES_ROOT}/{pdb_id.upper()}.cif"
    request = Request(source_url, headers={"User-Agent": USER_AGENT, "Accept": "chemical/x-cif,text/plain"})
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed HTTPS archive root
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
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    for candidate in load_candidates(args.candidates):
        pdb_id = candidate["pdb_id"].upper()
        destination = args.raw_dir / f"{candidate['case_id']}_{pdb_id}.cif"
        source_url = f"{FILES_ROOT}/{pdb_id}.cif"
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
            content = download_mmcif(pdb_id)
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
