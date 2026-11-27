# scCello

**`ov.llm` 中的状态：尚未集成**（占位类 `ScCelloModel`，model type `"sccello"`）。

## 模型简介

与细胞本体对齐的嵌入，用于层级一致的零样本注释（上游模型概述）。

## omicverse 中已有的内容

- `ov.llm.ModelFactory.available_models()` 中包含 `"sccello"`，`ModelFactory.create_model("sccello")` 返回占位对象 `ScCelloModel`（`omicverse.llm.external_model_stubs`）。
- `load_model(path)` 只检查权重路径是否存在并把占位对象标记为已加载，不会加载任何权重。
- `predict`、`fine_tune`、`get_embeddings`、`save_model` 一律抛出 `ModelExecutionBlockedError`，其中带有原因、上游地址与所需环境变量。

## 缺少的部分

scCello 有下载元数据，但模型运行时与零样本注释栈尚未集成。

## 目前可以运行的内容

只有下面的占位行为可以运行；`ov.llm` 中此模型没有嵌入、注释或整合功能。

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("sccello")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # sccello cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/cellarium-ai/scCello
```

占位对象打印的消息：`sccello cannot run task 'embed': scCello download metadata exists, but the model runtime and zero-shot annotation stack are not integrated yet.`

在集成之前如需使用该模型，请直接运行上游实现。继承 `SCLLMBase` 的自定义封装可通过 `ov.llm.ModelFactory.register_model("name", MyModel)` 接入。

## 参考

- 上游仓库：<https://github.com/cellarium-ai/scCello>
- [ov.llm 基础模型总览](t_fm_guide.md)
