---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 02_navier_stokes_2d_conditioned
spatial_dimension: 2
time_dependent: true
data_format: HDF5
paper: "arXiv:2209.15616v2"
download_key: NavierStokes-2D-conditoned
last_verified: 2026-07-21
title: "2D Incompressible Navier–Stokes (Conditioned)"
linkTitle: "NS-2D conditioned"
weight: 20
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "Same NS smoke system; scans vertical buoyancy and conditions on buoyancy and prediction horizon."
description: "Same NS smoke system; scans vertical buoyancy and conditions on buoyancy and prediction horizon."
---

# 2D Incompressible Navier–Stokes (Conditioned)

Same three-channel smoke–buoyancy system as the standard release, but training scans vertical buoyancy $b_y$ and conditions on $(b_y,\Delta t_{\mathrm{pred}})$ to probe cross-parameter and cross-timescale generalization. The official repo name is misspelled `NavierStokes-2D-conditoned` (missing an `i`); use that name when downloading.

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEArena** |
| Dataset paper | [Towards Multi-spatiotemporal-scale Generalized PDE Modeling](https://arxiv.org/abs/2209.15616) |
| Paper PDF | [arXiv PDF](https://arxiv.org/pdf/2209.15616) |
| Official repository | [pdearena/pdearena](https://github.com/pdearena/pdearena) |
| Hugging Face | [pdearena/NavierStokes-2D-conditoned](https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned) |
| Data size | 81.7 GB |
| Task config | [configs/cond_navierstokes2d.yaml](https://github.com/pdearena/pdearena/blob/main/configs/cond_navierstokes2d.yaml) |
| Solver | [PhiFlow](https://github.com/tum-pbs/PhiFlow) |
| License | MIT |
| Last checked | 2026-07-21 |

## Governing equation

\[
\frac{\partial s}{\partial t}+\mathbf{v}\cdot\nabla s=0,
\]
\[
\frac{\partial \mathbf{v}}{\partial t}+(\mathbf{v}\cdot\nabla)\mathbf{v}=-\nabla p+\nu\nabla^{2}\mathbf{v}+s\begin{pmatrix}0\\b_y\end{pmatrix},\qquad\nabla\cdot\mathbf{v}=0.
\]

$\nu=0.01$ is fixed; $b_y$ varies. Conditioning is $c=(b_y,\Delta t_{\mathrm{pred}})$; $\Delta t_{\mathrm{pred}}$ is a task window, not a new PDE coefficient.

## Variables and coordinates

Same as the [standard release](../01_navier_stokes_2d_standard/): $s,v_x,v_y$ on $128\times128$. Extra conditioning: $b_y$, $\Delta t_{\mathrm{pred}}$.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 2 |
| Time-dependent | yes |
| Grid | $128\times128$ |
| Time points | $T=56$ (task/generation config) |
| Trajectories | train 6,656 / valid 1,664 / test 1,664 (9,984 total) |
| Channels | 3: $s$, $v_x$, $v_y$ (+ conditions) |
| Size | 81.7 GB |
| Format | HDF5 |

## Initial conditions

Zero initial velocity; random smooth smoke (same noise family as standard).

## Boundary conditions

No-slip velocity; zero-normal scalar / boundary extrapolation.

## Numerical generation

Same PhiFlow smoke stepper; conditioned batching via `navierstokes_cond_jobs.sh` (per seed: train 128 / valid 32 / test 32).

## Parameters

| Parameter | How it varies | Value |
|---|---|---|
| Vertical buoyancy $b_y$ | scanned across files/traj. | train range about $[0.2,0.5]$ (in filenames); 9,984 trajectories released |
| Prediction window $\Delta t_{\mathrm{pred}}$ | task construction (frame skips) | from on-disk `dt` and chosen frame gap; config comments list `eval_dts` such as $[1,2,4,8,16]$ steps |
| Initial smoke seed | per trajectory | same noise family |
| Viscosity $\nu$, $b_x$ | fixed | $0.01$, $0$ |
| Grid / BCs / $v_0$ | fixed | same as standard |

## Released configurations

- Task config `cond_navierstokes2d.yaml`: `trajlen=56`; conditioned generation uses `sample_rate=1`.
- Full release: train 6,656 / valid 1,664 / test 1,664.
- Time and conditioning follow each HDF5’s `dt`, `buo_y`, and the task dataloader (do not override the release with the paper’s 0.375 s narrative).

## Data files

Examples:

`NavierStokes2D_{split}_{seed}_{buoyancy}.h5`  
`NavierStokes2D_train_{seed}_{buoyancy}_32.h5`

Buoyancy is encoded in the filename. See [Data format](../00_data_format/).

## Data layout and machine-learning task

Same field keys as standard. Typical conditioned sample is 1→1 (exact history/future follows the training config used):

\[
X\in\mathbb{R}^{1\times3\times128\times128}\to Y\in\mathbb{R}^{1\times3\times128\times128},
\]

with $(b_y,\Delta t)$ injected via embeddings (Addition / AdaGN / Spatial–Spectral are model choices).

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned
```

## Regenerating from the official code

```bash
./pdedatagen/scripts/navierstokes_cond_jobs.sh
```

## What is interesting and challenging about the data

Continuous buoyancy interpolation/extrapolation; time-window changes one-step difficulty; packs parameter and timescale generalization in one controlled system.

## Primary sources

- [PDEArena paper](https://arxiv.org/abs/2209.15616)
- [Conditioned task config](https://github.com/pdearena/pdearena/blob/main/configs/cond_navierstokes2d.yaml)
- [Data generation docs](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Hugging Face page](https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned)
