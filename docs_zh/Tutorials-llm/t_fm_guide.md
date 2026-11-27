# `ov.llm` 基础模型总览

`ov.llm` 通过一个工厂类封装单细胞基础模型：用 `ov.llm.ModelFactory.create_model(...)` 创建模型对象，再调用其方法（`get_embeddings`、`predict`、`fine_tune`、`integrate` 等）。已注册的 22 个模型中 6 个已集成，其余 16 个是会给出明确报错的占位对象，文档中标注为**尚未集成**。

早期的统一基础模型 API 和高层管理器类均已移除，请使用本页介绍的模型对象；旧管理器的调用与模型方法一一对应（见下方“迁移”一节）。

## 快速开始

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

`create_model(model_type, model_path=None, device=None, **kwargs)` 先实例化类，给定 `model_path` 时再调用 `load_model(model_path, **kwargs)`。额外关键字参数会同时传给构造函数与 `load_model`（例如 CellPLM 的 `pretrain_version`、UCE 的五个资源路径）。Geneformer 不传 `model_path` 创建，再用 `model.load_model(path, gene_median_file=..., token_dictionary_file=..., gene_mapping_file=...)` 加载。

## 已集成的模型

| 模型 | model_type | 类 | ov.llm 中的任务 | 已执行教程 |
|---|---|---|---|---|
| [scGPT](t_fm_scgpt_guide.md) | `scgpt` | `ScGPTModel` | 嵌入、注释、整合、扰动 | [t_scgpt](t_scgpt.ipynb) |
| [scFoundation](t_fm_scfoundation_guide.md) | `scfoundation` | `ScFoundationModel` | 嵌入、注释、整合 | [t_scfoundation](t_scfoundation.ipynb) |
| [Geneformer](t_fm_geneformer_guide.md) | `geneformer` | `GeneformerModel` | 嵌入、注释、整合、扰动 | [t_geneformer](t_geneformer.ipynb) |
| [CellPLM](t_fm_cellplm_guide.md) | `cellplm` | `CellPLMModel` | 嵌入、注释、整合（声明支持插补） | [t_cellplm](t_cellplm.ipynb) |
| [UCE](t_fm_uce_guide.md) | `uce` | `UCEModel` | 嵌入、整合、微调后注释 | [t_uce](t_uce.ipynb) |
| [scMulan](t_fm_scmulan_guide.md) | `scmulan` | `ScMulanModel` | 嵌入、零样本注释（不支持微调） | 无（未执行） |

## 模型方法

所有模型继承自 `SCLLMBase`（`load_model`、`preprocess`、`predict`、`fine_tune`、`get_embeddings`、`save_model`）。其余方法仅部分模型提供（已对照代码核实）：

| method | scGPT | scFoundation | Geneformer | CellPLM | UCE | scMulan |
|---|---|---|---|---|---|---|
| `get_embeddings` | yes | yes | yes | yes | yes | yes |
| `predict(task=...)` | annotation / embedding / integration | embedding / annotation / integration / generation | embedding / annotation / perturbation | annotation / embedding / imputation / integration | embedding；微调后 annotation | annotation |
| `fine_tune` | yes | yes | yes | yes | yes | 未实现 |
| `integrate` | yes | — | yes | yes | yes | — |
| `train_integration` | yes | — | — | yes | — | — |
| `predict_celltypes` | yes | yes | yes | yes | — | — |
| `predict_celltype` | — | — | — | — | yes | — |
| `predict_with_finetune` | — | yes | — | yes | — | — |
| `perturb_genes` | — | — | yes | — | — | — |
| `predict_perturbation` | yes | — | — | — | — | — |

`ModelFactory` 还提供 `available_models()` 与 `register_model(model_type, model_class)`（类必须继承 `SCLLMBase`）。

## 辅助函数

`omicverse.llm.model_factory` 包含按模型划分的便捷函数，创建模型并运行完整流程。各模型页面列出了详细签名：

```python
from omicverse.llm.model_factory import (
    load_scgpt, annotate_with_scgpt, integrate_with_scgpt,
    get_embeddings_with_scfoundation, extract_geneformer_embeddings,
    perturb_genes_with_geneformer, get_embeddings_with_cellplm,
)
```

| 模型 | 辅助函数 |
|---|---|
| [scGPT](t_fm_scgpt_guide.md) | `load_scgpt`, `annotate_with_scgpt`, `fine_tune_scgpt`, `predict_celltypes_workflow`, `end_to_end_scgpt_annotation`, `train_integration_scgpt`, `integrate_batches_workflow`, `end_to_end_scgpt_integration`, `integrate_with_scgpt` |
| [scFoundation](t_fm_scfoundation_guide.md) | `load_scfoundation`, `get_embeddings_with_scfoundation`, `end_to_end_scfoundation_embedding`, `fine_tune_scfoundation`, `predict_celltypes_with_scfoundation`, `end_to_end_scfoundation_annotation`, `integrate_with_scfoundation`, `integrate_batches_with_scfoundation`, `end_to_end_scfoundation_integration` |
| [Geneformer](t_fm_geneformer_guide.md) | `load_geneformer`, `annotate_with_geneformer`, `extract_geneformer_embeddings`, `perturb_genes_with_geneformer`, `fine_tune_geneformer` |
| [CellPLM](t_fm_cellplm_guide.md) | `load_cellplm`, `get_embeddings_with_cellplm`, `end_to_end_cellplm_embedding`, `fine_tune_cellplm`, `predict_celltypes_with_cellplm`, `end_to_end_cellplm_annotation`, `integrate_with_cellplm`, `end_to_end_cellplm_integration` |
| UCE、scMulan | 无 |

## 权重下载

`omicverse.llm.model_download` 内置权重来源注册表（Hugging Face、直链、Google Drive 文件夹）：

```python
from omicverse.llm.model_download import list_available_models, download_model

list_available_models()                      # e.g. 'geneformer-v2-104m', 'scfoundation', 'uce', 'scmulan', 'scgpt-whole-human', ...
path = download_model("geneformer-v2-104m", target_dir="llm_model/models/geneformer")
```

默认目录为 `$OMICVERSE_HOME/models` 或 `~/.cache/omicverse/models`。CellPLM 权重不在注册表中（请按其页面中的链接下载）。

## 尚未集成的模型

这 16 个 model type 在 `ModelFactory` 中注册为占位对象（`omicverse.llm.external_model_stubs`）。`create_model` 可用，但所有任务都会抛出带原因与上游地址的 `ModelExecutionBlockedError`。它们没有任何嵌入、注释或整合功能。

| 模型 | model_type | 占位类 | 将需要 |
|---|---|---|---|
| [scBERT](t_fm_scbert_guide.md) | `scbert` | `ScBERTModel` | 上游权重 |
| [GeneCompass](t_fm_genecompass_guide.md) | `genecompass` | `GeneCompassModel` | 上游权重 |
| [Nicheformer](t_fm_nicheformer_guide.md) | `nicheformer` | `NicheformerModel` | 上游权重 |
| [tGPT](t_fm_tgpt_guide.md) | `tgpt` | `TGPTModel` | 上游权重 |
| [CellFM](t_fm_cellfm_guide.md) | `cellfm` | `CellFMModel` | 上游权重 |
| [scCello](t_fm_sccello_guide.md) | `sccello` | `ScCelloModel` | 上游权重 |
| [scPRINT](t_fm_scprint_guide.md) | `scprint` | `ScPrintModel` | 上游权重 |
| [AIDO.Cell](t_fm_aidocell_guide.md) | `aidocell` | `AiDocellModel` | 上游权重 |
| [PULSAR](t_fm_pulsar_guide.md) | `pulsar` | `PulsarModel` | 上游权重 |
| [ATACformer](t_fm_atacformer_guide.md) | `atacformer` | `AtacformerModel` | 上游权重 |
| [scPlantLLM](t_fm_scplantllm_guide.md) | `scplantllm` | `ScPlantLLMModel` | 上游权重 |
| [LangCell](t_fm_langcell_guide.md) | `langcell` | `LangCellModel` | 上游权重 |
| [Cell2Sentence](t_fm_cell2sentence_guide.md) | `cell2sentence` | `Cell2SentenceModel` | 上游权重 |
| [GenePT](t_fm_genept_guide.md) | `genept` | `GenePTModel` | 无需 + OPENAI_API_KEY |
| [ChatCell](t_fm_chatcell_guide.md) | `chatcell` | `ChatCellModel` | 无需 |
| [Tabula](t_fm_tabula_guide.md) | `tabula` | `TabulaModel` | 上游权重 |

```python
try:
    ov.llm.ModelFactory.create_model("scbert").get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err.model_name, err.reason, err.checkpoint_url)
```

`ModelExecutionBlockedError` 属性：`model_name`、`status`、`reason`、`checkpoint_url`、`required_env_vars`、`required_checkpoint`。

## 迁移

已移除的高层管理器及其方法与模型对象 `model = ov.llm.ModelFactory.create_model(model_type, model_path, device, **kw)` 的对应关系：

| 已移除的调用 | 替代写法 |
|---|---|
| `annotate_cells(adata)` | `model.predict(adata, task="annotation")` |
| `get_embeddings(adata)` | `model.get_embeddings(adata)` |
| `fine_tune(train, valid, task)` | `model.fine_tune(train_adata=train, valid_adata=valid, task=task)` |
| `train_integration(...)` | `model.train_integration(train_adata=..., valid_adata=..., batch_key=...)` |
| `integrate(adata, batch_key)` | `model.integrate(adata, batch_key=...)` |
| `predict_celltypes(q)` | `model.predict_celltypes(q)`（scGPT、scFoundation、Geneformer、CellPLM）或 `model.predict(q, task="annotation")` |
| `perturb_genes(adata, genes, type)` | `model.perturb_genes(adata, genes, type)`（仅 Geneformer） |
| `save_model(path)` | `model.save_model(path)` |
| `manager.model` | `model` |

## 教程

- [ov.llm 概览 notebook](t_fm.ipynb)
- [scGPT](t_scgpt.ipynb)
- [scFoundation](t_scfoundation.ipynb)
- [Geneformer](t_geneformer.ipynb)
- [CellPLM](t_cellplm.ipynb)
- [UCE](t_uce.ipynb)
