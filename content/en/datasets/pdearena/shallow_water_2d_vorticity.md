---
title: "2D Spherical Shallow-Water Equations (Vorticity Task View)"
dataset_family: PDEArena
dataset_release: ShallowWater-2D
equation: "Rotating shallow-water equations in vorticity task representation"
spatial_dimension: 2
coordinate_system: "global longitude-latitude / spherical spectral grid"
task_variant: "vorticity-form 2-day task"
official_status: "official benchmark task view over the ShallowWater-2D release"
license: MIT
last_verified: 2026-07-21
linkTitle: "Shallow Water (vorticity)"
weight: 40
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
summary: "A two-scalar, 2-day benchmark view of the same shallow-water trajectories, using pressure/free-surface state and vertical vorticity instead of the two wind components."
description: "A two-scalar, 2-day benchmark view of the same shallow-water trajectories, using pressure/free-surface state and vertical vorticity instead of the two wind components."

---

# 2D Spherical Shallow-Water Equations (Vorticity Task View)

> **One-line description:** A two-scalar, 2-day benchmark view of the same shallow-water trajectories, using pressure/free-surface state and vertical vorticity instead of the two wind components.

[中文版本](../zh/shallow_water_2d_vorticity.md)

## Longer description

This page documents the paper's vorticity--stream-function representation. It is not a second 124 GB release. The wind field $(u,v)$ from `ShallowWater-2D` is transformed into vertical spherical vorticity $\zeta$, leaving two scalar model channels.

## Dataset affiliation and provenance

- **Dataset family:** PDEArena
- **Underlying release:** `pdearena/ShallowWater-2D`
- **Paper task:** shallow-water vorticity-stream formulation, 2-day prediction
- **Numerical software:** modified SpeedyWeather.jl
- **License:** MIT

## Equation and representation

The underlying dynamics are the rotating shallow-water equations. Vertical vorticity is

$$
\zeta=(\nabla_s\times\mathbf v)\cdot\hat{\mathbf r},
$$

or locally $\zeta\approx\partial_xv-\partial_yu$.

The task uses $[p,\zeta]$. It does not use potential vorticity $(\zeta+f_c)/h$, and streamfunction is not an independently stored output channel.

## About the data

| Item | Specification |
|---|---|
| Domain/grid | global sphere, $192$ longitude × $96$ latitude |
| Common array order | $[96,192]$ |
| prediction window | 2 days / 48 h |
| trajectory length | $T=11$ |
| history/future | 2 / 1 |
| fields | pressure/free-surface scalar, vertical vorticity |
| channels | 2 |

$$
X\in\mathbb R^{2\times2\times96\times192},\qquad
Y\in\mathbb R^{1\times2\times96\times192}.
$$

Flattened: $[4,96,192]\to[2,96,192]$.

### Number of trajectories and size

This view shares the underlying release:

| Split | Trajectories |
|---|---:|
| train | 5,600 |
| validation | 1,400 |
| test | 1,400 |
| **total**| **8,400** |

**Shared repository size: 124 GB.** Do not add another 124 GB for this task view.

### Initial conditions, boundaries, and normalization

All initial conditions, spherical topology, random `random2` wind generation, simulation settings, and solver parameters are shared with the [velocity-form page](../shallow_water_2d_velocity/). Vorticity is derived from the same wind trajectories. The paper appendix explicitly states that pressure and vorticity are normalized for training.

## Parameters: varied and fixed

| Type | Content |
|---|---|
| varied | random initial-wind coefficients, cellwise randomness, spectral perturbation, seed |
| derived | $\zeta$ from $(u,v)$; it is not a random physical coefficient |
| fixed | grid, sphere, solver physics/defaults, 20-day generation setup, perturbation structure |
| time task | a 2-day vorticity task is documented; no separate official 1-day vorticity repository is established |

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/ShallowWater-2D
```

The PDEArena data pipeline then constructs/reads the vorticity representation; there is no separate official `ShallowWater-Vorticity` Hugging Face release.

## What is interesting and challenging

- Vorticity emphasizes rotation, shear, and small-scale structures;
- Converting a vector field to a scalar representation changes symmetry and learning requirements;
- Recovering velocity from vorticity is globally coupled through an elliptic solve;
- Shared trajectories enable controlled comparisons between state representations.

## Known limitations

This is a representation change, not a parameter sweep. Documentation should always state that the underlying trajectories are shared with the velocity view.


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
- [Velocity-form companion page](../shallow_water_2d_velocity/)
- [Underlying Hugging Face release](https://huggingface.co/datasets/pdearena/ShallowWater-2D)
- [Repository](https://github.com/pdearena/pdearena)
