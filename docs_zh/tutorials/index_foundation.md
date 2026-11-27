# 基础模型

通过 `ov.llm.ModelFactory` 使用单细胞基础模型的教程与指南。已集成 6 个模型（scGPT、scFoundation、Geneformer、CellPLM、UCE、scMulan）；另有 16 个仅为注册占位，归入“尚未集成”。

## 概览

`ov.llm.ModelFactory` 与模型对象的用法、已集成模型清单，以及代码概览 notebook。

```{toctree}
:maxdepth: 1

../Tutorials-llm/t_fm_guide
../Tutorials-llm/t_fm

```

## 已集成模型

具备可用 `ov.llm` 实现的模型：每个模型一页指南；scGPT、Geneformer、UCE、scFoundation、CellPLM 另有已执行教程。scMulan 已集成嵌入与注释，但暂无已执行教程。

```{toctree}
:maxdepth: 1

../Tutorials-llm/t_fm_scgpt_guide
../Tutorials-llm/t_scgpt
../Tutorials-llm/t_fm_geneformer_guide
../Tutorials-llm/t_geneformer
../Tutorials-llm/t_fm_uce_guide
../Tutorials-llm/t_uce
../Tutorials-llm/t_fm_scfoundation_guide
../Tutorials-llm/t_scfoundation
../Tutorials-llm/t_fm_cellplm_guide
../Tutorials-llm/t_cellplm
../Tutorials-llm/t_fm_scmulan_guide

```

## 尚未集成：通用模型

仅为注册占位。这些模型在 `ov.llm` 中会抛出 `ModelExecutionBlockedError`，尚无嵌入、注释或整合实现。每页说明已有内容与缺失内容。

```{toctree}
:maxdepth: 1

../Tutorials-llm/t_fm_scbert_guide
../Tutorials-llm/t_fm_genecompass_guide
../Tutorials-llm/t_fm_nicheformer_guide
```

## 尚未集成：专用模型

仅为注册占位（`ov.llm` 中无可运行实现）。每页说明已有内容与缺失内容。

```{toctree}
:maxdepth: 1

../Tutorials-llm/t_fm_tgpt_guide
../Tutorials-llm/t_fm_cellfm_guide
../Tutorials-llm/t_fm_sccello_guide
../Tutorials-llm/t_fm_scprint_guide
../Tutorials-llm/t_fm_aidocell_guide
../Tutorials-llm/t_fm_pulsar_guide
../Tutorials-llm/t_fm_tabula_guide
```

## 尚未集成：领域专用与语言模型

仅为注册占位（`ov.llm` 中无可运行实现）。每页说明已有内容与缺失内容。

```{toctree}
:maxdepth: 1

../Tutorials-llm/t_fm_atacformer_guide
../Tutorials-llm/t_fm_scplantllm_guide
../Tutorials-llm/t_fm_langcell_guide
../Tutorials-llm/t_fm_cell2sentence_guide
../Tutorials-llm/t_fm_genept_guide
../Tutorials-llm/t_fm_chatcell_guide
```
