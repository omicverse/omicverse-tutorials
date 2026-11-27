# LangCell

**Status in `ov.llm`: not integrated yet** (placeholder `LangCellModel`, model type `"langcell"`).

## What the model is

Dual-tower (text + cell) model aligning natural-language descriptions with cell embeddings (summary of the upstream model).

## What exists in omicverse

- `"langcell"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("langcell")` returns a `LangCellModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

LangCell is registered but its text-cell dual-tower runtime is not integrated into omicverse.llm yet.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("langcell")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # langcell cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/langcell/LangCell
```

Message printed by the placeholder: `langcell cannot run task 'embed': LangCell is registered but its text-cell dual-tower runtime is not integrated into omicverse.llm yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/langcell/LangCell>
- [Foundation models in ov.llm](t_fm_guide.md)
