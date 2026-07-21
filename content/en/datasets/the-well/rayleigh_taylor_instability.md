---
title: "Rayleigh–Taylor Instability"
parent_collection: "The Well"
physical_family: "Variable-density miscible flow"
spatial_dimension: 3D
coordinate_system: "Cartesian $(x,y,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/rayleigh_taylor_instability/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/rayleigh_taylor_instability"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/rayleigh_taylor_instability"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: rayleigh_taylor_instability
weight: 160
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "A heavier miscible fluid lies above a lighter one in a gravitational field. Perturbations grow into bubbles and spikes, eventually creating a turbulent mixing layer. The Atwood…"
description: "A heavier miscible fluid lies above a lighter one in a gravitational field. Perturbations grow into bubbles and spikes, eventually creating a turbulent mixing layer. The Atwood…"

---

# Rayleigh–Taylor Instability

![Density evolution](/the-well/rayleigh_taylor_instability__density_normalized.gif)


> **Parent collection:** The Well
> **Directory:** `rayleigh_taylor_instability`
> **Equation family:** Variable-density miscible flow

## 1. Scope and physical overview

A heavier miscible fluid lies above a lighter one in a gravitational field. Perturbations grow into bubbles and spikes, eventually creating a turbulent mixing layer. The Atwood number controls density contrast and symmetry, while the initial Fourier spectrum controls morphology.

The Well treats each downloadable directory as a self-documenting HDF5 dataset.

## 2. Governing equations

$$
\frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf u)=0,
$$
$$
\frac{\partial(\rho\mathbf u)}{\partial t}
+\nabla\cdot(\rho\mathbf u\mathbf u)
=-\nabla p+\nabla\cdot\tau+\rho\mathbf g,
$$
$$
\nabla\cdot\mathbf u
=-\kappa\nabla\cdot\left(\frac{\nabla\rho}{\rho}\right),
$$
$$
\tau=\rho\nu\left[
\nabla\mathbf u+(\nabla\mathbf u)^\top
-\frac23(\nabla\cdot\mathbf u)I
\right].
$$
The density contrast is summarized by
$$
\mathrm{At}=\frac{\rho_h-\rho_l}{\rho_h+\rho_l}.
$$

### Variables and physical fields

- \(\rho,\mathbf u,p\): density, velocity and pressure.
- \(\mathbf g\): gravity.
- \(\kappa\): common molecular diffusivity.
- \(\nu\): kinematic viscosity, rescaled in the code to keep the Kolmogorov scale near mesh resolution.
- \(\mathrm{At}\): Atwood number.
- Initial perturbations are described in Fourier space by mean \(\mu\), width \(\sigma\) and phase range \(\phi_{\max}\).

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Atwood number, gravity, molecular diffusivity, viscosity/resolution rule, density-interface thickness, initial spectral amplitudes/phases, domain aspect ratio, boundary conditions and output time step. |
| Actually varied in this release | Atwood number \(\mathrm{At}\in\{3/4,1/2,1/4,1/8,1/16\}\). Initial interface spectra include Gaussian-like amplitude envelopes with \(\mu\in\{1,4,16\}\), \(\sigma\in\{1/4,1/2,1\}\), random phases, plus a second family with \(\mu=16,\sigma=0.25\) and \(\phi_{\max}\in\{\pi/128,\pi/8,\pi/2,\pi\}\). The released set contains 45 trajectories. |
| Fixed in this release | Grid \(128^3\), gravitational configuration, miscible-fluid equation family, pressure-solver/discretization, resolution-dependent viscosity prescription and dataset-specific sampling for each Atwood group. |

## 4. Initial and boundary conditions

### Initial conditions

A perturbed density interface between heavy and light fluids, with perturbations specified in Fourier space by the documented spectral families.

### Boundary conditions

The exact three-dimensional boundary configuration is encoded in the released HDF5 metadata and TURMIX3D setup; use those files rather than assuming full periodicity.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `rayleigh_taylor_instability` |
| Spatial dimension | 3D |
| Coordinate system | Cartesian $(x,y,z)$ |
| Spatial resolution | $128^3$ |
| Stored steps per trajectory | 119 on current dataset page (paper table: 120) |
| Number of trajectories | 45 |
| Dynamic channels after component expansion | 4 |
| Dynamic fields | density $\rho$ and velocity (3) |
| Static fields / scalar context | Atwood number and initialization-spectrum metadata |
| Time range | Atwood-dependent nondimensional time |
| Stored time spacing | varies with Atwood-number group |
| Spatial domain | uniform cubic cells |
| Estimated release size | 255.6 GB |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,L_3,4)\);
- standard 4-frame history: \((B,4,L_1,L_2,L_3,4)\);
- standard 1-frame target: \((B,1,L_1,L_2,L_3,4)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** TURMIX3D; staggered MAC mesh, Lagrange+remap, TVD, SSPRK2, multigrid pressure solve

TURMIX3D uses a staggered marker-and-cell mesh and a Lagrange-plus-remap scheme. The spatial discretization is second-order TVD with Van Leer limiting; time integration is second-order SSP Runge–Kutta. A modified variable-density pressure equation is solved with red–black relaxation and V-cycle multigrid.

## 7. Recommended ML tasks and diagnostics

Mass-conserving turbulent mixing, Atwood-conditioned generalization, time-step generalization, bubble/spike morphology, mixing-width growth-rate prediction and inertial-range spectral fidelity.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

The appendix describes 13 initialization designs for five Atwood numbers, which would suggest 65 combinations, while the released table/directory contains 45 trajectories. The current page reports 119 snapshots and the paper table reports 120. Time spacing changes across Atwood groups, so models should consume the time coordinates explicitly.

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
the-well-download --base-path ./the_well_data --dataset rayleigh_taylor_instability --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset rayleigh_taylor_instability --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="rayleigh_taylor_instability",
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
    well_dataset_name="rayleigh_taylor_instability",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.

## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/rayleigh_taylor_instability/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/rayleigh_taylor_instability> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/rayleigh_taylor_instability> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |
