# tGPT

**Status in `ov.llm`: not integrated yet** (placeholder `TGPTModel`, model type `"tgpt"`).

## What the model is

Autoregressive (GPT-style) next-token prediction of gene expression (summary of the upstream model).

## What exists in omicverse

- `"tgpt"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("tgpt")` returns a `TGPTModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

tGPT is registered but its autoregressive runtime is not wired into omicverse.llm yet.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("tgpt")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # tgpt cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/deeplearningplus/tGPT
```

Message printed by the placeholder: `tgpt cannot run task 'embed': tGPT is registered but its autoregressive runtime is not wired into omicverse.llm yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/deeplearningplus/tGPT>
- [Foundation models in ov.llm](t_fm_guide.md)
