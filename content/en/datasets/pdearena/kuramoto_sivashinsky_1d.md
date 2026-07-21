---
title: "1D Kuramoto--Sivashinsky Equation"
dataset_family: PDEArena
dataset_release: Kuramoto-Sivashinsky-1D
equation: "Kuramoto--Sivashinsky equation"
spatial_dimension: 1
coordinate_system: "uniform periodic 1D grid"
task_variant: "fixed- and conditional-viscosity rollout"
official_status: "external Hugging Face release supported by the PDEArena loader"
license: MIT
last_verified: 2026-07-21
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
summary: 'Chaotic scalar trajectories on a periodic 1D domain, provided in fixed-viscosity $\nu=1$ and conditional-viscosity $\nu\in[0.5,1.5]$ file families and supported by the PDEArena…'
description: 'Chaotic scalar trajectories on a periodic 1D domain, provided in fixed-viscosity $\nu=1$ and conditional-viscosity $\nu\in[0.5,1.5]$ file families and supported by the PDEArena…'

---

# 1D Kuramoto--Sivashinsky Equation

> **One-line description:** Chaotic scalar trajectories on a periodic 1D domain, provided in fixed-viscosity $\nu=1$ and conditional-viscosity $\nu\in[0.5,1.5]$ file families and supported by the PDEArena loader.

[中文版本](../zh/kuramoto_sivashinsky_1d.md)

## Longer description

The Kuramoto--Sivashinsky equation combines nonlinear advection, a long-wave instability, and fourth-order dissipation. PDEArena contains a loader and training configuration for these data. The currently accessible release is hosted under `phlippe/Kuramoto-Sivashinsky-1D`, while the current PDEArena Hugging Face organization lists only four other official repositories. This page therefore marks KS as an external, code-supported dataset.

## Dataset affiliation and provenance

- **Code ecosystem:** PDEArena
- **Accessible data repository:** `phlippe/Kuramoto-Sivashinsky-1D`
- **Generator source:** [LPSDA](https://github.com/brandstetter-johannes/LPSDA)
- **PDEArena configuration:** [kuramotosivashinsky1d.yaml](https://github.com/pdearena/pdearena/blob/main/configs/kuramotosivashinsky1d.yaml)
- **License:** MIT
- **Counting status:** excluded from the four official PDEArena-organization releases.

## Equation

$$
\frac{\partial u}{\partial t}
+u\frac{\partial u}{\partial x}
+\frac{\partial^2u}{\partial x^2}
+\nu\frac{\partial^4u}{\partial x^4}=0,
$$

with periodic boundary condition $u(x+L,t)=u(x,t)$.

The second derivative drives a long-wave instability, the fourth derivative damps high frequencies, and nonlinear advection produces spatiotemporal chaos.

## About the data

### PDEArena task configuration

| Item | Specification |
|---|---|
| spatial dimension | 1D |
| field/channels | scalar $u$, 1 channel |
| trajectory length | $T=140$ |
| history/future | 1 / 1 |
| padding | circular |
| fixed-family conditions | $[\Delta t,\Delta x]$ |
| conditional-family conditions | $[\Delta t,\Delta x,\nu]$ |

$$
X\in\mathbb R^{1\times1\times N_x},\qquad
Y\in\mathbb R^{1\times1\times N_x}.
$$

The task configuration does not hard-code one $N_x$; the loader can integer-downsample to a requested resolution.

### HDF5 loading

The loader reads a solution array whose name starts with `pde_`, along with `dt`, `dx`, and viscosity `v` for conditional files. It adds a channel dimension when needed, can temporally subsample with a configurable step, and randomly chooses a temporal phase during training. Scaling conditions for Fourier embeddings is preprocessing, not a change in physical values.

### File families

| Family | Viscosity | Varying factors |
|---|---|---|
| fixed viscosity | $\nu=1$ | initial condition and file metadata $\Delta t,\Delta x$ |
| conditional viscosity | $\nu\in[0.5,1.5]$ | initial condition, $\Delta t,\Delta x,\nu$ |

### Size and known trajectory counts

- **Total repository size:** 3.92 GB
- **Files:** six HDF5 files, fixed/conditional × train/valid/test
- Historical names `KS_train_2048_large.h5` and `KS_train_4096_conditional.h5` establish 2,048 and 4,096 training trajectories. The short current card does not state exact validation/test trajectory counts, so they are left unspecified.

## Parameters: varied and fixed

| Factor | Fixed family | Conditional family |
|---|---|---|
| initial condition | varied | varied |
| $\Delta t$ | metadata/condition | metadata/condition |
| $\Delta x$ | metadata/condition | metadata/condition |
| viscosity $\nu$ | fixed at 1 | **varied in $[0.5,1.5]$** |
| boundary | fixed periodic | fixed periodic |
| equation form | fixed | fixed |
| model resolution | loader may downsample | loader may downsample |

## Download

Use the currently accessible repository:

```bash
git lfs install
git clone https://huggingface.co/datasets/phlippe/Kuramoto-Sivashinsky-1D
```

The old PDEArena download page refers to `pdearena/Kuramoto-Sivashinsky-1D`, which is not currently listed in the PDEArena organization. The `phlippe` repository above is the reproducible current location.

## What is interesting and challenging

- Strong sensitivity and rapid error growth in chaotic rollouts;
- Fourth-order spatial derivatives require accurate high-frequency modeling;
- Periodic translation symmetry is useful for equivariant models and augmentation;
- Conditional viscosity tests continuous parameter generalization;
- $\Delta t$ and $\Delta x$ metadata support cross-discretization studies.

## Known limitations

The public card does not document exact validation/test counts, one canonical original $N_x$, generation precision, or the full initial-condition distribution. These items are intentionally left unspecified.

## Citation

```bibtex
@article{brandstetter2022lie,
  title={Lie Point Symmetry Data Augmentation for Neural PDE Solvers},
  author={Brandstetter, Johannes and Welling, Max and Worrall, Daniel E.},
  journal={arXiv preprint arXiv:2202.07643},
  year={2022}
}
```

## Sources

- [PDEArena task configuration](https://github.com/pdearena/pdearena/blob/main/configs/kuramotosivashinsky1d.yaml)
- [PDEArena download documentation](https://github.com/pdearena/pdearena/blob/main/docs/datadownload.md)
- [Current accessible dataset](https://huggingface.co/datasets/phlippe/Kuramoto-Sivashinsky-1D)
- [LPSDA generator](https://github.com/brandstetter-johannes/LPSDA)
