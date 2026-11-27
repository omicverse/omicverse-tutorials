# ChatCell

**`ov.llm` 中的状态：尚未集成**（占位类 `ChatCellModel`，model type `"chatcell"`）。

## 模型简介

单细胞分析的对话式界面，通过对话做零样本注释（上游模型概述）。

## omicverse 中已有的内容

- `ov.llm.ModelFactory.available_models()` 中包含 `"chatcell"`，`ModelFactory.create_model("chatcell")` 返回占位对象 `ChatCellModel`（`omicverse.llm.external_model_stubs`）。
- 构造占位对象或 `load_model(None)` 均不需要权重。
- `predict`、`fine_tune`、`get_embeddings`、`save_model` 一律抛出 `ModelExecutionBlockedError`，其中带有原因、上游地址与所需环境变量。

## 缺少的部分

ChatCell 需要上游对话式分析栈和凭据，尚未集成到 omicverse.llm。

## 目前可以运行的内容

只有下面的占位行为可以运行；`ov.llm` 中此模型没有嵌入、注释或整合功能。

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("chatcell")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # chatcell cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/chatcell/CHATCELL
```

占位对象打印的消息：`chatcell cannot run task 'embed': ChatCell requires the upstream conversational analysis stack and credentials, which are not integrated into omicverse.llm yet.`

在集成之前如需使用该模型，请直接运行上游实现。继承 `SCLLMBase` 的自定义封装可通过 `ov.llm.ModelFactory.register_model("name", MyModel)` 接入。

## 参考

- 上游仓库：<https://github.com/chatcell/CHATCELL>
- [ov.llm 基础模型总览](t_fm_guide.md)
