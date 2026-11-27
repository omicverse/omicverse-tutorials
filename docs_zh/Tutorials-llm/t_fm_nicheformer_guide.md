# Nicheformer

**`ov.llm` 中的状态：尚未集成**（占位类 `NicheformerModel`，model type `"nicheformer"`）。

## 模型简介

联合建模空间微环境与基因表达的空间 Transformer（上游模型概述）。

## omicverse 中已有的内容

- `ov.llm.ModelFactory.available_models()` 中包含 `"nicheformer"`，`ModelFactory.create_model("nicheformer")` 返回占位对象 `NicheformerModel`（`omicverse.llm.external_model_stubs`）。
- `load_model(path)` 只检查权重路径是否存在并把占位对象标记为已加载，不会加载任何权重。
- `predict`、`fine_tune`、`get_embeddings`、`save_model` 一律抛出 `ModelExecutionBlockedError`，其中带有原因、上游地址与所需环境变量。

## 缺少的部分

Nicheformer 需要上游空间运行时与检查点目录结构，本仓库未内置。

## 目前可以运行的内容

只有下面的占位行为可以运行；`ov.llm` 中此模型没有嵌入、注释或整合功能。

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("nicheformer")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # nicheformer cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/theislab/nicheformer
```

占位对象打印的消息：`nicheformer cannot run task 'embed': Nicheformer needs an upstream spatial runtime and checkpoint layout that are not bundled in this repository.`

在集成之前如需使用该模型，请直接运行上游实现。继承 `SCLLMBase` 的自定义封装可通过 `ov.llm.ModelFactory.register_model("name", MyModel)` 接入。

## 参考

- 上游仓库：<https://github.com/theislab/nicheformer>
- [ov.llm 基础模型总览](t_fm_guide.md)
