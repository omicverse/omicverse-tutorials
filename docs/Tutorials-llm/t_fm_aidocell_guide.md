# AIDO.Cell

⚠️ **Status:** Partial support | **Version:** v1.0

---

## Overview

Dense transformer optimized for unsupervised cell clustering, with no predefined labels required

!!! tip "When to choose AIDO.Cell"

    Use it when you need unsupervised clustering, label-free cell grouping, or dense transformer embeddings for discovery tasks

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | AIDO.Cell |
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
info = ov.fm.describe_model("aidocell")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "aidocell", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="aidocell",
    adata_path="your_data.h5ad",
    output_path="output_aidocell.h5ad",
    device="auto",
)

# 5. Interpret results
metrics = ov.fm.interpret_results("output_aidocell.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Standard preprocessing. The model is optimized for separation in unsupervised clustering. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_aidocell` | `adata.obsm` | Cell embedding vectors (512-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_aidocell.h5ad")
embeddings = adata.obsm["X_aidocell"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_aidocell")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/genbio-ai/AIDO](https://github.com/genbio-ai/AIDO)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [AIDO.Cell tutorial notebook](t_fm_aidocell.ipynb).
