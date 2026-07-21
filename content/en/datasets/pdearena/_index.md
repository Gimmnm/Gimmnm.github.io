---
title: "PDEArena"
linkTitle: PDEArena
weight: 30
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
math: true
summary: "Operator-learning PDE benchmark covering Navier–Stokes, shallow water, Maxwell-3D, and KS."
description: "Operator-learning PDE benchmark covering Navier–Stokes, shallow water, Maxwell-3D, and KS."
dataset_family: PDEArena
---

# PDEArena

## Problem definition

Operator learning relates solutions $u:\mathcal{X}\to\mathbb{R}^{n}$ and $u':\mathcal{X}'\to\mathbb{R}^{n'}$ on (possibly different) domains through an operator $\mathcal{G}$:

\[
\mathcal{G}:(u\in\mathcal{U})\mapsto(u'\in\mathcal{U}'),
\]

where $\mathcal{U}$ and $\mathcal{U}'$ are the corresponding solution spaces. In practice, neural PDE surrogates usually map several past frames on a fixed grid to one or more future frames.

PDEArena emphasizes generalization across initial conditions, PDE parameters, and time windows $\Delta t$. In conditioning experiments, solution pairs $\{u,u'\}$ may come from different solution spaces characterized by different force terms, while the map $u\mapsto u'$ should also generalize across time windows. Both force terms and $\Delta t$ are continuous scalars and can be encoded with sinusoidal Fourier embeddings before being injected into the network.

The benchmark desiderata are: tasks backed by domain solvers, sufficient difficulty, diversity of formulations (velocity vs. vorticity), and probes of temporal-scale and parameter generalization.

## Equation catalog

Start with [Data format](./00_data_format/); each equation card also lists download layout and naming.

| # | Equation card | Hugging Face release | Current advertised size |
|---:|---|---|---:|
| — | [Data format](./00_data_format/) | — | — |
| 1 | [2D incompressible NS smoke (standard)](./01_navier_stokes_2d_standard/) | `NavierStokes-2D` | 43 GB |
| 2 | [2D incompressible NS (conditioned)](./02_navier_stokes_2d_conditioned/) | `NavierStokes-2D-conditoned` | 81.7 GB |
| 3 | [Spherical shallow water (velocity)](./03_shallow_water_2d_velocity/) | `ShallowWater-2D` | 124 GB (shared) |
| 4 | [Spherical shallow water (vorticity)](./04_shallow_water_2d_vorticity/) | same `ShallowWater-2D` task view | no extra size |
| 5 | [3D Maxwell time-domain EM](./05_maxwell_3d/) | `Maxwell-3D` | 121 GB |
| 6 | [1D Kuramoto–Sivashinsky](./06_kuramoto_sivashinsky_1d/) | external `phlippe/...` (loader-supported) | 3.92 GB |

## Shared conventions

- The four official PDEArena organization releases total about **369.7 GB** and **35,784** trajectories; shallow-water velocity/vorticity and 1-day/2-day views share one release and must not be double-counted. KS is counted separately.
- Trajectory counts, time length, sampling, file layout and sizes follow the **Hugging Face release + official generators/task configs**; when the paper disagrees, the released dataset wins.
- Raw 2D trajectories are often written $[N,T,C,H,W]$; 3D as $[N,T,C,D,H,W]$. Model samples slice history frames to future frames; the history length $\ell$ follows the task config.
- Maxwell-3D is an official extension release; KS is external loader-supported data and is excluded from the four-release total.
