# CellPLM

✅ **Status:** Ready | **Version:** v1.0

---

## Overview

Cell-centric (rather than gene-centric) architecture with the highest batch throughput (batch_size=128) and fast inference

!!! tip "When to choose CellPLM"

    Use it when you need fast inference, high throughput, million-cell-scale processing, or cell-level (rather than gene-level) modeling

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | CellPLM |
| **Version** | v1.0 |
| **Tasks** | `embed`, `integrate` |
| **Modality** | RNA |
| **Species** | human |
| **Gene ID** | symbol |
| **Embedding dimension** | 512 |
| **Requires GPU** | Yes |
| **Minimum VRAM** | 8 GB |
| **Recommended VRAM** | 16 GB |
| **CPU fallback** | Yes |
| **Adapter status** | ✅ Ready |

---

## Quick start

```python
import omicverse as ov

# 1. Inspect the model specification
info = ov.fm.describe_model("cellplm")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "cellplm", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="cellplm",
    adata_path="your_data.h5ad",
    output_path="output_cellplm.h5ad",
    device="auto",
)

# 5. Interpret results
metrics = ov.fm.interpret_results("output_cellplm.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Standard preprocessing. The model handles tokenization internally. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_cellplm` | `adata.obsm` | Cell embedding vectors (512-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_cellplm.h5ad")
embeddings = adata.obsm["X_cellplm"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_cellplm")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/OmicsML/CellPLM](https://github.com/OmicsML/CellPLM)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [CellPLM tutorial notebook](t_cellplm.ipynb).
