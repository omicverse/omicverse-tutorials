# Electrophysiology & Behaviour

Tutorials for the neuroscience helpers in `omicverse.tl` — channel-level
quality control and event-related potentials for multichannel
electrophysiology (EEG), trial-by-trial computational models of choice
behaviour, and quantitative susceptibility mapping (QSM) from multi-echo
gradient-echo MRI. Every notebook simulates its data with a known ground
truth, so each step can be checked against the answer; the EEG and choice
notebooks need nothing beyond NumPy/SciPy, and the QSM notebook adds
scikit-image (and nibabel for the file round trip, which has a fallback).

```{toctree}
:maxdepth: 1

../Tutorials-neuro/t_eeg_channel_qc_erp
../Tutorials-neuro/t_choice_model
../Tutorials-neuro/t_qsm_reconstruction
```
