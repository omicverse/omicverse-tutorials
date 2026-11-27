# Tabula

**Status in `ov.llm`: not integrated yet** (placeholder `TabulaModel`, model type `"tabula"`).

## What the model is

Privacy-preserving federated learning with a tabular transformer (summary of the upstream model).

## What exists in omicverse

- `"tabula"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("tabula")` returns a `TabulaModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

Tabula is registered but its federated perturbation runtime is not integrated into omicverse.llm yet.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("tabula")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # tabula cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/aristoteleo/tabula
```

Message printed by the placeholder: `tabula cannot run task 'embed': Tabula is registered but its federated perturbation runtime is not integrated into omicverse.llm yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/aristoteleo/tabula>
- [Foundation models in ov.llm](t_fm_guide.md)
