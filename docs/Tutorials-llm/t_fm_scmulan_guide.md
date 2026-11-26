# scMulan

⚠️ **Status:** Partial | **Version:** v1.0

---

## Overview

Native multi-omics joint modeling (RNA+ATAC+protein processed simultaneously), designed for CITE-seq/10x Multiome

!!! tip "When to choose scMulan"

    Best for multi-omics data (CITE-seq, 10x Multiome, RNA+ATAC+protein) or when a joint multimodal embedding is needed

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | scMulan |
| **Version** | v1.0 |
| **Tasks** | `embed`, `integrate` |
| **Modalities** | RNA, ATAC, Protein, Multi-omics |
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
info = ov.fm.describe_model("scmulan")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "scmulan", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="scmulan",
    adata_path="your_data.h5ad",
    output_path="output_scmulan.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_scmulan.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | For multi-omics data, organize the data as MuData with separate modalities. For RNA-only data, use standard preprocessing. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_scmulan` | `adata.obsm` | Cell embedding vectors (512-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_scmulan.h5ad")
embeddings = adata.obsm["X_scmulan"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_scmulan")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoints:** [https://github.com/SuperBianC/scMulan](https://github.com/SuperBianC/scMulan)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [scMulan tutorial notebook](t_fm_scmulan.ipynb).
