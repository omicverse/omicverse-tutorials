# In-silico gene perturbation

`ov.single.perturb` runs a virtual gene perturbation on an `AnnData`
and returns a `PerturbResult` with backend-specific gene responses,
trajectory information and, where supported, gene regulatory networks.
The dynamo backend returns signed model responses and transition outputs;
it does not reconstruct a GRN or replace `adata.X` with predicted counts.

## When to use

| Use this | Use something else |
|---|---|
| Want to know which TF→target edges change after a KO/OE | Want a cell-fate trajectory shift only → `ov.single.cell_fate_perturbation` (Dynamo) |
| Want a tidy `Δ-expression` + statistical Z / p-value table for downstream genes | Want a foundation-model prediction → Geneformer / scGPT (separate path) |
| Have scRNA-seq alone | Want multi-omics (ATAC + RNA) GRN → SCENIC+ / Pando |

## Three modes, one call

| `mode=` | Effect | Notes |
|---|---|---|
| `'ko'` | Knockout | expression clamped to 0 in the simulated cell state |
| `'kd'` | Knockdown | dynamo sets each target to its mean expression divided by `fold_change` |
| `'oe'` | Over-expression | dynamo sets each target to its mean expression multiplied by `fold_change` |

For dynamo, these are common target levels across cells, not per-cell
scaling. The mean uses the selected `layer`, or `adata.X` by default, on
the expression scale used for PCA. Other backends apply the perturbation
through their own expression or regulatory-network models.

## Backends — pick by what data you have

| Backend | Min data | Strength | Tutorial |
|---|---|---|---|
| **`sctenifoldknk`** ⭐ | scRNA only | Built-in differential-regulation table with `Z`, `FC`, `adjusted p-value` from a PCNet that's identical to what raw scTenifoldKnk produces (parity verified — see end of the tutorial). | [t_perturb_sctenifoldknk](t_perturb_sctenifoldknk.ipynb) |
| **`cell_oracle`** | scRNA + base GRN (motif/ATAC, optional) | Propagates the perturbation through a base GRN for `n_propagation` steps; emits a `trajectory_shift` matrix + a perturbed GRN. Best when you already have an ATAC/motif-derived base GRN or want CellOracle's cell-state-shift heatmap. | [t_perturb_celloracle](t_perturb_celloracle.ipynb) |
| **`dynamo`** | RNA velocity + learned vector field (`VecFld_pca`) | By default, propagates the perturbation through the **analytical Jacobian** of the learned PCA vector field (`δY = J·δX`, Qiu 2022); reuses dynamo's own perturbation transition matrix and per-cell-type response ranking. `backend_kwargs={'auto_pipeline': True}` prepares missing PCA, dynamics, neighbors, embedding and vector field from velocity-compatible data (spliced/unspliced or metabolic-labeling layers). | [t_perturb_dynamo](t_perturb_dynamo.ipynb) |
| **`auto`** | — | Picks `dynamo` if `adata.uns['VecFld_pca']` is present; `cell_oracle` if `adata.uns['base_grn']` is present (or you pass `grn_base=`); otherwise falls back to `sctenifoldknk`. | — |

When both `VecFld_pca` and a base GRN are present, `auto` selects dynamo
and ignores `grn_base`. Set `backend='cell_oracle'` or
`backend='sctenifoldknk'` explicitly to retain those workflows.

Dynamo's `auto_pipeline=True` needs spliced/unspliced or metabolic-labeling
layers to estimate velocities; an expression matrix alone is insufficient.
The Monocle preprocessor preserves input gene identifiers and includes the
targets among PCA features without downloading gene annotations. Match
`target` to `adata.var_names`, including Ensembl IDs when applicable.
For kinetic labeling with separate spliced/unspliced and new/total layers,
automatic dynamics uses dynamo's `est_method='twostep'`; other layouts
keep native defaults.
The estimator is recorded in `result.meta['dynamics_est_method']`.
Existing PCA and vector fields are reused when only neighbors or the
projection embedding are missing. Without automatic preparation, provide
PCA metadata, `VecFld_pca`, `dynamics`, neighbors and `X_<emb_basis>`.

### Dynamo backend options

Pass these through `backend_kwargs`; the input dictionary is copied.

| Parameter | Default | Handling |
|---|---|---|
| `auto_pipeline` | `False` | Wrapper option: prepare missing prerequisites in place. |
| `vf_ko` | `False` | Add native KO velocity outputs for KO; KD/OE warn and skip. Shared results remain Jacobian responses. |
| `group` | `None` | `obs` column for mean signed and mean absolute per-cell response rankings. |
| `emb_basis` | `'umap'` | Forwarded projection basis. |
| `perturb_mode` | `'raw'` | Forwarded mode; `'z_score'` converts levels using the PCA-reconstructed distribution. |
| `perturbation_method` | `'j_delta_x'` | Forwarded as dynamo's `pertubation_method`; either spelling is accepted. |
| `add_delta_Y_key` | `'<method>_perturbation'` | Forwarded response key; used for `delta_X` and ranking. |
| `add_transition_key` | `'perturbation_transition_matrix'` | Forwarded transition key; used for `trajectory_shift`. |
| `add_velocity_key` | `'velocity_<emb_basis>_perturbation'` | Forwarded velocity key; recorded in result metadata. |
| `add_embedding_key` | `'X_<emb_basis>_perturbation'` | Forwarded copied-embedding key; recorded in result metadata. |

Output-key defaults are resolved together before forwarding. All remaining
options are forwarded unchanged to `dynamo.pd.perturbation`; unknown names
raise its `TypeError`. `projection_method='transform'` returns `trajectory_shift=None` and warns that native 1.5.3 can project baseline velocities instead of the response. Targets must be PCA genes. KD/OE set each target to
its mean expression divided/multiplied by `fold_change`; the chosen layer
must match the PCA model's expression scale. Constant reconstructed genes
cannot be converted to z-scores; use `perturb_mode='raw'` for them.

All three backends are **lazy imports** — `omicverse.single` itself doesn't
require any of them to be installed.

```{toctree}
:maxdepth: 1

t_perturb_sctenifoldknk
t_perturb_celloracle
t_perturb_dynamo
t_perturb_unified
```

Native dynamo group tables use `use_for_dynamics` genes. The signed table
is at `adata.uns[result.meta['rank_key']]`; `rank_abs_<response_key>` ranks
`mean(abs(delta))`, including strong negative responses. With `vf_ko=True`,
KO velocities are additional outputs; the shared `delta_X` and
`trajectory_shift` follow the selected perturbation method (Jacobian by default). Native KO also requires the default PCA model and `VecFld_pca`. For callable KO models
and fate integration, use dynamo's native KO interface explicitly.
Use `copy=True` to keep complete results independent, or distinct output
keys to retain multiple runs on one AnnData. Active `vf_ko` reserves native
KO coordinate/velocity names in `obsm` and `pearson_transition_matrix` in
`obsp`; conflicting custom perturbation output keys raise `ValueError` before
any computation.

Explicit `backend_kwargs['expression']` overrides generated target levels, using
native raw-expression or z-score units. Scalar values apply to all targets;
sequences follow caller target order. Prepared custom PCA keys and loading/mean
arrays are supported. The 1.5.3 precomputed `delta_Y` path and target-zeroing
combinations with inconsistent PCA/full-gene indices are rejected explicitly.
See the tutorial for native parameter access and compatibility boundaries.

## Dynamo result interpretation

`result.adata_perturbed` is the input object or its copy with response layers
and projection outputs added. Its `.X` remains baseline expression, possibly
preprocessed by the automatic pipeline. Read `result.delta_X` or
`result.adata_perturbed.layers[result.meta['perturbation_key']]` for model
responses. `grn` and `grn_base` are always `None`, and `delta_grn` is empty,
including when `grn_output=True`.

In `delta_expr`, `delta` is the mean signed response, and `mean_pert` is
`mean_base + delta`, a derived summary rather than fitted counts. Signed
responses are preserved if this sum is negative. `log2_fc` uses a pseudocount
of `1e-6` and is `NaN` if either mean is negative or non-finite. These columns
are response summaries, not experimentally measured fold changes.

See the [dynamo tutorial](t_perturb_dynamo.ipynb) for raw-data preparation,
parameter examples and frequently asked questions.

## Unified downstream analyses (Tier A / B / C)

Regardless of backend, every `PerturbResult` exposes the **same**
downstream API. See [t_perturb_unified](t_perturb_unified.ipynb) for an
end-to-end run on the official Paul15 dataset.

| Tier | Method | What it gives |
|---|---|---|
| **A** | `result.delta_X`, `.trajectory_shift` | unified per-cell + cell×cell |
| **A** | `result.add_significance()` | adds `z_score`/`p_value`/`adj_p_value` to delta_expr |
| **B** | `result.perturbation_score(pseudotime=)` | per-cell promote/block score |
| **B** | `result.cluster_transitions()` | source × target cluster matrix |
| **B** | `ov.pl.perturb_sankey/quiver/volcano(...)` | publication-style plots |
| **C** | `result.pathway_enrichment(...)` | GO / KEGG / Reactome enrichment |
| **C** | `result.phenotype_enrichment(...)` | MGI / HPO / DisGeNET enrichment |
| **C** | `result.run_markov(start_cells=...)` | long-run cell fate sampling |
| **C** | `result.validate_against_perturbseq(...)` | predicted-vs-observed correlation + top-K precision |
| **C** | `result.permutation_test(n_perms=...)` | overall robustness Z |

## API at a glance

```python
import omicverse as ov

result = ov.single.perturb(
    adata,
    target='Sox2',          # gene name or list of names
    mode='ko',              # 'ko' | 'kd' | 'oe'
    backend='auto',         # 'auto' | 'sctenifoldknk' | 'cell_oracle' | 'dynamo'
    fold_change=2.0,        # for OE / KD
    grn_base=None,          # for cell_oracle backend (DataFrame or networkx graph)
    n_propagation=3,        # CellOracle-only
    grn_output=True,
    return_delta=True,
    backend_kwargs={},      # backend extras, e.g. {'group': 'cell_type', 'vf_ko': True} for dynamo
)

# What you get back:
result.adata_perturbed
result.grn
result.grn_base
result.delta_grn
result.delta_expr
result.trajectory_shift    # backend transition matrix (CellOracle transition_prob / dynamo perturbation transition)
result.summary(top_n=10)   # printable + returned top-affected genes
```

Dynamo's `delta_expr` initially contains response summaries. Significance
columns are added separately with `result.add_significance()`; they are not
experimental differential-expression measurements.

## References

- Osorio, D., Zhong, Y. *et al.* **scTenifoldKnk: an efficient virtual
  knockout tool for gene function predictions via single-cell gene
  regulatory network perturbation.** *Patterns* 3, 100434 (2022).
- Kamimoto, K., Stringa, B., Hoffmann, C.M. *et al.* **Dissecting cell
  identity via network inference and in silico gene perturbation.**
  *Nature* 614, 742–751 (2023). — CellOracle.
- Qiu, X., Li, B. *et al.* **Mapping transcriptomic vector fields of
  single cells.** *Cell* 185, 690–711 (2022). — dynamo, whose analytical
  Jacobian powers the `dynamo` backend.
