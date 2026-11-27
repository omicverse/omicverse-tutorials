# GeneCompass

**Status in `ov.llm`: not integrated yet** (placeholder `GeneCompassModel`, model type `"genecompass"`).

## What the model is

Pre-training enhanced with prior knowledge (gene regulatory networks, pathways) on about 120 million cells (summary of the upstream model).

## What exists in omicverse

- `"genecompass"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("genecompass")` returns a `GeneCompassModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

GeneCompass is registered but requires upstream graph-prior assets and runtime wiring before local inference can run.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("genecompass")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # genecompass cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/xCompass-AI/GeneCompass
```

Message printed by the placeholder: `genecompass cannot run task 'embed': GeneCompass is registered but requires upstream graph-prior assets and runtime wiring before local inference can run.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/xCompass-AI/GeneCompass>
- [Foundation models in ov.llm](t_fm_guide.md)
