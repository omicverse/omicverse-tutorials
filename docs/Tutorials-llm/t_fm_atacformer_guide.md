# ATACformer

⚠️ **Status:** Partial support | **Version:** v1.0

---

## Overview

Transformer designed for ATAC-seq that takes chromatin-accessible peaks (not genes) as input; a specialist model for chromatin accessibility analysis

!!! tip "When to choose ATACformer"

    Use it when you have ATAC-seq data, chromatin accessibility profiles, or peak-based (rather than gene-expression) input

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | ATACformer |
| **Version** | v1.0 |
| **Tasks** | `embed`, `integrate` |
| **Modality** | ATAC |
| **Species** | human |
| **Gene ID** | custom (peak-based) |
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
info = ov.fm.describe_model("atacformer")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "atacformer", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="atacformer",
    adata_path="your_data.h5ad",
    output_path="output_atacformer.h5ad",
    device="auto",
)

# 5. Interpret results
metrics = ov.fm.interpret_results("output_atacformer.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | custom (peak-based) |
| **Preprocessing** | Input must be an ATAC-seq peak matrix (not gene expression). Follow the standard scATAC-seq preprocessing workflow (LSI/TF-IDF). |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_atacformer` | `adata.obsm` | Cell embedding vectors (512-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_atacformer.h5ad")
embeddings = adata.obsm["X_atacformer"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_atacformer")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/Atacformer/Atacformer](https://github.com/Atacformer/Atacformer)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [ATACformer tutorial notebook](t_fm_atacformer.ipynb).
