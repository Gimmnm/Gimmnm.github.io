---
title: "Magnetohydrodynamic Turbulence — $64^3$"
parent_collection: "The Well"
physical_family: "Ideal isothermal magnetohydrodynamics"
spatial_dimension: 3D
coordinate_system: "Cartesian $(x,y,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/MHD_64/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/MHD_64"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/MHD_64"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: MHD_64
weight: 20
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "These scale-free, non-self-gravitating simulations model driven isothermal magnetohydrodynamic turbulence. Sonic and Alfvénic Mach numbers span subsonic/supersonic and strong-/w…"
description: "These scale-free, non-self-gravitating simulations model driven isothermal magnetohydrodynamic turbulence. Sonic and Alfvénic Mach numbers span subsonic/supersonic and strong-/w…"

---

# Magnetohydrodynamic Turbulence — $64^3$

![Density evolution](/the-well/MHD_64__density_unnormalized.gif)


> **Parent collection:** The Well
> **Directory:** `MHD_64`
> **Equation family:** Ideal isothermal magnetohydrodynamics

## 1. Scope and physical overview

These scale-free, non-self-gravitating simulations model driven isothermal magnetohydrodynamic turbulence. Sonic and Alfvénic Mach numbers span subsonic/supersonic and strong-/weak-field regimes. Matched \(256^3\) and anti-aliased \(64^3\) data support both dynamics prediction and super-resolution.

The Well treats each downloadable directory as a self-documenting HDF5 dataset.

## 2. Governing equations

$$
\frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf v)=0,
$$
$$
\frac{\partial(\rho\mathbf v)}{\partial t}
+\nabla\cdot\left[
\rho\mathbf v\mathbf v+
\left(p+\frac{B^2}{8\pi}\right)I-\frac{\mathbf B\mathbf B}{4\pi}
\right]=\mathbf f,
$$
$$
\frac{\partial\mathbf B}{\partial t}
-\nabla\times(\mathbf v\times\mathbf B)=0,
\qquad p=c_s^2\rho.
$$

### Variables and physical fields

- \(\rho\): density.
- \(\mathbf v\): velocity.
- \(\mathbf B\): magnetic field.
- \(p=c_s^2\rho\): isothermal pressure.
- \(\mathbf f\): large-scale solenoidal forcing near wavenumber \(k\approx2.5\).
- \(M_s=|\mathbf v|/c_s\): sonic Mach number.
- \(M_A=|\mathbf v|/\langle v_A\rangle\): Alfvénic Mach number.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Sonic/Alfvénic Mach numbers, forcing amplitude/spectrum/correlation time, sound speed, mean magnetic field, initial perturbations, self-gravity, equation of state, box scale and resolution. |
| Actually varied in this release | Sonic Mach number \(M_s\in\{0.5,0.7,1.5,2.0,7.0\}\) and Alfvénic Mach number \(M_A\in\{0.7,2.0\}\). Ten realizations are provided per parameter pair, giving \(5\times2\times10=100\) trajectories. |
| Fixed in this release | Periodic cube; isothermal equation of state; no self-gravity; continuous large-scale solenoidal forcing near \(k\approx2.5\); 100 output frames; code-unit normalization. |

## 4. Initial and boundary conditions

### Initial conditions

Random turbulent realizations/forcing phases within each \((M_s,M_A)\) pair. In super-Alfvénic runs the initial \(M_A\) may be larger (reported as 7) before the small-scale dynamo saturates near the labeled final regime \(M_A\approx2\).

### Boundary conditions

Periodic in all three spatial directions.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `MHD_64` |
| Spatial dimension | 3D |
| Coordinate system | Cartesian $(x,y,z)$ |
| Spatial resolution | $64^3$ |
| Stored steps per trajectory | 100 |
| Number of trajectories | 100 |
| Dynamic channels after component expansion | 7 |
| Dynamic fields | density (1), velocity (3), magnetic field (3) |
| Static fields / scalar context | Mach-number labels and forcing configuration |
| Time range | $[0,1]$ (code units) |
| Stored time spacing | $\approx0.01$ |
| Spatial domain | periodic cube |
| Estimated release size | 71.6 GB |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,L_3,7)\);
- standard 4-frame history: \((B,4,L_1,L_2,L_3,7)\);
- standard 1-frame target: \((B,1,L_1,L_2,L_3,7)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** third-order hybrid ENO ideal-MHD solver; anti-aliased low-pass downsampling from $256^3$

A third-order hybrid essentially non-oscillatory scheme solves ideal MHD on a periodic cube at \(256^3\). The \(64^3\) release is produced from the high-resolution trajectories after ideal low-pass filtering and anti-aliased downsampling. One high-resolution simulation is reported to require about 48 h on 64 CPU cores.

## 7. Recommended ML tasks and diagnostics

3D turbulent forecasting, cross-Mach-number generalization, magnetic-field-aware conservation learning, spectral diagnostics, \(64^3\!\to256^3\) super-resolution and resolution transfer.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

This is the anti-aliased low-resolution representation paired with `MHD_256`. It is suitable as a low-resolution input/target for super-resolution experiments.

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
the-well-download --base-path ./the_well_data --dataset MHD_64 --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset MHD_64 --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="MHD_64",
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
    well_dataset_name="MHD_64",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.

## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/MHD_64/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/MHD_64> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/MHD_64> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |
