---
title: "2D Spherical Shallow-Water Equations (Velocity Form)"
dataset_family: PDEArena
dataset_release: ShallowWater-2D
equation: "Rotating shallow-water equations"
spatial_dimension: 2
coordinate_system: "global longitude-latitude / spherical spectral grid"
task_variant: "velocity-form 1-day and 2-day tasks"
official_status: "official PDEArena release and benchmark task view"
license: MIT
last_verified: 2026-07-21
linkTitle: "Shallow Water (velocity)"
weight: 30
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
summary: "Global rotating shallow-water trajectories containing a pressure/free-surface scalar and zonal and meridional wind, exposed through 1-day and 2-day prediction tasks."
description: "Global rotating shallow-water trajectories containing a pressure/free-surface scalar and zonal and meridional wind, exposed through 1-day and 2-day prediction tasks."

---

# 2D Spherical Shallow-Water Equations (Velocity Form)

> **One-line description:** Global rotating shallow-water trajectories containing a pressure/free-surface scalar and zonal and meridional wind, exposed through 1-day and 2-day prediction tasks.

[中文版本](../zh/shallow_water_2d_velocity.md)

## Longer description

The shallow-water equations model a thin fluid layer under hydrostatic balance. PDEArena uses a modified SpeedyWeather.jl solver on a global sphere. Each velocity-form frame contains one pressure/geopotential/free-surface-related scalar and a two-component tangential wind field.

`ShallowWater2DVel-1Day` and `ShallowWater2DVel-2Day` are temporal views of the same released trajectories, not independent physical datasets.

## Dataset affiliation and provenance

- **Dataset family:** PDEArena
- **Official release:** `pdearena/ShallowWater-2D`
- **Task views:** `ShallowWater2DVel-1Day`, `ShallowWater2DVel-2Day`
- **Associated work:** *Towards Multi-spatiotemporal-scale Generalized PDE Modeling*
- **Numerical software:** modified [SpeedyWeather.jl](https://github.com/SpeedyWeather/SpeedyWeather.jl)
- **License:** MIT

## Equation

The paper describes the model and fields but does not print a complete spherical shallow-water system. A standard equivalent vector form is

$$
\frac{\partial h}{\partial t}+\nabla_s\cdot(h\mathbf v)=0,
$$

$$
\frac{\partial\mathbf v}{\partial t}
+(\mathbf v\cdot\nabla_s)\mathbf v
+f_c\hat{\mathbf r}\times\mathbf v
+g\nabla_s h=\mathcal D.
$$

Here $\nabla_s$ is the spherical differential operator, $f_c$ the Coriolis parameter, and $\mathcal D$ solver dissipation/closure.

### Variables and coordinates

- $h$ or $p$: free-surface displacement, geopotential height, or the paper's pressure field;
- $u$: zonal velocity;
- $v$: meridional velocity;
- $(\lambda,\phi)$: longitude and latitude.

## Code and numerical configuration

- [Shallow-water generator directory](https://github.com/pdearena/pdearena/tree/main/pdedatagen/shallowwater)
- [Generator configuration](https://github.com/pdearena/pdearena/blob/main/pdedatagen/configs/shallowwater.yaml)
- [1-day task](https://github.com/pdearena/pdearena/blob/main/configs/shallowwater2d_1day.yaml)
- [2-day task](https://github.com/pdearena/pdearena/blob/main/configs/shallowwater2d_2day.yaml)

Core current settings include 20 simulation days, `model=:shallowwater`, `trunc=62`, `Δt_at_T85=40`, and `initial_conditions=:random2`.

## About the data

### Spatial grid

| Item | Specification |
|---|---|
| Physical domain | global sphere |
| Longitude points | 192 |
| Latitude points | 96 |
| Paper notation | $192\times96$, $\Delta x=1.875^\circ$, $\Delta y=3.75^\circ$ |
| Common array order | $[96,192]=[N_{lat},N_{lon}]$ |
| Solver/output | spherical spectral solver, regular longitude--latitude output |

Longitude is periodic; the poles are handled by the spherical spectral representation. The paper summarizes the setup as a regular grid with periodic boundary conditions.

### Fields

$$
[p,u,v]\quad\text{or equivalently}\quad[h,u,v],
$$

one scalar plus one two-component vector, for 3 channels per frame.

### 2-day task

| Item | Specification |
|---|---|
| trajectory length | $T=11$ |
| history/future | 2 / 1 |
| configuration comments | $n_t=88$, `sample_rate=8` |
| paper prediction window | 48 h |

$$
X\in\mathbb R^{2\times3\times96\times192},\qquad
Y\in\mathbb R^{1\times3\times96\times192}.
$$

Flattened: $[6,96,192]\to[3,96,192]$.

### 1-day task

| Item | Specification |
|---|---|
| trajectory length | $T=21$ |
| history/future | 2 / 1 |
| configuration comments | $n_t=84$, `sample_rate=4` |

The tensor shapes are identical to the 2-day task; only temporal sampling changes.

### Number of trajectories and size

| Split | Trajectories |
|---|---:|
| train | 5,600 |
| validation | 1,400 |
| test | 1,400 |
| **total**| **8,400** |

- **Repository size:** 124 GB
- Velocity/vorticity and 1-day/2-day views share this release and must not be double-counted.

### Initial conditions

The `random2` initialization samples an offset from 80--120, one coefficient from -20--30, two coefficients from -20--40, and cellwise uniform randomness. It constructs a random zonal wind and adds a fixed-form wave perturbation with

$$
A=10^{-4},\quad m=6,\quad\theta_0=45^\circ,\quad\theta_w=10^\circ,
$$

plus random spectral perturbations of fixed amplitude $5\times10^{-6}$.

### Storage and preprocessing

Generation uses NetCDF; the official documentation provides NetCDF-to-Zarr conversion and normalization-statistics computation. The appendix states that shallow-water inputs use the previous two time steps and that pressure and vorticity are normalized for training.

## Parameters: varied and fixed

| Factor | Treatment |
|---|---|
| seed and random initial-wind coefficients | **varied per trajectory** |
| cellwise randomness and spectral realization | **varied** |
| wave-perturbation structure | fixed |
| simulation duration | fixed at 20 days |
| spectral truncation | fixed at 62 |
| grid | fixed at $192\times96$ |
| 1-day/2-day sample rate | **varies across task views** |
| gravity, radius, rotation, dissipation | not reported as swept; solver-version defaults/fixed values |
| topology/boundaries | fixed global sphere |

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/ShallowWater-2D
```

Pointer-only clone:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/pdearena/ShallowWater-2D
```

## What is interesting and challenging

- Simultaneous local weather structures and global circulation;
- Spherical geometry, longitude periodicity, and polar behavior;
- Matched 1-day and 2-day tasks for temporal-scale comparisons;
- Strong initial-condition diversity under fixed governing physics.

## Known limitations

Gravity, rotation rate, planetary radius, mean depth, boundaries, and spatial resolution are not systematically swept.


## Citation

For the PDEArena Navier--Stokes and shallow-water datasets, cite:

```bibtex
@article{gupta2022towards,
  title={Towards Multi-spatiotemporal-scale Generalized PDE Modeling},
  author={Gupta, Jayesh K. and Brandstetter, Johannes},
  journal={arXiv preprint arXiv:2209.15616},
  year={2022}
}
```

## Sources

- [Paper](https://arxiv.org/abs/2209.15616)
- [Repository](https://github.com/pdearena/pdearena)
- [Data-generation documentation](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Hugging Face dataset](https://huggingface.co/datasets/pdearena/ShallowWater-2D)
