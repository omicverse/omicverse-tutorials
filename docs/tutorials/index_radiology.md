# Radiology

Tutorials for `omicverse.radiology` — reading a DICOM MR / CT study the way a
reader does, with the geometry and the measurements done by code: patient
coordinates and plane classification, contrast class from TR / TE / TI, survey
sheets whose cells map back to millimetres, a read ledger that votes on the
principal finding, signal profiles along a traced structure, and distances in
millimetres. The notebook builds its own synthetic DICOM study with a known
defect, so every recovered number can be compared with the truth.

```{toctree}
:maxdepth: 1

../Tutorials-radiology/t_radiology_band_defect
```
