---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 03_shallow_water_2d_velocity
spatial_dimension: 2
time_dependent: true
data_format: Zarr
paper: "arXiv:2209.15616v2"
download_key: ShallowWater-2D
last_verified: 2026-07-21
title: "2D Spherical Shallow Water (Velocity)"
linkTitle: "SWE velocity"
weight: 30
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "Rotating shallow water on a global lat–lon grid; pressure/free-surface + zonal/meridional winds; 1-day and 2-day views."
description: "Rotating shallow water on a global lat–lon grid; pressure/free-surface + zonal/meridional winds; 1-day and 2-day views."
---

# 2D Spherical Shallow Water (Velocity)

Rotating shallow-water trajectories on the global sphere from a modified SpeedyWeather.jl, storing a pressure/free-surface scalar and zonal/meridional winds. `ShallowWater2DVel-1Day` and `ShallowWater2DVel-2Day` are different temporal samplings of the same trajectories, not two independent simulations.

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEArena** |
| Dataset paper | [Towards Multi-spatiotemporal-scale Generalized PDE Modeling](https://arxiv.org/abs/2209.15616) |
| Paper PDF | [arXiv PDF](https://arxiv.org/pdf/2209.15616) |
| Official repository | [pdearena/pdearena](https://github.com/pdearena/pdearena) |
| Hugging Face | [pdearena/ShallowWater-2D](https://huggingface.co/datasets/pdearena/ShallowWater-2D) |
| Data size | 124 GB (shared with vorticity view) |
| Solver | [SpeedyWeather.jl](https://github.com/SpeedyWeather/SpeedyWeather.jl) |
| License | MIT |
| Last checked | 2026-07-21 |

## Governing equation

The paper describes the model and fields but does not print a full spherical equation set. A standard vector form used for cataloguing is

\[
\frac{\partial h}{\partial t}+\nabla_s\cdot(h\mathbf{v})=0,
\]
\[
\frac{\partial\mathbf{v}}{\partial t}+(\mathbf{v}\cdot\nabla_s)\mathbf{v}+f_c\,\hat{\mathbf{r}}\times\mathbf{v}+g\nabla_s h=\mathcal{D}.
\]

## Variables and coordinates

- $h$ or $p$: free-surface / geopotential height / paper “pressure”;
- $u$: zonal wind; $v$: meridional wind;
- $(\lambda,\phi)$: lon/lat; output grid $192\times96$ ($\Delta x=1.875^\circ$, $\Delta y=3.75^\circ$), often stored as $[96,192]$.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 2 (sphere) |
| Time-dependent | yes |
| Grid | regular lat–lon output; spherical spectral solver |
| Spatial resolution | $192\times96$ |
| 2-day length | $T=11$ ($n_t=88$, `sample_rate=8`) |
| 1-day length | $T=21$ ($n_t=84$, `sample_rate=4`) |
| Trajectories | train 5,600 / valid 1,400 / test 1,400 (8,400 total) |
| Channels | 3: $p$ (or $h$), $u$, $v$ |
| Size | 124 GB |
| Format | NetCDF → released Zarr; ships `normstats.pt` |

## Initial conditions

`random2`: $\mathrm{offset}\sim\mathrm{Unif}\{80,\ldots,120\}$, $a_1\sim\mathrm{Unif}\{-20,\ldots,30\}$, $a_2,a_3\sim\mathrm{Unif}\{-20,\ldots,40\}$, plus grid-wise random $r$, fixed wave perturbation ($A=10^{-4}$, $m=6$, $\theta_0=45^\circ$, $\theta_w=10^\circ$), and spectral noise of amplitude $5\times10^{-6}$.

## Boundary conditions

Periodic in longitude; poles handled by the spherical spectral representation. The paper’s “regular grid with periodic BCs” should not be read as a flat torus with identical edge wrapping.

## Numerical generation

Modified SpeedyWeather.jl with `n_days=20`, `trunc=62`, `Δt_at_T85=40`, `initial_conditions=:random2`. Convert with `convertnc2zarr.py`; normalize via `compute_normalization.py`.

## Parameters

| Parameter | How it varies | Value |
|---|---|---|
| Seeds / `offset,$a_i,r$ | per trajectory | see IC ranges |
| Spectral perturbation | per trajectory | fixed amplitude |
| Wave perturbation | fixed | as above |
| Duration / truncation / grid | fixed | 20 days; `trunc=62`; $192\times96$ |
| 1-day vs 2-day sampling | task views | `sample_rate` 4 vs 8 |
| $g$, planet radius, Coriolis, dissipation | fixed (solver defaults) | not scanned |

## Released configurations

- Task views: `shallowwater2d_2day.yaml` / `shallowwater2d_1day.yaml` (2 history frames → 1 future).
- Full release: train 5,600 / valid 1,400 / test 1,400; 1-day/2-day and velocity/vorticity share one repo.
- Pressure/vorticity training uses the shipped normalization stats (`normstats.pt`).

## Data files

```
train/seed=*/
valid/seed=*/
test/seed=*/
normstats.pt
```

About 56 seeds per split. Velocity/vorticity and 1-day/2-day share this release. See [Data format](../00_data_format/).

## Data layout and machine-learning task

2-day typical sample:

\[
X\in\mathbb{R}^{2\times3\times96\times192}\to Y\in\mathbb{R}^{1\times3\times96\times192}.
\]

1-day keeps spatial/channel shape with denser temporal sampling.

## Download

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/ShallowWater-2D
```

## Regenerating from the official code

```bash
python scripts/generate_data.py base=pdedatagen/configs/shallowwater.yaml \
  experiment=shallowwater mode=train samples=100 seed=$SEED \
  dirname=pdearena_data/shallowwater
python scripts/convertnc2zarr.py "pdearena_data/shallowwater/$mode"
python scripts/compute_normalization.py --dataset shallowwater pdearena_data/shallowwater
```

## What is interesting and challenging about the data

Local weather structure and large-scale circulation coexist; longitude periodicity and polar geometry weaken flat-convolution assumptions; 1-day vs 2-day isolates timescale effects.

## Primary sources

- [PDEArena paper](https://arxiv.org/abs/2209.15616)
- [Shallow-water generator](https://github.com/pdearena/pdearena/tree/main/pdedatagen/shallowwater)
- [Hugging Face page](https://huggingface.co/datasets/pdearena/ShallowWater-2D)
