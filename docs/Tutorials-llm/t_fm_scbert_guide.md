# scBERT

**Status in `ov.llm`: not integrated yet** (placeholder `ScBERTModel`, model type `"scbert"`).

## What the model is

BERT-style masked-gene pre-training with compact 200-dim embeddings (summary of the upstream model).

## What exists in omicverse

- `"scbert"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("scbert")` returns a `ScBERTModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

scBERT is registered but the upstream inference runtime is not yet integrated into omicverse.llm.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("scbert")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # scbert cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/TencentAILabHealthcare/scBERT
```

Message printed by the placeholder: `scbert cannot run task 'embed': scBERT is registered but the upstream inference runtime is not yet integrated into omicverse.llm.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/TencentAILabHealthcare/scBERT>
- Paper: <https://www.nature.com/articles/s42256-022-00534-z>
- [Foundation models in ov.llm](t_fm_guide.md)
