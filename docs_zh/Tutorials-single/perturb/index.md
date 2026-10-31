# 虚拟基因扰动

`ov.single.perturb` 为基因敲除（KO）、敲低（KD）和过表达（OE）提供统一接口，
返回 `PerturbResult`。不同后端提供的响应、转移及调控网络结果有所不同。

| 后端 | 输入与主要结果 |
|---|---|
| `sctenifoldknk` | 单细胞表达数据；通过调控网络扰动计算基因响应 |
| `cell_oracle` | 表达数据与 base GRN；提供响应、转移及调控网络结果 |
| `dynamo` | 速度兼容数据与向量场；提供逐细胞模型响应和扰动转移结果，不重建 GRN |

`backend='auto'` 优先选择含 `VecFld_pca` 的 dynamo 数据；存在 base GRN 时选择
CellOracle，否则选择 scTenifoldKnk。需要指定模型时，请显式设置 `backend`。

## dynamo 分析

对于尚未处理的数据，`backend_kwargs={'auto_pipeline': True}` 可完成缺失的 PCA、
动力学估计、邻居图、嵌入和向量场拟合。输入需包含剪接或代谢标记计数层及实验设计
所需的采样信息，仅有表达矩阵不足以估计速度。靶基因标识符应与 `adata.var_names`
一致，并被纳入 PCA 特征。

KD 将靶基因表达设为其平均表达除以 `fold_change`，OE 设为平均表达乘以
`fold_change`；各细胞使用共同的目标水平，不是逐细胞按比例缩放。
`group` 可生成分组响应排名，`vf_ko=True` 可在 KO 模式下附加原生 KO 速度；该计算需要默认 PCA 模型及 `VecFld_pca`。

可通过 `backend_kwargs['expression']` 显式覆盖自动目标水平，单位由原生 raw／z-score
模式决定；标量应用于全部靶基因，序列按调用者的靶基因顺序对应。支持已准备的自定义
PCA 键及载荷／均值数组。1.5.3 中不可用的预计算 `delta_Y` 路径，以及 PCA／完整基因
索引不一致的靶基因清零组合，会被明确拒绝。原生参数与兼容边界详见教程。

## 结果解释

- `result.delta_X` 及指定响应层保存逐细胞、逐基因的有符号模型响应。
- `result.trajectory_shift` 保存扰动转移矩阵；`projection_method='transform'`
  仅生成嵌入箭头，该字段为 `None`。
- `result.adata_perturbed.X` 保留基线表达，可能已经过自动预处理，不是预测计数。
- `result.grn` 和 `result.grn_base` 始终为 `None`；`result.delta_grn` 为空表，
  即使设置 `grn_output=True` 也不重建网络。
- `delta_expr` 中的 `mean_pert` 是基线均值加平均响应的派生汇总值；任一均值为负
  或非有限值时，`log2_fc` 为 `NaN`。模型响应保留，不进行裁剪。

教程包括参数说明、原始数据流程和常见问题：

```{toctree}
:maxdepth: 1

t_perturb_dynamo
```
