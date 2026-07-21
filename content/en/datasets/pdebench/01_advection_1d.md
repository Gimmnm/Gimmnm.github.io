---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 01_advection_1d
spatial_dimension: 1
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: advection
last_verified: 2026-07-21
title: "1D Linear Advection Equation"
linkTitle: "advection 1d"
weight: 10
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "Pure advection without nonlinearity; exact solution is a constant-speed shift of the initial profile."
description: "Pure advection without nonlinearity; exact solution is a constant-speed shift of the initial profile."

---

# 1D Linear Advection Equation

The advection equation models pure advection without nonlinearity: a scalar field translates at constant speed $\beta$, and the exact solution is a shift of the initial profile, $u(t,x)=u_0(x-\beta t)$. It isolates translation, phase preservation and parameter conditioning from diffusion and nonlinear effects.

![1D Advection (β = 0.4)](./1D-Advection.png)

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEBench** |
| Dataset paper | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| Paper PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| Official repository | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| Dataset DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| Current download category | `advection` |
| Data size | 47 GB |
| Data-generation entry point | [data_gen_NLE/AdvectionEq](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_gen/data_gen_NLE/AdvectionEq) |
| Last checked | 2026-07-21 |

## Governing equation

\[
\partial_t u(t,x)+\beta\,\partial_x u(t,x)=0,\qquad x\in(0,1),\quad t\in(0,2],
\]
\[
u(0,x)=u_0(x),\qquad u(t,x)=u_0(x-\beta t).
\]

## Variables and coordinates

**State variables**
- $u(t,x)$: transported scalar field.

**Parameters**
- $\beta$: constant advection speed.

**Coordinates and domain**
- Space: uniform 1D Cartesian coordinate $x\in(0,1)$, domain length $L_x=1$.
- Time: $t\in(0,2]$ (closed interval $[0,2]$ when including the initial state).
- Exact solution: $u(t,x)=u_0(x-\beta t)$.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 1 |
| Time-dependent | yes |
| Grid | uniform 1D Cartesian |
| Domain | $x\in(0,1)$ |
| Time range | $t\in[0,2]$ |
| Spatial res. | $N_x=1024$ |
| Time steps | 201 |
| Trajectories / file | 10,000 |
| Channels | 1: $u$ |
| Sample shape | $201\times1024\times1$ |
| Size | 47 GB |
| Format | HDF5 |

## Initial conditions

The initial condition is a random sinusoidal superposition
\[
u_0(x)=\sum_{i=1}^{N}A_i\sin(k_i x+\phi_i),\qquad k_i=2\pi n_i/L_x.
\]
Integers $n_i$ are drawn from $[1,n_{\max}]$. For 1D-advection the paper sets $N=2$, $n_{\max}=8$ (written as $k_{\max}=8$), $A_i\sim\mathcal U(0,1)$, and $\phi_i\in(0,2\pi)$. After that, an absolute-value transform with random sign and a window function are each applied with 10% probability.

## Boundary conditions

Periodic boundary conditions.

## Numerical generation

A second-order upwind finite-difference scheme is used in space and time.

## Parameters

Equation:

\[
\partial_t u(t,x)+\beta\,\partial_x u(t,x)=0,\qquad x\in(0,1),\quad t\in(0,2],
\]
\[
u(0,x)=u_0(x),\qquad u(t,x)=u_0(x-\beta t).
\]

### Released file configs

One row per official download file. Paper Table 1 lists $N_t=200$; released HDF5 has **201** steps including $t=0$.

| Data file | $\beta$ | Boundary | Per trajectory | Fixed |
|---|---:|---|---|---|
| `1D_Advection_Sols_beta0.1.hdf5` | $0.1$ | periodic | IC $n_i,A_i,\phi_i$; abs / window ~10% each | $N_x=1024$, $N_t=201$, domain $(0,1)\times[0,2]$ |
| `1D_Advection_Sols_beta0.2.hdf5` | $0.2$ | periodic | same | same |
| `1D_Advection_Sols_beta0.4.hdf5` | $0.4$ | periodic | same | same |
| `1D_Advection_Sols_beta0.7.hdf5` | $0.7$ | periodic | same | same |
| `1D_Advection_Sols_beta1.0.hdf5` | $1.0$ | periodic | same | same |
| `1D_Advection_Sols_beta2.0.hdf5` | $2.0$ | periodic | same | same |
| `1D_Advection_Sols_beta4.0.hdf5` | $4.0$ | periodic | same | same |
| `1D_Advection_Sols_beta7.0.hdf5` | $7.0$ | periodic | same | same |

10,000 trajectories per file; default IC family $N=2$, $n_{\max}=8$, $A_i\sim\mathcal U(0,1)$, $\phi_i\in(0,2\pi)$.

### Generator-tunable ranges

Parameters the Hydra YAML / generator **can** change (even if the download does not sweep them). Re-generate after editing YAML.

| Parameter | Tunable range / options | Covered by release? |
|---|---|---|
| $\beta$ (advection speed) | any positive scalar in YAML; repo also has example `beta=10` | yes: $\{0.1,0.2,0.4,0.7,1,2,4,7\}$ |
| IC $N,n_{\max},A_i,\phi_i$ | editable in scripts/config | no (defaults; only seed varies) |
| abs / window probability | editable | no (~10% defaults) |
| BC, domain, grid, time | editable | release fixed: periodic / $(0,1)$ / $1024$ / $[0,2]$ |

## Data files

The current official download manifest (`pdebench_data_urls.csv`) lists **8** files; paths are relative to the download root. See [Data format](../00_data_format/).

- `1D/Advection/Train/1D_Advection_Sols_beta0.1.hdf5`
- `1D/Advection/Train/1D_Advection_Sols_beta0.2.hdf5`
- `1D/Advection/Train/1D_Advection_Sols_beta0.4.hdf5`
- `1D/Advection/Train/1D_Advection_Sols_beta0.7.hdf5`
- `1D/Advection/Train/1D_Advection_Sols_beta1.0.hdf5`
- `1D/Advection/Train/1D_Advection_Sols_beta2.0.hdf5`
- `1D/Advection/Train/1D_Advection_Sols_beta4.0.hdf5`
- `1D/Advection/Train/1D_Advection_Sols_beta7.0.hdf5`

## Data layout and machine-learning task

The full sample is a scalar trajectory. A typical dynamics task is $u_{t-\ell:t-1}\mapsto u_t$ or a multi-step rollout; $\beta$ can be supplied explicitly for cross-parameter training.

- **Trajectory versus training example:** a complete HDF5 trajectory is not a fixed neural-network input. Autoregressive training normally extracts $\ell$ input frames and a one-step or multi-step target; $\ell$ is controlled by `initial_step` in the training configuration.
- **Source precedence:** equations, initial/boundary conditions and publication-scale statistics follow paper v7 and its supplement; current commands, paths and download categories follow the official GitHub `main` branch. Discrepancies are preserved rather than silently reconciled.

## Download

The current repository recommends `download_direct.py`; the EasyDataverse route is documented as slower and potentially error-prone.

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name advection
```

Files may also be selected manually from the [DaRUS DOI page](https://doi.org/10.18419/darus-2986). After downloading, inspect the actual HDF5 `shape`, coordinate arrays, variable keys and YAML attributes. In particular, do not infer CFD or incompressible-NS resolution solely from a filename.

## Regenerating from the official code

```bash
cd PDEBench/pdebench/data_gen/data_gen_NLE/AdvectionEq
CUDA_VISIBLE_DEVICES=0 python3 advection_multi_solution_Hydra.py +multi=beta1e0.yaml
# all configured training parameters
bash run_trainset.sh
cd ..
python Data_Merge.py
```

Generator parameters can be changed through the corresponding Hydra YAML. NLE generators first write `.npy` arrays; run `Data_Merge.py` to obtain the HDF5 layout used by the official dataloaders.

## What is interesting and challenging about the data

Phase error accumulates during long rollouts. Changing the speed changes the per-step shift directly, making this dataset useful for parameter conditioning, temporal extrapolation and spectral/phase preservation.

## Primary sources

- [PDEBench paper and supplementary material](https://arxiv.org/abs/2210.07182)
- [Official PDEBench repository](https://github.com/pdebench/PDEBench)
- [Official download instructions](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench dataset DOI](https://doi.org/10.18419/darus-2986)
