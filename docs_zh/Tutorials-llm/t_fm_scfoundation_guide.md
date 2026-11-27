# scFoundation

**`ov.llm` 中的状态：已集成**（model type `"scfoundation"`，类 `ScFoundationModel`）。

## 简介

**scFoundation**（xTrimoGene）是在固定 19,264 基因词表上预训练的大规模非对称编码器-解码器 Transformer。在 `ov.llm`（`ScFoundationModel`）中提供细胞嵌入、线性探测微调注释，以及嵌入 + 事后校正的批次整合。

文献：Hao, M. 等. Large-scale foundation model on single-cell transcriptomics. *Nature Methods* 21, 1481–1491 (2024)。代码：<https://github.com/biomap-research/scFoundation>

## `ov.llm` 支持的任务

| 任务 | 调用 | 说明 |
|---|---|---|
| embedding | `model.get_embeddings(adata, output_type="cell", pool_type="all")` | 已执行教程中细胞嵌入为 3072 维 |
| annotation | `model.fine_tune(train_adata=...)` → `model.predict_celltypes(adata)` / `model.predict_with_finetune(adata)` / `model.predict(adata, task="annotation")` | 线性探测微调（`frozen_more=True` 冻结 token/位置嵌入） |
| integration | `model.predict(adata, task="integration", batch_key=..., correction_method=...)` | 在嵌入上做事后校正。`ScFoundationModel` 没有 `integrate()` 方法，请使用 `predict` |
| generation | `model.predict(adata, task="generation")` is listed in the docstring | 包装器声明支持，但本处无教程覆盖；请视为未测试 |

并非每个模型都实现所有方法；调用不存在的方法会抛出 `AttributeError`（例如只有 Geneformer 提供 `perturb_genes`）。

## 权重获取

作者共享文件夹中的 `models.ckpt`（已执行教程给出 SharePoint 链接）；注册表键 `scfoundation` 指向 Hugging Face 仓库 `genbio-ai/scFoundation`（`omicverse.llm.model_download.download_model('scfoundation', target_dir)`）。

## 最小示例

该示例需要上述权重和 GPU，本页不执行。相同的调用已在教程 [scFoundation 教程](t_scfoundation.ipynb) 中完整执行并保留输出。

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
res = model.predict(adata, task="integration", batch_key="batch",
                    correction_method="mnn", pre_normalized="T")
adata.obsm["X_scfoundation_fine"] = res["embeddings"]
anno = model.predict(adata, task="annotation", pre_normalized="T")
```

## 输出

| 调用 | 返回 |
|---|---|
| `get_embeddings` | ndarray `(n_cells, 3072)` |
| `predict(task="integration")` | dict：`embeddings` |
| `predict_celltypes` | dict：`predictions`、`predicted_celltypes`、`probabilities`、`celltype_mapping`、`prediction_summary` |

需自行保存结果（教程：`obsm['X_scfoundation']`、`obsm['X_scfoundation_fine']`）。`pre_normalized` 取 `'T'`、`'F'`、`'A'`（已归一化/原始计数/自动）。

## 辅助函数

`omicverse.llm.model_factory` 中的便捷函数，一次调用完成建模型与整套流程，例如 `from omicverse.llm.model_factory import load_scfoundation`。

| 函数 | 用途 |
|---|---|
| `load_scfoundation(model_path, device=None, **kwargs)` | 加载 scFoundation 模型对象 |
| `get_embeddings_with_scfoundation(adata, model_path, device=None, output_type='cell', **kwargs)` | 加载并提取嵌入 |
| `end_to_end_scfoundation_embedding(adata, model_path, save_embeddings_path=None, device=None, output_type='cell', pool_type='all', **kwargs)` | 提取嵌入，可选保存到磁盘 |
| `fine_tune_scfoundation(train_adata, model_path, valid_adata=None, save_path=None, device=None, **kwargs)` | 在参考数据上线性探测微调 |
| `predict_celltypes_with_scfoundation(query_adata, finetuned_model_path, device=None, save_predictions=True, **kwargs)` | 用微调权重预测细胞类型 |
| `end_to_end_scfoundation_annotation(reference_adata, query_adata, pretrained_model_path, save_finetuned_path=None, device=None, validation_split=0.2, **kwargs)` | 参考集微调后注释查询集 |
| `integrate_with_scfoundation(query_adata, model_path, batch_key='batch', correction_method='harmony', device=None, save_embeddings=True, **kwargs)` | 嵌入 + 事后批次校正 |
| `integrate_batches_with_scfoundation(query_adata, model_path, batch_key='batch', correction_method='harmony', device=None, save_embeddings=True, **kwargs)` | 与 `integrate_with_scfoundation` 签名相同的另一入口 |
| `end_to_end_scfoundation_integration(query_adata, model_path, batch_key='batch', correction_methods=['harmony'], device=None, save_all_methods=False, **kwargs)` | 多种校正方法的整合 |

## 相关页面

- [ov.llm 基础模型总览](t_fm_guide.md)
- [scFoundation 教程（已执行）](t_scfoundation.ipynb)
