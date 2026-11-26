# CellFM

⚠️ **Status:** Partial support | **Version:** v1.0

---

## Overview

MLP-based architecture (not a transformer), trained on about 126 million cells (the largest training set)

!!! tip "When to choose CellFM"

    Use it when you specifically want an MLP (rather than transformer) model, or need the largest pretraining scale (about 126 million cells)

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | CellFM |
| **Version** | v1.0 |
| **Tasks** | `embed`, `integrate` |
| **Modality** | RNA |
| **Species** | human |
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
info = ov.fm.describe_model("cellfm")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "cellfm", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="cellfm",
    adata_path="your_data.h5ad",
    output_path="output_cellfm.h5ad",
    device="auto",
)

# 5. Interpret results
metrics = ov.fm.interpret_results("output_cellfm.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Standard preprocessing. The model uses MLP layers in place of attention. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_cellfm` | `adata.obsm` | Cell embedding vectors (512-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_cellfm.h5ad")
embeddings = adata.obsm["X_cellfm"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_cellfm")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/cellverse/CellFM](https://github.com/cellverse/CellFM)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [CellFM tutorial notebook](t_fm_cellfm.ipynb).
