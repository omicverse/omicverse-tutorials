# PULSAR

**Status in `ov.llm`: not integrated yet** (placeholder `PulsarModel`, model type `"pulsar"`).

## What the model is

Multi-scale multicellular model capturing cell-cell communication and tissue organisation (summary of the upstream model).

## What exists in omicverse

- `"pulsar"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("pulsar")` returns a `PulsarModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

PULSAR is registered but its multicellular runtime is not integrated into omicverse.llm yet.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("pulsar")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # pulsar cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/pulsar-ai/PULSAR
```

Message printed by the placeholder: `pulsar cannot run task 'embed': PULSAR is registered but its multicellular runtime is not integrated into omicverse.llm yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/pulsar-ai/PULSAR>
- [Foundation models in ov.llm](t_fm_guide.md)
