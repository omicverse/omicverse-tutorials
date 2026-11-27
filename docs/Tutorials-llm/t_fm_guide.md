# Foundation models in `ov.llm`

`ov.llm` wraps single-cell foundation models behind one factory. You create a model object with `ov.llm.ModelFactory.create_model(...)` and call its methods (`get_embeddings`, `predict`, `fine_tune`, `integrate`, ...). Six of the 22 registered models are integrated; the other 16 are registered placeholders that raise a clear error and are documented as **not integrated yet**.

The earlier unified foundation-model API and the high-level manager class have been removed. Use the model objects described here; the old manager calls map one-to-one onto model methods (see the Migration section below).

## Quick start

```python
import omicverse as ov

ov.llm.ModelFactory.available_models()          # all 22 registered model types
model = ov.llm.ModelFactory.create_model(
    model_type="scgpt",                         # see the table below
    model_path="llm_model/models/scgpt",        # checkpoint folder / file
    device="cuda",
)
embeddings = model.get_embeddings(adata)        # numpy array (n_cells, dim)
```

`create_model(model_type, model_path=None, device=None, **kwargs)` instantiates the class, then calls `load_model(model_path, **kwargs)` when `model_path` is given. Extra keyword arguments reach both the constructor and `load_model` (for example `pretrain_version` for CellPLM or the five asset paths for UCE). Geneformer is created without `model_path` and loaded with `model.load_model(path, gene_median_file=..., token_dictionary_file=..., gene_mapping_file=...)`.

## Integrated models

| Model | model_type | Class | Tasks in ov.llm | Executed tutorial |
|---|---|---|---|---|
| [scGPT](t_fm_scgpt_guide.md) | `scgpt` | `ScGPTModel` | embedding, annotation, integration, perturbation | [t_scgpt](t_scgpt.ipynb) |
| [scFoundation](t_fm_scfoundation_guide.md) | `scfoundation` | `ScFoundationModel` | embedding, annotation, integration | [t_scfoundation](t_scfoundation.ipynb) |
| [Geneformer](t_fm_geneformer_guide.md) | `geneformer` | `GeneformerModel` | embedding, annotation, integration, perturbation | [t_geneformer](t_geneformer.ipynb) |
| [CellPLM](t_fm_cellplm_guide.md) | `cellplm` | `CellPLMModel` | embedding, annotation, integration (imputation declared) | [t_cellplm](t_cellplm.ipynb) |
| [UCE](t_fm_uce_guide.md) | `uce` | `UCEModel` | embedding, integration, annotation after fine-tuning | [t_uce](t_uce.ipynb) |
| [scMulan](t_fm_scmulan_guide.md) | `scmulan` | `ScMulanModel` | embedding, zero-shot annotation (no fine-tuning) | none (not executed) |

## Model methods

All models derive from `SCLLMBase` (`load_model`, `preprocess`, `predict`, `fine_tune`, `get_embeddings`, `save_model`). The remaining methods exist only on some models (verified against the code):

| method | scGPT | scFoundation | Geneformer | CellPLM | UCE | scMulan |
|---|---|---|---|---|---|---|
| `get_embeddings` | yes | yes | yes | yes | yes | yes |
| `predict(task=...)` | annotation / embedding / integration | embedding / annotation / integration / generation | embedding / annotation / perturbation | annotation / embedding / imputation / integration | embedding; annotation after fine-tune | annotation |
| `fine_tune` | yes | yes | yes | yes | yes | blocked |
| `integrate` | yes | — | yes | yes | yes | — |
| `train_integration` | yes | — | — | yes | — | — |
| `predict_celltypes` | yes | yes | yes | yes | — | — |
| `predict_celltype` | — | — | — | — | yes | — |
| `predict_with_finetune` | — | yes | — | yes | — | — |
| `perturb_genes` | — | — | yes | — | — | — |
| `predict_perturbation` | yes | — | — | — | — | — |

`ModelFactory` also offers `available_models()` and `register_model(model_type, model_class)` (the class must inherit `SCLLMBase`).

## Helper functions

`omicverse.llm.model_factory` contains per-model convenience functions that create a model and run a complete workflow. They are listed on each model page:

```python
from omicverse.llm.model_factory import (
    load_scgpt, annotate_with_scgpt, integrate_with_scgpt,
    get_embeddings_with_scfoundation, extract_geneformer_embeddings,
    perturb_genes_with_geneformer, get_embeddings_with_cellplm,
)
```

| Model | Helpers |
|---|---|
| [scGPT](t_fm_scgpt_guide.md) | `load_scgpt`, `annotate_with_scgpt`, `fine_tune_scgpt`, `predict_celltypes_workflow`, `end_to_end_scgpt_annotation`, `train_integration_scgpt`, `integrate_batches_workflow`, `end_to_end_scgpt_integration`, `integrate_with_scgpt` |
| [scFoundation](t_fm_scfoundation_guide.md) | `load_scfoundation`, `get_embeddings_with_scfoundation`, `end_to_end_scfoundation_embedding`, `fine_tune_scfoundation`, `predict_celltypes_with_scfoundation`, `end_to_end_scfoundation_annotation`, `integrate_with_scfoundation`, `integrate_batches_with_scfoundation`, `end_to_end_scfoundation_integration` |
| [Geneformer](t_fm_geneformer_guide.md) | `load_geneformer`, `annotate_with_geneformer`, `extract_geneformer_embeddings`, `perturb_genes_with_geneformer`, `fine_tune_geneformer` |
| [CellPLM](t_fm_cellplm_guide.md) | `load_cellplm`, `get_embeddings_with_cellplm`, `end_to_end_cellplm_embedding`, `fine_tune_cellplm`, `predict_celltypes_with_cellplm`, `end_to_end_cellplm_annotation`, `integrate_with_cellplm`, `end_to_end_cellplm_integration` |
| UCE, scMulan | none |

## Checkpoints

`omicverse.llm.model_download` has a registry of checkpoint sources (Hugging Face, direct URLs, Google Drive folders):

```python
from omicverse.llm.model_download import list_available_models, download_model

list_available_models()                      # e.g. 'geneformer-v2-104m', 'scfoundation', 'uce', 'scmulan', 'scgpt-whole-human', ...
path = download_model("geneformer-v2-104m", target_dir="llm_model/models/geneformer")
```

The default target is `$OMICVERSE_HOME/models` or `~/.cache/omicverse/models`. CellPLM weights are not in the registry (download them from the link on its page).

## Not integrated yet

These 16 model types are registered in `ModelFactory` as placeholders (`omicverse.llm.external_model_stubs`). `create_model` works, but every task raises `ModelExecutionBlockedError` with the reason and upstream URL. No embeddings, annotation or integration are available for them.

| Model | model_type | Placeholder class | Would need |
|---|---|---|---|
| [scBERT](t_fm_scbert_guide.md) | `scbert` | `ScBERTModel` | upstream checkpoint |
| [GeneCompass](t_fm_genecompass_guide.md) | `genecompass` | `GeneCompassModel` | upstream checkpoint |
| [Nicheformer](t_fm_nicheformer_guide.md) | `nicheformer` | `NicheformerModel` | upstream checkpoint |
| [tGPT](t_fm_tgpt_guide.md) | `tgpt` | `TGPTModel` | upstream checkpoint |
| [CellFM](t_fm_cellfm_guide.md) | `cellfm` | `CellFMModel` | upstream checkpoint |
| [scCello](t_fm_sccello_guide.md) | `sccello` | `ScCelloModel` | upstream checkpoint |
| [scPRINT](t_fm_scprint_guide.md) | `scprint` | `ScPrintModel` | upstream checkpoint |
| [AIDO.Cell](t_fm_aidocell_guide.md) | `aidocell` | `AiDocellModel` | upstream checkpoint |
| [PULSAR](t_fm_pulsar_guide.md) | `pulsar` | `PulsarModel` | upstream checkpoint |
| [ATACformer](t_fm_atacformer_guide.md) | `atacformer` | `AtacformerModel` | upstream checkpoint |
| [scPlantLLM](t_fm_scplantllm_guide.md) | `scplantllm` | `ScPlantLLMModel` | upstream checkpoint |
| [LangCell](t_fm_langcell_guide.md) | `langcell` | `LangCellModel` | upstream checkpoint |
| [Cell2Sentence](t_fm_cell2sentence_guide.md) | `cell2sentence` | `Cell2SentenceModel` | upstream checkpoint |
| [GenePT](t_fm_genept_guide.md) | `genept` | `GenePTModel` | none needed + OPENAI_API_KEY |
| [ChatCell](t_fm_chatcell_guide.md) | `chatcell` | `ChatCellModel` | none needed |
| [Tabula](t_fm_tabula_guide.md) | `tabula` | `TabulaModel` | upstream checkpoint |

```python
try:
    ov.llm.ModelFactory.create_model("scbert").get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err.model_name, err.reason, err.checkpoint_url)
```

`ModelExecutionBlockedError` attributes: `model_name`, `status`, `reason`, `checkpoint_url`, `required_env_vars`, `required_checkpoint`.

## Migration

The removed high-level manager and its method names map onto the model object `model = ov.llm.ModelFactory.create_model(model_type, model_path, device, **kw)`:

| Removed call | Replacement |
|---|---|
| `annotate_cells(adata)` | `model.predict(adata, task="annotation")` |
| `get_embeddings(adata)` | `model.get_embeddings(adata)` |
| `fine_tune(train, valid, task)` | `model.fine_tune(train_adata=train, valid_adata=valid, task=task)` |
| `train_integration(...)` | `model.train_integration(train_adata=..., valid_adata=..., batch_key=...)` |
| `integrate(adata, batch_key)` | `model.integrate(adata, batch_key=...)` |
| `predict_celltypes(q)` | `model.predict_celltypes(q)` (scGPT, scFoundation, Geneformer, CellPLM) or `model.predict(q, task="annotation")` |
| `perturb_genes(adata, genes, type)` | `model.perturb_genes(adata, genes, type)` (Geneformer only) |
| `save_model(path)` | `model.save_model(path)` |
| `manager.model` | `model` |

## Tutorials

- [ov.llm overview notebook](t_fm.ipynb)
- [scGPT](t_scgpt.ipynb)
- [scFoundation](t_scfoundation.ipynb)
- [Geneformer](t_geneformer.ipynb)
- [CellPLM](t_cellplm.ipynb)
- [UCE](t_uce.ipynb)
