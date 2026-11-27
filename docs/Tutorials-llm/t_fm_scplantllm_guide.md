# scPlantLLM

**Status in `ov.llm`: not integrated yet** (placeholder `ScPlantLLMModel`, model type `"scplantllm"`).

## What the model is

Plant-specific single-cell model handling polyploidy and plant gene nomenclature (summary of the upstream model).

## What exists in omicverse

- `"scplantllm"` is listed by `ov.llm.ModelFactory.available_models()` and `ModelFactory.create_model("scplantllm")` returns a `ScPlantLLMModel` placeholder (`omicverse.llm.external_model_stubs`).
- `load_model(path)` only checks that the checkpoint path exists and marks the placeholder as loaded; it loads no weights.
- `predict`, `fine_tune`, `get_embeddings` and `save_model` always raise `ModelExecutionBlockedError`, carrying the reason, the upstream URL and the required environment variables.

## What is missing

scPlantLLM is registered but its plant-specific runtime is not integrated into omicverse.llm yet.

## What you can run today

Only the placeholder behaviour below runs; there is no embedding, annotation or integration for this model in `ov.llm`.

```python
import omicverse as ov

model = ov.llm.ModelFactory.create_model("scplantllm")
try:
    model.get_embeddings(adata)
except ov.llm.ModelExecutionBlockedError as err:
    print(err)                 # scplantllm cannot run task 'embed': ...
    print(err.checkpoint_url)  # https://github.com/scPlantLLM/scPlantLLM
```

Message printed by the placeholder: `scplantllm cannot run task 'embed': scPlantLLM is registered but its plant-specific runtime is not integrated into omicverse.llm yet.`

To use the model before it is integrated, run the upstream implementation directly. A custom wrapper that subclasses `SCLLMBase` can be plugged in with `ov.llm.ModelFactory.register_model("name", MyModel)`.

## References

- Upstream repository: <https://github.com/scPlantLLM/scPlantLLM>
- [Foundation models in ov.llm](t_fm_guide.md)
