# scBERT

⚠️ **Status:** Partial support | **Version:** v1.0

---

## Overview

Compact 200-dim embeddings, BERT-style masked-gene pretraining, lightweight model

!!! tip "When to choose scBERT"

    Use it when you need compact 200-dim embeddings, BERT-style pretraining, or a lightweight model on resource-constrained hardware

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | scBERT |
| **Version** | v1.0 |
| **Tasks** | `embed`, `integrate` |
| **Modality** | RNA |
| **Species** | human |
| **Gene ID** | symbol |
| **Embedding dimension** | 200 |
| **Requires GPU** | Yes |
| **Minimum VRAM** | 8 GB |
| **Recommended VRAM** | 16 GB |
| **CPU fallback** | Yes |
| **Adapter status** | ⚠️ Partial support |

---

## Quick start

```python
import omicverse as ov

# 1. Inspect the model specification
info = ov.fm.describe_model("scbert")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "scbert", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="scbert",
    adata_path="your_data.h5ad",
    output_path="output_scbert.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_scbert.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Standard log-normalization and gene filtering. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_scBERT` | `adata.obsm` | Cell embedding vectors (200-dim) |
| `scbert_pred` | `adata.obs` | Predicted cell-type labels |

```python
import scanpy as sc

adata = sc.read_h5ad("output_scbert.h5ad")
embeddings = adata.obsm["X_scBERT"]  # shape: (n_cells, 200)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_scBERT")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/TencentAILabHealthcare/scBERT](https://github.com/TencentAILabHealthcare/scBERT)
- **Paper:** [https://www.nature.com/articles/s42256-022-00534-z](https://www.nature.com/articles/s42256-022-00534-z)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [scBERT tutorial notebook](t_fm_scbert.ipynb)。
