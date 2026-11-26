# tGPT

⚠️ **Status:** Partial | **Version:** v1.0

---

## Overview

Autoregressive next-token prediction of gene expression values (GPT-style, not masked)

!!! tip "When to choose tGPT"

    Best for autoregressive/generative modeling, next-token prediction of gene expression, or GPT-style generation

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | tGPT |
| **Version** | v1.0 |
| **Tasks** | `embed`, `integrate` |
| **Modalities** | RNA |
| **Species** | human |
| **Gene ID** | symbol |
| **Embedding dim** | 512 |
| **Requires GPU** | Yes |
| **Min VRAM** | 16 GB |
| **Recommended VRAM** | 32 GB |
| **CPU fallback** | No |
| **Adapter status** | ⚠️ Partial |

---

## Quick start

```python
import omicverse as ov

# 1. Inspect the model spec
info = ov.fm.describe_model("tgpt")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "tgpt", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="tgpt",
    adata_path="your_data.h5ad",
    output_path="output_tgpt.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_tgpt.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Standard preprocessing. Gene expression values are tokenized autoregressively. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_tgpt` | `adata.obsm` | Cell embedding vectors (512-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_tgpt.h5ad")
embeddings = adata.obsm["X_tgpt"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_tgpt")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoints:** [https://github.com/deeplearningplus/tGPT](https://github.com/deeplearningplus/tGPT)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [tGPT tutorial notebook](t_fm_tgpt.ipynb).
