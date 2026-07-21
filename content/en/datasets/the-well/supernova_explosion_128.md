---
title: "Supernova Explosion — $128^3$"
parent_collection: "The Well"
physical_family: "Compressible SPH hydrodynamics + cooling"
spatial_dimension: 3D
coordinate_system: "Cartesian $(x,y,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/supernova_explosion_128/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/supernova_explosion_128"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/supernova_explosion_128"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: supernova_explosion_128
weight: 180
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "A supernova deposits energy into a turbulent, radiatively cooling interstellar medium. The resulting blast wave expands anisotropically through dense filaments. The release prov…"
description: "A supernova deposits energy into a turbulent, radiatively cooling interstellar medium. The resulting blast wave expands anisotropically through dense filaments. The release prov…"

---

# Supernova Explosion — $128^3$

![Temperature evolution](/the-well/supernova_explosion_128__temperature_normalized.gif)


> **Parent collection:** The Well
> **Directory:** `supernova_explosion_128`
> **Equation family:** Compressible SPH hydrodynamics + cooling

## 1. Scope and physical overview

A supernova deposits energy into a turbulent, radiatively cooling interstellar medium. The resulting blast wave expands anisotropically through dense filaments. The release provides two spatial resolutions, but the trajectory counts differ, so they should not be assumed to form a complete one-to-one paired set.

The Well treats each downloadable directory as a self-documenting HDF5 dataset.

## 2. Governing equations

For a monatomic ideal gas with \(\gamma=5/3\),
$$
P=(\gamma-1)\rho u.
$$
The Lagrangian form used in the appendix is
$$
\frac{d\rho}{dt}=-\rho\nabla\cdot\mathbf v,
$$
$$
\frac{d^2\mathbf r}{dt^2}
=-\frac{\nabla P}{\rho}+\mathbf a_{\rm visc}-\nabla\Phi,
$$
$$
\frac{du}{dt}
=-\frac{P}{\rho}\nabla\cdot\mathbf v
+\frac{\Gamma-\Lambda}{\rho}.
$$
For comparison, the spherical Sedov scaling is
$$
R(t)=\xi\left(\frac{E}{\rho}\right)^{1/5}t^{2/5}.
$$

### Variables and physical fields

- \(\rho,P,u,\mathbf v,\mathbf r\): density, pressure, specific internal energy, velocity and position.
- \(\Phi\): gravitational potential.
- \(\mathbf a_{\rm visc}\): numerical/physical viscous acceleration in the SPH formulation.
- \(\Gamma,\Lambda\): radiative heating and cooling per unit volume.
- \(E\): injected supernova energy.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Explosion energy/location, ambient density/temperature/metallicity, turbulence realization and spectrum, cooling/heating functions, gravity, mass/spatial resolution, box size and output cadence. |
| Actually varied in this release | The released campaign varies turbulent ambient realizations and resolution-specific membership. 260 trajectories at \(128^3\). The explicitly documented physical settings are fixed: initial temperature \(T_0=100\) K, hydrogen number density \(n_{\rm H}=44.5\,{\rm cm}^{-3}\), solar metallicity \(Z=Z_\odot\), and a standard supernova energy scale. |
| Fixed in this release | Monatomic ideal-gas ratio \(\gamma=5/3\), ambient thermodynamic parameters above, cooling model/metallicity, supernova injection convention, output length of 59 frames and the chosen resolution within this directory. |

## 4. Initial and boundary conditions

### Initial conditions

A turbulent, filamentary interstellar-medium realization receives a localized supernova thermal-energy injection. The exact turbulence seed and explosion placement are dataset realization metadata.

### Boundary conditions

Open/outflow-type box treatment as defined by the ASURA-FDPS simulation; consult generator metadata for exact particle-to-grid post-processing.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `supernova_explosion_128` |
| Spatial dimension | 3D |
| Coordinate system | Cartesian $(x,y,z)$ |
| Spatial resolution | $128^3$ |
| Stored steps per trajectory | 59 |
| Number of trajectories | 260 |
| Dynamic channels after component expansion | 6 |
| Dynamic fields | density, pressure, temperature, velocity (3) |
| Static fields / scalar context | fixed ambient thermodynamic/metallicity setup plus realization metadata |
| Time range | approximately $0$–$0.2$ Myr |
| Stored time spacing | uniform in released trajectory |
| Spatial domain | approximately 60 pc box |
| Estimated release size | 754 GB |
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

**Documented solver:** ASURA-FDPS N-body/SPH with density-independent SPH (DISPH)

ASURA-FDPS performs N-body/SPH simulations with density-independent SPH (DISPH), chosen to improve contact-discontinuity and shock treatment. The gas has solar metallicity in the released supernova setup. Aggregate generation costs are reported in the thousands of CPU hours on up to 1040 cores.

## 7. Recommended ML tasks and diagnostics

Blast-wave forecasting, shock/shell preservation, anisotropic expansion, cross-resolution transfer, super-resolution, morphology/statistics prediction and acceleration of galaxy-scale subgrid models.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

The high-resolution set is much smaller than the \(64^3\) set. Cross-resolution experiments must explicitly match trajectory identifiers where available rather than pair by row index.

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
the-well-download --base-path ./the_well_data --dataset supernova_explosion_128 --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset supernova_explosion_128 --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="supernova_explosion_128",
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
    well_dataset_name="supernova_explosion_128",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.

## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/supernova_explosion_128/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/supernova_explosion_128> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/supernova_explosion_128> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |
