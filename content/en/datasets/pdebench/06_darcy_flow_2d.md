---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 06_darcy_flow_2d
spatial_dimension: 2
time_dependent: false
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: darcy
last_verified: 2026-07-21
title: "2D Darcy Flow"
linkTitle: "darcy flow 2d"
weight: 60
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "Steady Darcy map: coefficient field a(x)→solution u(x) with constant forcing β."
description: "Steady Darcy map: coefficient field a(x)→solution u(x) with constant forcing β."

---

# 2D Darcy Flow

Darcy Flow is a time-independent steady operator-learning task: map a spatially varying coefficient field $a(x)$ to the steady solution $u(x)$ under zero Dirichlet boundaries. A constant forcing $\beta$ rescales the solution, while coefficient-field realizations change its spatial structure.

![2D Darcy Flow (β = 1.0)](./2D-Darcy-Flow.png)

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEBench** |
| Dataset paper | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| Paper PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| Official repository | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| Dataset DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| Current download category | `darcy` |
| Data size | 6.2 GB |
| Data-generation entry point | [ReactionDiffusionEq/run_DarcyFlow2D.sh](https://github.com/pdebench/PDEBench/blob/main/pdebench/data_gen/data_gen_NLE/ReactionDiffusionEq/run_DarcyFlow2D.sh) |
| Last checked | 2026-07-21 |

## Governing equation

\[
-\nabla\!\cdot\!\bigl(a(\mathbf x)\nabla u(\mathbf x)\bigr)=f(\mathbf x),\qquad \mathbf x\in(0,1)^2,
\]
\[
u(\mathbf x)=0\quad\text{on }\partial(0,1)^2,\qquad f(\mathbf x)=\beta.
\]

## Variables and coordinates

**Field variables**
- $a(\mathbf{x})$: spatially varying diffusion / permeability coefficient (called a viscosity term in the paper); operator-task input.
- $u(\mathbf{x})$: steady-state solution; operator-task output.
- $f(\mathbf{x})$: forcing term; in the release set to the spatial constant $f=\beta$.

**Parameters**
- $\beta$: constant forcing that scales the solution.

**Coordinates and domain**
- Space: uniform 2D Cartesian coordinates, $\mathbf{x}\in(0,1)^2$.
- Time: the released task is a steady map with no time axis; generation may integrate a transient until steady state.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 2 |
| Time-dependent | no (steady) |
| Grid | uniform 2D Cartesian |
| Domain | $(0,1)^2$ |
| Time range | — |
| Spatial res. | $128\times128$ |
| Time steps | 1 (steady) |
| Samples / file | 10,000 |
| Channels | 2: input $a$, output $u$ |
| Sample shape | $128\times128\times2$ |
| Size | 6.2 GB |
| Format | HDF5 |

## Initial conditions

The coefficient field $a(x,y)$ varies across samples. To obtain the steady state, the generator integrates $\partial_tu-\nabla\cdot(a\nabla u)=f$ from a random transient initial field until convergence. That transient initial condition is not the final operator-learning input.

## Boundary conditions

Homogeneous Dirichlet boundary condition $u=0$.

## Numerical generation

The paper obtains the steady state by integrating a transient diffusion equation and states that the numerical treatment follows the diffusion part of the 1D diffusion–reaction solver. The generation script resides under `ReactionDiffusionEq`, followed by `Data_Merge.py` conversion to HDF5.

## Parameters

| Parameter | How it varies | Values |
|---|---|---|
| $\beta$ (constant force $f=\beta$) | differs across HDF5 files | $\beta\in\{0.01,0.1,1,10,100\}$ (5 files) |
| coefficient field $a(x,y)$ | per sample | spatially varying diffusivity realizations |
| BC, domain, resolution, steady setup | fixed | $u=0$ Dirichlet; $(0,1)^2$; $128^2$ |

## Released configurations

Five `2D_DarcyFlow_beta*_Train.hdf5` parameter files, each containing 10,000 coefficient-field/solution pairs.

## Data files

The current official download manifest (`pdebench_data_urls.csv`) lists **5** files; paths are relative to the download root. See [Data format](../00_data_format/).

- `2D/DarcyFlow/2D_DarcyFlow_beta0.01_Train.hdf5`
- `2D/DarcyFlow/2D_DarcyFlow_beta0.1_Train.hdf5`
- `2D/DarcyFlow/2D_DarcyFlow_beta1.0_Train.hdf5`
- `2D/DarcyFlow/2D_DarcyFlow_beta10.0_Train.hdf5`
- `2D/DarcyFlow/2D_DarcyFlow_beta100.0_Train.hdf5`

## Data layout and machine-learning task

Static operator task $a(x,y)\mapsto u(x,y)$. It should not be described as two channels co-evolving in time. $\beta$ may be supplied as an additional scalar condition.

- **Trajectory versus training example:** a complete HDF5 trajectory is not a fixed neural-network input. Autoregressive training normally extracts $\ell$ input frames and a one-step or multi-step target; $\ell$ is controlled by `initial_step` in the training configuration.
- **Source precedence:** equations, initial/boundary conditions and publication-scale statistics follow paper v7 and its supplement; current commands, paths and download categories follow the official GitHub `main` branch. Discrepancies are preserved rather than silently reconciled.

## Download

The current repository recommends `download_direct.py`; the EasyDataverse route is documented as slower and potentially error-prone.

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name darcy
```

Files may also be selected manually from the [DaRUS DOI page](https://doi.org/10.18419/darus-2986). After downloading, inspect the actual HDF5 `shape`, coordinate arrays, variable keys and YAML attributes. In particular, do not infer CFD or incompressible-NS resolution solely from a filename.

## Regenerating from the official code

```bash
cd PDEBench
bash pdebench/data_gen/data_gen_NLE/ReactionDiffusionEq/run_DarcyFlow2D.sh
# set type: ReacDiff and dim: 2 in data_gen_NLE/config/config.yaml
python pdebench/data_gen/data_gen_NLE/Data_Merge.py
```

Generator parameters can be changed through the corresponding Hydra YAML. NLE generators first write `.npy` arrays; run `Data_Merge.py` to obtain the HDF5 layout used by the official dataloaders.

## What is interesting and challenging about the data

Spatially heterogeneous coefficients, global elliptic dependence, forcing-scale variation and the distinction between operator mapping and state time stepping.

## Primary sources

- [PDEBench paper and supplementary material](https://arxiv.org/abs/2210.07182)
- [Official PDEBench repository](https://github.com/pdebench/PDEBench)
- [Official download instructions](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench dataset DOI](https://doi.org/10.18419/darus-2986)
