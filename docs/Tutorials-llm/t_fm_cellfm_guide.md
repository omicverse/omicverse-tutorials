# CellFM

**Status in `ov.llm`: not integrated yet** (placeholder `CellFMModel`, model type `"cellfm"`).

## What the model is

MLP-based (non-transformer) model trained on about 126 million cells (summary of the upstream model).

## What exists in omicverse

- `"cellfm"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("cellfm")` returns a `CellFMModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

CellFM is registered but its upstream MLP checkpoint/runtime is not integrated into omicverse.llm yet.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("cellfm")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # cellfm cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/cellverse/CellFM
```

Message printed by the placeholder: `cellfm cannot run task 'embed': CellFM is registered but its upstream MLP checkpoint/runtime is not integrated into omicverse.llm yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/cellverse/CellFM>
- [Foundation models in ov.llm](t_fm_guide.md)
