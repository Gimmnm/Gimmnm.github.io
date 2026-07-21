---
title: "3D Time-Domain Maxwell Electromagnetic Fields"
dataset_family: PDEArena
dataset_release: Maxwell-3D
equation: "Maxwell equations"
spatial_dimension: 3
coordinate_system: "uniform Cartesian grid with periodic boundaries"
task_variant: "raw 8-frame electromagnetic trajectories"
official_status: "official PDEArena extension; associated with Clifford Neural Layers"
license: MIT
last_verified: 2026-07-21
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
summary: "FDTD trajectories of electric and magnetic fields in a periodic homogeneous 3D medium, excited by multiple randomized plane sources and saved on a central $32^3$ crop."
description: "FDTD trajectories of electric and magnetic fields in a periodic homogeneous 3D medium, excited by multiple randomized plane sources and saved on a central $32^3$ crop."

---

# 3D Time-Domain Maxwell Electromagnetic Fields

> **One-line description:** FDTD trajectories of electric and magnetic fields in a periodic homogeneous 3D medium, excited by multiple randomized plane sources and saved on a central $32^3$ crop.

[中文版本](../zh/maxwell_3d.md)

## Longer description

Maxwell-3D is an official current PDEArena release, but it is not part of the Navier--Stokes/shallow-water experiments in the original 2022 PDEArena paper. The repository associates it with *Clifford Neural Layers for PDE Modeling*. The generator runs on a periodic $64^3$ grid, places 18 randomized plane sources, burns in the simulation, and saves a central $32^3$ crop.

## Dataset affiliation and provenance

- **Dataset family:** PDEArena
- **Official release:** `pdearena/Maxwell-3D`
- **Associated paper:** *Clifford Neural Layers for PDE Modeling*
- **Generator:** [pdedatagen/maxwell.py](https://github.com/pdearena/pdearena/blob/main/pdedatagen/maxwell.py)
- **Software:** [Python 3D FDTD Simulator](https://github.com/flaport/fdtd)
- **License:** MIT

## Equation

$$
\nabla\cdot\mathbf D=\rho,\qquad\nabla\cdot\mathbf B=0,
$$

$$
\partial_t\mathbf D=\nabla\times\mathbf H-\mathbf J,
\qquad
\partial_t\mathbf B=-\nabla\times\mathbf E,
$$

$$
\mathbf D=\epsilon\mathbf E,\qquad\mathbf B=\mu\mathbf H.
$$

### Fields and a naming caveat

The code-semantic six channels are

$$
[E_x,E_y,E_z,H_x,H_y,H_z].
$$

The HDF5 arrays are named `d_field` and `h_field`, but the current generator writes `grid.E` to `d_field` and `grid.H` to `h_field`. The first array should therefore be interpreted according to the code as $\mathbf E$, despite its key name.

## About the data

### Grid and time

| Item | Specification |
|---|---|
| simulation grid | $64^3$ |
| saved crop | central $32^3$ |
| saved frames | $T=8$ |
| channels per frame | 6 |
| burn-in | 250 FDTD steps |
| sampling | one frame every 25 FDTD steps |
| boundaries | periodic in $x,y,z$ |
| domain length | $L=3.2\times10^{-5}$ m |
| simulation spacing | $5\times10^{-7}$ m |

$$
\texttt{d\_field},\texttt{h\_field}
\in\mathbb R^{N\times8\times32\times32\times32\times3},
$$

or concatenated as $U\in\mathbb R^{N\times8\times6\times32^3}$.

No unique official Maxwell history/future slice is specified in the current repository. Downstream work must state whether it uses 1-to-1, multi-frame-to-1, or sequence-to-sequence prediction.

### Fixed configuration

| Parameter | Value |
|---|---:|
| wavelength | $10^{-5}$ m |
| speed of light | 299,792,458 m/s |
| maximum source amplitude | 1 |
| permittivity | 10 |
| permeability | 1 |
| domain length | $3.2\times10^{-5}$ m |
| `n_large`, output `n` | 64, 32 |
| `nt`, `skip_nt`, `sample_rate` | 8, 250, 25 |

### Randomized sources

There are 18 plane sources: six each in XY, XZ, and YZ planes. Each source randomizes its location, side lengths (2--5 cells), amplitude, phase, allowed polarization, and period

$$
T_{source}=\frac{\lambda}{c}q,
\qquad q\sim\mathrm{Unif}[10^{-3},10^3].
$$

Thus the release varies forcing/source conditions, not material coefficients or geometry.

### Number of trajectories and size

| Split | Trajectories |
|---|---:|
| train | 6,400 |
| validation | 1,600 |
| test | 1,600 |
| **total**| **9,600** |

- **Repository size:** 121 GB

## Parameters: configurable, varied, and fixed

| Factor | Release treatment |
|---|---|
| source location/size/orientation | **randomized** |
| source amplitude/phase/period | **randomized** |
| number of sources | fixed at 18 |
| $\epsilon,\mu$ | fixed at 10 and 1 |
| wavelength, light speed, domain | fixed |
| boundaries | fixed periodic |
| grid/crop | fixed $64^3\to32^3$ |
| burn-in/sampling/frames | fixed 250/25/8 |

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/Maxwell-3D
```

Pointer-only clone:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/pdearena/Maxwell-3D
```

## What is interesting and challenging

- Volumetric six-channel trajectories are memory intensive;
- Electric and magnetic fields are geometric vector fields;
- Multiple sources generate interference and multiscale frequency structure;
- Periodic boundaries and the central crop hide part of the full source--domain relation;
- HDF5 key naming must be reconciled with actual written variables.

## Known limitations

Material properties, geometry, and boundaries are fixed, and the release has no single canonical history/future task definition.

## Citation

```bibtex
@article{brandstetter2022clifford,
  title={Clifford Neural Layers for PDE Modeling},
  author={Brandstetter, Johannes and van den Berg, Rianne and Welling, Max and Gupta, Jayesh K.},
  journal={arXiv preprint arXiv:2209.04934},
  year={2022}
}
```

## Sources

- [PDEArena repository and citation guidance](https://github.com/pdearena/pdearena)
- [Generator](https://github.com/pdearena/pdearena/blob/main/pdedatagen/maxwell.py)
- [Generator configuration](https://github.com/pdearena/pdearena/blob/main/pdedatagen/configs/maxwell3d.yaml)
- [Hugging Face dataset](https://huggingface.co/datasets/pdearena/Maxwell-3D)
