# Tabula

⚠️ **Status:** Partial | **Version:** federated-v1

---

## Overview

Privacy-preserving federated learning + tabular Transformer, 60,697-gene vocabulary, quantile-binned expression, FlashAttention support

!!! tip "When to choose Tabula"

    Best for privacy-preserving analysis, federated-trained embeddings, or perturbation prediction with a tabular modeling approach

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | Tabula |
| **Version** | federated-v1 |
| **Tasks** | `embed`, `annotate`, `integrate`, `perturb` |
| **Modalities** | RNA |
| **Species** | human |
| **Gene ID** | custom (60,697 gene vocabulary) |
| **Embedding dim** | 192 |
| **Requires GPU** | Yes |
| **Min VRAM** | 8 GB |
| **Recommended VRAM** | 16 GB |
| **CPU fallback** | No |
| **Adapter status** | ⚠️ Partial |

---

## Quick start

```python
import omicverse as ov

# 1. Inspect the model spec
info = ov.fm.describe_model("tabula")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "tabula", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="tabula",
    adata_path="your_data.h5ad",
    output_path="output_tabula.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_tabula.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | custom (60,697 gene vocabulary) |
| **Preprocessing** | Gene expression is quantile-binned. The model tokenizes with its own 60,697-gene vocabulary. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |
| **Label key** | `.obs` column for cell type labels (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_tabula` | `adata.obsm` | Cell embedding vectors (192-dim) |
| `tabula_pred` | `adata.obs` | Predicted cell type labels |

```python
import scanpy as sc

adata = sc.read_h5ad("output_tabula.h5ad")
embeddings = adata.obsm["X_tabula"]  # shape: (n_cells, 192)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_tabula")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoints:** [https://github.com/aristoteleo/tabula](https://github.com/aristoteleo/tabula)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [Tabula tutorial notebook](t_fm_tabula.ipynb).
