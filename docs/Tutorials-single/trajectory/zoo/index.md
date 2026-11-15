# Trajectory inference — backend zoo

This zoo holds one tutorial per `ov.single.TrajInfer(method=...)` backend.
Every tutorial follows the same template — load → `TrajInfer` → pseudotime
plot → downstream — so you can swap methods by changing one line.

## Vendored backends (ship with omicverse)

| Method | Tutorial | Strength |
|---|---|---|
| Palantir | [t_traj_palantir](t_traj_palantir.ipynb) | Branch probabilities; best continuous-differentiation hierarchy. |
| Diffusion-map / DPT | [t_traj_diffusion](t_traj_diffusion.ipynb) | scanpy's diffmap + PAGA. |
| scTour | [t_traj_sctour](t_traj_sctour.ipynb) | Generative; yields a latent velocity vector field. |
| StaVIA | [t_traj_stavia](t_traj_stavia.ipynb) · [toy](t_traj_stavia_toy_multifurcating.ipynb) | Spatial-aware variant. |
| Monocle 2 | [t_traj_monocle2](t_traj_monocle2.ipynb) | DDRTree-based hierarchy. |
| VIA | [t_via](t_via.ipynb) · [t_via_velo](t_via_velo.ipynb) | Markov-chain pseudotime; velocity-aware. |
| CytoTrace 2 | [t_cytotrace2](t_cytotrace2.ipynb) | Differentiation potential. |

## dynbenchmark zoo (install via `pip install omicverse[trajectory]`)

| Method | Tutorial | Topology | Backend |
|---|---|---|---|
| SCORPIUS | [t_traj_scorpius](t_traj_scorpius.ipynb) | linear | pyscorpius |
| TSCAN | [t_traj_tscan](t_traj_tscan.ipynb) | tree | pytscan |
| destiny | [t_traj_destiny](t_traj_destiny.ipynb) | linear, branching | pydestiny-bio |
| URD | [t_traj_urd](t_traj_urd.ipynb) | branching | pyurd-bio |
| Monocle 3 | [t_traj_monocle3](t_traj_monocle3.ipynb) | tree | pymonocle3-bio |
| CytoTRACE | [t_traj_cytotrace_bio](t_traj_cytotrace_bio.ipynb) | gradient | pycytotrace-bio |

The Python ports preserve byte-equivalent geodesic distances against the
R upstream (`dynverse/dyneval`), with metric drift `|Δ| < 0.07` across the
13-method × 14-dataset benchmark.

For Slingshot (the recommended outer-level backend), see
[../t_traj_slingshot](../t_traj_slingshot.ipynb).

## Deep generative trajectory model (`ov.vi`)

Unlike the `TrajInfer` backends above, Decipher is a generative model
(`ov.vi.Decipher` / `ov.single.decipher`) that *jointly learns* a 2-D
interpretable latent space and the trajectory through it, rather than
ordering cells in a pre-existing embedding.

| Method | Tutorial | Strength |
|---|---|---|
| Decipher | [t_traj_decipher](t_traj_decipher.ipynb) | Learns its own 2-D "decipher space" (no separate UMAP step); `ov.vi.Trajectory` + `compute_decipher_time` + imputed gene patterns along it. No scvi-tools / Pyro needed. |

```{toctree}
:maxdepth: 1
:hidden:

t_traj_palantir
t_traj_diffusion
t_traj_sctour
t_traj_stavia
t_traj_stavia_toy_multifurcating
t_traj_monocle2
t_via
t_via_velo
t_cytotrace2
t_traj_scorpius
t_traj_tscan
t_traj_destiny
t_traj_urd
t_traj_monocle3
t_traj_cytotrace_bio
t_traj_decipher
```
