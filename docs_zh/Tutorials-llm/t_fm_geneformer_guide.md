# Geneformer

**`ov.llm` 中的状态：已集成**（model type `"geneformer"`，类 `GeneformerModel`）。

## 简介

**Geneformer** 是在大规模单细胞转录组上用 rank-value 编码预训练的上下文感知注意力模型。`GeneformerModel` 支持嵌入、微调后注释、基于嵌入的批次整合，以及 in silico 基因扰动（`overexpress`、`inhibit`、`delete`）。基因符号通过提供的字典文件映射到 Ensembl ID。

文献：Theodoris, C. V. 等. Transfer learning enables predictions in network biology. *Nature* 618, 616–624 (2023)。模型库：<https://huggingface.co/ctheodoris/Geneformer>

## `ov.llm` 支持的任务

| 任务 | 调用 | 说明 |
|---|---|---|
| embedding | `model.get_embeddings(adata, max_ncells=...)` | 已执行教程中 Geneformer-V2-104M 为 768 维 |
| annotation | `model.fine_tune(train_adata=...)` → `model.predict(adata, task="annotation")` / `model.predict_celltypes(adata)` | `fine_tune` 的 `task` 可为 `annotation`、`gene_classification` |
| integration | `model.integrate(adata, batch_key=..., correction_method=...)` | 在嵌入上做事后校正 |
| perturbation | `model.perturb_genes(adata, target_genes, perturb_type)`; `model.get_perturbed_adata(...)`, `model.compare_perturbed_expression(...)` | 仅 Geneformer 提供 `perturb_genes`；结果可供 `ov.pl.perturbation_*` 使用 |

并非每个模型都实现所有方法；调用不存在的方法会抛出 `AttributeError`（例如只有 Geneformer 提供 `perturb_genes`）。

## 权重获取

Hugging Face：<https://huggingface.co/ctheodoris/Geneformer>（如 `Geneformer-V2-104M` 模型目录，以及 `gene_median_dictionary_gc104M.pkl`、`token_dictionary_gc104M.pkl`、`ensembl_mapping_dict_gc104M.pkl`）。注册表键 `geneformer`、`geneformer-v2-316m`、`geneformer-v2-104m`、`geneformer-v1-10m` 可通过 `omicverse.llm.model_download.download_model` 下载。可选依赖：`tdigest`、`peft`（缺失时仅告警）。

## 最小示例

该示例需要上述权重和 GPU，本页不执行。相同的调用已在教程 [Geneformer 教程](t_geneformer.ipynb) 中完整执行并保留输出。

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

## 输出

| 调用 | 返回 |
|---|---|
| `get_embeddings` | ndarray `(n_cells, 768)`（V2-104M） |
| `integrate` | dict：`embeddings`（及统计） |
| `predict_celltypes` | dict：预测与统计 |
| `perturb_genes` | 扰动结果 dict（细胞级余弦变化、基因级变化）；可传给 `ov.pl.perturbation_*` |

需自行保存结果（教程：`obsm['X_geneformer_fine']`）。V2 分词需像教程那样提供 `adata.obs['cell_barcode']`。

## 辅助函数

`omicverse.llm.model_factory` 中的便捷函数，一次调用完成建模型与整套流程，例如 `from omicverse.llm.model_factory import load_geneformer`。

| 函数 | 用途 |
|---|---|
| `load_geneformer(model_path, gene_median_file, token_dictionary_file, gene_mapping_file, device=None, model_version='V1', **kwargs)` | 创建模型并用三个字典文件 `load_model` |
| `annotate_with_geneformer(adata, model_path, device=None, model_version='V1', **kwargs)` | 加载并 `predict(task="annotation")` |
| `extract_geneformer_embeddings(adata, model_path, device=None, model_version='V1', emb_layer=0, **kwargs)` | 加载并提取嵌入（`emb_layer` 选层） |
| `perturb_genes_with_geneformer(adata, target_genes, model_path, perturb_type='overexpress', device=None, model_version='V1', **kwargs)` | 一步完成 in silico 扰动 |
| `fine_tune_geneformer(train_adata, model_path, valid_adata=None, save_path=None, device=None, model_version='V1', task='annotation', **kwargs)` | 在参考数据上微调 |

## 相关页面

- [ov.llm 基础模型总览](t_fm_guide.md)
- [Geneformer 教程（已执行）](t_geneformer.ipynb)
