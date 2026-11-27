# ChatCell

**Status in `ov.llm`: not integrated yet** (placeholder `ChatCellModel`, model type `"chatcell"`).

## What the model is

Conversational interface for single-cell analysis with zero-shot annotation through dialogue (summary of the upstream model).

## What exists in omicverse

- `"chatcell"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("chatcell")` returns a `ChatCellModel` placeholder (`omicverse.llm.external_model_stubs`).
- No checkpoint is required to construct or `load_model(None)` the placeholder.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

ChatCell requires the upstream conversational analysis stack and credentials, which are not integrated into omicverse.llm yet.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("chatcell")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # chatcell cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/chatcell/CHATCELL
```

Message printed by the placeholder: `chatcell cannot run task 'embed': ChatCell requires the upstream conversational analysis stack and credentials, which are not integrated into omicverse.llm yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/chatcell/CHATCELL>
- [Foundation models in ov.llm](t_fm_guide.md)
