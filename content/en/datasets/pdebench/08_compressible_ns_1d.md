---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 08_compressible_ns_1d
spatial_dimension: 1
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: 1d_cfd
last_verified: 2026-07-21
title: "1D Compressible Navier–Stokes / CFD"
linkTitle: "compressible ns 1d"
weight: 80
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "1D compressible conservation laws; random-field and shock-tube setups."
description: "1D compressible conservation laws; random-field and shock-tube setups."

---

# 1D Compressible Navier–Stokes / CFD

Compressible Navier–Stokes describes a conservation-law system coupling density, velocity and pressure, supporting acoustic waves, contacts, shocks and rarefactions. The 1D configurations span smooth random fields to Riemann shock tubes by varying viscosity, initial-condition family and boundary type.

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEBench** |
| Dataset paper | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| Paper PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| Official repository | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| Dataset DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| Current download category | `1d_cfd` |
| Data size | 88 GB |
| Data-generation entry point | [data_gen_NLE/CompressibleFluid](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_gen/data_gen_NLE/CompressibleFluid) |
| Last checked | 2026-07-21 |

## Governing equation

\[
\partial_t\rho+\nabla\cdot(\rho\mathbf v)=0,
\]
\[
\rho(\partial_t\mathbf v+\mathbf v\cdot\nabla\mathbf v)
=-\nabla p+\eta\Delta\mathbf v+\left(\zeta+\frac{\eta}{3}\right)\nabla(\nabla\cdot\mathbf v),
\]
\[
\partial_t\!\left(\epsilon+\frac{\rho|\mathbf v|^2}{2}\right)
+\nabla\cdot\!\left[\left(\epsilon+p+\frac{\rho|\mathbf v|^2}{2}\right)\mathbf v-\mathbf v\cdot\boldsymbol\sigma'\right]=0,
\qquad \epsilon=\frac{p}{\Gamma-1},\quad \Gamma=\frac53.
\]

## Variables and coordinates

**State variables**
- $\rho$: mass density.
- $p$: gas pressure.
- $\mathbf{v}$ (1D: $v_x$): velocity.
- $\epsilon=p/(\Gamma-1)$: internal energy (equation-of-state derived; usually not a separate released channel).

**Parameters and auxiliaries**
- $N_d=1$: number of spatial dimensions.
- $\Gamma=5/3$: heat-capacity ratio.
- $\eta,\zeta$: shear and bulk viscosities.
- $\boldsymbol{\sigma}'$: viscous stress tensor.
- Mach number $M=|\mathbf{v}|/c_s$ with sound speed $c_s=\sqrt{\Gamma p/\rho}$ (1D training configs typically do not sweep $M$).

**Coordinates and domain**
- Space: uniform 1D Cartesian grid; read domain / coordinates from HDF5 or generation YAML (paper does not give one domain for all CFD files).
- Time: typically 100 stored frames; physical time from coordinates / attributes.
- Logical channel order: $[\rho,p,v_x]$ (often stored as separate HDF5 datasets).

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 1 |
| Time-dependent | yes |
| Grid | uniform 1D Cartesian |
| Domain | from HDF5 coords |
| Time range | from coordinate array |
| Spatial res. | 1024 |
| Time steps | 100 |
| Trajectories / file | 10,000 |
| Channels | 3: $\rho$, $p$, $v_x$ |
| Sample shape | $100\times1024\times3$ |
| Size | 88 GB |
| Format | HDF5 |

## Initial conditions

PDEBench uses three initial-condition families for compressible NS.

### 1. Random field

A randomized sinusoidal superposition (paper Eq. 8), extended to this spatial setting. Density and pressure are prepared by adding a uniform background to a perturbation field.

### 2. Turbulence

Mass density and pressure are taken as uniform. The initial velocity is (paper Eq. 17)
\[
\mathbf{v}(x,t=0)=\sum_{i=1}^{n}\mathbf{A}_i\sin(k_i x+\phi_i),
\]
with $n=4$ and amplitude $A_i=\bar{v}/|k_i|^d$. The mean velocity $\bar{v}$ is set by the initial Mach number via $\bar{v}=c_s M$, where $c_s=\sqrt{\Gamma p/\rho}$. A Helmholtz decomposition in Fourier space then subtracts the compressible component from this velocity field. The 1D main training list emphasizes random / shock-tube cases; the turbulence family is more common in higher dimensions.

### 3. Shock tube / Riemann

The shock-tube initial field is
\[
Q(x,t=0)=(Q_L,Q_R),\qquad Q=(\rho,v,p),
\]
where the left/right constant states $Q_L,Q_R$ and the discontinuity location are randomized. This Riemann problem generates shocks and rarefaction waves and is a rigorous test for ML models.

## Boundary conditions

Training configurations use **periodic** or **outgoing** boundaries (often labeled `trans` in scripts/files).

- **Periodic:** used by most random training configurations.
- **Outgoing:** neighboring interior cells are copied into boundary ghost regions so waves and fluid can leave the domain (also common in astrohydrodynamics); shock-tube configurations use outgoing boundaries.

## Numerical generation

The inviscid part of the conservation laws is advanced with a temporally and spatially second-order **HLLC** Riemann scheme with **MUSCL** reconstruction; viscous terms use centered differences. Logical state channels are $\rho$, $p$, and velocity; internal energy follows from $\epsilon=p/(\Gamma-1)$.

## Parameters

Equation:

\[
\partial_t\rho+\nabla\cdot(\rho\mathbf v)=0,
\]
\[
\rho(\partial_t\mathbf v+\mathbf v\cdot\nabla\mathbf v)
=-\nabla p+\eta\Delta\mathbf v+\left(\zeta+\frac{\eta}{3}\right)\nabla(\nabla\cdot\mathbf v),
\]
\[
\partial_t\!\left(\epsilon+\frac{\rho|\mathbf v|^2}{2}\right)
+\nabla\cdot\!\left[\left(\epsilon+p+\frac{\rho|\mathbf v|^2}{2}\right)\mathbf v-\mathbf v\cdot\boldsymbol\sigma'\right]=0,
\qquad \epsilon=\frac{p}{\Gamma-1},\quad \Gamma=\frac53.
\]

### Released file configs

The first five rows are the main training sweep. `Sod*` are **extra classic shock-tube tests** (not the random training IC family), but they **do have parameters**: YAML sets `init_mode=shocktube1…7`, `bc=trans`, $(\eta,\zeta)=(10^{-8},10^{-8})$, $\Gamma=5/3$. 1D main training does not sweep Mach, so $M$ is —.

> **What “extra test set” means:** fixed classic cases outside the main training distribution (random field / random Riemann), used for generalization checks — often called OOD (out-of-distribution) in the literature. It does **not** mean “no parameters”.

| Data file | initial field | boundary | $(\eta,\zeta,M)$ | Per trajectory | Note |
|---|---|---|---|---|---|
| `1D_CFD_Rand_Eta1.e-8_Zeta1.e-8_periodic_Train.hdf5` | random field | periodic | $(10^{-8},10^{-8},\text{—})$ | random-field realization | main train |
| `1D_CFD_Rand_Eta0.01_Zeta0.01_periodic_Train.hdf5` | random field | periodic | $(10^{-2},10^{-2},\text{—})$ | same | main train |
| `1D_CFD_Rand_Eta0.1_Zeta0.1_periodic_Train.hdf5` | random field | periodic | $(10^{-1},10^{-1},\text{—})$ | same | main train |
| `1D_CFD_Rand_Eta1.e-8_Zeta1.e-8_trans_Train.hdf5` | random field | outgoing (`trans`) | $(10^{-8},10^{-8},\text{—})$ | same | main train |
| `1D_CFD_Shock_Eta1.e-8_Zeta1.e-8_trans_Train.hdf5` | shock-tube (random Riemann) | outgoing (`trans`) | $(10^{-8},10^{-8},\text{—})$ | random L/R states & discontinuity | main train |
| `Sod1.hdf5` | `shocktube1` (fixed classic) | outgoing | $(10^{-8},10^{-8},\text{—})$ | no (fixed IC) | extra test |
| `Sod2.hdf5` | `shocktube2` | outgoing | $(10^{-8},10^{-8},\text{—})$ | no | extra test |
| `Sod3.hdf5` | `shocktube3` | outgoing | $(10^{-8},10^{-8},\text{—})$ | no | extra test |
| `Sod4.hdf5` | `shocktube4` | outgoing | $(10^{-8},10^{-8},\text{—})$ | no | extra test |
| `Sod5.hdf5` | `shocktube5` | outgoing | $(10^{-8},10^{-8},\text{—})$ | no | extra test |
| `Sod6.hdf5` | `shocktube6` | outgoing | $(10^{-8},10^{-8},\text{—})$ | no | extra test (listed under Train/ShockTube) |
| `Sod7.hdf5` | `shocktube7` | outgoing | $(10^{-8},10^{-8},\text{—})$ | no | extra test |

Exact Sod L/R states follow the matching YAML / HDF5 attributes (`fin_time` may also differ).

### Generator-tunable ranges

| Parameter | Tunable range / options | Covered by release? |
|---|---|---|
| $\eta,\zeta$ (usually $\eta=\zeta$) | any nonnegative; common $\{10^{-8},10^{-2},10^{-1}\}$ | main train covers these three |
| boundary | `periodic` / `trans` (outgoing), … | yes |
| IC family | random / random shock-tube / `shocktube1…7`, … | yes |
| Mach $M$ | YAML has `M0`; 1D main train usually does not sweep it | not swept in 1D main train |
| $\Gamma$, grid, CFL, time window | editable | mostly fixed in release |

## Data files

The current official download manifest (`pdebench_data_urls.csv`) lists **12** files; paths are relative to the download root. See [Data format](../00_data_format/).

- `1D/CFD/Train/1D_CFD_Rand_Eta0.01_Zeta0.01_periodic_Train.hdf5`
- `1D/CFD/Train/1D_CFD_Rand_Eta0.1_Zeta0.1_periodic_Train.hdf5`
- `1D/CFD/Train/1D_CFD_Rand_Eta1.e-8_Zeta1.e-8_periodic_Train.hdf5`
- `1D/CFD/Train/1D_CFD_Rand_Eta1.e-8_Zeta1.e-8_trans_Train.hdf5`
- `1D/CFD/Train/1D_CFD_Shock_Eta1.e-8_Zeta1.e-8_trans_Train.hdf5`
- `1D/CFD/Train/ShockTube/Sod6.hdf5`
- `1D/CFD/Test/ShockTube/Sod1.hdf5`
- `1D/CFD/Test/ShockTube/Sod2.hdf5`
- `1D/CFD/Test/ShockTube/Sod3.hdf5`
- `1D/CFD/Test/ShockTube/Sod4.hdf5`
- `1D/CFD/Test/ShockTube/Sod5.hdf5`
- `1D/CFD/Test/ShockTube/Sod7.hdf5`

## Data layout and machine-learning task

Multiphysics trajectory forecasting. Align separate HDF5 arrays into $[\rho,p,v_x]$ and optionally condition on $(\eta,\zeta)$, boundary type and IC family.

- **Trajectory versus training example:** a complete HDF5 trajectory is not a fixed neural-network input. Autoregressive training normally extracts $\ell$ input frames and a one-step or multi-step target; $\ell$ is controlled by `initial_step` in the training configuration.
- **Source precedence:** equations, initial/boundary conditions and publication-scale statistics follow paper v7 and its supplement; current commands, paths and download categories follow the official GitHub `main` branch. Discrepancies are preserved rather than silently reconciled.

## Download

The current repository recommends `download_direct.py`; the EasyDataverse route is documented as slower and potentially error-prone.

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name 1d_cfd
```

Files may also be selected manually from the [DaRUS DOI page](https://doi.org/10.18419/darus-2986). After downloading, inspect the actual HDF5 `shape`, coordinate arrays, variable keys and YAML attributes. In particular, do not infer CFD or incompressible-NS resolution solely from a filename.

## Regenerating from the official code

```bash
cd PDEBench/pdebench/data_gen/data_gen_NLE/CompressibleFluid
# main random-field configurations
bash run_trainset_1D.sh
# outgoing and shock-tube variants
bash run_trainset_1D_trans.sh
bash run_trainset_1DShock.sh
cd ..
python Data_Merge.py
```

Generator parameters can be changed through the corresponding Hydra YAML. NLE generators first write `.npy` arrays; run `Data_Merge.py` to obtain the HDF5 layout used by the official dataloaders.

## What is interesting and challenging about the data

Coupled conservation laws, strong discontinuities, changing boundary type, viscosities spanning orders of magnitude and different channel scales/units.

## Primary sources

- [PDEBench paper and supplementary material](https://arxiv.org/abs/2210.07182)
- [Official PDEBench repository](https://github.com/pdebench/PDEBench)
- [Official download instructions](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench dataset DOI](https://doi.org/10.18419/darus-2986)
