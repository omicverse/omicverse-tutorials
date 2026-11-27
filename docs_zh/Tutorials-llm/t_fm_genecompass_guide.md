# GeneCompass

**`ov.llm` 中的状态：尚未集成**（占位类 `GeneCompassModel`，model type `"genecompass"`）。

## 模型简介

融合先验知识（基因调控网络、通路）的预训练，约 1.2 亿细胞（上游模型概述）。

## omicverse 中已有的内容

- `ov.llm.ModelFactory.available_models()` 中包含 `"genecompass"`，`ModelFactory.create_model("genecompass")` 返回占位对象 `GeneCompassModel`（`omicverse.llm.external_model_stubs`）。
- `load_model(path)` 只检查权重路径是否存在并把占位对象标记为已加载，不会加载任何权重。
- `predict`、`fine_tune`、`get_embeddings`、`save_model` 一律抛出 `ModelExecutionBlockedError`，其中带有原因、上游地址与所需环境变量。

## 缺少的部分

GeneCompass 已注册，但需要上游的图先验资源与运行时对接后才能本地推理。

## 目前可以运行的内容

只有下面的占位行为可以运行；`ov.llm` 中此模型没有嵌入、注释或整合功能。

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("genecompass")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # genecompass cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/xCompass-AI/GeneCompass
```

占位对象打印的消息：`genecompass cannot run task 'embed': GeneCompass is registered but requires upstream graph-prior assets and runtime wiring before local inference can run.`

在集成之前如需使用该模型，请直接运行上游实现。继承 `SCLLMBase` 的自定义封装可通过 `ov.llm.ModelFactory.register_model("name", MyModel)` 接入。

## 参考

- 上游仓库：<https://github.com/xCompass-AI/GeneCompass>
- [ov.llm 基础模型总览](t_fm_guide.md)
