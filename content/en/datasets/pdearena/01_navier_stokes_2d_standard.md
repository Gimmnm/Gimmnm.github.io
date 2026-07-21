---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 01_navier_stokes_2d_standard
spatial_dimension: 2
time_dependent: true
data_format: HDF5
paper: "arXiv:2209.15616v2"
download_key: NavierStokes-2D
last_verified: 2026-07-21
title: "2D Incompressible Navier–Stokes Smoke (Standard)"
linkTitle: "NS-2D standard"
weight: 10
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "Closed-box incompressible NS + smoke scalar; fixed viscosity and buoyancy, random ICs only."
description: "Closed-box incompressible NS + smoke scalar; fixed viscosity and buoyancy, random ICs only."
---

# 2D Incompressible Navier–Stokes Smoke (Standard)

In a closed 2D square domain, incompressible Navier–Stokes advances the velocity while an advected smoke/particle scalar feeds back through a fixed vertical buoyancy force. Pressure is not stored as a supervised channel. The standard release varies only random initial smoke; viscosity, buoyancy, domain, grid and BCs are fixed, so the task probes multi-IC trajectory prediction.

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEArena** |
| Dataset paper | [Towards Multi-spatiotemporal-scale Generalized PDE Modeling](https://arxiv.org/abs/2209.15616) |
| Paper PDF | [arXiv PDF](https://arxiv.org/pdf/2209.15616) |
| Official repository | [pdearena/pdearena](https://github.com/pdearena/pdearena) |
| Hugging Face | [pdearena/NavierStokes-2D](https://huggingface.co/datasets/pdearena/NavierStokes-2D) |
| Data size | 43 GB |
| Generator entry | [pdedatagen/navier_stokes.py](https://github.com/pdearena/pdearena/blob/main/pdedatagen/navier_stokes.py) |
| Solver | [PhiFlow](https://github.com/tum-pbs/PhiFlow) |
| License | MIT |
| Last checked | 2026-07-21 |

## Governing equation

\[
\frac{\partial \mathbf{v}}{\partial t}+(\mathbf{v}\cdot\nabla)\mathbf{v}=-\nabla p+\nu\nabla^{2}\mathbf{v}+\mathbf{f},\qquad\nabla\cdot\mathbf{v}=0,
\]
\[
\frac{\partial s}{\partial t}+\mathbf{v}\cdot\nabla s=0,\qquad
\mathbf{f}=s\begin{pmatrix}b_x\\b_y\end{pmatrix},\qquad(b_x,b_y)=(0,0.5).
\]

(Paper Eq. (5) writes viscosity as $\mu$; release/code use $\nu=0.01$.)

## Variables and coordinates

**State**
- $s$: smoke/particle concentration; $\mathbf{v}=(v_x,v_y)$: velocity; $p$: pressure (projection multiplier, not released).

**Parameters**
- $\nu$: viscosity; $b_y$: vertical buoyancy coefficient.

**Domain**
- Space: $128\times128$ uniform Cartesian; $L_x=L_y=32$ ($\Delta x=\Delta y=0.25$);
- Time: generator $t\in[18,102]$, $n_t=56$ base steps; release uses `sample_rate=4` → **14** saved frames.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 2 |
| Time-dependent | yes |
| Grid | uniform Cartesian $128\times128$ |
| Spatial domain | closed box, $L_x=L_y=32$ |
| Time range | generation window $[18,102]$; 14 saved frames (`sample_rate=4`) |
| Spatial resolution | $128\times128$ |
| Time points | 14 |
| Trajectories | train 5,200 / valid 1,300 / test 1,300 (7,800 total) |
| Channels | 3: $s$, $v_x$, $v_y$ |
| Trajectory shape | $14\times3\times128\times128$ |
| Size | 43 GB |
| Format | HDF5 |

## Initial conditions

- Scalar: `abs(Noise(scale=11.0, smoothness=6.0))`, seed per trajectory;
- Velocity: $\mathbf{v}_0=0$ on a staggered grid.

## Boundary conditions

- Velocity: no-slip Dirichlet $\mathbf{v}=0$;
- Scalar: Neumann $\partial_n s=0$ (generator uses boundary extrapolation).

## Numerical generation

PhiFlow; one step: semi-Lagrangian scalar advection → buoyancy → velocity advection + force → explicit viscosity → incompressible projection.

## Parameters

| Parameter | How it varies | Value |
|---|---|---|
| Initial smoke seed | per trajectory | Noise scale=11, smoothness=6 |
| Viscosity $\nu$ | fixed | 0.01 |
| Buoyancy $(b_x,b_y)$ | fixed | $(0,0.5)$ |
| Grid / domain | fixed | $128^2$, $L=32$ |
| Initial velocity | fixed | $\mathbf{0}$ |
| Boundaries | fixed | no-slip velocity; zero-normal scalar |

## Released configurations

- Task config `navierstokes2d.yaml`: `time_history=4`, `time_future=1`, `trajlen=14`.
- Full release: train 5,200 / valid 1,300 / test 1,300.
- Use on-disk `dt` in each HDF5 (generator base step ≈ 1.5 s, then subsampled with `sample_rate=4`).

## Data files

Flat Hugging Face directory; naming

`NavierStokes2D_{train|valid|test}_{seed}_0.50000.h5`

Official `navierstokes_jobs.sh` uses 52 seeds × (100/25/25) trajectories. See [Data format](../00_data_format/).

## Data layout and machine-learning task

HDF5 keys: `u` ($s$), `vx`, `vy`, plus `t`,`x`,`y`,`dt`,`dx`,`dy`,`buo_y`.

Typical model sample:

\[
X\in\mathbb{R}^{4\times3\times128\times128}\to Y\in\mathbb{R}^{1\times3\times128\times128}
\]

(channel-stacked: $[12,128,128]\to[3,128,128]$).

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D
```

## Regenerating from the official code

```bash
./pdedatagen/scripts/navierstokes_jobs.sh
```

## What is interesting and challenging about the data

Two-way scalar–velocity coupling; incompressibility couples velocity components globally; multi-IC / fixed-physics setting suits long rollouts and data-efficiency studies.

## Primary sources

- [PDEArena paper](https://arxiv.org/abs/2209.15616)
- [Official repository](https://github.com/pdearena/pdearena)
- [Data generation docs](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Hugging Face page](https://huggingface.co/datasets/pdearena/NavierStokes-2D)
