---
title: "Turbulence, Gravity and Cooling"
parent_collection: "The Well"
physical_family: "Self-gravitating compressible hydrodynamics"
spatial_dimension: 3D
coordinate_system: "Cartesian $(x,y,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/turbulence_gravity_cooling/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/turbulence_gravity_cooling"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/turbulence_gravity_cooling"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: turbulence_gravity_cooling
weight: 200
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "Self-gravitating turbulent gas clouds evolve under compressible hydrodynamics, radiative heating/cooling and gravity. Temperature, density, metallicity and turbulence realizatio…"
description: "Self-gravitating turbulent gas clouds evolve under compressible hydrodynamics, radiative heating/cooling and gravity. Temperature, density, metallicity and turbulence realizatio…"

---

# Turbulence, Gravity and Cooling

![Temperature evolution](/the-well/turbulence_gravity_cooling__temperature_normalized.gif)


> **Parent collection:** The Well
> **Directory:** `turbulence_gravity_cooling`
> **Equation family:** Self-gravitating compressible hydrodynamics

## 1. Scope and physical overview

Self-gravitating turbulent gas clouds evolve under compressible hydrodynamics, radiative heating/cooling and gravity. Temperature, density, metallicity and turbulence realization span Milky-Way-like, dwarf-galaxy-like and primordial/adiabatic regimes.

The Well treats each downloadable directory as a self-documenting HDF5 dataset.

## 2. Governing equations

The thermodynamic and Lagrangian hydrodynamic equations are the same family as the supernova release:
$$
P=(\gamma-1)\rho u,\qquad \gamma=\frac53,
$$
$$
\frac{d\rho}{dt}=-\rho\nabla\cdot\mathbf v,
$$
$$
\frac{d^2\mathbf r}{dt^2}
=-\frac{\nabla P}{\rho}+\mathbf a_{\rm visc}-\nabla\Phi,
$$
$$
\frac{du}{dt}
=-\frac{P}{\rho}\nabla\cdot\mathbf v+\frac{\Gamma-\Lambda}{\rho}.
$$

### Variables and physical fields

- \(\rho,P,T,u,\mathbf v\): density, pressure, temperature, specific internal energy and velocity.
- \(\Phi\): self-gravitational potential.
- \(\Gamma,\Lambda\): metallicity-dependent heating/cooling.
- The released fields are density, pressure, temperature and velocity; gravity and cooling parameters are metadata rather than dynamic output channels.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Initial temperature/density/metallicity, cloud mass/radius, turbulence seed/spectrum/amplitude, cooling/heating table, self-gravity, mass resolution, equation of state and stopping/output times. |
| Actually varied in this release | Initial temperature \(T_0\in\{10,100,1000\}\) K, hydrogen number density \(n_{\rm H}\in\{44.5,4.45,0.445\}\,{\rm cm}^{-3}\), metallicity \(Z\in\{Z_\odot,0.1Z_\odot,0\}\), and 100 turbulence seeds per physical parameter combination. The product \(3\times3\times3\times100=2700\) gives the released trajectory count. |
| Fixed in this release | Cloud mass \(10^6M_\odot\), monatomic gas \(\gamma=5/3\), turbulence spectral convention, \(64^3\) released grid, self-gravity and the CLOUDY-derived heating/cooling framework. |

## 4. Initial and boundary conditions

### Initial conditions

A spherical turbulent cloud with density-dependent radius and a random velocity field following the documented power-law spectrum. Temperature, density, metallicity and seed label each realization.

### Boundary conditions

Isolated/open cloud-box treatment with self-gravity as implemented in ASURA-FDPS; exact boundaries and gridding are encoded in the generator/released metadata.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `turbulence_gravity_cooling` |
| Spatial dimension | 3D |
| Coordinate system | Cartesian $(x,y,z)$ |
| Spatial resolution | $64^3$ |
| Stored steps per trajectory | 50 |
| Number of trajectories | 2700 |
| Dynamic channels after component expansion | 6 |
| Dynamic fields | density, pressure, temperature, velocity (3) |
| Static fields / scalar context | initial temperature, density, metallicity and turbulence seed |
| Time range | dataset-specific; stored relative to free-fall time |
| Stored time spacing | about $0.02$ free-fall time |
| Spatial domain | density-dependent cloud boxes (about 60/129/278 pc) |
| Estimated release size | 829.4 GB |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,L_3,6)\);
- standard 4-frame history: \((B,4,L_1,L_2,L_3,6)\);
- standard 1-frame target: \((B,1,L_1,L_2,L_3,6)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** ASURA-FDPS with DISPH, self-gravity and CLOUDY-derived cooling/heating

ASURA-FDPS with DISPH evolves \(10^6\,M_\odot\) turbulent clouds. Initial turbulence follows a documented power-law spectrum; cloud radius changes to realize three density levels. CLOUDY-derived metallicity-dependent cooling/heating functions cover \(10\)–\(10^9\) K. The paper reports 577 aggregate hours on a large CPU system.

## 7. Recommended ML tasks and diagnostics

Filament formation, gravitational collapse statistics, multi-parameter generalization, cooling-regime transfer, long-horizon stability, simulation acceleration and latent representations of multiphase ISM structure.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

Metallicity acts primarily as a cooling/heating-strength axis; \(Z=0\) is effectively the adiabatic/primordial limit in the documented release. Storage cadence is expressed relative to the free-fall time, so physical time depends on density.

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
the-well-download --base-path ./the_well_data --dataset turbulence_gravity_cooling --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset turbulence_gravity_cooling --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="turbulence_gravity_cooling",
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
    well_dataset_name="turbulence_gravity_cooling",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.

## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/turbulence_gravity_cooling/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/turbulence_gravity_cooling> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/turbulence_gravity_cooling> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |
