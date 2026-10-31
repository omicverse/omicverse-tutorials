# In-silico Perturbation

In-silico gene knockout, knockdown and over-expression through
`ov.single.perturb`. scTenifoldKnk (scRNA), CellOracle (RNA + base GRN) and
dynamo (velocity + vector field) share the `PerturbResult` interface.
Dynamo supplies model responses and transition outputs; GRN outputs are
available through the network-based backends.

```{toctree}
:maxdepth: 1

../Tutorials-single/perturb/index
../Tutorials-single/perturb/t_perturb_sctenifoldknk
../Tutorials-single/perturb/t_perturb_celloracle
../Tutorials-single/perturb/t_perturb_dynamo
../Tutorials-single/perturb/t_perturb_unified
```
