---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 05_maxwell_3d
spatial_dimension: 3
time_dependent: true
data_format: HDF5
paper: "Clifford Neural Layers (associated); not in PDEArena 2022 main experiments"
download_key: Maxwell-3D
last_verified: 2026-07-21
title: "3D Maxwell Time-Domain EM"
linkTitle: Maxwell-3D
weight: 50
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "FDTD EM trajectories in a 3D periodic uniform medium; central $32^3$, 8 frames; random plane sources."
description: "FDTD EM trajectories in a 3D periodic uniform medium; central $32^3$, 8 frames; random plane sources."
---

# 3D Maxwell Time-Domain EM

Official PDEArena extension (associated with *Clifford Neural Layers for PDE Modeling*), not part of the 2022 NS/shallow-water main experiments. Eighteen random plane sources on a $64^3$ periodic grid; after burn-in, the central $32^3$ is saved for 8 frames.

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEArena** (extension) |
| Associated paper | [Clifford Neural Layers for PDE Modeling](https://arxiv.org/abs/2209.04934) |
| Official repository | [pdearena/pdearena](https://github.com/pdearena/pdearena) |
| Hugging Face | [pdearena/Maxwell-3D](https://huggingface.co/datasets/pdearena/Maxwell-3D) |
| Data size | 121 GB |
| Generator | [pdedatagen/maxwell.py](https://github.com/pdearena/pdearena/blob/main/pdedatagen/maxwell.py) |
| Solver | [Python 3D FDTD Simulator](https://github.com/flaport/fdtd) |
| License | MIT |
| Last checked | 2026-07-21 |

## Governing equation

\[
\nabla\cdot\mathbf{D}=\rho,\qquad\nabla\cdot\mathbf{B}=0,
\]
\[
\frac{\partial\mathbf{D}}{\partial t}=\nabla\times\mathbf{H}-\mathbf{J},\qquad
\frac{\partial\mathbf{B}}{\partial t}=-\nabla\times\mathbf{E},
\]
\[
\mathbf{D}=\epsilon\mathbf{E},\qquad\mathbf{B}=\mu\mathbf{H}.
\]

Random PlaneSources provide external excitation.

## Variables and coordinates

- Six channels per frame: $[E_x,E_y,E_z,H_x,H_y,H_z]$;
- HDF5 keys `d_field` / `h_field` currently store `grid.E` / `grid.H`—treat the first group as $\mathbf{E}$;
- Solve on $64^3$, save central $32^3$; domain length $L=3.2\times10^{-5}$ m.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 3 |
| Time-dependent | yes |
| Grid | uniform Cartesian, periodic |
| Saved region | central $32^3$ |
| Time points | 8 (burn-in 250 steps; save every 25) |
| Trajectories | train 6,400 / valid 1,600 / test 1,600 (9,600 total) |
| Channels | 6: $\mathbf{E}$, $\mathbf{H}$ |
| Size | 121 GB |
| Format | HDF5 |

## Initial conditions

Eighteen PlaneSources (6 per XY/XZ/YZ): random size $\in\{2,3,4,5\}$ cells, position, amplitude, phase, polarization, and period.

## Boundary conditions

Periodic in $x,y,z$.

## Numerical generation

FDTD; config `pdedatagen/configs/maxwell3d.yaml`. Generation script: 64 seeds × (100/25/25).

## Parameters

| Parameter | How it varies | Value |
|---|---|---|
| Source geometry / amp / phase / period | per trajectory | $T=\lambda q/c$, $q\sim\mathrm{Unif}[10^{-3},10^3]$ |
| Number of sources | fixed | 18 |
| $\epsilon_r,\mu_r$ | fixed | 10, 1 |
| Wavelength / $c$ / $L$ | fixed | $10^{-5}$ m; $c$; $L=3.2\times10^{-5}$ m |
| Grid / crop / frames | fixed | $64^3\to32^3$; $T=8$ |

## Released configurations

No single official Maxwell `time_history`/`time_future` task config in the repo; state I/O slicing explicitly in downstream experiments.

## Data files

`Maxwell3D_{train|valid|test}_{seed}.h5`  
Arrays: `d_field`,`h_field` $\in\mathbb{R}^{N\times8\times32\times32\times32\times3}$. See [Data format](../00_data_format/).

## Data layout and machine-learning task

Stacked $U\in\mathbb{R}^{N\times8\times6\times32\times32\times32}$. History/future lengths are experiment-defined.

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/Maxwell-3D
```

## Regenerating from the official code

```bash
python scripts/generate_data.py base=pdedatagen/configs/maxwell3d.yaml \
  experiment=maxwell mode=train samples=100 seed=$SEED \
  dirname=pdearena_data/maxwell3d/
python scripts/compute_normalization.py --dataset maxwell pdearena_data/maxwell3d
```

## What is interesting and challenging about the data

Large 3D vector fields; multi-source interference; key names vs. $\mathbf{E}/\mathbf{H}$ semantics need care.

## Primary sources

- [PDEArena repository](https://github.com/pdearena/pdearena)
- [Maxwell generator](https://github.com/pdearena/pdearena/blob/main/pdedatagen/maxwell.py)
- [Hugging Face page](https://huggingface.co/datasets/pdearena/Maxwell-3D)
