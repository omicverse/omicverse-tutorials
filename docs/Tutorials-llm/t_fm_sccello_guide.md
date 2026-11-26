# scCello

⚠️ **Status:** Partial support | **Version:** v1.0

---

## Overview

Embeddings aligned with the cell ontology, enabling zero-shot cell-type annotation with hierarchical consistency

!!! tip "When to choose scCello"

    Use it for zero-shot cell-type annotation, ontology-consistent predictions, or hierarchical cell-type labeling

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | scCello |
| **Version** | v1.0 |
| **Tasks** | `embed`, `integrate`, `annotate` |
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
info = ov.fm.describe_model("sccello")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "sccello", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="sccello",
    adata_path="your_data.h5ad",
    output_path="output_sccello.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_sccello.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Standard preprocessing. Annotation results are aligned with the cell ontology hierarchy. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |
| **Label key** | `.obs` column holding cell-type labels (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_sccello` | `adata.obsm` | Cell embedding vectors (512-dim) |
| `sccello_pred` | `adata.obs` | Predicted cell-type labels |

```python
import scanpy as sc

adata = sc.read_h5ad("output_sccello.h5ad")
embeddings = adata.obsm["X_sccello"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_sccello")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/cellarium-ai/scCello](https://github.com/cellarium-ai/scCello)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [scCello tutorial notebook](t_fm_sccello.ipynb)。
