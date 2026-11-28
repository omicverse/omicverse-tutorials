# scFoundation

**Status in `ov.llm`: integrated** (model type `"scfoundation"`, class `ScFoundationModel`).

## What it is

**scFoundation** (xTrimoGene) is a large-scale asymmetric encoder-decoder transformer over a fixed 19,264-gene vocabulary. In `ov.llm` (`ScFoundationModel`) it provides cell embeddings, linear-probe fine-tuning for annotation, and batch integration through embeddings plus post-hoc correction.

Reference: Hao, M. et al. Large-scale foundation model on single-cell transcriptomics. *Nature Methods* 21, 1481–1491 (2024). Code: <https://github.com/biomap-research/scFoundation>

## Supported tasks in `ov.llm`

| Task | Call | Notes |
|---|---|---|
| embedding | `model.get_embeddings(adata, output_type="cell", pool_type="all")` | Cell embedding is 3072-dimensional in the executed tutorial |
| annotation | `model.fine_tune(train_adata=...)` → `model.predict_celltypes(adata)` / `model.predict_with_finetune(adata)` / `model.predict(adata, task="annotation")` | Linear-probe fine-tuning (`frozen_more=True` freezes token/position embeddings) |
| integration | `model.integrate(adata, batch_key=..., correction_method=...)` (same as `model.predict(adata, task="integration", ...)`) | Post-hoc correction on the embeddings: `harmony` (default), `combat`, `scanorama`, `mnn`, `center_scale`, `none` |
| generation | `model.predict(adata, task="generation")` is listed in the docstring | Declared by the wrapper but not covered by any tutorial here; treat as untested |

Not every model implements every method; calling a missing one raises `AttributeError` (for example only Geneformer has `perturb_genes`).

## Checkpoint

`models.ckpt` from the authors' shared folder (the executed tutorial links the SharePoint release); the registry key `scfoundation` points to the Hugging Face repo `genbio-ai/scFoundation` (`omicverse.llm.model_download.download_model('scfoundation', target_dir)`).

## Minimal example

This needs the checkpoint above and a GPU, so the block is not run on this page. The same calls are executed end to end, with outputs, in the tutorial [scFoundation tutorial](t_scfoundation.ipynb).

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model(
    model_type="scfoundation",
    model_path="llm_model/models/scfoundation/models.ckpt",
    device="cuda",
)

adata.obsm["X_scfoundation"] = model.get_embeddings(
    adata, pre_normalized="T", input_type="singlecell")

model.fine_tune(train_adata=reference_adata, epochs=5, batch_size=32,
                pre_normalized="T", lr=1e-3, frozen_more=True)
res = model.integrate(adata, batch_key="batch",
                      correction_method="mnn", pre_normalized="T")
adata.obsm["X_scfoundation_fine"] = res["embeddings"]
anno = model.predict(adata, task="annotation", pre_normalized="T")
```

## Outputs

| Call | Returns |
|---|---|
| `get_embeddings` | ndarray `(n_cells, 3072)` |
| `integrate` / `predict(task="integration")` | dict: `embeddings` |
| `predict_celltypes` | dict: `predictions`, `predicted_celltypes`, `probabilities`, `celltype_mapping`, `prediction_summary` |

Store results yourself (tutorial: `obsm['X_scfoundation']`, `obsm['X_scfoundation_fine']`). `pre_normalized` is `'T'`, `'F'` or `'A'` (already normalised / raw / auto).

## Helper functions

Convenience wrappers in `omicverse.llm.model_factory` that create the model and run a whole workflow in one call, e.g. `from omicverse.llm.model_factory import load_scfoundation`.

| Function | Purpose |
|---|---|
| `load_scfoundation(model_path, device=None, **kwargs)` | load a scFoundation model object |
| `get_embeddings_with_scfoundation(adata, model_path, device=None, output_type='cell', **kwargs)` | load + embeddings in one call |
| `end_to_end_scfoundation_embedding(adata, model_path, save_embeddings_path=None, device=None, output_type='cell', pool_type='all', **kwargs)` | embeddings, optionally saved to disk |
| `fine_tune_scfoundation(train_adata, model_path, valid_adata=None, save_path=None, device=None, **kwargs)` | linear-probe fine-tuning on a reference AnnData |
| `predict_celltypes_with_scfoundation(query_adata, finetuned_model_path, device=None, save_predictions=True, **kwargs)` | predict cell types with a fine-tuned checkpoint |
| `end_to_end_scfoundation_annotation(reference_adata, query_adata, pretrained_model_path, save_finetuned_path=None, device=None, validation_split=0.2, **kwargs)` | fine-tune on reference, then annotate query |
| `integrate_with_scfoundation(query_adata, model_path, batch_key='batch', correction_method='harmony', device=None, save_embeddings=True, **kwargs)` | embeddings + post-hoc batch correction |
| `integrate_batches_with_scfoundation(query_adata, model_path, batch_key='batch', correction_method='harmony', device=None, save_embeddings=True, **kwargs)` | second entry point with the same signature as `integrate_with_scfoundation` |
| `end_to_end_scfoundation_integration(query_adata, model_path, batch_key='batch', correction_methods=['harmony'], device=None, save_all_methods=False, **kwargs)` | integration with several correction methods |

## See also

- [Foundation models in ov.llm](t_fm_guide.md)
- [scFoundation tutorial (executed)](t_scfoundation.ipynb)
