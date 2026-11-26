# Geneformer

✅ **Status:** Ready | **Version:** v2-106M

---

## Overview

Rank-value-encoding transformer using Ensembl gene IDs, supporting CPU inference, with pretraining that incorporates network biology

!!! tip "When to choose Geneformer"

    Use it when you have Ensembl gene IDs, need CPU-only inference, or want gene-network-aware embeddings

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | Geneformer |
| **Version** | v2-106M |
| **Tasks** | `embed`, `integrate` |
| **Modality** | RNA |
| **Species** | human |
| **Gene ID** | ensembl (ENSG...) |
| **Embedding dimension** | 512 |
| **Requires GPU** | No |
| **Minimum VRAM** | 4 GB |
| **Recommended VRAM** | 16 GB |
| **CPU fallback** | Yes |
| **Adapter status** | ✅ Ready |

---

## Quick start

```python
import omicverse as ov

# 1. Inspect the model specification
info = ov.fm.describe_model("geneformer")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "geneformer", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="geneformer",
    adata_path="your_data.h5ad",
    output_path="output_geneformer.h5ad",
    device="auto",
)

# 5. Interpret results
metrics = ov.fm.interpret_results("output_geneformer.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | ensembl (ENSG...) |
| **Preprocessing** | Rank-value encoding. Use `geneformer.preprocess()` for correct tokenization. If Ensembl version suffixes (e.g. `.15`) are present, strip them. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

!!! warning "Gene ID conversion"

    Geneformer requires Ensembl IDs (e.g. `ENSG00000141510`). If your data uses gene symbols, convert them as follows:
    ```python
    # ov.fm.preprocess_validate() detects this automatically and suggests fixes
    check = ov.fm.preprocess_validate("data.h5ad", "geneformer", "embed")
    print(check["auto_fixes"])  # Show conversion suggestions
    ```

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_geneformer` | `adata.obsm` | Cell embedding vectors (512-dim) |
| `geneformer_pred` | `adata.obs` | Predicted cell-type labels |

```python
import scanpy as sc

adata = sc.read_h5ad("output_geneformer.h5ad")
embeddings = adata.obsm["X_geneformer"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_geneformer")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://huggingface.co/ctheodoris/Geneformer](https://huggingface.co/ctheodoris/Geneformer)
- **Paper:** [https://www.nature.com/articles/s41586-023-06139-9](https://www.nature.com/articles/s41586-023-06139-9)
- **Documentation:** [https://geneformer.readthedocs.io/](https://geneformer.readthedocs.io/)
- **License:** Apache 2.0 (code)

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [Geneformer tutorial notebook](t_geneformer.ipynb).
