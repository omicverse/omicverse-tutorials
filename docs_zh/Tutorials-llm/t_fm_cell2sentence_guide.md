# Cell2Sentence

**`ov.llm` 中的状态：尚未集成**（占位类 `Cell2SentenceModel`，model type `"cell2sentence"`）。

## 模型简介

把细胞转换成文本“句子”，用于语言模型微调（上游模型概述）。

## omicverse 中已有的内容

- `ov.llm.ModelFactory.available_models()` 中包含 `"cell2sentence"`，`ModelFactory.create_model("cell2sentence")` 返回占位对象 `Cell2SentenceModel`（`omicverse.llm.external_model_stubs`）。
- `load_model(path)` 只检查权重路径是否存在并把占位对象标记为已加载，不会加载任何权重。
- `predict`、`fine_tune`、`get_embeddings`、`save_model` 一律抛出 `ModelExecutionBlockedError`，其中带有原因、上游地址与所需环境变量。

## 缺少的部分

Cell2Sentence 已注册，但细胞到文本的转换及下游嵌入栈尚未集成。

## 目前可以运行的内容

只有下面的占位行为可以运行；`ov.llm` 中此模型没有嵌入、注释或整合功能。

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("cell2sentence")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # cell2sentence cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/vandijklab/cell2sentence
```

占位对象打印的消息：`cell2sentence cannot run task 'embed': Cell2Sentence is registered but the cells-to-text conversion and downstream embedding stack are not integrated yet.`

在集成之前如需使用该模型，请直接运行上游实现。继承 `SCLLMBase` 的自定义封装可通过 `ov.llm.ModelFactory.register_model("name", MyModel)` 接入。

## 参考

- 上游仓库：<https://github.com/vandijklab/cell2sentence>
- [ov.llm 基础模型总览](t_fm_guide.md)
