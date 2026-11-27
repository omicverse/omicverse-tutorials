# scMulan

**`ov.llm` 中的状态：已集成**（model type `"scmulan"`，类 `ScMulanModel`）。

## 简介

**scMulan** 是多任务生成式预训练语言模型，把细胞表示为基因 token 加元信息（细胞类型、器官等）的句子。在 `ov.llm`（`ScMulanModel`）中封装了 `omicverse.external.scMulan` 内置的推理代码，**仅支持嵌入与细胞类型注释**。微调与 `save_model` 未实现，会抛出 `ModelExecutionBlockedError`。scMulan 目前没有已执行教程。

文献：Bian, H. 等. scMulan: a multitask generative pre-trained language model for single-cell analysis. *RECOMB* 2024。代码：<https://github.com/SuperBianC/scMulan>

## `ov.llm` 支持的任务

| 任务 | 调用 | 说明 |
|---|---|---|
| embedding | `model.get_embeddings(adata)` | 返回 float32 ndarray（scMulan 自身的 `X_scMulan`） |
| annotation | `model.predict(adata, task="annotation")` | 零样本；其他 `task` 会抛出 `ValueError` |
| fine-tuning / saving | `model.fine_tune(...)`, `model.save_model(...)` | 未实现：抛出 `ModelExecutionBlockedError` |

并非每个模型都实现所有方法；调用不存在的方法会抛出 `AttributeError`（例如只有 Geneformer 提供 `perturb_genes`）。

## 权重获取

作者清华云盘链接中的 `ckpt_scMulan.pt`（<https://cloud.tsinghua.edu.cn/f/2250c5df51034b2e9a85/?dl=1>）；注册表键 `scmulan`。`model_path` 可为文件，或包含 `ckpt_scMulan.pt`、`model.pt`、`model.pth` 的文件夹。基因符号元文件 `meta_info.pt` 随 `omicverse.external.scMulan` 提供（可用 `meta_info_path=` 覆盖）。

## 最小示例

该示例需要上述权重和 GPU。文档中**未**执行过，scMulan 目前也没有教程 notebook；请视为依据代码编写的 API 示意。

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

## 输出

| 调用 | 返回 |
|---|---|
| `get_embeddings` | float32 ndarray `(n_cells, n_dim)` |
| `predict(task="annotation")` | dict：`predicted_celltypes`（来自 `obs['cell_type_from_scMulan']`）、`embeddings` |

scMulan 在副本上运行：`preprocess` 统一基因符号、转 CSC，并在 `X.max() > 10` 时做 log 归一化。需自行保存返回的数组。

## 辅助函数

scMulan 没有专用辅助函数，请直接使用 `ModelFactory.create_model` 与模型方法。

## 相关页面

- [ov.llm 基础模型总览](t_fm_guide.md)
