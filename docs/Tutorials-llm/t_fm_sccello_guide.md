# scCello

**Status in `ov.llm`: not integrated yet** (placeholder `ScCelloModel`, model type `"sccello"`).

## What the model is

Embeddings aligned with the cell ontology for zero-shot, hierarchy-consistent annotation (summary of the upstream model).

## What exists in omicverse

- `"sccello"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("sccello")` returns a `ScCelloModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

scCello download metadata exists, but the model runtime and zero-shot annotation stack are not integrated yet.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("sccello")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # sccello cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/cellarium-ai/scCello
```

Message printed by the placeholder: `sccello cannot run task 'embed': scCello download metadata exists, but the model runtime and zero-shot annotation stack are not integrated yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/cellarium-ai/scCello>
- [Foundation models in ov.llm](t_fm_guide.md)
