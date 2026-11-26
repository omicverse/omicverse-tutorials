---
orphan: true
---

# HE-zoo — predicting spatial transcriptomics from H&E

`ov.space.histo` predicts spatial gene-expression from a hematoxylin-and-eosin (H&E) histology slide. It wraps the strongest 2024–2026 methods behind one dispatcher so you can swap backends without re-staging your data:

```python
import omicverse as ov

wsi = ov.space.histo.open_wsi('slide.tif')
ov.space.histo.tile(wsi, tile_px=224, mpp=0.5)
ov.space.histo.embed(wsi, model='gigapath')

ov.space.histo.predict_expression(wsi, method='stpath',
                                  organ='Breast', tech='Visium')
```

The container is a `wsidata.WSIData` (a `spatialdata.SpatialData` subclass with WSI accessors). Predictions land in `wsi.tables['{method}_tiles']` as an AnnData with tile-pixel centroids in `obsm['spatial']`. This means downstream tools — `ov.space.svg`, `ov.pl.spatial`, `zs.pl.tiles`, `scanpy.pl.spatial` — accept HE→ST predictions and real Visium tables interchangeably.

## When to use which backend

| Method | Needs paired Visium? | Pretrained weights | Output | Best for |
|---|---|---|---|---|
| **`stpath`** | No (zero-shot) | ✅ `tlhuang/STPath` on HuggingFace | spot-level, 38,984 genes | Zero-shot inference on H&E-only slides across 17 organs |
| **`stflow`** | Yes (1 slide) | ❌ trains a per-slide head | spot-level | Same-cohort prediction when STPath's gene vocabulary doesn't cover your panel |
| **`hest_fm`** | Yes (1 slide) | uses public pathology FM + ridge | spot-level | Custom panels, transparent and reproducible baseline |
| **`istar`** | Yes (1 slide) | uses HIPT (mahmoodlab) | sub-spot (~8 µm) | Super-resolving an existing Visium sample to near-single-cell resolution |

All four are exercised on the same H&E (10x Visium Breast Cancer Block A Section 1, ~1.7 GB) so the tutorials are directly comparable.

## Foundation-model access

The strongest backbones — `gigapath`, `uni2`, `conch_v1.5`, `virchow2`, `h-optimus-1` — are **gated** on HuggingFace. Request access on each model card, then login with `huggingface-cli login` once. The `hest_fm` tutorial also runs on the fully-public `ctranspath` backbone so you can verify the pipeline without any gated weights.

## Tutorials

- [Quick start: HEST-FM with CTransPath](t_histo_hest_fm.ipynb) — fastest path, all-public, ridge head on a single paired Visium slide
- [STPath zero-shot prediction](t_histo_stpath.ipynb) — npj Digital Medicine 2025 generative foundation model
- [STFlow per-slide fine-tune](t_histo_stflow.ipynb) — ICML 2025 flow matching
- [iStar super-resolution](t_histo_istar.ipynb) — Nature Biotechnology 2024 sub-spot imputation

## References

- Huang T. et al. **STPath: a generative foundation model for integrating spatial transcriptomics and whole-slide images.** *npj Digital Medicine* (2025).
- Huang T. et al. **Scalable Generation of Spatial Transcriptomics from Histology Images via Whole-Slide Flow Matching.** *ICML 2025* (Spotlight).
- Jaume G. et al. **HEST-1k: A Dataset For Spatial Transcriptomics and Histology Image Analysis.** *NeurIPS 2024* (Spotlight).
- Zhang D. et al. **Inferring super-resolution tissue architecture by integrating spatial transcriptomics with histology.** *Nature Biotechnology* (2024).
- Yu C. et al. **LazySlide: scalable and modular whole slide image analysis with scverse integration.** *bioRxiv* (2025).
