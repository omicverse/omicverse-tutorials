# scGPT

**Status in `ov.llm`: integrated** (model type `"scgpt"`, class `ScGPTModel`).

## What it is

**scGPT** is a generative pre-trained transformer for single-cell multi-omics, pre-trained on more than 33 million cells. In `ov.llm` it is wrapped as `ScGPTModel`: cell embeddings, annotation after fine-tuning, batch integration (zero-shot embeddings with post-hoc correction, or a trained integration model) and perturbation prediction.

Reference: Cui, H. et al. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. *Nature Methods* 21, 1470–1480 (2024). Code: <https://github.com/bowang-lab/scGPT>

## Supported tasks in `ov.llm`

| Task | Call | Notes |
|---|---|---|
| embedding | `model.get_embeddings(adata)` | Returns an `(n_cells, 512)` ndarray (whole-human checkpoint) |
| annotation | `model.fine_tune(train_adata=...)` → `model.predict_celltypes(adata)` / `model.predict(adata, task="annotation")` | Needs `.obs` cell-type labels on the reference set; fine-tuning is required |
| integration | `model.integrate(adata, batch_key=..., correction_method=...)`; `model.train_integration(...)` | `correction_method` in `combat`, `mnn`, `center_scale`, `none`; a model trained with `train_integration` uses its own integration head |
| perturbation | `model.setup_generator_for_perturbation()`, `model.fine_tune_generator(...)`, `model.predict_perturbation(adata, target_genes, ...)` | Returns an AnnData with predicted perturbed expression; not covered by the executed tutorial |

Not every model implements every method; calling a missing one raises `AttributeError` (for example only Geneformer has `perturb_genes`).

## Checkpoint

Checkpoints are released by the authors as Google Drive folders (`args.json`, `best_model.pt`, `vocab.json`). The registry in `omicverse.llm.model_download` knows `scgpt-whole-human`, `scgpt-continual-pretrained`, `scgpt-brain`, `scgpt-blood`, `scgpt-heart`, `scgpt-lung`, `scgpt-kidney` and `scgpt-pan-cancer`; the executed tutorial downloads the whole-human folder with `gdown`.

## Minimal example

This needs the checkpoint above and a GPU, so the block is not run on this page. The same calls are executed end to end, with outputs, in the tutorial [scGPT tutorial](t_scgpt.ipynb).

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model(
    model_type="scgpt",
    model_path="llm_model/models/scgpt",   # folder with args.json / best_model.pt / vocab.json
    device="cuda",
)

# zero-shot cell embeddings
adata.obsm["X_scgpt"] = model.get_embeddings(adata, skip_normalization=True)

# fine-tune on a labelled reference, then annotate
model.fine_tune(train_adata=reference_adata, epochs=5, batch_size=32, lr=1e-4,
                mask_ratio=0.0, data_is_raw=False, log1p=False, skip_normalization=True)
res = model.predict_celltypes(adata, skip_normalization=True)
adata.obs["predicted_celltype"] = res["predicted_celltypes"]

# batch integration (embeddings + MNN)
res = model.integrate(adata, batch_key="batch", correction_method="mnn",
                      log1p=False, data_is_raw=False, skip_normalization=True)
adata.obsm["X_scgpt_fine"] = res["embeddings"]
```

## Outputs

| Call | Returns |
|---|---|
| `get_embeddings` | ndarray `(n_cells, 512)` |
| `predict_celltypes` | dict: `predicted_celltypes`, `predictions` (class ids), probabilities |
| `integrate` | dict: `embeddings` (+ batch statistics) |
| `fine_tune` | dict: `best_accuracy`, `training_history`, `celltype_mapping`, `n_celltypes` |

The model does not write into `adata` for you; store the arrays yourself (the tutorial uses `obsm['X_scgpt']`, `obsm['X_scgpt_fine']`, `obs['predicted_celltype']`).

## Helper functions

Convenience wrappers in `omicverse.llm.model_factory` that create the model and run a whole workflow in one call, e.g. `from omicverse.llm.model_factory import load_scgpt`.

| Function | Purpose |
|---|---|
| `load_scgpt(model_path, device=None, **kwargs)` | load a scGPT model object |
| `annotate_with_scgpt(adata, model_path, device=None, **kwargs)` | load + `predict(task="annotation")` in one call |
| `fine_tune_scgpt(train_adata, model_path, valid_adata=None, save_path=None, device=None, **kwargs)` | load, fine-tune on a reference AnnData, optionally save |
| `predict_celltypes_workflow(query_adata, finetuned_model_path, device=None, save_predictions=True, **kwargs)` | predict cell types with a fine-tuned scGPT checkpoint |
| `end_to_end_scgpt_annotation(reference_adata, query_adata, pretrained_model_path, save_finetuned_path=None, device=None, validation_split=0.2, **kwargs)` | fine-tune on reference, then annotate query |
| `train_integration_scgpt(train_adata, model_path, batch_key='batch', valid_adata=None, save_path=None, device=None, **kwargs)` | train scGPT for batch integration |
| `integrate_batches_workflow(query_adata, integration_model_path, batch_key='batch', device=None, save_embeddings=True, **kwargs)` | integrate batches with a trained integration checkpoint |
| `end_to_end_scgpt_integration(train_adata, query_adata, pretrained_model_path, batch_key='batch', save_integration_path=None, device=None, validation_split=0.2, **kwargs)` | train integration, then integrate query |
| `integrate_with_scgpt(query_adata, model_path, batch_key='batch', correction_method='combat', device=None, save_embeddings=True, **kwargs)` | zero-shot embeddings + post-hoc batch correction |

## See also

- [Foundation models in ov.llm](t_fm_guide.md)
- [scGPT tutorial (executed)](t_scgpt.ipynb)
