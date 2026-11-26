# scFoundation

✅ **Status:** Ready | **Version:** xTrimoGene

---

## Overview

Large-scale asymmetric Transformer (xTrimoGene) with a custom 19,264-gene vocabulary, pretrained for perturbation/drug-response tasks

!!! tip "When to choose scFoundation"

    Use it when you need perturbation prediction, drug-response modeling, or the xTrimoGene gene vocabulary

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | scFoundation |
| **Version** | xTrimoGene |
| **Tasks** | `embed`, `integrate` |
| **Modality** | RNA |
| **Species** | human |
| **Gene ID** | custom (19,264 gene set) |
| **Embedding dimension** | 512 |
| **Requires GPU** | Yes |
| **Minimum VRAM** | 16 GB |
| **Recommended VRAM** | 32 GB |
| **CPU fallback** | No |
| **Adapter status** | ✅ Ready |

---

## Quick start

```python
import omicverse as ov

# 1. Inspect the model specification
info = ov.fm.describe_model("scfoundation")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "scfoundation", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="scfoundation",
    adata_path="your_data.h5ad",
    output_path="output_scfoundation.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_scfoundation.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | custom (19,264 gene set) |
| **Preprocessing** | Align genes to the model vocabulary. Follow the xTrimoGene preprocessing pipeline. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_scfoundation` | `adata.obsm` | Cell embedding vectors (512-dim) |
| `scfoundation_pred` | `adata.obs` | Predicted cell-type labels |

```python
import scanpy as sc

adata = sc.read_h5ad("output_scfoundation.h5ad")
embeddings = adata.obsm["X_scfoundation"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_scfoundation")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/biomap-research/scFoundation](https://github.com/biomap-research/scFoundation)
- **Paper:** [https://www.nature.com/articles/s41592-024-02305-7](https://www.nature.com/articles/s41592-024-02305-7)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [scFoundation tutorial notebook](t_scfoundation.ipynb)。
