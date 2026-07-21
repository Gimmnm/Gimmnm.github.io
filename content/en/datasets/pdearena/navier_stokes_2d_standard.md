---
title: "2D Incompressible Navier--Stokes Smoke Buoyancy Flow (Standard)"
dataset_family: PDEArena
dataset_release: NavierStokes-2D
equation: "Incompressible Navier--Stokes + advected scalar"
spatial_dimension: 2
coordinate_system: "uniform Cartesian grid"
task_variant: "standard rollout"
official_status: "official PDEArena release"
license: MIT
last_verified: 2026-07-21
linkTitle: "NS-2D Standard"
weight: 10
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
summary: "A closed-domain incompressible Navier--Stokes simulation with an advected smoke/particle-concentration scalar that feeds back into the velocity through a fixed vertical buoyancy…"
description: "A closed-domain incompressible Navier--Stokes simulation with an advected smoke/particle-concentration scalar that feeds back into the velocity through a fixed vertical buoyancy…"

---

# 2D Incompressible Navier--Stokes Smoke Buoyancy Flow (Standard)

> **One-line description:** A closed-domain incompressible Navier--Stokes simulation with an advected smoke/particle-concentration scalar that feeds back into the velocity through a fixed vertical buoyancy force.

[中文版本](../zh/navier_stokes_2d_standard.md)

## Longer description

Each trajectory contains a scalar concentration field $s(x,y,t)$ and a two-component velocity field $\mathbf v=(v_x,v_y)$. The velocity advects the scalar, while the scalar drives the velocity through buoyancy. Pressure is used internally by the incompressibility projection but is not stored as a supervised output channel.

The standard release varies the random initial scalar realization and seed. Viscosity, buoyancy, geometry, grid, initial velocity, and boundary conditions are fixed, so this is primarily an initial-condition generalization benchmark.

## Dataset affiliation and provenance

- **Dataset family:** PDEArena
- **Official release:** `pdearena/NavierStokes-2D`
- **Associated work:** *Towards Multi-spatiotemporal-scale Generalized PDE Modeling*
- **Authors/maintainers:** Jayesh K. Gupta and Johannes Brandstetter; maintained in the PDEArena repository
- **Domain expert:** not separately identified in the source paper
- **License:** MIT on the current repository and Hugging Face card

## Code and numerical software

- [Current PDEArena repository](https://github.com/pdearena/pdearena)
- [Data-generation documentation](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Navier--Stokes generator](https://github.com/pdearena/pdearena/blob/main/pdedatagen/navier_stokes.py)
- [Generator configuration](https://github.com/pdearena/pdearena/blob/main/pdedatagen/configs/navierstokes2dsmoke.yaml)
- Numerical software: [PhiFlow](https://github.com/tum-pbs/PhiFlow)

The generator performs scalar semi-Lagrangian advection, constructs buoyancy, advects the velocity, applies explicit diffusion, and projects the velocity to a divergence-free field.

## Equation

$$
\frac{\partial \mathbf v}{\partial t}+(\mathbf v\cdot\nabla)\mathbf v
=-\nabla p+\nu\nabla^2\mathbf v+\mathbf f,
\qquad \nabla\cdot\mathbf v=0,
$$

$$
\frac{\partial s}{\partial t}+\mathbf v\cdot\nabla s=0,
$$

with

$$
\mathbf f=s\begin{pmatrix}b_x\\b_y\end{pmatrix},
\qquad (b_x,b_y)=(0,0.5)
$$

for the standard release.

### Variables

- $s$: smoke or particle concentration;
- $\mathbf v=(v_x,v_y)$: velocity;
- $p$: pressure/Lagrange multiplier for incompressibility, not stored as a dataset channel;
- $\nu$: kinematic viscosity;
- $(b_x,b_y)$: buoyancy per unit concentration.

## About the data

### Discretized dimensions

| Item | Specification |
|---|---|
| Spatial dimension | 2D |
| Grid | $128\times128$ uniform Cartesian |
| Paper grid spacing | $\Delta x=\Delta y=0.25$ |
| Current code domain size | $L_x=L_y=32$ |
| Fields per frame | $s,v_x,v_y$ |
| Channels per frame | 3 |
| Paper trajectory length | 14 saved time points |
| Benchmark input/output | 4 history frames to 1 future frame |

$$
U\in\mathbb R^{N\times14\times3\times128\times128},
$$

$$
X\in\mathbb R^{4\times3\times128\times128},\qquad
Y\in\mathbb R^{1\times3\times128\times128}.
$$

Flattening history into channels gives $[12,128,128]\to[3,128,128]$.

### HDF5 fields

| Key | Meaning | Typical shape |
|---|---|---|
| `u` | scalar concentration $s$ | $[N,T,128,128]$ |
| `vx`, `vy` | velocity components | $[N,T,128,128]$ |
| `t` | time coordinates | $[N,T]$ |
| `x`, `y` | spatial coordinates | $[N,128]$ |
| `dt`, `dx`, `dy` | spacing metadata | $[N]$ |
| `buo_y` | vertical buoyancy | $[N]$ |

### Number of trajectories and size

| Split | Trajectories |
|---|---:|
| train | 5,200 |
| validation | 1,300 |
| test | 1,300 |
| **total**| **7,800** |

- **Repository size:** 43 GB
- The 2,080-trajectory setting in the paper is a data-efficiency subset, not the full training split.

### Initial conditions

- Scalar: `abs(Noise(scale=11.0, smoothness=6.0))`, with a different random realization per trajectory;
- Velocity: zero on a staggered grid.

### Boundary conditions

- Velocity: closed domain with no-slip Dirichlet condition $\mathbf v=0$;
- Scalar: zero-normal-gradient Neumann condition in the paper, implemented with boundary extrapolation in the generator.

### Temporal-resolution version note

The paper describes a 21 s simulation sampled every 1.5 s for 14 time points. The current main-branch generator configuration commonly uses $t_\min=18$, $t_\max=102$, $n_t=56$, giving a 1.5 s base step, while the standard batch script sets `sample_rate=4`, yielding 14 saved frames at 6 s spacing. These are version-specific definitions and should not be silently merged.

## Parameters: configurable, varied, and fixed

| Parameter | Configurable | Standard release |
|---|---|---|
| $t_\min,t_\max,n_t$ | yes | fixed |
| `sample_rate`, `skip_nt` | yes | fixed; current script uses `sample_rate=4` |
| $L_x,L_y,n_x,n_y$ | yes | fixed at $32,32,128,128$ |
| viscosity $\nu$ | yes | fixed at 0.01 |
| buoyancy $b_x,b_y$ | yes | fixed at 0 and 0.5 |
| scalar random seed | yes | **varied per trajectory** |
| noise scale/smoothness | code-level | fixed at 11/6 |
| initial velocity | code-level | fixed at zero |
| geometry/boundaries | code-level | fixed |
| correction/force helper parameters | exposed in dataclass | not used by the shown smoke update path |

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D
```

Pointer-only clone:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D
```

## What is interesting and challenging

- Two-way coupling between a transported scalar and velocity;
- Global coupling induced by incompressibility;
- Vortex transport, entrainment, and filamentation across spatial scales;
- A controlled fixed-physics setting for rollout stability and data-efficiency studies.

## Known limitations

The release does not vary viscosity, geometry, boundaries, resolution, or the initial-velocity family. Performance on it is therefore not evidence of generalization to arbitrary Navier--Stokes systems.


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
- [Download documentation](https://github.com/pdearena/pdearena/blob/main/docs/datadownload.md)
- [Hugging Face dataset](https://huggingface.co/datasets/pdearena/NavierStokes-2D)
