---
title: "Planetary Shallow-Water Equations"
parent_collection: "The Well"
physical_family: "Rotating spherical shallow-water equations"
spatial_dimension: "2D on sphere"
coordinate_system: "spherical angular grid $(\\\\theta,\\\\phi)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/planetswe/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/planetswe"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/planetswe"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: planetswe
weight: 120
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "A rotating, forced, hyperviscous shallow-water model on the sphere approximates a single atmospheric pressure level. Initial conditions are derived from ERA5 500 hPa fields, whi…"
description: "A rotating, forced, hyperviscous shallow-water model on the sphere approximates a single atmospheric pressure level. Initial conditions are derived from ERA5 500 hPa fields, whi…"

---

# Planetary Shallow-Water Equations

> **Parent collection:** The Well  
> **Directory:** `planetswe`  
> **Equation family:** Rotating spherical shallow-water equations  
> **Documentation type:** source-faithful structured rewrite of the official dataset page, paper appendix and current repository metadata.

## 1. Scope and physical overview

A rotating, forced, hyperviscous shallow-water model on the sphere approximates a single atmospheric pressure level. Initial conditions are derived from ERA5 500 hPa fields, while realistic Earth topography and synthetic daily/annual forcing introduce geographical and seasonal structure.

The Well treats each downloadable directory as a self-documenting HDF5 dataset. This page separates three notions that are often conflated: parameters that are theoretically adjustable in the equations/generator, parameters actually varied in the released ensemble, and parameters fixed in this release.

## 2. Governing equations

$$
\frac{\partial\mathbf u}{\partial t}
=-\mathbf u\cdot\nabla\mathbf u-g\nabla h
-\nu\nabla^4\mathbf u-2\boldsymbol\Omega\times\mathbf u,
$$
$$
\frac{\partial h}{\partial t}
=-H\nabla\cdot\mathbf u-\nabla\cdot(h\mathbf u)
-\nu\nabla^4 h+F(\theta,\phi,t).
$$

### Variables and physical fields

- \(\mathbf u\): depth-averaged horizontal velocity on the sphere.
- \(h\): pressure-surface/free-surface height perturbation.
- \(H\): reference layer depth.
- \(g\): gravitational acceleration.
- \(\boldsymbol\Omega\): planetary rotation vector.
- \(\nu=1.76\times10^{-10}\): fixed hyperviscosity in the documented setup.
- \(F\): forcing with model-day and model-year periodicity.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Planet radius/rotation, gravity, reference depth, topography, hyperviscosity, forcing amplitude/seasonality, initial atmospheric state, spectral resolution and output cadence. |
| Actually varied in this release | Only the initial atmospheric state varies across physical runs. Forty ERA5-derived, balanced initial conditions are simulated for three model years each. For ML storage, each run is segmented into three one-year trajectories, yielding 120 trajectories of 1008 hourly snapshots. |
| Fixed in this release | Earth topography, planetary geometry/rotation and gravity, \(\nu=1.76\times10^{-10}\), daily/annual forcing definition, numerical resolution, hourly output cadence and the burn-in procedure. |

## 4. Initial and boundary conditions

### Initial conditions

ERA5 500 hPa \(u,v,z\) fields are mapped into the shallow-water state, repeatedly integrated/projected toward balance, and burned in for half a model year before recording.

### Boundary conditions

Global sphere; no physical lateral boundary. Spherical representation is periodic in longitude and regular at the poles through the spectral basis.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `planetswe` |
| Spatial dimension | 2D on sphere |
| Coordinate system | spherical angular grid $(\theta,\phi)$ |
| Spatial resolution | $256\times512$ |
| Stored steps per trajectory | 1008 |
| Number of trajectories | 120 ML trajectories (from 40 three-year simulations) |
| Dynamic channels after component expansion | 3 |
| Dynamic fields | surface height $h$ and horizontal velocity (2) |
| Static fields / scalar context | Earth topography/bathymetry and forcing definition |
| Time range | one model year per stored ML trajectory |
| Stored time spacing | one model hour |
| Spatial domain | global sphere |
| Estimated release size | 185.8 GB |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,3)\);
- standard 4-frame history: \((B,4,L_1,L_2,3)\);
- standard 1-frame target: \((B,1,L_1,L_2,3)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** Dedalus spin-weighted spherical harmonics; 3/2 anti-aliasing; second-order IMEX RK

Dedalus uses spin-weighted spherical harmonics with 3/2 over-sampling for anti-aliasing. ERA5-derived states are repeatedly adjusted toward balance and then burned in for half a model year. Three subsequent model years are recorded hourly. The released ML representation splits each three-year physical run into three one-year trajectories.

## 7. Recommended ML tasks and diagnostics

Stable multi-year forecasting, spherical operator learning, conservation and climatological-statistics evaluation, transfer across ERA5 initial states, and forcing/topography-conditioned prediction.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

Do not confuse 40 solver runs with 120 released ML trajectories. The time units are model-defined rather than calibrated physical days/years. The topography is a time-invariant model input, not a dynamic prediction target.

Current repository status: **active**. This document was checked against the repository state/release information available on 2026-07-21. Always inspect `dataset_name.yaml`, `stats.yaml`, HDF5 coordinates and release notes for the exact files used in an experiment.

## Download and loading

### Install the interface

```bash
python -m venv .venv
source .venv/bin/activate
pip install the_well
```

### Download one split

```bash
the-well-download --base-path ./the_well_data --dataset planetswe --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset planetswe --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="planetswe",
    well_split_name="train",
)
loader = DataLoader(trainset, batch_size=1, shuffle=True)

sample = trainset[0]
print(sample.keys())
```

### Hugging Face streaming

This directory is listed for Hub access in the current collection:

```python
from the_well.data import WellDataset

trainset = WellDataset(
    well_base_path="hf://datasets/polymathic-ai/",
    well_dataset_name="planetswe",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.


## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/planetswe/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/planetswe> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/planetswe> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. Citation and provenance

Recommended citation: McCabe et al., *Towards stability of autoregressive neural operators*; also cite ERA5 when appropriate.

Also cite the collection paper:

> Ohana et al., **The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**, NeurIPS 2024 Datasets and Benchmarks.

This English page is a structured, source-faithful synthesis, not a byte-for-byte mirror of the website. Equations and numerical values are reconciled from the official dataset documentation, the paper appendix and current repository metadata. The paired Chinese document is an annotated translation and reorganization.
