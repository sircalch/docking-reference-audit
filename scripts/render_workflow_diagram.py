#!/usr/bin/env python3
"""Render the protocol workflow diagram (Fig. 6).

A schematic of the audit's actual pipeline stages, with the real counts
already reported elsewhere in this project attached to each stage (not new
numbers). Purely for reader orientation; no data claim is made here that
is not already established in the corresponding reports:
  - reports/AUDIT-SYNTHESIS-v0.1.md (candidate registration, classification)
  - reports/STRICT-PREPARATION-SUMMARY-v0.1.md (preparation outcomes)
  - reports/REPRODUCIBILITY-VERIFICATION-v0.1.md (RMSD verification)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, FancyBboxPatch

NAVY = "#17324D"
TEAL = "#007C83"
GOLD = "#C78B1B"
CORAL = "#B5473C"
GRAY = "#6C7781"
LIGHT = "#F4F7F8"

STAGES = [
    {
        "title": "1. Registro de\ncandidatos",
        "detail": "30 estructuras PDB\npúblicas, criterios\nverificados vía RCSB\nData API",
        "color": NAVY,
    },
    {
        "title": "2. Clasificación\nestructural",
        "detail": "12 casos limpios /\n18 contextuales,\npolítica declarada\npor caso",
        "color": TEAL,
    },
    {
        "title": "3. Preparación\nestricta",
        "detail": "Meeko 0.7.1,\nsin reparación\n23 intentos,\n7 preparados (30%)",
        "color": GOLD,
    },
    {
        "title": "4. Redocking de\nreferencia",
        "detail": "AutoDock Vina 1.2.5\n\n7 corridas completas",
        "color": CORAL,
    },
    {
        "title": "5. Verificación\nde RMSD",
        "detail": "Identidad CCD→SDF→\nmmCIF verificada\n6 verificados,\n1 no verificable",
        "color": NAVY,
    },
]


def render() -> None:
    figure, axis = plt.subplots(figsize=(14.5, 3.6))
    axis.set_xlim(0, len(STAGES))
    axis.set_ylim(0, 1)
    axis.axis("off")

    box_w, box_h = 0.86, 0.72
    for index, stage in enumerate(STAGES):
        cx = index + 0.5
        cy = 0.5
        box = FancyBboxPatch(
            (cx - box_w / 2, cy - box_h / 2), box_w, box_h,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            linewidth=1.6, edgecolor=stage["color"], facecolor=LIGHT, zorder=3,
        )
        axis.add_patch(box)
        axis.text(cx, cy + 0.22, stage["title"], ha="center", va="center",
                   fontsize=9.5, fontweight="bold", color=stage["color"], zorder=4, linespacing=1.3)
        axis.text(cx, cy - 0.11, stage["detail"], ha="center", va="center",
                   fontsize=7.4, color=NAVY, zorder=4, linespacing=1.6)

        if index < len(STAGES) - 1:
            gap = 1 - box_w
            arrow = FancyArrow(
                cx + box_w / 2 + gap * 0.12, cy, gap * 0.76, 0,
                width=0.012, head_width=0.05, head_length=gap * 0.28,
                length_includes_head=True, color=GRAY, zorder=2,
            )
            axis.add_patch(arrow)

    axis.set_title(
        "Docking Reference Audit — flujo del protocolo (congelado, sin reparación)",
        fontsize=11, color=NAVY, pad=14,
    )
    figure.tight_layout()

    output = Path("reports/generated/figures/figure-06-workflow")
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output.with_suffix(".svg"), bbox_inches="tight")
    figure.savefig(output.with_suffix(".png"), dpi=300, bbox_inches="tight")
    plt.close(figure)
    print(f"Wrote {output}.svg / .png")


if __name__ == "__main__":
    render()
