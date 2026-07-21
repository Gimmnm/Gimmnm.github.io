---
title: "Turbulent Radiative Mixing Layer — 2D"
parent_collection: "The Well"
physical_family: "Compressible hydrodynamics + radiative cooling"
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,y)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/turbulent_radiative_layer_2D/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/turbulent_radiative_layer_2D"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/turbulent_radiative_layer_2D"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: turbulent_radiative_layer_2D
weight: 210
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "A cold dense phase and a hot diffuse phase shear past each other. Turbulent mixing creates intermediate-temperature gas that can radiatively cool and join the cold phase. The 2D…"
description: "A cold dense phase and a hot diffuse phase shear past each other. Turbulent mixing creates intermediate-temperature gas that can radiatively cool and join the cold phase. The 2D…"

---

# Turbulent Radiative Mixing Layer — 2D

> **Parent collection:** The Well  
> **Directory:** `turbulent_radiative_layer_2D`  
> **Equation family:** Compressible hydrodynamics + radiative cooling  
> **Documentation type:** source-faithful structured rewrite of the official dataset page, paper appendix and current repository metadata.

## 1. Scope and physical overview

A cold dense phase and a hot diffuse phase shear past each other. Turbulent mixing creates intermediate-temperature gas that can radiatively cool and join the cold phase. The 2D and 3D releases share the same physical parameter sweep and support transfer across dimensionality.

The Well treats each downloadable directory as a self-documenting HDF5 dataset. This page separates three notions that are often conflated: parameters that are theoretically adjustable in the equations/generator, parameters actually varied in the released ensemble, and parameters fixed in this release.

## 2. Governing equations

$$
\frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf v)=0,
$$
$$
\frac{\partial(\rho\mathbf v)}{\partial t}
+\nabla\cdot(\rho\mathbf v\mathbf v+P I)=0,
$$
$$
\frac{\partial E}{\partial t}
+\nabla\cdot[(E+P)\mathbf v]
=-\frac{E}{t_{\rm cool}},
$$
$$
E=\frac{P}{\gamma-1},\qquad \gamma=\frac53.
$$
The associated scaling is
$$
\dot E_{\rm cool}\propto\dot M
\propto v_{\rm rel}^{3/4}t_{\rm cool}^{-1/4}.
$$

### Variables and physical fields

- \(\rho,\mathbf v,P,E\): density, velocity, pressure and thermal energy density.
- \(t_{\rm cool}\): cooling time.
- \(v_{\rm rel}\): relative speed of the phases.
- \(\dot M\): net mass-transfer rate from hot to cold phase.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Cooling time/function, density and temperature contrasts, relative velocity, perturbation spectrum/seed, dimensionality, domain aspect ratio, boundary conditions, equation of state and resolution. |
| Actually varied in this release | Cooling time \(t_{\rm cool}\in\{0.03,0.06,0.10,0.18,0.32,0.56,1.00,1.78,3.16\}\), with 10 random realizations per value, giving 90 trajectories. |
| Fixed in this release | Equation of state \(\gamma=5/3\), hot/cold phase setup and relative-flow convention, two-dimensional geometry, released resolution, 101 snapshots and the Athena++ solver configuration. |

## 4. Initial and boundary conditions

### Initial conditions

A perturbed interface between cold dense and hot diffuse phases with a prescribed relative velocity; ten random seeds are used for each cooling time.

### Boundary conditions

Mixing-layer boundary conditions as defined by the Athena++ setup; verify exact periodic/outflow directions in HDF5 metadata.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `turbulent_radiative_layer_2D` |
| Spatial dimension | 2D |
| Coordinate system | Cartesian $(x,y)$ |
| Spatial resolution | $128\times384$ |
| Stored steps per trajectory | 101 |
| Number of trajectories | 90 |
| Dynamic channels after component expansion | 4 |
| Dynamic fields | density, pressure, velocity (2) |
| Static fields / scalar context | cooling-time label $t_{\rm cool}$ |
| Time range | nondimensional mixing-layer time |
| Stored time spacing | uniform in released trajectories |
| Spatial domain | 2D mixing-layer box |
| Estimated release size | 6.9 GB |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,4)\);
- standard 4-frame history: \((B,4,L_1,L_2,4)\);
- standard 1-frame target: \((B,1,L_1,L_2,4)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** Athena++; compressible finite-volume hydrodynamics with radiative energy sink

Athena++ solves compressible finite-volume hydrodynamics with a radiative energy sink. The 2D campaign required roughly 100 CPU-core-hours in total; the 3D campaign roughly 34,560 CPU-core-hours. Both contain nine cooling times and repeated random realizations.

## 7. Recommended ML tasks and diagnostics

Cross-dimensional transfer, cooling-conditioned forecasting, multiphase-interface tracking, mass-growth/cooling-rate statistics, long-rollout stability and 2D-pretraining-to-3D-finetuning.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

This is the inexpensive 2D member of a dimension-transfer pair. It shares the cooling-time grid with the 3D release but is not a literal planar slice of each 3D trajectory.

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
the-well-download --base-path ./the_well_data --dataset turbulent_radiative_layer_2D --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset turbulent_radiative_layer_2D --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="turbulent_radiative_layer_2D",
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
    well_dataset_name="turbulent_radiative_layer_2D",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.


## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/turbulent_radiative_layer_2D/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/turbulent_radiative_layer_2D> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/turbulent_radiative_layer_2D> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. Citation and provenance

Recommended citation: Fielding et al., *Multiphase Gas and the Fractal Nature of Radiative Turbulent Mixing Layers* (2020).

Also cite the collection paper:

> Ohana et al., **The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**, NeurIPS 2024 Datasets and Benchmarks.

This English page is a structured, source-faithful synthesis, not a byte-for-byte mirror of the website. Equations and numerical values are reconciled from the official dataset documentation, the paper appendix and current repository metadata. The paired Chinese document is an annotated translation and reorganization.
