# Figure catalog v0.1

The scripts render all figures from versioned CSV manifests; neither values nor
labels are entered manually in an image editor. Run:

```text
python scripts/render_audit_figures.py
```

The generated SVG and 300 dpi PNG files are intentionally not versioned; they
are reproducible derivatives under `reports/generated/figures/`.

The recorded Python dependencies for this version are in `requirements.txt`.

| File stem | Purpose | Source data | Interpretation boundary |
| --- | --- | --- | --- |
| `figure-01-structural-inventory` | Shows clean/contextual inventory disposition | `data/eligibility_register.csv` | Structural class is not a docking result. |
| `figure-02-strict-preparation` | Shows every recorded strict preparation outcome | preparation manifests | A rejection is compatibility with this frozen no-repair policy, not an intrinsic defect of a PDB entry. |
| `figure-03-reference-pose-outcomes` | Shows all retained Vina poses against experimental reference RMSD | `data/reference_pose_rmsd.csv` | Small current sample; no comparative performance claim. |
