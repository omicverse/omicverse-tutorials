# GenePT

⚠️ **Status:** Partial support | **Version:** v1.0

---

## Overview

API-based GPT-3.5 gene embeddings (1536-dim); no local GPU required; operates per gene (not per cell)

!!! tip "When to choose GenePT"

    Use it when you need gene-level (rather than cell-level) embeddings, have no local GPU, or want API-based OpenAI embeddings

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | GenePT |
| **Version** | v1.0 |
| **Tasks** | `embed` |
| **Modality** | RNA |
| **Species** | human |
| **Gene ID** | symbol |
| **Embedding dimension** | 1536 |
| **Requires GPU** | No |
| **Minimum VRAM** | 0 GB |
| **Recommended VRAM** | 0 GB |
| **CPU fallback** | Yes |
| **Adapter status** | ⚠️ Partial support |

---

## Quick start

```python
import omicverse as ov

# 1. Inspect the model specification
info = ov.fm.describe_model("genept")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "genept", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="genept",
    adata_path="your_data.h5ad",
    output_path="output_genept.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_genept.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | No local preprocessing required. An OpenAI API key is needed to generate embeddings. |
| **Data format** | AnnData (`.h5ad`) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_genept` | `adata.obsm` | Cell embedding vectors (1536-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_genept.h5ad")
embeddings = adata.obsm["X_genept"]  # shape: (n_cells, 1536)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_genept")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/yiqunchen/GenePT](https://github.com/yiqunchen/GenePT)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [GenePT tutorial notebook](t_fm_genept.ipynb)。
