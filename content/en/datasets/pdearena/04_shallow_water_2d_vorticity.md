---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 04_shallow_water_2d_vorticity
spatial_dimension: 2
time_dependent: true
data_format: Zarr
paper: "arXiv:2209.15616v2"
download_key: ShallowWater-2D
last_verified: 2026-07-21
title: "2D Spherical Shallow Water (Vorticity)"
linkTitle: "SWE vorticity"
weight: 40
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "Vorticity task view over the same shallow-water trajectories: pressure/free-surface + vertical vorticity, 2-day."
description: "Vorticity task view over the same shallow-water trajectories: pressure/free-surface + vertical vorticity, 2-day."
---

# 2D Spherical Shallow Water (Vorticity)

Paper **vorticity–stream-function task representation**: from the same `ShallowWater-2D` velocity trajectories, convert winds to spherical normal vorticity $\zeta$ so the model sees two scalar channels. Not a second 124 GB release.

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEArena** |
| Underlying release | [pdearena/ShallowWater-2D](https://huggingface.co/datasets/pdearena/ShallowWater-2D) |
| Dataset paper | [Towards Multi-spatiotemporal-scale Generalized PDE Modeling](https://arxiv.org/abs/2209.15616) |
| Velocity companion | [Velocity form](../03_shallow_water_2d_velocity/) |
| Data size | shared 124 GB (no extra) |
| License | MIT |
| Last checked | 2026-07-21 |

## Governing equation

Same rotating shallow-water dynamics as the velocity form. Vertical vorticity

\[
\zeta=(\nabla_s\times\mathbf{v})\cdot\hat{\mathbf{r}}
\]

(local Cartesian: $\zeta\approx\partial_x v-\partial_y u$). The task uses $[p,\zeta]$, not potential vorticity $(\zeta+f_c)/h$, and does not store streamfunction as a separate output channel.

## Variables and coordinates

- $p$: pressure/free-surface scalar; $\zeta$: vertical vorticity from $(u,v)$;
- Grid/coordinates as in the [velocity form](../03_shallow_water_2d_velocity/).

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 2 (sphere) |
| Time-dependent | yes |
| Spatial resolution | $192\times96$ |
| Task horizon | 2 days / 48 h |
| Trajectory length | $T=11$ |
| Trajectories | same 8,400 underlying |
| Channels | 2: $p$, $\zeta$ |
| Size | not counted separately |
| Format | same Zarr; vorticity derived in the pipeline |

## Initial conditions

Identical to the velocity form (`random2`, etc.).

## Boundary conditions

Same as the velocity form.

## Numerical generation

Same generator; vorticity computed from winds on the same trajectories. Appendix: normalize pressure and vorticity before training.

## Parameters

| Parameter | How it varies | Value |
|---|---|---|
| IC randomness | per trajectory | same as velocity |
| $\zeta$ | derived from $(u,v)$ | not an independent random parameter |
| Grid / physics / 20-day setup | fixed | same as velocity |
| Time task | paper’s 2-day vorticity task | no evidence of a separate 1-day vorticity repo |

## Released configurations

- 2-day vorticity task: 2 history frames → 1 future; same underlying trajectories as the velocity form.
- Full release size matches `ShallowWater-2D` (8,400 trajectories, shared 124 GB).

## Data files

Download the same `ShallowWater-2D`; there is no separate official “ShallowWater-Vorticity” repo. Layout: [velocity form](../03_shallow_water_2d_velocity/) and [Data format](../00_data_format/).

## Data layout and machine-learning task

\[
X\in\mathbb{R}^{2\times2\times96\times192}\to Y\in\mathbb{R}^{1\times2\times96\times192}.
\]

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/ShallowWater-2D
```

Then build the vorticity view via the PDEArena pipeline.

## Regenerating from the official code

Same as [velocity form](../03_shallow_water_2d_velocity/); compute $\zeta$ on the task side.

## What is interesting and challenging about the data

Vorticity highlights rotation and fine eddies; compressing 2D winds to one scalar changes difficulty; shared trajectories enable fair representation comparisons.

## Primary sources

- [PDEArena paper](https://arxiv.org/abs/2209.15616)
- [Velocity companion](../03_shallow_water_2d_velocity/)
- [Hugging Face underlying page](https://huggingface.co/datasets/pdearena/ShallowWater-2D)
