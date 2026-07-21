---
title: "Rayleigh–Bénard Convection — Native Grid"
parent_collection: "The Well"
physical_family: "Boussinesq convection"
spatial_dimension: 2D
coordinate_system: "Cartesian; Fourier in $x$, Chebyshev in wall-normal $z$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/rayleigh_benard/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/rayleigh_benard"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/rayleigh_benard"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: rayleigh_benard
weight: 140
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "A horizontally periodic fluid layer is heated from below and cooled from above. Buoyancy drives convection against viscosity and thermal diffusion, producing Bénard cells whose…"
description: "A horizontally periodic fluid layer is heated from below and cooled from above. Buoyancy drives convection against viscosity and thermal diffusion, producing Bénard cells whose…"

---

# Rayleigh–Bénard Convection — Native Grid

![Buoyancy field](/the-well/rayleigh_benard__buoyancy_good_normalized.gif)


> **Parent collection:** The Well
> **Directory:** `rayleigh_benard`
> **Equation family:** Boussinesq convection

## 1. Scope and physical overview

A horizontally periodic fluid layer is heated from below and cooled from above. Buoyancy drives convection against viscosity and thermal diffusion, producing Bénard cells whose location and turbulent evolution are sensitive to small initial perturbations.

The Well treats each downloadable directory as a self-documenting HDF5 dataset.

## 2. Governing equations

$$
\frac{\partial b}{\partial t}-\kappa\Delta b
=-\mathbf u\cdot\nabla b,
$$
$$
\frac{\partial\mathbf u}{\partial t}
-\nu\Delta\mathbf u+\nabla p-b\mathbf e_z
=-\mathbf u\cdot\nabla\mathbf u,
\qquad \nabla\cdot\mathbf u=0,
$$
with
$$
\kappa=(\mathrm{Ra}\,\mathrm{Pr})^{-1/2},\qquad
\nu=\left(\frac{\mathrm{Ra}}{\mathrm{Pr}}\right)^{-1/2}.
$$

### Variables and physical fields

- \(b\): buoyancy/temperature-related scalar.
- \(\mathbf u=(u_x,u_z)\): incompressible velocity.
- \(p\): pressure with a zero-mean gauge.
- \(\mathrm{Ra}\): Rayleigh number.
- \(\mathrm{Pr}\): Prandtl number.
- \(\kappa,\nu\): thermal diffusivity and kinematic viscosity.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Rayleigh/Prandtl numbers, plate temperatures, aspect ratio, no-slip versus free-slip walls, perturbation spectrum/amplitude, viscosity/diffusivity, spatial basis/resolution and output interval. |
| Actually varied in this release | Rayleigh number \(\mathrm{Ra}\in\{10^6,10^7,10^8,10^9,10^{10}\}\), Prandtl number \(\mathrm{Pr}\in\{0.1,0.2,0.5,1,2,5,10\}\), and initial buoyancy-perturbation amplitude \(\delta b_0\in\{0.2,0.4,0.6,0.8,1.0\}\), with repeated random perturbations. The product \(5\times7\times50=1750\) indicates 50 initial realizations per \((\mathrm{Ra},\mathrm{Pr})\) pair. |
| Fixed in this release | Aspect ratio/domain, plate buoyancy values, no-slip wall velocity, horizontal periodicity, 200 stored frames over \([0,50]\), and the Dedalus simulation campaign. The uniform directory changes representation, not physics. |

## 4. Initial and boundary conditions

### Initial conditions

A conductive buoyancy profile plus randomized perturbations whose amplitude is controlled by \(\delta b_0\); velocity begins from the generator's quiescent/perturbed setup.

### Boundary conditions

Periodic in \(x\). At \(z=0,1\), velocity is no-slip and buoyancy is fixed (hot below, cold above).

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `rayleigh_benard` |
| Spatial dimension | 2D |
| Coordinate system | Cartesian; Fourier in $x$, Chebyshev in wall-normal $z$ |
| Spatial resolution | $512\times128$ |
| Stored steps per trajectory | 200 |
| Number of trajectories | 1750 |
| Dynamic channels after component expansion | 4 |
| Dynamic fields | buoyancy $b$, pressure $p$, velocity $(u_x,u_z)$ |
| Static fields / scalar context | Rayleigh, Prandtl and initial-perturbation labels |
| Time range | $[0,50]$ |
| Stored time spacing | $0.25$ |
| Spatial domain | $x\in[0,4], z\in[0,1]$ |
| Estimated release size | approximately 342–358 GB across documentation versions |
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

**Documented solver:** Dedalus mixed Fourier–Chebyshev pseudo-spectral method with adaptive time stepping

Dedalus solves the equations with a Fourier basis horizontally and a Chebyshev basis vertically, using adaptive time steps. Horizontal boundaries are periodic; the upper and lower plates impose no-slip velocity and fixed buoyancy. The uniform release is a post-processed resampling of the same trajectories, not a new physical simulation campaign.

## 7. Recommended ML tasks and diagnostics

Sensitivity to initial conditions, convection-cell localization, turbulent forecasting, parameter transfer over \((\mathrm{Ra},\mathrm{Pr})\), native/nonuniform-grid learning and comparison with uniformly resampled data.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

This directory stores the native Dedalus wall-normal coordinate, which is Chebyshev/nonuniform. Release updates corrected coordinate metadata; models assuming uniform spacing should use coordinate-aware operators or the uniform resampling.

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
the-well-download --base-path ./the_well_data --dataset rayleigh_benard --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset rayleigh_benard --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="rayleigh_benard",
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
    well_dataset_name="rayleigh_benard",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.

## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/rayleigh_benard/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/rayleigh_benard> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/rayleigh_benard> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |
