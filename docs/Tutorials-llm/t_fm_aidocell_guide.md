# AIDO.Cell

**Status in `ov.llm`: not integrated yet** (placeholder `AiDocellModel`, model type `"aidocell"`).

## What the model is

Dense transformer from the AIDO family for label-free cell clustering (summary of the upstream model).

## What exists in omicverse

- `"aidocell"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("aidocell")` returns a `AiDocellModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

AiDocell is registered but its upstream AIDO runtime is not exposed through omicverse.llm yet.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("aidocell")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # aidocell cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/genbio-ai/AIDO
```

Message printed by the placeholder: `aidocell cannot run task 'embed': AiDocell is registered but its upstream AIDO runtime is not exposed through omicverse.llm yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/genbio-ai/AIDO>
- [Foundation models in ov.llm](t_fm_guide.md)
