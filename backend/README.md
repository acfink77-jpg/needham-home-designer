# House Design Assistant

This project includes a lightweight CLI that helps generate a detailed home-design concept from:
- written design goals,
- image inspiration descriptions,
- room requirements,
- and plot constraints.

## Run

```bash
python backend/main.py \
  --brief "I want a cozy farmhouse with natural materials and warm lighting" \
  --images "white siding, black roof, stone porch" \
  --rooms "4 bedrooms,3 bathrooms,home office,mudroom" \
  --plot-width 18 \
  --plot-depth 32 \
  --climate cold \
  --orientation south-facing street
```

Use `--json` for machine-readable output.
