# ATACformer

**Status in `ov.llm`: not integrated yet** (placeholder `AtacformerModel`, model type `"atacformer"`).

## What the model is

Transformer for ATAC-seq that takes accessible peaks (not genes) as input (summary of the upstream model).

## What exists in omicverse

- `"atacformer"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("atacformer")` returns a `AtacformerModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

Atacformer requires an ATAC-specific peak tokenizer/runtime that is not bundled in this repository.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("atacformer")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # atacformer cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/Atacformer/Atacformer
```

Message printed by the placeholder: `atacformer cannot run task 'embed': Atacformer requires an ATAC-specific peak tokenizer/runtime that is not bundled in this repository.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/Atacformer/Atacformer>
- [Foundation models in ov.llm](t_fm_guide.md)
