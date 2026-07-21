---
title: "Helmholtz Staircase"
parent_collection: "The Well"
physical_family: "Wave / Helmholtz scattering"
spatial_dimension: 2D
coordinate_system: "Cartesian $(x_1,x_2)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/helmholtz_staircase/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/helmholtz_staircase"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/helmholtz_staircase"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: helmholtz_staircase
weight: 110
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "A point source radiates above an infinite periodic sound-hard staircase. The simulation is solved in the frequency domain and analytically sampled through one oscillation period…"
description: "A point source radiates above an infinite periodic sound-hard staircase. The simulation is solved in the frequency domain and analytically sampled through one oscillation period…"

---

# Helmholtz Staircase

![Pressure field](/the-well/helmholtz_staircase__pressure_normalized.gif)


> **Parent collection:** The Well
> **Directory:** `helmholtz_staircase`
> **Equation family:** Wave / Helmholtz scattering

## 1. Scope and physical overview

A point source radiates above an infinite periodic sound-hard staircase. The simulation is solved in the frequency domain and analytically sampled through one oscillation period. Trapped surface modes coexist with outgoing waves, creating two spatial scales whose temporal evolution must be disentangled.

The Well treats each downloadable directory as a self-documenting HDF5 dataset.

## 2. Governing equations

The time-domain problem is
$$
\frac{\partial^2 U}{\partial t^2}-\Delta U
=\delta(t)\delta(\mathbf x-\mathbf x_0),\qquad
\partial_n U=0\ \text{on }\partial\Omega.
$$
After Fourier transformation in time,
$$
-(\Delta+\omega^2)u=\delta_{\mathbf x_0}\quad\text{in }\Omega,\qquad
\partial_nu=0\quad\text{on }\partial\Omega,
$$
together with outgoing-radiation conditions. Time samples are reconstructed as the real/imaginary components of \(u(\mathbf x)e^{-i\omega t}\).

### Variables and physical fields

- \(U(t,\mathbf x)\): time-domain acoustic field.
- \(u(\mathbf x)\): complex frequency-domain acoustic pressure.
- \(\omega\): point-source angular frequency.
- \(\mathbf x_0\): source position.
- \(\partial_n\): derivative along the boundary normal.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Source frequency and position, staircase period/geometry, sound speed/density, boundary type, output-window extent, spatial discretization, Floquet–Bloch quadrature and phase sampling. |
| Actually varied in this release | Source frequency takes 16 values: \(0.062,0.251,0.439,0.626,0.813,0.998,1.182,1.363,1.541,1.715,1.882,2.042,2.191,2.323,2.433,2.511\). The source position takes 32 configured values, producing \(16\times32=512\) parameter combinations. Each combination is sampled at 50 phases over one period. |
| Fixed in this release | Staircase geometry and period, sound-hard Neumann boundary, constant-density gas and normalized sound speed \(c=1\), low-frequency/trapped-mode regime, output-grid resolution and 50 phase samples. |

## 4. Initial and boundary conditions

### Initial conditions

A single impulsive point source at \(t=0\) and \(\mathbf x=\mathbf x_0\), with quiescent field before excitation. In the released frequency-domain representation, \((\omega,\mathbf x_0)\) fully specifies the source.

### Boundary conditions

Neumann/sound-hard condition \(\partial_nu=0\) on the staircase, periodic surface geometry, and outgoing-radiation conditions in the unbounded region.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `helmholtz_staircase` |
| Spatial dimension | 2D |
| Coordinate system | Cartesian $(x_1,x_2)$ |
| Spatial resolution | $1024\times256$ |
| Stored steps per trajectory | 50 |
| Number of trajectories | 512 |
| Dynamic channels after component expansion | 2 |
| Dynamic fields | real and imaginary parts of acoustic pressure |
| Static fields / scalar context | staircase mask; source/frequency metadata |
| Time range | one period $T=2\pi/\omega$ per trajectory |
| Stored time spacing | $T/50$ |
| Spatial domain | periodic corrugated half-space represented on a finite output window |
| Estimated release size | 52.4 GB |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,2)\);
- standard 4-frame history: \((B,4,L_1,L_2,2)\);
- standard 1-frame target: \((B,1,L_1,L_2,2)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** Floquet–Bloch transform + high-order boundary integral equation method

The generator combines a Floquet–Bloch transform with a high-order boundary integral equation method. The 2D PDE is reduced to integrals over the 1D boundary; specialized quadrature handles staircase corners and radiation conditions. The appendix reports about 7–8 digits of accuracy and roughly 400 s per parameter combination on 64 CPU cores.

## 7. Recommended ML tasks and diagnostics

Frequency/phase-conditioned forecasting, inverse source localization, inverse boundary/geometry inference, trapped-mode identification and learning across source frequencies.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

The appendix prose lists candidate \(x\) and \(y\) coordinate sets whose full Cartesian product would exceed 32 positions; therefore the actual HDF5/source-position metadata is authoritative for the exact 32-point list. The 50 frames are analytically generated phases, not 50 independent PDE time steps.

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
the-well-download --base-path ./the_well_data --dataset helmholtz_staircase --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset helmholtz_staircase --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="helmholtz_staircase",
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
    well_dataset_name="helmholtz_staircase",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.

## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/helmholtz_staircase/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/helmholtz_staircase> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/helmholtz_staircase> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |
