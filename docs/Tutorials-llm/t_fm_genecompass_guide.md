# GeneCompass

⚠️ **Status:** Partial support | **Version:** 120M-cells

---

## Overview

Pretraining enhanced with prior knowledge (gene regulatory networks + pathway information), on a corpus of 120 million cells

!!! tip "When to choose GeneCompass"

    Use it when prior knowledge, gene regulatory networks, pathway-informed embeddings, or cross-species mouse + human analysis are involved

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | GeneCompass |
| **Version** | 120M-cells |
| **Tasks** | `embed`, `integrate` |
| **Modality** | RNA |
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
info = ov.fm.describe_model("genecompass")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "genecompass", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="genecompass",
    adata_path="your_data.h5ad",
    output_path="output_genecompass.h5ad",
    device="auto",
)

# 5. Interpret results
metrics = ov.fm.interpret_results("output_genecompass.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Follow the GeneCompass preprocessing workflow. Both human and mouse gene symbols are supported. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_genecompass` | `adata.obsm` | Cell embedding vectors (512-dim) |
| `genecompass_pred` | `adata.obs` | Predicted cell-type labels |

```python
import scanpy as sc

adata = sc.read_h5ad("output_genecompass.h5ad")
embeddings = adata.obsm["X_genecompass"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_genecompass")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/xCompass-AI/GeneCompass](https://github.com/xCompass-AI/GeneCompass)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [GeneCompass tutorial notebook](t_fm_genecompass.ipynb).
