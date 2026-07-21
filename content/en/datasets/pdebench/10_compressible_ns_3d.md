---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 10_compressible_ns_3d
spatial_dimension: 3
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: 3d_cfd
last_verified: 2026-07-21
title: "3D Compressible Navier–Stokes / CFD"
linkTitle: "compressible ns 3d"
weight: 100
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "3D compressible flow; high-dimensional, large, sample-scarce."
description: "3D compressible flow; high-dimensional, large, sample-scarce."

---

# 3D Compressible Navier–Stokes / CFD

3D compressible Navier–Stokes lifts the same conservation-law system onto a high-dimensional grid. Per-trajectory volume is large and samples are relatively few, stressing high-dimensional memory and sample-efficient modeling.

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEBench** |
| Dataset paper | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| Paper PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| Official repository | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| Dataset DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| Current download category | `3d_cfd` |
| Data size | 285 GB |
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
- $\mathbf{v}=(v_x,v_y,v_z)$: 3D velocity.
- $\epsilon=p/(\Gamma-1)$: internal energy (equation-of-state derived).

**Parameters and auxiliaries**
- $N_d=3$: number of spatial dimensions.
- $\Gamma=5/3$: heat-capacity ratio.
- $\eta,\zeta$: shear and bulk viscosities.
- $\boldsymbol{\sigma}'$: viscous stress tensor.
- Mach number $M=|\mathbf{v}|/c_s$ with sound speed $c_s=\sqrt{\Gamma p/\rho}$.

**Coordinates and domain**
- Space: uniform 3D Cartesian periodic grid; read coordinates from HDF5 / YAML.
- Time: typically 21 stored frames.
- Logical channel order: $[\rho,p,v_x,v_y,v_z]$.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 3 |
| Time-dependent | yes |
| Grid | uniform 3D periodic Cartesian |
| Domain | from HDF5 coords |
| Time range | 21 stored times |
| Spatial res. | $128\times128\times128$ |
| Time steps | 21 |
| Trajectories / file | 100 |
| Channels | 5: $\rho$, $p$, $v_x$, $v_y$, $v_z$ |
| Sample shape | $21\times128^3\times5$ |
| Size | 285 GB |
| Format | HDF5 |

## Initial conditions

PDEBench uses three initial-condition families for compressible NS.

### 1. Random field

The 1D randomized sinusoidal superposition (paper Eq. 8) is extended to 3D as multidimensional sinusoidal random fields. Density and pressure are prepared by adding a uniform background to a perturbation field.

### 2. Turbulence

Mass density and pressure are taken as uniform. The initial velocity is (paper Eq. 17)
\[
\mathbf{v}(\mathbf{x},t=0)=\sum_{i=1}^{n}\mathbf{A}_i\sin(k_i x+\phi_i),
\]
with $n=4$ and amplitude $A_i=\bar{v}/|k_i|^d$, where $d=2$ in 3D. The mean velocity $\bar{v}$ is set by the initial Mach number via $\bar{v}=c_s M$, where $c_s=\sqrt{\Gamma p/\rho}$. A Helmholtz decomposition in Fourier space then subtracts the compressible component from this velocity field.

### 3. Shock tube / Riemann

The shock-tube initial field is
\[
Q(\mathbf{x},t=0)=(Q_L,Q_R),\qquad Q=(\rho,\mathbf{v},p),
\]
where the left/right constant states $Q_L,Q_R$ and the discontinuity location are randomized. This Riemann problem generates shocks and rarefactions; the 3D main training convention emphasizes random / turbulence, while BlastWave cases are often extra test files.

## Boundary conditions

- **Periodic:** main training configurations use periodic boundaries.
- **Outgoing:** neighboring interior cells are copied into boundary ghost regions so waves and fluid can leave the domain; additional test files may use other boundary setups.

## Numerical generation

The inviscid part of the conservation laws is advanced with a temporally and spatially second-order **HLLC** Riemann scheme with **MUSCL** reconstruction; viscous terms use centered differences. Logical state channels are $\rho$, $p$, and velocity components; internal energy follows from $\epsilon=p/(\Gamma-1)$.

## Parameters

| Parameter | How it varies | Values |
|---|---|---|
| IC family / $M$ / $(\eta,\zeta)$ | differs across HDF5 config files (2 main) | common reading: (1) random, $M=1$, near-inviscid; (2) turbulence, $M=1$, near-inviscid — trust filenames + HDF5 attributes |
| field realization | per trajectory | seed |
| $\Gamma$, grid, scheme | fixed | $\Gamma=5/3$; $128^3$; 21 frames |

## Released configurations

The released main set is typically two configurations with 100 trajectories each: inviscid random and inviscid turbulence; extra test files are not part of these 200.

## Data files

The current official download manifest (`pdebench_data_urls.csv`) lists **8** files; paths are relative to the download root. See [Data format](../00_data_format/).

- `3D/Train/3D_CFD_Rand_M1.0_Eta1e-08_Zeta1e-08_periodic_Train.hdf5`
- `3D/Train/3D_CFD_Turb_M1.0_Eta1e-08_Zeta1e-08_periodic_Train.hdf5`
- `3D/Test/BlastWave/BlastWave.hdf5`
- `3D/Test/Turbulence/Turb_M01.hdf5`
- `3D/Test/Turbulence/Turb_M1.hdf5`
- `3D/Test/Turbulence/Turb_M2.hdf5`
- `3D/Test/Turbulence/Turb_M4.hdf5`
- `3D/Test/Turbulence/Turb_M05.hdf5`

## Data layout and machine-learning task

Five-channel 3D temporal forecasting. A single trajectory contains roughly $2.20\times10^8$ scalar values, typically requiring spatial/temporal reduction, patching, sharded I/O or distributed training.

- **Trajectory versus training example:** a complete HDF5 trajectory is not a fixed neural-network input. Autoregressive training normally extracts $\ell$ input frames and a one-step or multi-step target; $\ell$ is controlled by `initial_step` in the training configuration.
- **Source precedence:** equations, initial/boundary conditions and publication-scale statistics follow paper v7 and its supplement; current commands, paths and download categories follow the official GitHub `main` branch. Discrepancies are preserved rather than silently reconciled.

## Download

The current repository recommends `download_direct.py`; the EasyDataverse route is documented as slower and potentially error-prone.

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name 3d_cfd
```

Files may also be selected manually from the [DaRUS DOI page](https://doi.org/10.18419/darus-2986). After downloading, inspect the actual HDF5 `shape`, coordinate arrays, variable keys and YAML attributes. In particular, do not infer CFD or incompressible-NS resolution solely from a filename.

## Regenerating from the official code

```bash
cd PDEBench/pdebench/data_gen/data_gen_NLE/CompressibleFluid
bash run_trainset_3D.sh
bash run_trainset_3DTurb.sh
# optional 3D turbulence tests
bash run_testset_3DTurb.sh
cd ..
python Data_Merge.py
```

Generator parameters can be changed through the corresponding Hydra YAML. NLE generators first write `.npy` arrays; run `Data_Merge.py` to obtain the HDF5 layout used by the official dataloaders.

## What is interesting and challenging about the data

Extreme memory/I/O requirements, only O(100) samples, 3D multiscale structure, rollout stability and an internal inconsistency in the paper’s configuration tables.

## Primary sources

- [PDEBench paper and supplementary material](https://arxiv.org/abs/2210.07182)
- [Official PDEBench repository](https://github.com/pdebench/PDEBench)
- [Official download instructions](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench dataset DOI](https://doi.org/10.18419/darus-2986)
