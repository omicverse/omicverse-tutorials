# GenePT

**Status in `ov.llm`: not integrated yet** (placeholder `GenePTModel`, model type `"genept"`).

## What the model is

GPT-3.5 based gene embeddings obtained through an API (per gene, not per cell) (summary of the upstream model).

## What exists in omicverse

- `"genept"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("genept")` returns a `GenePTModel` placeholder (`omicverse.llm.external_model_stubs`).
- No checkpoint is required to construct or `load_model(None)` the placeholder.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

GenePT requires external API-backed gene embeddings and is not runnable through the local omicverse.llm stack yet.

Required environment variables recorded by the placeholder: `OPENAI_API_KEY`.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("genept")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # genept cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/yiqunchen/GenePT
```

Message printed by the placeholder: `genept cannot run task 'embed': GenePT requires external API-backed gene embeddings and is not runnable through the local omicverse.llm stack yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/yiqunchen/GenePT>
- [Foundation models in ov.llm](t_fm_guide.md)
