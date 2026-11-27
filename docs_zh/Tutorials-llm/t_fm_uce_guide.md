# UCE

**`ov.llm` 中的状态：已集成**（model type `"uce"`，类 `UCEModel`）。

## 简介

**UCE（Universal Cell Embeddings）** 是在八个物种的细胞图谱数据上自监督训练的 Transformer。基因通过 ESM2 蛋白嵌入与基因组位置做 token 化，跨物种无需对齐基因词表。`UCEModel` 提供零样本嵌入、基于嵌入的批次整合，以及加分类头微调（冻结/不冻结骨干）后的注释。

文献：Rosen, Y. 等. Universal Cell Embeddings: A Foundation Model for Cell Biology. *bioRxiv* (2023)。代码：<https://github.com/snap-stanford/UCE>

## `ov.llm` 支持的任务

| 任务 | 调用 | 说明 |
|---|---|---|
| embedding | `model.get_embeddings(adata, filter_cells=False, filter_genes=False)` | `(n_cells, 1280)` |
| integration | `model.integrate(adata, batch_key=..., correction_method="mnn")` | `correction_method` 可选 `harmony`、`mnn`、`center_scale`、`none` |
| annotation | `model.fine_tune(train_adata=..., freeze_backbone=True/False)` → `model.predict(adata, task="annotation")` / `model.predict_celltype(adata)` | 微调前 `predict(task="annotation")` 会抛出 `ValueError`（仅 `embedding` 可用） |

并非每个模型都实现所有方法；调用不存在的方法会抛出 `AttributeError`（例如只有 Geneformer 提供 `perturb_genes`）。

## 权重获取

UCE 作者的 figshare 文件包：`4layer_model.torch`、`species_chrom.csv`、`species_offsets.pkl`、token 嵌入文件（教程中为 `all_tokens.torch`）和需解压的 `protein_embeddings.tar.gz`。注册表键 `uce` 可通过 `omicverse.llm.model_download.download_model('uce', target_dir)` 下载同一文件包。这五个路径需传给 `create_model`（`model_path`、`token_file`、`protein_embeddings_dir`、`spec_chrom_csv_path`、`offset_pkl_path`）。

## 最小示例

该示例需要上述权重和 GPU，本页不执行。相同的调用已在教程 [UCE 教程](t_uce.ipynb) 中完整执行并保留输出。

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model(
    model_type="uce",
    model_path="llm_model/models/UCE/4layer_model.torch",
    token_file="llm_model/models/UCE/all_tokens.torch",
    protein_embeddings_dir="llm_model/models/UCE/protein_embeddings/",
    spec_chrom_csv_path="llm_model/models/UCE/species_chrom.csv",
    offset_pkl_path="llm_model/models/UCE/species_offsets.pkl",
    species="human",
    device="cuda",
)

adata.obsm["X_uce"] = model.get_embeddings(adata, filter_cells=False, filter_genes=False)

res = model.integrate(adata, batch_key="batch", correction_method="mnn")
adata.obsm["X_uce_mnn"] = res["embeddings"]

model.fine_tune(train_adata=reference_adata, epochs=10, batch_size=32, lr=1e-4,
                freeze_backbone=True)
pred = model.predict(adata, task="annotation")
adata.obs["predicted_celltype"] = pred["predictions"]
```

## 输出

| 调用 | 返回 |
|---|---|
| `get_embeddings` | ndarray `(n_cells, 1280)` |
| `predict(task="embedding")` | dict：`embeddings`、`task`、`model_name` |
| `integrate` | dict：`embeddings`（校正后） |
| `predict(task="annotation")` + `fine_tune` | dict：`predictions`、`task`、`model_name`、`fine_tuned` |

需自行保存结果（教程：`obsm['X_uce']`、`obsm['X_uce_mnn']`、`obsm['X_uce_fine']`）。

## 辅助函数

UCE 没有专用辅助函数，请直接使用 `ModelFactory.create_model` 与模型方法。

## 相关页面

- [ov.llm 基础模型总览](t_fm_guide.md)
- [UCE 教程（已执行）](t_uce.ipynb)
