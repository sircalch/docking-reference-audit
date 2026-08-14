#!/usr/bin/env python3
"""Compose Fig. 5 and Fig. 7 as single multi-panel figures for submission.

JMM figure specs (verified 2026-08-14): combination art (color + line) at
>=600 dpi, sized to 84 mm (single column) or 174 mm (double column) width.
This assembles the 7 already-generated per-case PNGs for each figure into
one labeled 4x2 grid at 174 mm / 600 dpi, matching the companion
manuscript's own practice of one composite panel figure per Fig. N. No new
rendering — purely a layout composite of existing images.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

MM_TO_IN = 1 / 25.4
DPI = 600
WIDTH_MM = 174
WIDTH_PX = int(WIDTH_MM * MM_TO_IN * DPI)

CASES = [
    ("pilot-001", "1STP"), ("pilot-007", "3D4Q"), ("expansion-001", "1B9V"),
    ("pilot-008", "3CJO"), ("pilot-002", "1HVR"), ("pilot-006", "3PTB"),
    ("pilot-003", "1IEP"),
]


def load_font(size: int) -> ImageFont.ImageFont:
    for candidate in ("arial.ttf", "Arial.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def compose(image_dir: Path, filename_fn, output: Path, label_prefix: str) -> None:
    cols, rows = 4, 2
    cell_w = WIDTH_PX // cols
    panels = []
    for case_id, pdb_id in CASES:
        path = image_dir / filename_fn(case_id, pdb_id)
        img = Image.open(path).convert("RGB")
        scale = cell_w / img.width
        img = img.resize((cell_w, int(img.height * scale)), Image.LANCZOS)
        panels.append((f"{pdb_id}", img))

    cell_h = max(img.height for _, img in panels)
    label_h = int(cell_h * 0.09)
    canvas = Image.new("RGB", (cell_w * cols, (cell_h + label_h) * rows), "white")
    draw = ImageDraw.Draw(canvas)
    font = load_font(max(28, cell_w // 22))

    for index, (label, img) in enumerate(panels):
        col, row = index % cols, index // cols
        x, y = col * cell_w, row * (cell_h + label_h)
        letter = chr(ord("a") + index)
        draw.text((x + 10, y + 6), f"{letter}) {label}", fill="black", font=font)
        canvas.paste(img, (x, y + label_h))

    canvas.save(output, dpi=(DPI, DPI))
    print(f"Wrote {output} ({canvas.width}x{canvas.height}px, {WIDTH_MM} mm @ {DPI} dpi)")


def main() -> int:
    out_dir = Path("reports/generated/figures/composite")
    out_dir.mkdir(parents=True, exist_ok=True)

    compose(
        Path("reports/generated/figures/platform-3d"),
        lambda c, p: f"{c}-{p}-platform-3d-white.png",
        out_dir / "figure-05-binding-sites-composite.png",
        "Fig5",
    )
    compose(
        Path("reports/generated/figures/interaction-diagrams"),
        lambda c, p: f"interaction-diagram-{c}-{p}.png",
        out_dir / "figure-07-interaction-diagrams-composite.png",
        "Fig7",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
