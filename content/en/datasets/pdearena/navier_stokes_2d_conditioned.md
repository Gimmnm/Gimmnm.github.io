---
title: "2D Incompressible Navier--Stokes Smoke Buoyancy Flow (Conditioned)"
dataset_family: PDEArena
dataset_release: NavierStokes-2D-conditoned
equation: "Incompressible Navier--Stokes + advected scalar"
spatial_dimension: 2
coordinate_system: "uniform Cartesian grid"
task_variant: "buoyancy- and time-conditioned rollout"
official_status: "official PDEArena release; repository name contains a typo"
license: MIT
last_verified: 2026-07-21
linkTitle: "NS-2D Conditioned"
weight: 20
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
summary: "The same three-channel smoke-buoyancy system as the standard release, but with a sweep over vertical buoyancy and a continuous prediction-time condition."
description: "The same three-channel smoke-buoyancy system as the standard release, but with a sweep over vertical buoyancy and a continuous prediction-time condition."

---

# 2D Incompressible Navier--Stokes Smoke Buoyancy Flow (Conditioned)

> **One-line description:** The same three-channel smoke-buoyancy system as the standard release, but with a sweep over vertical buoyancy and a continuous prediction-time condition.

[中文版本](../zh/navier_stokes_2d_conditioned.md)

## Longer description

This release tests whether one surrogate can generalize across both a PDE parameter and temporal scales. The physical parameter is the vertical buoyancy $b_y$. The prediction interval $\Delta t_{\rm pred}$ specifies the separation between input and target frames and is a task/discretization condition, not a new physical coefficient.

The actual Hugging Face repository is spelled `NavierStokes-2D-conditoned`; download commands must preserve this typo.

## Dataset affiliation and provenance

- **Dataset family:** PDEArena
- **Official release:** `pdearena/NavierStokes-2D-conditoned`
- **Associated work:** *Towards Multi-spatiotemporal-scale Generalized PDE Modeling*
- **License:** MIT
- **Relation to standard data:** same PDE, fields, grid, viscosity, boundaries, and initial-condition family; adds buoyancy and time-window conditioning.

## Equation

$$
\frac{\partial s}{\partial t}+\mathbf v\cdot\nabla s=0,
$$

$$
\frac{\partial\mathbf v}{\partial t}+(\mathbf v\cdot\nabla)\mathbf v
=-\nabla p+\nu\nabla^2\mathbf v
+s\begin{pmatrix}0\\b_y\end{pmatrix},
\qquad\nabla\cdot\mathbf v=0.
$$

The release fixes $\nu=0.01$ and varies $b_y$.

## Continuous conditions

$$
c=(b_y,\Delta t_{\rm pred}).
$$

- Paper training range: $0.2\le b_y\le0.5$;
- 832 distinct uniformly sampled training-force values;
- evaluation averaged over 208 unseen force values;
- prediction intervals described in the paper: $0.375$ s to $20$ s;
- representative reported intervals: $0.375,0.75,1.5,3,6$ s.

Sinusoidal embeddings and Addition, AdaGN, or Spatial--Spectral injection are model choices, not extra physical channels.

## About the data

| Item | Specification |
|---|---|
| Grid | $128\times128$ Cartesian |
| Per-frame fields | $s,v_x,v_y$ |
| Channels | 3 |
| Current task trajectory length | $T=56$ |
| Paper input/output | previous 1 frame to target frame |
| Conditions | $b_y,\Delta t_{\rm pred}$ |

$$
X,Y\in\mathbb R^{1\times3\times128\times128},
\qquad
U\in\mathbb R^{N\times56\times3\times128\times128}.
$$

HDF5 fields, initial conditions, and boundaries match the standard release.

### Number of trajectories and size

| Split | Trajectories |
|---|---:|
| train | 6,656 |
| validation | 1,664 |
| test | 1,664 |
| **total**| **9,984** |

- **Repository size:** 81.7 GB
- The paper compares 1,664- and 6,656-trajectory training regimes.

## Parameters: varied and fixed

| Factor | Treatment |
|---|---|
| vertical buoyancy $b_y$ | **varied**, training range $[0.2,0.5]$ |
| prediction interval $\Delta t_{\rm pred}$ | **varied** by target-frame separation |
| initial scalar realization | **varied** |
| viscosity $\nu$ | fixed at 0.01 |
| $b_x$ | fixed at 0 |
| grid/domain | fixed |
| initial velocity | fixed at zero |
| boundaries | fixed |
| noise family | fixed distribution, random realization |

## Paper-versus-current-code timing discrepancy

The paper calls this a higher-temporal-resolution dataset with a 0.375 s base spacing. The visible current main-branch generator comments specify $t_\min=18$, $t_\max=102$, $n_t=56$, and `sample_rate=1`, which imply 1.5 s. The dataset card does not provide enough metadata to reconcile the versions. Reproduction should therefore use the paper definition for the paper experiment and inspect the generated HDF5 `dt` when running current code.

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned
```

Pointer-only clone:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned
```

## What is interesting and challenging

- Continuous interpolation and extrapolation in buoyancy;
- One model must represent multiple prediction horizons;
- Incompressibility and scalar--velocity coupling remain fully active;
- A controlled benchmark for separating parameter and temporal-scale generalization.

## Known limitations

Only buoyancy is swept. Viscosity, geometry, boundaries, and material properties are fixed.


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
- [Conditioned task configuration](https://github.com/pdearena/pdearena/blob/main/configs/cond_navierstokes2d.yaml)
- [Data-generation documentation](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Hugging Face dataset](https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned)
