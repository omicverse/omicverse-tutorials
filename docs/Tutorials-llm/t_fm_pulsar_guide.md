# PULSAR

⚠️ **Status:** Partial support | **Version:** v1.0

---

## Overview

Multi-scale multicellular biology modeling that captures cell-cell communication and tissue-level organization

!!! tip "When to choose PULSAR"

    Use it for cell-cell communication analysis, tissue-level modeling, multicellular program studies, or intercellular signaling analysis

---

## Specifications

| Property | Value |
|----------|-------|
| **Model** | PULSAR |
| **Version** | v1.0 |
| **Tasks** | `embed`, `integrate` |
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
info = ov.fm.describe_model("pulsar")

# 2. Profile your data
profile = ov.fm.profile_data("your_data.h5ad")

# 3. Validate compatibility
check = ov.fm.preprocess_validate("your_data.h5ad", "pulsar", "embed")

# 4. Run inference
result = ov.fm.run(
    task="embed",
    model_name="pulsar",
    adata_path="your_data.h5ad",
    output_path="output_pulsar.h5ad",
    device="auto",
)

# 5. Interpret the results
metrics = ov.fm.interpret_results("output_pulsar.h5ad", task="embed")
```

---

## Input requirements

| Requirement | Details |
|-------------|--------|
| **Gene ID scheme** | symbol |
| **Preprocessing** | Standard preprocessing. For tissue-level analysis, also provide spatial or neighborhood context if available. |
| **Data format** | AnnData (`.h5ad`) |
| **Batch key** | `.obs` column used for batch integration (optional) |

---

## Output keys

After running `ov.fm.run()`, results are stored in the AnnData object:

| Key | Location | Description |
|-----|----------|-------------|
| `X_pulsar` | `adata.obsm` | Cell embedding vectors (512-dim) |

```python
import scanpy as sc

adata = sc.read_h5ad("output_pulsar.h5ad")
embeddings = adata.obsm["X_pulsar"]  # shape: (n_cells, 512)

# Downstream analysis
sc.pp.neighbors(adata, use_rep="X_pulsar")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## References

- **Repository / checkpoint:** [https://github.com/pulsar-ai/PULSAR](https://github.com/pulsar-ai/PULSAR)
- **License:** See the upstream LICENSE

---

## Hands-on tutorial

For a step-by-step walkthrough with code, see the [PULSAR tutorial notebook](t_fm_pulsar.ipynb)。
