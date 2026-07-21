---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 06_kuramoto_sivashinsky_1d
spatial_dimension: 1
time_dependent: true
data_format: HDF5
paper: "LPSDA / external; loader-supported in PDEArena"
download_key: Kuramoto-Sivashinsky-1D
last_verified: 2026-07-21
title: "1D Kuramoto–Sivashinsky Equation"
linkTitle: KS-1D
weight: 60
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "1D periodic KS chaos; fixed- and conditional-viscosity families; external data supported by the PDEArena loader."
description: "1D periodic KS chaos; fixed- and conditional-viscosity families; external data supported by the PDEArena loader."
---

# 1D Kuramoto–Sivashinsky Equation

Spatiotemporal chaos on a 1D periodic domain. PDEArena ships a KS loader and training config, but the current organization does not list KS among its four releases; accessible data live at `phlippe/Kuramoto-Sivashinsky-1D`. Marked as **loader-supported external data**, excluded from the official-four totals.

## Parent dataset and access

| Field | Value |
|---|---|
| Code ecosystem | **PDEArena** |
| Current data repo | [phlippe/Kuramoto-Sivashinsky-1D](https://huggingface.co/datasets/phlippe/Kuramoto-Sivashinsky-1D) |
| Generator | [LPSDA](https://github.com/brandstetter-johannes/LPSDA) |
| Task config | [configs/kuramotosivashinsky1d.yaml](https://github.com/pdearena/pdearena/blob/main/configs/kuramotosivashinsky1d.yaml) |
| Data size | 3.92 GB |
| License | MIT |
| Last checked | 2026-07-21 |

## Governing equation

\[
\frac{\partial u}{\partial t}+u\frac{\partial u}{\partial x}+\frac{\partial^{2}u}{\partial x^{2}}+\nu\frac{\partial^{4}u}{\partial x^{4}}=0,\qquad u(x+L,t)=u(x,t).
\]

## Variables and coordinates

- $u(x,t)$: scalar state; uniform periodic 1D grid;
- Loader may integer-downsample via `resolution`; this page does not guess a unique raw $N_x$.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 1 |
| Time-dependent | yes |
| Grid | uniform periodic 1D |
| Trajectory length (task config) | $T=140$ |
| Channels | 1: $u$ |
| Families | fixed $\nu=1$; conditional $\nu\in[0.5,1.5]$ |
| Size | 3.92 GB |
| Format | HDF5 (6 files) |

Historical filenames suggest ~2,048 / ~4,096 train trajectories for fixed / conditional; valid/test counts are not fully listed on the short data card and are left unspecified here.

## Initial conditions

Full IC distribution is not documented on the public card; use trajectories in the files.

## Boundary conditions

Periodic.

## Numerical generation

Generated with LPSDA; PDEArena loader reads a `pde_*` solution array plus `dt`,`dx` (and viscosity for conditional files). Default `time_step=4` can downsample in time.

## Parameters

| Parameter | How it varies | Value |
|---|---|---|
| Initial conditions | per trajectory | as in files |
| $\nu$ | fixed vs scanned | $1$; $[0.5,1.5]$ |
| $\Delta t,\Delta x$ | metadata / conditioning | as in files |
| Boundaries / PDE form | fixed | periodic; equation above |

## Released configurations

PDEArena task config: 1→1; fixed conditions $[\Delta t,\Delta x]$, conditional also $\nu$. Older download docs mentioned `pdearena/Kuramoto-Sivashinsky-1D`; use the `phlippe` URL for reproducibility.

## Data files

| File | Role |
|---|---|
| `KS_train_fixed_viscosity.h5` | fixed-viscosity train |
| `KS_valid_fixed_viscosity.h5` | fixed-viscosity valid |
| `KS_test_fixed_viscosity.h5` | fixed-viscosity test |
| `KS_train_conditional_viscosity.h5` | conditional train |
| `KS_valid_conditional_viscosity.h5` | conditional valid |
| `KS_test_conditional_viscosity.h5` | conditional test |

See [Data format](../00_data_format/).

## Data layout and machine-learning task

\[
X\in\mathbb{R}^{1\times1\times N_x}\to Y\in\mathbb{R}^{1\times1\times N_x}.
\]

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/phlippe/Kuramoto-Sivashinsky-1D
```

## Regenerating from the official code

Follow [LPSDA](https://github.com/brandstetter-johannes/LPSDA), then read with the PDEArena KS loader.

## What is interesting and challenging about the data

Chaos amplifies short-horizon errors; fourth-order dissipation stresses high frequencies; conditional viscosity probes continuous parameter interpolation/extrapolation.

## Primary sources

- [PDEArena KS config](https://github.com/pdearena/pdearena/blob/main/configs/kuramotosivashinsky1d.yaml)
- [Accessible data page](https://huggingface.co/datasets/phlippe/Kuramoto-Sivashinsky-1D)
- [LPSDA](https://github.com/brandstetter-johannes/LPSDA)
