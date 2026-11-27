# scGPT

**`ov.llm` 中的状态：已集成**（model type `"scgpt"`，类 `ScGPTModel`）。

## 简介

**scGPT** 是面向单细胞多组学的生成式预训练 Transformer，在超过 3300 万个细胞上预训练。在 `ov.llm` 中封装为 `ScGPTModel`：细胞嵌入、微调后注释、批次整合（零样本嵌入 + 事后校正，或训练整合模型）以及扰动预测。

文献：Cui, H. 等. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. *Nature Methods* 21, 1470–1480 (2024)。代码：<https://github.com/bowang-lab/scGPT>

## `ov.llm` 支持的任务

| 任务 | 调用 | 说明 |
|---|---|---|
| embedding | `model.get_embeddings(adata)` | 返回 `(n_cells, 512)` ndarray（whole-human 权重） |
| annotation | `model.fine_tune(train_adata=...)` → `model.predict_celltypes(adata)` / `model.predict(adata, task="annotation")` | 参考集需要 `.obs` 细胞类型标签；必须先微调 |
| integration | `model.integrate(adata, batch_key=..., correction_method=...)`; `model.train_integration(...)` | `correction_method` 可选 `combat`、`mnn`、`center_scale`、`none`；经 `train_integration` 训练的模型使用自带整合头 |
| perturbation | `model.setup_generator_for_perturbation()`, `model.fine_tune_generator(...)`, `model.predict_perturbation(adata, target_genes, ...)` | 返回预测扰动后表达的 AnnData；执行版教程未覆盖 |

并非每个模型都实现所有方法；调用不存在的方法会抛出 `AttributeError`（例如只有 Geneformer 提供 `perturb_genes`）。

## 权重获取

权重由作者以 Google Drive 文件夹发布（`args.json`、`best_model.pt`、`vocab.json`）。`omicverse.llm.model_download` 的注册表包含 `scgpt-whole-human`、`scgpt-continual-pretrained`、`scgpt-brain`、`scgpt-blood`、`scgpt-heart`、`scgpt-lung`、`scgpt-kidney`、`scgpt-pan-cancer`；已执行教程用 `gdown` 下载 whole-human 文件夹。

## 最小示例

该示例需要上述权重和 GPU，本页不执行。相同的调用已在教程 [scGPT 教程](t_scgpt.ipynb) 中完整执行并保留输出。

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

## 输出

| 调用 | 返回 |
|---|---|
| `get_embeddings` | ndarray `(n_cells, 512)` |
| `predict_celltypes` | dict：`predicted_celltypes`、`predictions`（类别 id）、概率 |
| `integrate` | dict：`embeddings`（及批次统计） |
| `fine_tune` | dict：`best_accuracy`、`training_history`、`celltype_mapping`、`n_celltypes` |

模型不会自动写入 `adata`，需自行保存（教程使用 `obsm['X_scgpt']`、`obsm['X_scgpt_fine']`、`obs['predicted_celltype']`）。

## 辅助函数

`omicverse.llm.model_factory` 中的便捷函数，一次调用完成建模型与整套流程，例如 `from omicverse.llm.model_factory import load_scgpt`。

| 函数 | 用途 |
|---|---|
| `load_scgpt(model_path, device=None, **kwargs)` | 加载 scGPT 模型对象 |
| `annotate_with_scgpt(adata, model_path, device=None, **kwargs)` | 加载并调用 `predict(task="annotation")` |
| `fine_tune_scgpt(train_adata, model_path, valid_adata=None, save_path=None, device=None, **kwargs)` | 加载、在参考数据上微调，可选保存 |
| `predict_celltypes_workflow(query_adata, finetuned_model_path, device=None, save_predictions=True, **kwargs)` | 用微调后的 scGPT 权重预测细胞类型 |
| `end_to_end_scgpt_annotation(reference_adata, query_adata, pretrained_model_path, save_finetuned_path=None, device=None, validation_split=0.2, **kwargs)` | 参考集微调后注释查询集 |
| `train_integration_scgpt(train_adata, model_path, batch_key='batch', valid_adata=None, save_path=None, device=None, **kwargs)` | 训练 scGPT 批次整合 |
| `integrate_batches_workflow(query_adata, integration_model_path, batch_key='batch', device=None, save_embeddings=True, **kwargs)` | 用训练好的整合权重做批次整合 |
| `end_to_end_scgpt_integration(train_adata, query_adata, pretrained_model_path, batch_key='batch', save_integration_path=None, device=None, validation_split=0.2, **kwargs)` | 训练整合后整合查询集 |
| `integrate_with_scgpt(query_adata, model_path, batch_key='batch', correction_method='combat', device=None, save_embeddings=True, **kwargs)` | 零样本嵌入 + 事后批次校正 |

## 相关页面

- [ov.llm 基础模型总览](t_fm_guide.md)
- [scGPT 教程（已执行）](t_scgpt.ipynb)
