# scPRINT

⚠️ **Status:** Partial | **Version:** v1.0

---

## Overview

Focuses on protein-coding genes with built-in denoising and robust batch integration

!!! tip "When to choose scPRINT"

    Best for denoising, protein-coding genes, ambient RNA removal, or when built-in noise reduction is needed

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | scPRINT |
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
info = ov.fm.describe_model("scprint")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "scprint", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="scprint",
    adata_path="your_data.h5ad",
    output_path="output_scprint.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_scprint.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Standard preprocessing. The model includes a built-in denoising step during inference. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_scprint` | `adata.obsm` | Cell embedding vectors (512-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_scprint.h5ad")
embeddings = adata.obsm["X_scprint"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_scprint")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoints:** [https://github.com/scprint/scPRINT](https://github.com/scprint/scPRINT)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [scPRINT tutorial notebook](t_fm_scprint.ipynb).
