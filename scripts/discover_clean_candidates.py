#!/usr/bin/env python3
"""Discover, but do not register, possible clean RCSB PDB candidates.

The query is fixed by ``protocol/CANDIDATE-DISCOVERY-v0.1.md``.  Every hit
still needs chemical screening and original-coordinate mmCIF inventory before
it can enter ``data/candidates.csv``.  This script never downloads structures,
prepares receptors, or runs docking.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from urllib.request import Request, urlopen


SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
DATA_ROOT = "https://data.rcsb.org/rest/v1/core"
USER_AGENT = "docking-reference-audit/0.1 (candidate discovery)"
FIELDS = (
    "rank",
    "pdb_id",
    "component_id",
    "component_name",
    "formula_weight_kda",
    "entry_url",
    "entity_url",
    "discovery_status",
)


def get_json(url: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    with urlopen(Request(url, data=data, headers=headers), timeout=60) as response:  # nosec B310: fixed HTTPS roots
        return json.loads(response.read().decode("utf-8"))


def discovery_query(limit: int) -> dict:
    return {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "exptl.method",
                        "operator": "exact_match",
                        "value": "X-RAY DIFFRACTION",
                    },
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.resolution_combined",
                        "operator": "less_or_equal",
                        "value": 2.0,
                    },
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.nonpolymer_entity_count",
                        "operator": "equals",
                        "value": 1,
                    },
                },
            ],
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": limit},
            "sort": [{"sort_by": "rcsb_entry_info.resolution_combined", "direction": "asc"}],
            "results_verbosity": "compact",
        },
    }


def component_for_entry(pdb_id: str) -> tuple[str, str, str, str]:
    entry_url = f"{DATA_ROOT}/entry/{pdb_id}"
    entry = get_json(entry_url)
    entity_ids = entry.get("rcsb_entry_container_identifiers", {}).get("non_polymer_entity_ids", [])
    if len(entity_ids) != 1:
        raise ValueError(f"{pdb_id}: search hit no longer has exactly one non-polymer entity")
    entity_url = f"{DATA_ROOT}/nonpolymer_entity/{pdb_id}/{entity_ids[0]}"
    entity = get_json(entity_url)
    nonpoly = entity.get("pdbx_entity_nonpoly", {})
    summary = entity.get("rcsb_nonpolymer_entity", {})
    return (
        nonpoly.get("comp_id", ""),
        nonpoly.get("name", ""),
        str(summary.get("formula_weight", "")),
        entity_url,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--output", type=Path, default=Path("reports/generated/discovery/clean-candidates.csv"))
    args = parser.parse_args()
    if not 1 <= args.limit <= 10000:
        raise ValueError("--limit must be between 1 and 10000")

    response = get_json(SEARCH_URL, discovery_query(args.limit))
    identifiers = response.get("result_set", [])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for rank, pdb_id in enumerate(identifiers, start=1):
            component_id, component_name, weight, entity_url = component_for_entry(pdb_id)
            writer.writerow({
                "rank": rank,
                "pdb_id": pdb_id,
                "component_id": component_id,
                "component_name": component_name,
                "formula_weight_kda": weight,
                "entry_url": f"{DATA_ROOT}/entry/{pdb_id}",
                "entity_url": entity_url,
                "discovery_status": "unreviewed_not_registered",
            })
    print(f"Wrote {len(identifiers)} discovery rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
