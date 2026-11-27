# UCE

**Status in `ov.llm`: integrated** (model type `"uce"`, class `UCEModel`).

## What it is

**UCE (Universal Cell Embeddings)** is a self-supervised transformer trained on cell-atlas data from eight species. Genes are tokenised through ESM2 protein embeddings and genomic position, so no gene vocabulary alignment is needed across species. `UCEModel` gives zero-shot embeddings, batch integration on the embeddings, and annotation after fine-tuning with a classification head (frozen or unfrozen backbone).

Reference: Rosen, Y. et al. Universal Cell Embeddings: A Foundation Model for Cell Biology. *bioRxiv* (2023). Code: <https://github.com/snap-stanford/UCE>

## Supported tasks in `ov.llm`

| Task | Call | Notes |
|---|---|---|
| embedding | `model.get_embeddings(adata, filter_cells=False, filter_genes=False)` | `(n_cells, 1280)` |
| integration | `model.integrate(adata, batch_key=..., correction_method="mnn")` | `correction_method` in `harmony`, `mnn`, `center_scale`, `none` |
| annotation | `model.fine_tune(train_adata=..., freeze_backbone=True/False)` → `model.predict(adata, task="annotation")` / `model.predict_celltype(adata)` | `predict(task="annotation")` raises `ValueError` before fine-tuning (only `embedding` is available) |

Not every model implements every method; calling a missing one raises `AttributeError` (for example only Geneformer has `perturb_genes`).

## Checkpoint

figshare bundle from the UCE authors: `4layer_model.torch`, `species_chrom.csv`, `species_offsets.pkl`, the token embedding file (`all_tokens.torch` in the tutorial) and `protein_embeddings.tar.gz` (extract it). The registry key `uce` downloads the same bundle through `omicverse.llm.model_download.download_model('uce', target_dir)`. The five paths must be passed to `create_model` (`model_path`, `token_file`, `protein_embeddings_dir`, `spec_chrom_csv_path`, `offset_pkl_path`).

## Minimal example

This needs the checkpoint above and a GPU, so the block is not run on this page. The same calls are executed end to end, with outputs, in the tutorial [UCE tutorial](t_uce.ipynb).

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model(
    model_type="uce",
    model_path="llm_model/models/UCE/4layer_model.torch",
    token_file="llm_model/models/UCE/all_tokens.torch",
    protein_embeddings_dir="llm_model/models/UCE/protein_embeddings/",
    spec_chrom_csv_path="llm_model/models/UCE/species_chrom.csv",
    offset_pkl_path="llm_model/models/UCE/species_offsets.pkl",
    species="human",
    device="cuda",
)

adata.obsm["X_uce"] = model.get_embeddings(adata, filter_cells=False, filter_genes=False)

res = model.integrate(adata, batch_key="batch", correction_method="mnn")
adata.obsm["X_uce_mnn"] = res["embeddings"]

model.fine_tune(train_adata=reference_adata, epochs=10, batch_size=32, lr=1e-4,
                freeze_backbone=True)
pred = model.predict(adata, task="annotation")
adata.obs["predicted_celltype"] = pred["predictions"]
```

## Outputs

| Call | Returns |
|---|---|
| `get_embeddings` | ndarray `(n_cells, 1280)` |
| `predict(task="embedding")` | dict: `embeddings`, `task`, `model_name` |
| `integrate` | dict: `embeddings` (corrected) |
| `predict(task="annotation")` + `fine_tune` | dict: `predictions`, `task`, `model_name`, `fine_tuned` |

Store results yourself (tutorial: `obsm['X_uce']`, `obsm['X_uce_mnn']`, `obsm['X_uce_fine']`).

## Helper functions

There are no dedicated helper functions for UCE; use `ModelFactory.create_model` and the model methods directly.

## See also

- [Foundation models in ov.llm](t_fm_guide.md)
- [UCE tutorial (executed)](t_uce.ipynb)
