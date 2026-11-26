# scPlantLLM

⚠️ **Status:** Partial | **Version:** v1.0

---

## Overview

Plant-specific single-cell model that handles polyploidy and plant gene nomenclature

!!! tip "When to choose scPlantLLM"

    Best for plant single-cell data (Arabidopsis, rice, maize, etc.) or when polyploidy is a concern

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | scPlantLLM |
| **Version** | v1.0 |
| **Tasks** | `embed`, `integrate` |
| **Modalities** | RNA |
| **Species** | plant (Arabidopsis, rice, maize, etc.) |
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
info = ov.fm.describe_model("scplantllm")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "scplantllm", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="scplantllm",
    adata_path="your_data.h5ad",
    output_path="output_scplantllm.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_scplantllm.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Standard preprocessing with plant gene nomenclature. The model handles polyploidy-specific challenges. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_scplantllm` | `adata.obsm` | Cell embedding vectors (512-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_scplantllm.h5ad")
embeddings = adata.obsm["X_scplantllm"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_scplantllm")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoints:** [https://github.com/scPlantLLM/scPlantLLM](https://github.com/scPlantLLM/scPlantLLM)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [scPlantLLM tutorial notebook](t_fm_scplantllm.ipynb).
