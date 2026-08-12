#!/usr/bin/env python3
"""Retrieve auditable RCSB entry and non-polymer metadata for registered cases.

This is a collection step only: it never prepares a receptor, changes a
structure or runs docking.  The raw API responses are retained so later
reports can be regenerated from the same public source.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_ROOT = "https://data.rcsb.org/rest/v1/core"
USER_AGENT = "docking-reference-audit/0.1 (metadata collection)"


def get_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(request, timeout=30) as response:  # nosec B310: fixed HTTPS API root
        raw = response.read()
    return json.loads(raw.decode("utf-8"))


def load_candidates(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get("status") == "candidate"]


def fetch_case(candidate: dict[str, str]) -> dict:
    pdb_id = candidate["pdb_id"].upper()
    entity_url = f"{API_ROOT}/nonpolymer_entity/{pdb_id}"
    entry_url = f"{API_ROOT}/entry/{pdb_id}"
    entry = get_json(entry_url)
    entity_ids = entry.get("rcsb_entry_container_identifiers", {}).get("non_polymer_entity_ids", [])
    components: list[dict] = []
    for entity_id in entity_ids:
        entity = get_json(f"{entity_url}/{entity_id}")
        components.append(
            {
                "entity_id": entity_id,
                "component_id": entity.get("pdbx_entity_nonpoly", {}).get("comp_id"),
                "name": entity.get("pdbx_entity_nonpoly", {}).get("name"),
            }
        )
    declared_component = candidate["ligand_component_id"].upper()
    if not any(component["component_id"] == declared_component for component in components):
        raise ValueError(
            f"Registered ligand {declared_component} is not present among the RCSB "
            f"non-polymeric components for {pdb_id}."
        )
    return {
        "schema_version": "docking-reference-audit.rcsb-metadata.v1",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "candidate": candidate,
        "sources": {"entry": entry_url, "nonpolymer_entities": entity_url},
        "entry": entry,
        "nonpolymer_components": components,
        "declared_ligand_verified": declared_component,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=Path("data/candidates.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports/generated/rcsb-metadata"))
    args = parser.parse_args()

    candidates = load_candidates(args.candidates)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for candidate in candidates:
        payload = fetch_case(candidate)
        encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
        digest = hashlib.sha256(encoded).hexdigest()
        payload["payload_sha256"] = digest
        destination = args.output_dir / f"{candidate['case_id']}.json"
        destination.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"{candidate['case_id']} {candidate['pdb_id']} -> {destination}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HTTPError, URLError, TimeoutError) as error:
        raise SystemExit(f"RCSB retrieval failed: {error}")
