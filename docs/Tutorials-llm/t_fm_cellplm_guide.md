# CellPLM

**Status in `ov.llm`: integrated** (model type `"cellplm"`, class `CellPLMModel`).

## What it is

**CellPLM** is a single-cell pre-trained language model that treats cells (not genes) as tokens and encodes cell-cell relations. `CellPLMModel` provides embeddings, annotation after fine-tuning, imputation (pipeline), and batch integration through embeddings.

Reference: Wen, H. et al. CellPLM: pre-training of cell language model beyond single cells. *bioRxiv* (2023); ICLR 2024. Code: <https://github.com/OmicsML/CellPLM>

## Supported tasks in `ov.llm`

| Task | Call | Notes |
|---|---|---|
| embedding | `model.get_embeddings(adata)` | 512-dimensional in the executed tutorial |
| annotation | `model.fine_tune(train_adata=...)` → `model.predict_celltypes(adata)` | `fine_tune` `task` in `annotation`, `imputation` |
| integration | `model.integrate(adata, batch_key=..., correction_method=...)`; `model.train_integration(...)` | Embedding-based |
| imputation | `model.predict(adata, task="imputation")` | Listed in the wrapper docstring; not covered by a tutorial here |

Not every model implements every method; calling a missing one raises `AttributeError` (for example only Geneformer has `perturb_genes`).

## Checkpoint

Dropbox folder of the authors (linked from the executed tutorial): <https://www.dropbox.com/scl/fo/i5rmxgtqzg7iykt2e9uqm/h/ckpt>. Default `pretrain_version` is `20231027_85M`; `model_path` is the folder holding the checkpoint and its config.

## Minimal example

This needs the checkpoint above and a GPU, so the block is not run on this page. The same calls are executed end to end, with outputs, in the tutorial [CellPLM tutorial](t_cellplm.ipynb).

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model(
    model_type="cellplm",
    model_path="llm_model/models/cellplm",
    pretrain_version="20231027_85M",
)

adata.obsm["X_cellplm"] = model.get_embeddings(adata)

model.fine_tune(train_adata=reference_adata, epochs=1500, batch_size=32, lr=1e-4)
res = model.integrate(adata, batch_key="batch", correction_method="mnn")
adata.obsm["X_cellplm_fine"] = res["embeddings"]

pred = model.predict_celltypes(adata)
adata.obs["predicted_celltype"] = pred["predicted_celltypes"]
```

## Outputs

| Call | Returns |
|---|---|
| `get_embeddings` | ndarray `(n_cells, 512)` |
| `integrate` | dict: `embeddings` |
| `predict_celltypes` | dict: `predicted_celltypes`, `predictions` (class ids), statistics |

Store results yourself (tutorial: `obsm['X_cellplm_fine']`, `obs['predicted_celltype']`).

## Helper functions

Convenience wrappers in `omicverse.llm.model_factory` that create the model and run a whole workflow in one call, e.g. `from omicverse.llm.model_factory import load_cellplm`.

| Function | Purpose |
|---|---|
| `load_cellplm(model_path, pretrain_version='20231027_85M', device=None, **kwargs)` | load a CellPLM model object |
| `get_embeddings_with_cellplm(adata, model_path, pretrain_version='20231027_85M', device=None, **kwargs)` | load + embeddings in one call |
| `end_to_end_cellplm_embedding(adata, model_path, pretrain_version='20231027_85M', save_embeddings_path=None, device=None, **kwargs)` | embeddings, optionally saved to disk |
| `fine_tune_cellplm(train_adata, model_path, pretrain_version='20231027_85M', valid_adata=None, save_path=None, device=None, task='annotation', **kwargs)` | fine-tune on a reference AnnData |
| `predict_celltypes_with_cellplm(query_adata, finetuned_model_path, pretrain_version='20231027_85M', device=None, save_predictions=True, **kwargs)` | predict cell types with a fine-tuned checkpoint |
| `end_to_end_cellplm_annotation(reference_adata, query_adata, model_path, pretrain_version='20231027_85M', save_finetuned_path=None, device=None, validation_split=0.2, **kwargs)` | fine-tune on reference, then annotate query |
| `integrate_with_cellplm(query_adata, model_path, pretrain_version='20231027_85M', batch_key='batch', correction_method='harmony', device=None, save_embeddings=True, **kwargs)` | embeddings + post-hoc batch correction |
| `end_to_end_cellplm_integration(query_adata, model_path, pretrain_version='20231027_85M', batch_key='batch', correction_methods=['harmony'], device=None, save_all_methods=False, **kwargs)` | integration with several correction methods |

## See also

- [Foundation models in ov.llm](t_fm_guide.md)
- [CellPLM tutorial (executed)](t_cellplm.ipynb)
