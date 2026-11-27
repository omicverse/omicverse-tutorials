# CellPLM

**`ov.llm` 中的状态：已集成**（model type `"cellplm"`，类 `CellPLMModel`）。

## 简介

**CellPLM** 是以细胞（而非基因）为 token、编码细胞间关系的单细胞预训练语言模型。`CellPLMModel` 提供嵌入、微调后注释、插补（pipeline）以及基于嵌入的批次整合。

文献：Wen, H. 等. CellPLM: pre-training of cell language model beyond single cells. *bioRxiv* (2023)；ICLR 2024。代码：<https://github.com/OmicsML/CellPLM>

## `ov.llm` 支持的任务

| 任务 | 调用 | 说明 |
|---|---|---|
| embedding | `model.get_embeddings(adata)` | 已执行教程中为 512 维 |
| annotation | `model.fine_tune(train_adata=...)` → `model.predict_celltypes(adata)` | `fine_tune` 的 `task` 可为 `annotation`、`imputation` |
| integration | `model.integrate(adata, batch_key=..., correction_method=...)`; `model.train_integration(...)` | 基于嵌入 |
| imputation | `model.predict(adata, task="imputation")` | 包装器文档声明；本处无教程覆盖 |

并非每个模型都实现所有方法；调用不存在的方法会抛出 `AttributeError`（例如只有 Geneformer 提供 `perturb_genes`）。

## 权重获取

作者的 Dropbox 文件夹（已执行教程中给出链接）：<https://www.dropbox.com/scl/fo/i5rmxgtqzg7iykt2e9uqm/h/ckpt>。默认 `pretrain_version` 为 `20231027_85M`；`model_path` 为存放权重及配置的文件夹。

## 最小示例

该示例需要上述权重和 GPU，本页不执行。相同的调用已在教程 [CellPLM 教程](t_cellplm.ipynb) 中完整执行并保留输出。

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

## 输出

| 调用 | 返回 |
|---|---|
| `get_embeddings` | ndarray `(n_cells, 512)` |
| `integrate` | dict：`embeddings` |
| `predict_celltypes` | dict：`predicted_celltypes`、`predictions`（类别 id）、统计 |

需自行保存结果（教程：`obsm['X_cellplm_fine']`、`obs['predicted_celltype']`）。

## 辅助函数

`omicverse.llm.model_factory` 中的便捷函数，一次调用完成建模型与整套流程，例如 `from omicverse.llm.model_factory import load_cellplm`。

| 函数 | 用途 |
|---|---|
| `load_cellplm(model_path, pretrain_version='20231027_85M', device=None, **kwargs)` | 加载 CellPLM 模型对象 |
| `get_embeddings_with_cellplm(adata, model_path, pretrain_version='20231027_85M', device=None, **kwargs)` | 加载并提取嵌入 |
| `end_to_end_cellplm_embedding(adata, model_path, pretrain_version='20231027_85M', save_embeddings_path=None, device=None, **kwargs)` | 提取嵌入，可选保存到磁盘 |
| `fine_tune_cellplm(train_adata, model_path, pretrain_version='20231027_85M', valid_adata=None, save_path=None, device=None, task='annotation', **kwargs)` | 在参考数据上微调 |
| `predict_celltypes_with_cellplm(query_adata, finetuned_model_path, pretrain_version='20231027_85M', device=None, save_predictions=True, **kwargs)` | 用微调权重预测细胞类型 |
| `end_to_end_cellplm_annotation(reference_adata, query_adata, model_path, pretrain_version='20231027_85M', save_finetuned_path=None, device=None, validation_split=0.2, **kwargs)` | 参考集微调后注释查询集 |
| `integrate_with_cellplm(query_adata, model_path, pretrain_version='20231027_85M', batch_key='batch', correction_method='harmony', device=None, save_embeddings=True, **kwargs)` | 嵌入 + 事后批次校正 |
| `end_to_end_cellplm_integration(query_adata, model_path, pretrain_version='20231027_85M', batch_key='batch', correction_methods=['harmony'], device=None, save_all_methods=False, **kwargs)` | 多种校正方法的整合 |

## 相关页面

- [ov.llm 基础模型总览](t_fm_guide.md)
- [CellPLM 教程（已执行）](t_cellplm.ipynb)
