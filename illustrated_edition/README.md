# Scientific illustrations for the revised book

This directory supplies the reproducible source for 32 chapter teaching figures, two original views of deposited experimental molecular coordinates, and three additional data plots. The complete book also includes five separately credited anatomical, mammographic and microscopic source images; those images are documented in `scientific_plate_sources.json` and are not redistributed here.

These are deterministic scientific schematics, plots and coordinate views. No image-generator artwork or simulated diagnostic image is included. Schematics simplify relationships; hypothetical and fictional inputs are identified in the captions. Numerical figures do not establish clinical validation.

## Reproduce

Use Python 3.12 from the repository root. The original numerical results remain pinned to analysis commit `64f8e9996d8d7c940b8ac26177ced6fd8702c7f6`.

```bash
python -m pip install -r illustrated_edition/requirements.txt
python illustrated_edition/run_all.py
```

Outputs are PNGs at 300 dpi and matching PDFs under `illustrated_edition/art`. The scripts read the existing top-level `results` directory; they do not refit a model. The runner downloads coordinate files from the official PDB archive into `research` and verifies their recorded hashes. If an archive record changes, it stops for review rather than silently changing the depicted model. Plot layout, fonts and PDF metadata can vary between software platforms; compare numerical content, not PDF file hashes.

## Scientific status and reuse

`render_experimental_structures.py` draws C-alpha backbone traces from PDB 1AO7 (X-ray model, viral Tax peptide–HLA-A2–TCR example) and PDB 8SK7 (cryo-EM-derived influenza HA model with designed HA_20 binder). These examples are not breast cancer targets or vaccine efficacy results. The coordinate archive is CC0; see https://www.wwpdb.org/about/usage-policies and the original structure records at https://www.rcsb.org/structure/1AO7 and https://www.rcsb.org/structure/8SK7.

The five external scientific images retain their individual public-domain or CC BY-SA 3.0 status; this repository's code licence does not override those terms. In particular, the cytology image is Nephron's separate teaching image, not a WDBC source image. Consult the source manifest and the book image credits before reusing an image.

No licence has been selected for the newly written diagram code or original figures. External data and images retain the reuse status stated by their sources. The MASAI plot is a new visualization of the published ratio 0.88 and 95% confidence interval 0.65–1.18, not a patient-level reanalysis. The prevalence plot is hypothetical arithmetic. The candidate-priority triangle uses fictional unitless features and arbitrary weights; winner frequency is not efficacy probability.
