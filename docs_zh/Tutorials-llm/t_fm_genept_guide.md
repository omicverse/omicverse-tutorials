# GenePT

**`ov.llm` 中的状态：尚未集成**（占位类 `GenePTModel`，model type `"genept"`）。

## 模型简介

通过 API 获得的 GPT-3.5 基因嵌入（以基因而非细胞为单位）（上游模型概述）。

## omicverse 中已有的内容

- `ov.llm.ModelFactory.available_models()` 中包含 `"genept"`，`ModelFactory.create_model("genept")` 返回占位对象 `GenePTModel`（`omicverse.llm.external_model_stubs`）。
- 构造占位对象或 `load_model(None)` 均不需要权重。
- `predict`、`fine_tune`、`get_embeddings`、`save_model` 一律抛出 `ModelExecutionBlockedError`，其中带有原因、上游地址与所需环境变量。

## 缺少的部分

GenePT 依赖外部 API 提供的基因嵌入，目前无法通过本地 omicverse.llm 运行。

占位对象记录的所需环境变量：`OPENAI_API_KEY`。

## 目前可以运行的内容

只有下面的占位行为可以运行；`ov.llm` 中此模型没有嵌入、注释或整合功能。

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("genept")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # genept cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/yiqunchen/GenePT
```

占位对象打印的消息：`genept cannot run task 'embed': GenePT requires external API-backed gene embeddings and is not runnable through the local omicverse.llm stack yet.`

在集成之前如需使用该模型，请直接运行上游实现。继承 `SCLLMBase` 的自定义封装可通过 `ov.llm.ModelFactory.register_model("name", MyModel)` 接入。

## 参考

- 上游仓库：<https://github.com/yiqunchen/GenePT>
- [ov.llm 基础模型总览](t_fm_guide.md)
