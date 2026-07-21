---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 07_shallow_water_2d
spatial_dimension: 2
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: swe
last_verified: 2026-07-21
title: "2D Shallow-Water Equations: Radial Dam Break"
linkTitle: "shallow water 2d"
weight: 70
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "2D shallow-water free-surface flow; radial dam break with random radius."
description: "2D shallow-water free-surface flow; radial dam break with random radius."

---

# 2D Shallow-Water Equations: Radial Dam Break

The shallow-water equations, derived from Navier–Stokes, model free-surface flow: in 2D they conserve depth and two momentum components and remain valid across shocks. PDEBench uses a radial dam-break scenario as a representative setting for gravity-driven surface-wave propagation.

![2D Shallow-Water Equations time evolution](./2D-SWE.png)

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEBench** |
| Dataset paper | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| Paper PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| Official repository | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| Dataset DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| Current download category | `swe` |
| Data size | 6.2 GB |
| Data-generation entry point | [gen_radial_dam_break.py + radial_dam_break.yaml](https://github.com/pdebench/PDEBench/blob/main/pdebench/data_gen/gen_radial_dam_break.py) |
| Last checked | 2026-07-21 |

## Governing equation

\[
\partial_th+\partial_x(hu)+\partial_y(hv)=0,
\]
\[
\partial_t(hu)+\partial_x\!\left(u^2h+\tfrac12g_rh^2\right)+\partial_y(uvh)=-g_rh\,\partial_xb,
\]
\[
\partial_t(hv)+\partial_y\!\left(v^2h+\tfrac12g_rh^2\right)+\partial_x(uvh)=-g_rh\,\partial_yb.
\]

## Variables and coordinates

**State variables**
- $h(t,x,y)$: water depth.
- $u(t,x,y),\,v(t,x,y)$: horizontal and vertical velocities.
- $hu,\,hv$: directional momentum components.

**Geometry and parameters**
- $b(x,y)$: bathymetry.
- $g_r$: gravitational acceleration.

**Coordinates and domain**
- Space: uniform 2D Cartesian finite-volume grid, $\Omega=[-2.5,2.5]^2$.
- Time: released trajectories commonly use $t\in[0,1]$.
- The published benchmark often stores / scores only $h$; the full conserved state includes $h,hu,hv$.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 2 |
| Time-dependent | yes |
| Grid | uniform 2D finite volume |
| Domain | $[-2.5,2.5]^2$ |
| Time range | $[0,1]$ |
| Spatial res. | $128\times128$ |
| Time steps | 101 |
| Trajectories / file | 1,000 |
| Channels | 1: $h$ (water depth) |
| Sample shape | $101\times128\times128\times1$ |
| Size | 6.2 GB |
| Format | HDF5 |

## Initial conditions

Radial dam-break initial condition
\[
h(0,x,y)=\begin{cases}2,&\sqrt{x^2+y^2}<r,\\1,&\sqrt{x^2+y^2}\ge r,\end{cases}
\qquad r\sim\mathcal U(0.3,0.7).
\]
The center and inner/outer heights are fixed in the release; radius and seed vary by trajectory.

## Boundary conditions

The paper main text summarizes this dataset as using Neumann boundaries; the complete boundary implementation of the PyClaw scenario should be taken from the generator.

## Numerical generation

PyClaw finite-volume solver. Current YAML: `T_end=1.0, n_time_steps=100, xdim=ydim=128, gravity=1.0, inner_height=2.0, domain=[-2.5,2.5]^2`; the script samples `dam_radius ~ U(0.3,0.7)` for each seed.

## Parameters

| Parameter | How it varies | Values |
|---|---|---|
| dam-break radius $r$ | per trajectory (only varying physical quantity in release) | $r\sim\mathcal U(0.3,0.7)$; filename `NA_NA` |
| dam center | fixed | domain center |
| inner / outer water height | fixed | inner $h=2$, outer $h=1$ |
| gravity $g_r$, bathymetry $b$ | fixed | $g_r=1.0$; $b$ fixed |
| BC, domain, grid, time | fixed | Neumann; $[-2.5,2.5]^2$; $128^2$; $t\in[0,1]$ |

## Released configurations

Released file `2D_rdb_NA_NA.h5` with 1,000 trajectories. The generator default cap may be larger — do not confuse it with the released size.

## Data files

The current official download manifest (`pdebench_data_urls.csv`) lists **1** files; paths are relative to the download root. See [Data format](../00_data_format/).

- `2D/shallow-water/2D_rdb_NA_NA.h5`

## Data layout and machine-learning task

The released task is single-channel depth forecasting. A regenerated $(h,hu,hv)$ version must be labeled as a custom three-channel dataset rather than conflated with the published file.

- **Trajectory versus training example:** a complete HDF5 trajectory is not a fixed neural-network input. Autoregressive training normally extracts $\ell$ input frames and a one-step or multi-step target; $\ell$ is controlled by `initial_step` in the training configuration.
- **Source precedence:** equations, initial/boundary conditions and publication-scale statistics follow paper v7 and its supplement; current commands, paths and download categories follow the official GitHub `main` branch. Discrepancies are preserved rather than silently reconciled.

## Download

The current repository recommends `download_direct.py`; the EasyDataverse route is documented as slower and potentially error-prone.

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name swe
```

Files may also be selected manually from the [DaRUS DOI page](https://doi.org/10.18419/darus-2986). After downloading, inspect the actual HDF5 `shape`, coordinate arrays, variable keys and YAML attributes. In particular, do not infer CFD or incompressible-NS resolution solely from a filename.

## Regenerating from the official code

```bash
cd PDEBench
python -m pdebench.data_gen.gen_radial_dam_break
# Hydra configuration: pdebench/data_gen/configs/radial_dam_break.yaml
```

Generator parameters can be changed through the corresponding Hydra YAML. This generation path writes HDF5 directly and does not require `Data_Merge.py`.

## What is interesting and challenging about the data

Discontinuous initial depth, expanding ring waves, conservation, nonperiodic boundaries and the information gap between the full physical state and the released single-channel observation.

## Primary sources

- [PDEBench paper and supplementary material](https://arxiv.org/abs/2210.07182)
- [Official PDEBench repository](https://github.com/pdebench/PDEBench)
- [Official download instructions](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench dataset DOI](https://doi.org/10.18419/darus-2986)
