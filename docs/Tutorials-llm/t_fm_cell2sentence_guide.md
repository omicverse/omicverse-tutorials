# Cell2Sentence

**Status in `ov.llm`: not integrated yet** (placeholder `Cell2SentenceModel`, model type `"cell2sentence"`).

## What the model is

Converts cells into text "sentences" so that a language model can be fine-tuned on them (summary of the upstream model).

## What exists in omicverse

- `"cell2sentence"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("cell2sentence")` returns a `Cell2SentenceModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

Cell2Sentence is registered but the cells-to-text conversion and downstream embedding stack are not integrated yet.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("cell2sentence")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # cell2sentence cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/vandijklab/cell2sentence
```

Message printed by the placeholder: `cell2sentence cannot run task 'embed': Cell2Sentence is registered but the cells-to-text conversion and downstream embedding stack are not integrated yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/vandijklab/cell2sentence>
- [Foundation models in ov.llm](t_fm_guide.md)
