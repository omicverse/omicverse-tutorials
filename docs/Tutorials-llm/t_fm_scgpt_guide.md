# scGPT

✅ **Status:** Ready | **Version:** whole-human-2024

---

## Overview

Multimodal Transformer (RNA+ATAC+spatial) with attention-based gene interaction modeling

!!! tip "When to choose scGPT"

    Best for multimodal analysis (RNA+ATAC or spatial) or explicit attention-based gene interaction graphs

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | scGPT |
| **Version** | whole-human-2024 |
| **Tasks** | `embed`, `integrate` |
| **Modalities** | RNA, ATAC, Spatial |
| **Species** | human, mouse |
| **Gene ID** | symbol (HGNC) |
| **Embedding dim** | 512 |
| **Requires GPU** | Yes |
| **Min VRAM** | 8 GB |
| **Recommended VRAM** | 16 GB |
| **CPU fallback** | Yes |
| **Adapter status** | ✅ Ready |

---

## Quick start

```python
import omicverse as ov

# 1. Inspect the model spec
info = ov.fm.describe_model("scgpt")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "scgpt", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="scgpt",
    adata_path="your_data.h5ad",
    output_path="output_scgpt.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_scgpt.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol (HGNC) |
| **Preprocessing** | Normalize to 1e4 with `sc.pp.normalize_total`, then bin into 51 expression bins. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_scGPT` | `adata.obsm` | Cell embedding vectors (512-dim) |
| `scgpt_pred` | `adata.obs` | Predicted cell type labels |

```python
import scanpy as sc

adata = sc.read_h5ad("output_scgpt.h5ad")
embeddings = adata.obsm["X_scGPT"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_scGPT")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoints:** [https://github.com/bowang-lab/scGPT#pretrained-scgpt-model-zoo](https://github.com/bowang-lab/scGPT#pretrained-scgpt-model-zoo)
- **Paper:** [https://www.nature.com/articles/s41592-024-02201-0](https://www.nature.com/articles/s41592-024-02201-0)
- **Documentation:** [https://scgpt.readthedocs.io/](https://scgpt.readthedocs.io/)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [scGPT tutorial notebook](t_scgpt.ipynb).
