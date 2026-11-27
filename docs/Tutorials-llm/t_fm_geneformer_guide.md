# Geneformer

**Status in `ov.llm`: integrated** (model type `"geneformer"`, class `GeneformerModel`).

## What it is

**Geneformer** is a context-aware, attention-based model pre-trained on a large corpus of single-cell transcriptomes using rank-value encoding. `GeneformerModel` supports embeddings, annotation after fine-tuning, batch integration on embeddings, and in silico gene perturbation (`overexpress`, `inhibit`, `delete`). Gene symbols are mapped to Ensembl IDs through the supplied dictionary files.

Reference: Theodoris, C. V. et al. Transfer learning enables predictions in network biology. *Nature* 618, 616–624 (2023). Hub: <https://huggingface.co/ctheodoris/Geneformer>

## Supported tasks in `ov.llm`

| Task | Call | Notes |
|---|---|---|
| embedding | `model.get_embeddings(adata, max_ncells=...)` | 768-dimensional for Geneformer-V2-104M in the executed tutorial |
| annotation | `model.fine_tune(train_adata=...)` → `model.predict(adata, task="annotation")` / `model.predict_celltypes(adata)` | `task` in `annotation`, `gene_classification` for `fine_tune` |
| integration | `model.integrate(adata, batch_key=..., correction_method=...)` | Post-hoc correction on embeddings |
| perturbation | `model.perturb_genes(adata, target_genes, perturb_type)`; `model.get_perturbed_adata(...)`, `model.compare_perturbed_expression(...)` | Only Geneformer exposes `perturb_genes`; feeds `ov.pl.perturbation_*` |

Not every model implements every method; calling a missing one raises `AttributeError` (for example only Geneformer has `perturb_genes`).

## Checkpoint

Hugging Face: <https://huggingface.co/ctheodoris/Geneformer> (model folders such as `Geneformer-V2-104M`, plus `gene_median_dictionary_gc104M.pkl`, `token_dictionary_gc104M.pkl`, `ensembl_mapping_dict_gc104M.pkl`). The registry keys `geneformer`, `geneformer-v2-316m`, `geneformer-v2-104m`, `geneformer-v1-10m` fetch them via `omicverse.llm.model_download.download_model`. Optional packages: `tdigest`, `peft` (warned about when missing).

## Minimal example

This needs the checkpoint above and a GPU, so the block is not run on this page. The same calls are executed end to end, with outputs, in the tutorial [Geneformer tutorial](t_geneformer.ipynb).

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model(
    model_type="geneformer", device="cuda", model_version="V2")
model.load_model(
    "llm_model/models/geneformer/Geneformer-V2-104M",
    gene_median_file="llm_model/models/geneformer/gene_median_dictionary_gc104M.pkl",
    token_dictionary_file="llm_model/models/geneformer/token_dictionary_gc104M.pkl",
    gene_mapping_file="llm_model/models/geneformer/ensembl_mapping_dict_gc104M.pkl",
)

adata.obsm["X_geneformer"] = model.get_embeddings(adata, max_ncells=100000)

# in silico knockout of transcription factors
perturb_result = model.perturb_genes(
    adata, target_genes=["SPI1", "PAX5", "TBX21"], perturb_type="delete",
    max_ncells=adata.n_obs, forward_batch_size=50)
```

## Outputs

| Call | Returns |
|---|---|
| `get_embeddings` | ndarray `(n_cells, 768)` (V2-104M) |
| `integrate` | dict: `embeddings` (+ statistics) |
| `predict_celltypes` | dict: predictions and statistics |
| `perturb_genes` | dict of perturbation results (cell-level cosine shifts, per-gene shifts); input of `ov.pl.perturbation_*` |

Store results yourself (tutorial: `obsm['X_geneformer_fine']`). Pass `adata.obs['cell_barcode']` for V2 tokenisation as in the tutorial.

## Helper functions

Convenience wrappers in `omicverse.llm.model_factory` that create the model and run a whole workflow in one call, e.g. `from omicverse.llm.model_factory import load_geneformer`.

| Function | Purpose |
|---|---|
| `load_geneformer(model_path, gene_median_file, token_dictionary_file, gene_mapping_file, device=None, model_version='V1', **kwargs)` | create + `load_model` with the three dictionary files |
| `annotate_with_geneformer(adata, model_path, device=None, model_version='V1', **kwargs)` | load + `predict(task="annotation")` |
| `extract_geneformer_embeddings(adata, model_path, device=None, model_version='V1', emb_layer=0, **kwargs)` | load + embeddings (`emb_layer` selects the layer) |
| `perturb_genes_with_geneformer(adata, target_genes, model_path, perturb_type='overexpress', device=None, model_version='V1', **kwargs)` | in silico perturbation in one call |
| `fine_tune_geneformer(train_adata, model_path, valid_adata=None, save_path=None, device=None, model_version='V1', task='annotation', **kwargs)` | fine-tune on a reference AnnData |

## See also

- [Foundation models in ov.llm](t_fm_guide.md)
- [Geneformer tutorial (executed)](t_geneformer.ipynb)
