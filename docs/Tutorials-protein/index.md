---
orphan: true
---

# Tutorials of Proteomics

`ov.protein` is the AnnData-native downstream framework for **bulk
quantitative proteomics** — label-free LC-MS/MS (MaxQuant, DIA-NN,
FragPipe) and affinity proteomics (Olink NPX). Every analysis stage is
a single dispatcher function with a `method=` selector, the same design
as `ov.es` and `ov.metabol`.

The statistical engines are five standalone, R-parity-tested packages
that `ov.protein` wraps — pure-Python ports of the canonical
Bioconductor / CRAN proteomics R packages:

| Backend package | Ports R package | Role |
|---|---|---|
| `pyimputelcmd` | Bioconductor **imputeLCMD** | left-censored imputation (MinDet / MinProb / QRILC / MLE / KNN / SVD), MCAR/MNAR classification |
| `pydeqms` | Bioconductor **DEqMS** | peptide-count-aware moderated *t*, peptide→protein summarization, variance diagnostics |
| `pyproda` | Bioconductor **proDA** | MNAR probabilistic differential expression |
| `pymsstats` | Bioconductor **MSstats** | DDA/DIA converters, dataProcess pipeline, group comparison, design / power |
| `pyolinkanalyze` | CRAN **OlinkAnalyze** | Olink NPX QC, bridge normalization, LMM / ANOVA, pathway enrichment |

All five are pure-Python (no `rpy2`), validated against the original R
packages. Every tutorial below runs on a **real, published dataset**
served through `ov.datasets`.

!!! note "Out of scope"
    Single-cell proteomics (SCP) and spatial proteomics (IMC / CODEX)
    are **not** covered by `ov.protein` — use `squidpy` / `SCIMAP` for
    spatial protein imaging.

## The five tutorials

1. **[Bulk LC-MS/MS best-practice pipeline](t_protein_01_bulk_pipeline.ipynb)** — the complete protein-level workflow on ProteomeXchange **PXD000022**: QC → missing-value diagnosis → MCAR/MNAR classification → normalization → informed imputation → differential expression → volcano / heatmap → enrichment.

2. **[Missing values: diagnosis & imputation](t_protein_02_missing_values.ipynb)** — the hardest part of proteomics, on **PXD000438** (~41% missing): MNAR vs MCAR theory, benchmarking all nine imputers by artificial masking, and how the imputation choice changes the differential-expression result.

3. **[Peptide → protein summarization & DIA](t_protein_03_summarization_dia.ipynb)** — from feature/peptide-level search output to a protein matrix, on the MSstats spike-in **DDA** and **DIA** datasets: median / median-sweeping / Tukey-median-polish / MSstats dataProcess.

4. **[Differential expression: methods compared](t_protein_04_differential_expression.ipynb)** — DEqMS vs proDA vs MSstats vs limma vs *t*-test on the MSstats spike-in data: the variance–peptide-count relationship, the MNAR dropout model, multi-group ANOVA, contrasts, and sample-size / power analysis.

5. **[Olink NPX affinity proteomics](t_protein_05_olink.ipynb)** — the OlinkAnalyze workflow on the real **`npx_data1`** Explore study: NPX QC, LOD, bridge normalization, *t*-test / Wilcoxon / ANOVA / LMM, and pathway enrichment.

## The datasets

All five tutorials load real published data through `ov.datasets`:

```python
ov.datasets.protein_pxd000022()    # PXD000022 — label-free LFQ, 2-group
ov.datasets.protein_pxd000438()    # PXD000438 — label-free LFQ, 4-group, 41% missing
ov.datasets.protein_dda_spikein()  # MSstats DDARawData — controlled spike-in DDA
ov.datasets.protein_dia()          # MSstats DIARawData — DIA, S. Pyogenes
ov.datasets.protein_olink()        # OlinkAnalyze npx_data1 — Olink Explore NPX
```
