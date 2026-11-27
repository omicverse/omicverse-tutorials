# scMulan

**Status in `ov.llm`: integrated** (model type `"scmulan"`, class `ScMulanModel`).

## What it is

**scMulan** is a multitask generative pre-trained language model that casts a cell as a sentence of gene tokens plus meta-information (cell type, organ, ...). In `ov.llm` (`ScMulanModel`) it wraps the vendored inference code in `omicverse.external.scMulan` and supports **embedding and cell-type annotation only**. Fine-tuning and `save_model` are not implemented and raise `ModelExecutionBlockedError`. There is no executed tutorial for scMulan yet.

Reference: Bian, H. et al. scMulan: a multitask generative pre-trained language model for single-cell analysis. *RECOMB* 2024. Code: <https://github.com/SuperBianC/scMulan>

## Supported tasks in `ov.llm`

| Task | Call | Notes |
|---|---|---|
| embedding | `model.get_embeddings(adata)` | Returns a float32 ndarray (scMulan's own `X_scMulan`) |
| annotation | `model.predict(adata, task="annotation")` | Zero-shot; any other `task` raises `ValueError` |
| fine-tuning / saving | `model.fine_tune(...)`, `model.save_model(...)` | Not implemented: raises `ModelExecutionBlockedError` |

Not every model implements every method; calling a missing one raises `AttributeError` (for example only Geneformer has `perturb_genes`).

## Checkpoint

`ckpt_scMulan.pt` from the authors' Tsinghua Cloud link (<https://cloud.tsinghua.edu.cn/f/2250c5df51034b2e9a85/?dl=1>); registry key `scmulan`. `model_path` may be the file or a folder containing `ckpt_scMulan.pt`, `model.pt` or `model.pth`. The gene-symbol meta file `meta_info.pt` ships with `omicverse.external.scMulan` (override with `meta_info_path=`).

## Minimal example

This needs the checkpoint above and a GPU. It has **not** been executed in these docs and there is no tutorial notebook for scMulan yet; treat it as an API sketch built from the code.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model(
    model_type="scmulan",
    model_path="llm_model/models/scmulan/ckpt_scMulan.pt",
    device="cuda",
)

adata.obsm["X_scMulan"] = model.get_embeddings(adata)

res = model.predict(adata, task="annotation")
adata.obs["scmulan_celltype"] = res["predicted_celltypes"]
```

## Outputs

| Call | Returns |
|---|---|
| `get_embeddings` | float32 ndarray `(n_cells, n_dim)` |
| `predict(task="annotation")` | dict: `predicted_celltypes` (from `obs['cell_type_from_scMulan']`), `embeddings` |

scMulan runs on a copy: `preprocess` unifies gene symbols, converts to CSC and log-normalises when `X.max() > 10`. Store the returned arrays yourself.

## Helper functions

There are no dedicated helper functions for scMulan; use `ModelFactory.create_model` and the model methods directly.

## See also

- [Foundation models in ov.llm](t_fm_guide.md)
