# ATACformer

**`ov.llm` 中的状态：尚未集成**（占位类 `AtacformerModel`，model type `"atacformer"`）。

## 模型简介

面向 ATAC-seq 的 Transformer，以开放区域 peak（而非基因）为输入（上游模型概述）。

## omicverse 中已有的内容

- `ov.llm.ModelFactory.available_models()` 中包含 `"atacformer"`，`ModelFactory.create_model("atacformer")` 返回占位对象 `AtacformerModel`（`omicverse.llm.external_model_stubs`）。
- `load_model(path)` 只检查权重路径是否存在并把占位对象标记为已加载，不会加载任何权重。
- `predict`、`fine_tune`、`get_embeddings`、`save_model` 一律抛出 `ModelExecutionBlockedError`，其中带有原因、上游地址与所需环境变量。

## 缺少的部分

Atacformer 需要 ATAC 专用的 peak 分词器/运行时，本仓库未内置。

## 目前可以运行的内容

只有下面的占位行为可以运行；`ov.llm` 中此模型没有嵌入、注释或整合功能。

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("atacformer")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # atacformer cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/Atacformer/Atacformer
```

占位对象打印的消息：`atacformer cannot run task 'embed': Atacformer requires an ATAC-specific peak tokenizer/runtime that is not bundled in this repository.`

在集成之前如需使用该模型，请直接运行上游实现。继承 `SCLLMBase` 的自定义封装可通过 `ov.llm.ModelFactory.register_model("name", MyModel)` 接入。

## 参考

- 上游仓库：<https://github.com/Atacformer/Atacformer>
- [ov.llm 基础模型总览](t_fm_guide.md)
