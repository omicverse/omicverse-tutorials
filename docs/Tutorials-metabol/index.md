---
orphan: true
---

# Tutorials of Metabolomics

The tutorials start from a peak intensity table (produced upstream by XCMS / MZmine / MS-DIAL / MetaboAnalyst) and cover the full downstream workflow: QC, batch correction, statistics (two-group + multi-factor + time-series), biomarker discovery, correlation networks, multi-omics integration, and a real-data case study on a public Metabolights dataset.

## Preprocessing and univariate analysis

- [Metabolomics preprocessing and univariate statistics](t_metabol_01_intro.ipynb) — QC, impute, normalize, transform, two-group differential, plus ``anova`` for 3+ groups.

## Multivariate discrimination

- [Multivariate discrimination with PLS-DA and OPLS-DA](t_metabol_02_multivariate.ipynb)

## Pathway enrichment

- [Metabolite-set enrichment analysis (MSEA)](t_metabol_03_pathway.ipynb)

## Untargeted LC-MS

- [Untargeted LC-MS and mummichog pathway inference](t_metabol_04_untargeted.ipynb)

## Lipidomics

- [Lipidomics with LIPID MAPS and LION](t_metabol_05_lipidomics.ipynb)

## Batch effect and drift correction

- [Batch correction for LC-MS — drift, SERRF, ComBat, plus sample-level outlier detection](t_metabol_06_batch_correction.ipynb)

## Multi-factor designs

- [ASCA, linear mixed models, and MEBA time-series Hotelling T²](t_metabol_07_multifactor.ipynb)

## Biomarker discovery

- [Per-feature ROC and multivariate nested-CV panels](t_metabol_08_biomarker.ipynb)

## Correlation analysis

- [Differential (DGCA) and static per-condition correlation networks](t_metabol_09_dgca.ipynb)

## Multi-omics integration

- [Joint analysis of metabolomics and RNA-seq with MOFA+](t_metabol_10_multiomics.ipynb)

## Real-data case study

- [End-to-end workflow on MTBLS1 (urine NMR, Type 2 Diabetes)](t_metabol_11_real_data_mtbls1.ipynb) — public Metabolights data, shows which tools apply and which don't for a QC-less cross-sectional study.
