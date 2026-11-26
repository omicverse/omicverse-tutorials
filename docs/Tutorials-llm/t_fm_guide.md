---
title: "ov.fm — Foundation Model Module"
---

# ov.fm — Foundation Model Module

`ov.fm` provides a **unified API** for discovering, selecting, validating, running, and interpreting single-cell foundation models. It wraps 17+ models (scGPT, Geneformer, UCE, scFoundation, CellPLM, and more) behind a consistent AnnData-based interface, with automatic data profiling and model selection.

!!! note "When to use ov.fm"

    Use `ov.fm` when you want to apply pretrained foundation models to single-cell data without manually configuring each model's preprocessing pipeline. It automatically handles gene ID conversion, compatibility checks, and output standardization for you.

---

## Quick Start

```python
import omicverse as ov

# 1. See the available models
models = ov.fm.list_models(task="embed")

# 2. Profile your data
profile = ov.fm.profile_data("pbmc3k.h5ad")

# 3. Which model fits best?
selection = ov.fm.select_model("pbmc3k.h5ad", task="embed")
print(selection["recommended"]["name"])

# 4. Is the data ready?
check = ov.fm.preprocess_validate("pbmc3k.h5ad", "scgpt", "embed")

# 5. Run the model
result = ov.fm.run(task="embed", model_name="scgpt", adata_path="pbmc3k.h5ad",
                   output_path="pbmc3k_embedded.h5ad")

# 6. Visualize and evaluate
metrics = ov.fm.interpret_results("pbmc3k_embedded.h5ad", task="embed")
```

---

## Six-Step Workflow

`ov.fm` is designed around six composable steps. You can use any step on its own, or chain all of them together.

```
Discover ──▸ Profile ──▸ Select ──▸ Validate ──▸ Run ──▸ Interpret
```

| Step | Function | Purpose |
|------|----------|---------|
| **Discover** | `list_models()`, `describe_model()` | Browse available models and their capabilities |
| **Profile** | `profile_data()` | Detect species, gene scheme, modality, and per-model compatibility |
| **Select** | `select_model()` | Score and rank models for your data and task |
| **Validate** | `preprocess_validate()` | Check data compatibility and get auto-fix suggestions |
| **Run** | `run()` | Execute model inference (embedding, annotation, integration, etc.) |
| **Interpret** | `interpret_results()` | Compute metrics (silhouette score), generate UMAP visualizations |

---

## API Reference

### `ov.fm.list_models`

```python
ov.fm.list_models(task=None, skill_ready_only=False) -> dict
```

Lists the available foundation models, with optional filtering.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `task` | str \| None | `None` | Filter by task: `"embed"`, `"annotate"`, `"integrate"`, `"perturb"`, `"spatial"`, `"drug_response"` |
| `skill_ready_only` | bool | `False` | Only return models with a fully implemented adapter |

**Returns:** A dict with `count` (int) and `models` (list of model summaries).

```python
result = ov.fm.list_models(task="embed")
for m in result["models"]:
    print(f"{m['name']:15s} status={m['status']:10s} tasks={m['tasks']}")
```

---

### `ov.fm.describe_model`

```python
ov.fm.describe_model(model_name: str) -> dict
```

Gets the full specification for a single model, including input/output contracts, hardware requirements, and resource links.

**Returns:** A dict with `model`, `input_contract`, `output_contract`, and `resources` keys.

```python
spec = ov.fm.describe_model("scgpt")
print(spec["input_contract"]["gene_id_scheme"])   # "symbol"
print(spec["output_contract"]["embedding_key"])    # "X_scGPT"
print(spec["output_contract"]["embedding_dim"])    # 512
```

---

### `ov.fm.profile_data`

```python
ov.fm.profile_data(adata_path: str) -> dict
```

Analyzes a `.h5ad` file and returns a data profile with automatic species/gene-scheme detection and per-model compatibility assessment.

**Returns:** A dict with `n_cells`, `n_genes`, `species`, `gene_scheme`, `modality`, `has_raw`, `layers`, `obs_columns`, `obsm_keys`, `batch_columns`, `celltype_columns`, `model_compatibility`.

```python
profile = ov.fm.profile_data("pbmc3k.h5ad")
print(f"Species: {profile['species']}")
print(f"Gene IDs: {profile['gene_scheme']}")

# See which models are compatible
for name, compat in profile["model_compatibility"].items():
    status = "OK" if compat["compatible"] else "ISSUES"
    print(f"  {name}: {status}")
```

---

### `ov.fm.select_model`

```python
ov.fm.select_model(
    adata_path: str,
    task: str,
    prefer_zero_shot: bool = True,
    max_vram_gb: int = None,
) -> dict
```

Scores and ranks models for a given dataset and task.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `adata_path` | str | — | Path to the `.h5ad` file |
| `task` | str | — | Task type (required) |
| `prefer_zero_shot` | bool | `True` | Prefer models that need no fine-tuning |
| `max_vram_gb` | int \| None | `None` | Maximum VRAM budget |

**Returns:** A dict with `recommended` (name + rationale), `fallbacks` (list), `preprocessing_notes`, `data_profile`.

**Scoring logic:**

- Skill-ready adapter: +100 (ready), +50 (partial), 0 (reference only)
- Zero-shot match: +30
- Gene-scheme match: +20
- CPU fallback supported: +10
- Low VRAM requirement: +5

```python
result = ov.fm.select_model("pbmc3k.h5ad", task="embed", prefer_zero_shot=True)
print(f"Recommended: {result['recommended']['name']}")
print(f"Rationale: {result['recommended']['rationale']}")
print(f"Fallbacks: {[f['name'] for f in result['fallbacks']]}")
```

---

### `ov.fm.preprocess_validate`

```python
ov.fm.preprocess_validate(
    adata_path: str,
    model_name: str,
    task: str,
) -> dict
```

Validates data compatibility with a specific model and task. Returns diagnostics and auto-fix suggestions.

**Returns:** A dict with `status` (`"ready"` | `"needs_preprocessing"` | `"incompatible"`), `diagnostics`, `auto_fixes`, `data_summary`.

```python
result = ov.fm.preprocess_validate("pbmc3k.h5ad", "scgpt", "embed")
if result["status"] == "ready":
    print("Data is ready for scGPT")
else:
    for diag in result["diagnostics"]:
        print(f"[{diag['severity']}] {diag['message']}")
    for fix in result["auto_fixes"]:
        print(f"Suggested fix: {fix['action']}")
        if "code" in fix:
            print(fix["code"])
```

---

### `ov.fm.run`

```python
ov.fm.run(
    task: str,
    model_name: str,
    adata_path: str,
    output_path: str = None,
    batch_key: str = None,
    label_key: str = None,
    device: str = "auto",
    batch_size: int = None,
    checkpoint_dir: str = None,
) -> dict
```

Runs a foundation model on your data.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `task` | str | — | Task type (required) |
| `model_name` | str | — | Model name (required) |
| `adata_path` | str | — | Path to the input `.h5ad` (required) |
| `output_path` | str \| None | `None` | Output path (defaults to overwriting the input file) |
| `batch_key` | str \| None | `None` | `.obs` column with batch labels (required for `integrate`) |
| `label_key` | str \| None | `None` | `.obs` column with cell-type labels |
| `device` | str | `"auto"` | `"auto"`, `"cuda"`, `"cpu"`, `"mps"` |
| `batch_size` | int \| None | `None` | Overrides the model's default batch size |
| `checkpoint_dir` | str \| None | `None` | Path to the model checkpoint directory |

**Returns:** On success, a dict with `output_path`, `output_keys`, `n_cells`, `status`; on failure, a dict with `error`, `status`.

**Execution flow:**

1. Validates the data via `preprocess_validate()`
2. Attempts conda subprocess execution (isolated environment)
3. Falls back to the in-process adapter if conda is unavailable
4. Writes results and provenance metadata to the output AnnData

```python
result = ov.fm.run(
    task="embed",
    model_name="scgpt",
    adata_path="pbmc3k.h5ad",
    output_path="pbmc3k_embedded.h5ad",
    device="cuda",
)
if "error" not in result:
    print(f"Output keys: {result['output_keys']}")
    print(f"Cells processed: {result['n_cells']}")
```

---

### `ov.fm.interpret_results`

```python
ov.fm.interpret_results(
    adata_path: str,
    task: str,
    output_dir: str = None,
    generate_umap: bool = True,
    color_by: list = None,
) -> dict
```

Generates quality metrics and visualizations for model outputs.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `adata_path` | str | — | Path to the `.h5ad` with model results |
| `task` | str | — | The task that was run |
| `output_dir` | str \| None | `None` | Output directory for visualizations |
| `generate_umap` | bool | `True` | Whether to generate a UMAP plot |
| `color_by` | list \| None | `None` | `.obs` columns to color the UMAP by |

**Computed metrics:**

- Embedding dimensionality and cell count
- Silhouette score (if cell-type labels and sklearn are available)
- Annotation column detection
- Provenance metadata from `adata.uns["fm"]`

```python
result = ov.fm.interpret_results(
    "pbmc3k_embedded.h5ad",
    task="embed",
    generate_umap=True,
    color_by=["louvain"],
)
for key, info in result["metrics"]["embeddings"].items():
    print(f"{key}: dim={info['dim']}, silhouette={info.get('silhouette', 'N/A')}")
```

---

## Supported Tasks

| Task | Description | Example Models |
|------|-------------|----------------|
| `embed` | Generate cell embeddings for downstream analysis | scGPT, Geneformer, UCE, CellPLM |
| `annotate` | Predict cell-type labels | scGPT (fine-tuned), sccello, ChatCell |
| `integrate` | Batch integration across datasets | scGPT, Geneformer, UCE |
| `perturb` | Perturbation-response prediction | scFoundation, Tabula |
| `spatial` | Spatial transcriptomics analysis | Nicheformer |
| `drug_response` | Drug-response modeling | scFoundation |

---

## Model Catalog

### Skill-Ready Models (Full Adapter)

These models have fully implemented adapters and can be run directly via `ov.fm.run()`.

| Model | Version | Tasks | Species | Gene IDs | GPU | Min VRAM |
|-------|---------|-------|---------|----------|-----|----------|
| **scGPT** | whole-human-2024 | embed, integrate | human, mouse | symbol | Yes | 8 GB |
| **Geneformer** | v2-106M | embed, integrate | human | ensembl | No (CPU-capable) | 4 GB |
| **UCE** | 4-layer | embed, integrate | 7 species | symbol | Yes | 16 GB |

### Partial-Spec Models

These models have partial specifications. They can be used for model selection and data profiling; execution capability depends on adapter availability.

| Model | Tasks | Modality | Key Strength |
|-------|-------|------------|-------------------|
| **scFoundation** | embed, integrate | RNA | 19K-gene vocabulary, perturbation pretraining |
| **scBERT** | embed, integrate | RNA | BERT-style masked language modeling |
| **GeneCompass** | embed, integrate | RNA | Pretrained on 120M cells |
| **CellPLM** | embed, integrate | RNA | Cell-centric (not gene-centric), high throughput |
| **Nicheformer** | embed, integrate, spatial | RNA, Spatial | Niche-aware spatial modeling |
| **scMulan** | embed, integrate | RNA, ATAC, Protein, Multi-omics | Native multi-omics |
| **Tabula** | embed, annotate, integrate, perturb | RNA | Federated learning + FlashAttention |
| **tGPT** | embed, integrate | RNA | Autoregressive next-token prediction |
| **CellFM** | embed, integrate | RNA | MLP architecture, 126M cells |
| **sccello** | embed, integrate, annotate | RNA | Zero-shot annotation via cell ontology |
| **scPRINT** | embed, integrate | RNA | Denoising + protein-coding-gene focus |
| **ATACformer** | embed, integrate | ATAC | Native peak-based ATAC-seq |
| **scPlantLLM** | embed, integrate | RNA | Plant-specific (Arabidopsis, rice, maize) |
| **LangCell** | embed, integrate | RNA | Text + cell alignment, natural-language queries |

!!! tip "Model selection cheat sheet"

    - **Default (RNA, human):** scGPT
    - **Ensembl IDs / CPU-only:** Geneformer
    - **Cross-species:** UCE (7 species supported)
    - **Multi-omics (RNA+ATAC+protein):** scMulan
    - **Spatial transcriptomics:** Nicheformer
    - **ATAC-seq only:** ATACformer
    - **Plant data:** scPlantLLM
    - **Large-scale (1M+ cells):** CellPLM

---

## Data Types and Enums

```python
from omicverse.fm import TaskType, Modality, GeneIDScheme, SkillReadyStatus
```

=== "TaskType"

    ```python
    TaskType.EMBED          # "embed"
    TaskType.ANNOTATE       # "annotate"
    TaskType.INTEGRATE      # "integrate"
    TaskType.PERTURB        # "perturb"
    TaskType.SPATIAL        # "spatial"
    TaskType.DRUG_RESPONSE  # "drug_response"
    ```

=== "Modality"

    ```python
    Modality.RNA         # "RNA"
    Modality.ATAC        # "ATAC"
    Modality.SPATIAL     # "Spatial"
    Modality.PROTEIN     # "Protein"
    Modality.MULTIOMICS  # "Multi-omics"
    ```

=== "GeneIDScheme"

    ```python
    GeneIDScheme.SYMBOL   # "symbol"  — HGNC symbol (e.g. TP53)
    GeneIDScheme.ENSEMBL  # "ensembl" — Ensembl ID (e.g. ENSG00000141510)
    GeneIDScheme.CUSTOM   # "custom"  — model-specific vocabulary
    ```

=== "SkillReadyStatus"

    ```python
    SkillReadyStatus.READY      # Full adapter implemented
    SkillReadyStatus.PARTIAL    # Partial spec, needs validation
    SkillReadyStatus.REFERENCE  # Documentation only
    ```

---

## Plugin System

You can register custom foundation models by writing a plugin.

### Entry-point plugins (pip install)

In your `pyproject.toml`:

```toml
[project.entry-points."omicverse.fm"]
my_model = "my_package.fm_plugin:register"
```

### Local plugins (for development)

Create a file at `~/.omicverse/plugins/fm/my_model.py`:

```python
from omicverse.fm import ModelSpec, SkillReadyStatus, TaskType, Modality, GeneIDScheme
from omicverse.fm.adapters import BaseAdapter

MY_SPEC = ModelSpec(
    name="my_model",
    version="v1.0",
    skill_ready=SkillReadyStatus.PARTIAL,
    tasks=[TaskType.EMBED],
    modalities=[Modality.RNA],
    species=["human"],
    gene_id_scheme=GeneIDScheme.SYMBOL,
    zero_shot_embedding=True,
    embedding_dim=256,
)

class MyAdapter(BaseAdapter):
    def run(self, task, adata_path, output_path, **kwargs):
        ...  # your implementation

    def _load_model(self, device):
        ...

    def _preprocess(self, adata, task):
        ...

    def _postprocess(self, adata, embeddings, task):
        ...

def register():
    """Return a (spec, adapter_class) tuple."""
    return (MY_SPEC, MyAdapter)
```

!!! note

    Plugins cannot override built-in models. If a name collision occurs, the plugin is skipped and a warning is emitted.

---

## Registry API

For advanced usage, you can query the model registry directly:

```python
from omicverse.fm import get_registry

registry = get_registry()

# Get the spec for a specific model
spec = registry.get("scgpt")
print(spec.embedding_dim)       # 512
print(spec.supports_task("embed"))  # True

# Find models matching criteria
matches = registry.find_models(
    task="embed",
    species="human",
    gene_scheme="symbol",
    zero_shot=True,
    max_vram_gb=16,
)
for m in matches:
    print(m.name, m.version)
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OV_FM_CHECKPOINT_DIR` | Base directory for model checkpoints (`<base>/<model_name>/`) |
| `OV_FM_CHECKPOINT_DIR_<MODEL>` | Per-model checkpoint directory (for any uppercase model name) |
| `OV_FM_DISABLE_CONDA_SUBPROCESS` | Disable conda subprocess execution, use the in-process adapter only |

**Checkpoint resolution order:**

1. The `checkpoint_dir` argument to `ov.fm.run()`
2. The `OV_FM_CHECKPOINT_DIR_<MODEL>` environment variable
3. `OV_FM_CHECKPOINT_DIR/<model_name>/`
4. Default cache: `~/.omicverse/models/<model_name>/`

---

## Error Handling

All functions return errors through the result dict rather than raising exceptions:

```python
result = ov.fm.run(task="embed", model_name="scgpt", adata_path="data.h5ad")
if "error" in result:
    print(f"Error: {result['error']}")
    print(f"Status: {result['status']}")  # "not_implemented", "incompatible", etc.
```

Common error messages:

| Error | Cause |
|-------|-------|
| `Model 'xxx' not found` | Model name not in the registry |
| `File not found: xxx` | Invalid file path |
| `Expected .h5ad file` | Wrong file format |
| `No compatible models found` | No model satisfies the task/data constraints |
| `No adapter implemented for model 'xxx'` | Model is documentation-only, no adapter |

---

## Hands-On Tutorial

For a step-by-step walkthrough with real data (PBMC 3K + scGPT), see the
[foundation model tutorial notebook](t_fm.ipynb).
