---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 05_reaction_diffusion_2d
spatial_dimension: 2
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: 2d_reacdiff
last_verified: 2026-07-21
title: "2D FitzHugh–Nagumo Diffusion–Reaction System"
linkTitle: "reaction diffusion 2d"
weight: 50
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "FitzHugh–Nagumo activator–inhibitor coupling for biological pattern formation."
description: "FitzHugh–Nagumo activator–inhibitor coupling for biological pattern formation."

---

# 2D FitzHugh–Nagumo Diffusion–Reaction System

The 2D diffusion–reaction system evolves two nonlinearly coupled fields—an activator and an inhibitor—with FitzHugh–Nagumo kinetics, motivated by biological pattern formation. Distinct diffusivities, two-channel coupling and no-flow boundaries make it a representative multichannel dynamical benchmark.

![2D Diffusion–Reaction time evolution](./2D-diffusion-reaction.png)

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEBench** |
| Dataset paper | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| Paper PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| Official repository | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| Dataset DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| Current download category | `2d_reacdiff` |
| Data size | 13 GB |
| Data-generation entry point | [gen_diff_react.py + configs/diff-react.yaml](https://github.com/pdebench/PDEBench/blob/main/pdebench/data_gen/gen_diff_react.py) |
| Last checked | 2026-07-21 |

## Governing equation

\[
\partial_tu=D_u(\partial_{xx}u+\partial_{yy}u)+R_u(u,v),\qquad
\partial_tv=D_v(\partial_{xx}v+\partial_{yy}v)+R_v(u,v),
\]
\[
R_u=u-u^3-k-v,\qquad R_v=u-v.
\]

## Variables and coordinates

**State variables**
- $u(t,x,y)$: activator.
- $v(t,x,y)$: inhibitor.

**Parameters and reaction terms**
- $D_u,D_v$: diffusivities of activator / inhibitor (release values $D_u=10^{-3}$, $D_v=5\times10^{-3}$).
- $R_u(u,v)=u-u^3-k-v$, $R_v(u,v)=u-v$: FitzHugh–Nagumo reaction functions.
- $k$: reaction parameter (release value $5\times10^{-3}$).

**Coordinates and domain**
- Space: uniform 2D Cartesian coordinates, $(x,y)\in(-1,1)^2$.
- Time: $t\in(0,5]$.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 2 |
| Time-dependent | yes |
| Grid | uniform 2D finite volume |
| Domain | $(x,y)\in(-1,1)^2$ |
| Time range | $t\in[0,5]$ |
| Spatial res. | train $128\times128$; raw $512\times512$ |
| Time steps | train 101; raw 501 |
| Trajectories / file | 1,000 |
| Channels | 2: $u$ (activator), $v$ (inhibitor) |
| Sample shape | $101\times128\times128\times2$ |
| Size | 13 GB |
| Format | HDF5 |

## Initial conditions

The paper explicitly states standard normal noise for the activator, $u(0,x,y)\sim\mathcal N(0,1)$. It does not give a separate complete sampling formula for the inhibitor in that paragraph, so users should inspect both HDF5 fields and the generator rather than infer it.

## Boundary conditions

No-flux Neumann boundaries: $D_u\partial_nu=0$ and $D_v\partial_nv=0$. The paper writes the corresponding zero $x$- and $y$-derivatives explicitly.

## Numerical generation

Finite-volume spatial discretization. The paper describes a fourth-order Runge–Kutta method, while current YAML metadata labels it RK45. Current configuration: `Du=1e-3, Dv=5e-3, k=5e-3, t=5, tdim=101, xdim=ydim=128`.

## Parameters

| Parameter | How it varies | Values |
|---|---|---|
| $D_u,D_v,k$ | fixed | $D_u=10^{-3}$, $D_v=5\times10^{-3}$, $k=5\times10^{-3}$; filename `NA_NA` |
| IC noise seed | per trajectory | activator $u(0)\sim\mathcal N(0,1)$ |
| BC, domain, grid, time | fixed | Neumann; $(-1,1)^2$; train $128^2$ |

## Released configurations

One main released file, `2D_diff-react_NA_NA.h5`, with 1,000 two-channel trajectories.

## Data files

The current official download manifest (`pdebench_data_urls.csv`) lists **1** files; paths are relative to the download root. See [Data format](../00_data_format/).

- `2D/diffusion-reaction/2D_diff-react_NA_NA.h5`

## Data layout and machine-learning task

Multichannel forecasting: $[u,v]_{t-\ell:t-1}\mapsto[u,v]_t$. The fields should not be treated as interchangeable image channels because they have different roles in the reaction terms.

- **Trajectory versus training example:** a complete HDF5 trajectory is not a fixed neural-network input. Autoregressive training normally extracts $\ell$ input frames and a one-step or multi-step target; $\ell$ is controlled by `initial_step` in the training configuration.
- **Source precedence:** equations, initial/boundary conditions and publication-scale statistics follow paper v7 and its supplement; current commands, paths and download categories follow the official GitHub `main` branch. Discrepancies are preserved rather than silently reconciled.

## Download

The current repository recommends `download_direct.py`; the EasyDataverse route is documented as slower and potentially error-prone.

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name 2d_reacdiff
```

Files may also be selected manually from the [DaRUS DOI page](https://doi.org/10.18419/darus-2986). After downloading, inspect the actual HDF5 `shape`, coordinate arrays, variable keys and YAML attributes. In particular, do not infer CFD or incompressible-NS resolution solely from a filename.

## Regenerating from the official code

```bash
cd PDEBench
python -m pdebench.data_gen.gen_diff_react
# Hydra configuration: pdebench/data_gen/configs/diff-react.yaml
```

Generator parameters can be changed through the corresponding Hydra YAML. This generation path writes HDF5 directly and does not require `Data_Merge.py`.

## What is interesting and challenging about the data

Nonlinear two-field coupling, unequal diffusion scales, pattern formation, high-frequency noise initialization, Neumann boundaries and downsampling error.

## Primary sources

- [PDEBench paper and supplementary material](https://arxiv.org/abs/2210.07182)
- [Official PDEBench repository](https://github.com/pdebench/PDEBench)
- [Official download instructions](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench dataset DOI](https://doi.org/10.18419/darus-2986)
