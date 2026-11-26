# Nicheformer

⚠️ **Status:** Partial support | **Version:** v1.0

---

## Overview

Niche-aware spatial Transformer that jointly models spatial coordinates and gene expression

!!! tip "When to choose Nicheformer"

    Use it when you have spatial transcriptomics data (Visium, MERFISH, Slide-seq) and want niche-aware or spatial-context embeddings

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | Nicheformer |
| **Version** | v1.0 |
| **Tasks** | `embed`, `integrate`, `spatial` |
| **Modality** | RNA, Spatial |
| **Species** | human, mouse |
| **Gene ID** | symbol |
| **Embedding dimension** | 512 |
| **Requires GPU** | Yes |
| **Minimum VRAM** | 16 GB |
| **Recommended VRAM** | 32 GB |
| **CPU fallback** | No |
| **Adapter status** | ⚠️ Partial support |

---

## Quick start

```python
import omicverse as ov

# 1. Inspect the model specification
info = ov.fm.describe_model("nicheformer")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "nicheformer", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="nicheformer",
    adata_path="your_data.h5ad",
    output_path="output_nicheformer.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_nicheformer.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Standard preprocessing. For spatial tasks, include spatial coordinates in `adata.obsm['spatial']`. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_nicheformer` | `adata.obsm` | Cell embedding vectors (512-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_nicheformer.h5ad")
embeddings = adata.obsm["X_nicheformer"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_nicheformer")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/theislab/nicheformer](https://github.com/theislab/nicheformer)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [Nicheformer tutorial notebook](t_fm_nicheformer.ipynb)。
