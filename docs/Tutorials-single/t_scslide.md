# Sample-level cell-state distributions with scSLIDE

:::{warning}
This tutorial describes the adapter proposed in
[OmicVerse PR #1098](https://github.com/omicverse/omicverse/pull/1098), with this
guide tracked in [tutorial PR #145](https://github.com/omicverse/omicverse-tutorials/pull/145).
The real-backend comparison and fresh-kernel notebook execution have passed with
the exact reviewed wheel, which is now publicly installable. The OmicVerse adapter
still awaits upstream merge; an installed OmicVerse release may not include this API.
:::

scSLIDE represents each **sample** through its distribution of cells near
landmarks in a cell-state/phenotype-aware representation. It is not RNA velocity,
and its sample embedding is not a replacement for a cell-level AnnData embedding.
This adapter calls the separately maintained native-Python backend, rather than
copying or changing its numerical algorithms.

## Installation and availability

Use an OmicVerse development checkout containing `ov.single.scslide`. The
independent backend is available from the public
[scSLIDE-py repository](https://github.com/LCGaoZzz/scSLIDE-py).
In a Python 3.11 environment, install the exact reviewed wheel with its `[anndata]`
extra and verified constraints. No GitHub authentication or PyPI release is required:

```bash
python -m pip install --constraint "https://raw.githubusercontent.com/LCGaoZzz/scSLIDE-py/57605d55054a3c26b0d30721f696ef67eab1809d/constraints/verified-primary-py311.txt" \
  "scslide-py[anndata] @ https://raw.githubusercontent.com/LCGaoZzz/scSLIDE-py/57605d55054a3c26b0d30721f696ef67eab1809d/artifacts/scslide_py-0.3.3-py3-none-any.whl#sha256=02043e3c1215320beca93c9ce58645f4fdebf29796dbbdc30d7ce00a580aacbd"
```

Both public artifact downloads have been checked against their complete SHA256
values; see the [publication receipt](https://github.com/LCGaoZzz/scSLIDE-py/blob/main/docs/PUBLICATION.md).

The audited backend candidate is version 0.3.3, wheel SHA256
`02043e3c1215320beca93c9ce58645f4fdebf29796dbbdc30d7ce00a580aacbd`.
Historical private candidates used the same version string, so it is not enough
to check only `0.3.3` when reproducing that audit.

The initial adapter targets in-memory NumPy/CSR/CSC AnnData. It does not claim
backed, Dask, GPU or full standalone-backend coverage. It copies the input object;
large datasets should use the backend's documented storage APIs directly until
adapter-specific storage tests have been completed.

## Input contract

`obs` contains `sample`, `subject` and `condition` (or explicitly selected names).
A subject can have multiple samples; those samples are not independent replicates.
Each sample has a single response and subject identity. Keep raw counts in a named
layer, existing log-normalized expression in another layer, a boolean HVG mask in
`var`, and a cell-state embedding in `obsm`. The adapter does not silently perform
normalization, HVG selection or embedding construction.

The accompanying notebook generates small synthetic counts and explicitly prepares
all these fields. Its simulated severity is only a demonstration, not a disease
finding or an external validation dataset.

## Public call

```python
result = ov.single.scslide(
    adata,
    sample_key="sample",
    response_key="condition",
    subject_key="subject",
    counts_layer="counts",
    data_layer="data",
    embedding_key="X_pca",
    n_jobs=1,
    random_state=17,
    workflow_kwargs={
        "ncells_per_group": 15,
        "ncells_landmark": 60,
        "ncomp_pls": 3,
        "k_nn": 3,
        "knn_range": 30,
        "ncomp_diffusion": 3,
        "fit_curve": False,
    },
)
sample_adata = result.sample_adata
```

`sample_adata.obs` is **samples**, `sample_adata.var` is **landmarks**. Its `counts`
layer represents cell-to-landmark assignments, not UMI expression.
`sample_adata.obsm['X_scslide_diffmap']` is the sample-level geometry.
`result.prepared.adata` is the backend's cell-level working copy, and
`result.prepared.pls_model` retains the fitted model. The original `adata` is not
modified. A rectangular cell-to-landmark relation is not placed into a cell-level
square `.obsp` slot.

## Reading, plotting and saving

```python
import scanpy as sc
sc.pl.embedding(sample_adata, basis="scslide_diffmap", color="condition", size=100)
sample_adata.write_h5ad("scslide_samples.h5ad")
result.diffusion.embeddings.to_csv("sample_diffusion_source_data.csv")
result.sample_object.counts.to_csv("landmark_by_sample_counts.csv")
```

When a curve is requested, the adapter adds `obs['scslide_trajectory']` to the sample
object. Its direction is geometrically arbitrary until scientifically anchored.
An overall reversal also reverses trajectory coefficients; do not interpret a raw
positive coefficient as disease upregulation without defining orientation.

## Interpretation and limitations

The response participates in supervised representation learning. Separation by that
same response is not independent prediction. Use subject-level study designs and
appropriate held-out evaluation for generalization. Descriptive gene/trajectory
associations do not automatically have confirmatory FDR guarantees after learning a
trajectory. Experimental OOF, count-splitting and permutation modes are intentionally
not exposed by this adapter. Optional descriptive DE can be requested explicitly via
native workflow parameters; choose real available covariates rather than silently
assuming defaults apply to a new cohort.

The wrapper must preserve the backend's counts and numerical outputs on identical
inputs. Its integration test compares direct and wrapped calls. Contract unit tests
use explicit test doubles and are not evidence for R parity or biological correctness.

## Executable notebook

```{toctree}
:maxdepth: 1

t_scslide_example
```

## References

- Original scSLIDE: <https://github.com/satijalab/scSLIDE>
- Author workflow: <https://satijalab.org/seurat/articles/scslide_vignette>
- Independent Python backend: <https://github.com/LCGaoZzz/scSLIDE-py>

The Python adapter is a community contribution, not a claim of endorsement by the
original authors or of a universal speed/FDR advantage.
