# Nicheformer

**Status in `ov.llm`: not integrated yet** (placeholder `NicheformerModel`, model type `"nicheformer"`).

## What the model is

Spatial transformer that jointly models spatial context and gene expression (summary of the upstream model).

## What exists in omicverse

- `"nicheformer"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("nicheformer")` returns a `NicheformerModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

Nicheformer needs an upstream spatial runtime and checkpoint layout that are not bundled in this repository.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("nicheformer")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # nicheformer cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/theislab/nicheformer
```

Message printed by the placeholder: `nicheformer cannot run task 'embed': Nicheformer needs an upstream spatial runtime and checkpoint layout that are not bundled in this repository.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/theislab/nicheformer>
- [Foundation models in ov.llm](t_fm_guide.md)
