---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 11_incompressible_ns_2d
spatial_dimension: 2
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: ns_incom
last_verified: 2026-07-21
title: "2D Inhomogeneously Forced Incompressible Navier–Stokes"
linkTitle: "incompressible ns 2d"
weight: 110
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "Incompressible flow with inhomogeneous forcing and Dirichlet boundaries."
description: "Incompressible flow with inhomogeneous forcing and Dirichlet boundaries."

---

# 2D Inhomogeneously Forced Incompressible Navier–Stokes

Incompressible Navier–Stokes applies when flow speeds are far below wave-propagation speeds. PDEBench uses an augmented form with spatially inhomogeneous forcing and nonperiodic Dirichlet boundaries to challenge models built for periodic convolutions; the force field can also serve as an inverse-problem target.

## Parent dataset and access

| Field | Value |
|---|---|
| Parent dataset | **PDEBench** |
| Dataset paper | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| Paper PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| Official repository | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| Dataset DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| Current download category | `ns_incom` |
| Data size | 2.3 TB |
| Data-generation entry point | [gen_ns_incomp.py + configs/ns_incomp.yaml](https://github.com/pdebench/PDEBench/blob/main/pdebench/data_gen/gen_ns_incomp.py) |
| Last checked | 2026-07-21 |

## Governing equation

\[
\nabla\cdot\mathbf v=0,
\]
\[
\rho(\partial_t\mathbf v+\mathbf v\cdot\nabla\mathbf v)
=-\nabla p+\eta\Delta\mathbf v+\mathbf f(\mathbf x).
\]

## Variables and coordinates

**State variables**
- $\mathbf{v}=(v_x,v_y)$: incompressible velocity field (dynamic prediction target).
- $p$: constraint pressure (enforced by incompressibility).

**Condition fields and parameters**
- $\mathbf{f}=(f_x,f_y)$: spatially varying, time-independent forcing field (static conditioning input).
- The paper's augmented equation denotes the force by $\mathbf{u}$; this document uses $\mathbf{f}$ to avoid confusion with velocity.
- $\rho$: density (homogeneous-fluid assumption).
- $\eta$ (release viscosity often written $\nu=0.01$): viscosity coefficient.

**Coordinates and domain**
- Space: uniform 2D Cartesian, $\Omega=[0,1]^2$; PhiFlow staggered / scalar grid details are handled by the generator.
- Time: current config total duration about $5$ ($10^5$ steps $\times 5\cdot10^{-5}$), frames stored at intervals.

## About the data

| Attribute | Value |
|---|---|
| Spatial dim | 2 |
| Time-dependent | yes |
| Grid | uniform 2D Cartesian |
| Domain | $[0,1]^2$ |
| Time range | physical time ≈ 5 |
| Spatial res. | $256\times256$ |
| Time steps | 1,000 |
| Trajectories / file | 1,000 (sharded) |
| Channels | dynamic 2: $v_x$, $v_y$; conditioning 2: $f_x$, $f_y$ |
| Sample shape | velocity $1000\times256\times256\times2$ (force stored separately) |
| Size | 2.3 TB |
| Format | HDF5 shards |

## Initial conditions

Initial velocity and forcing are sampled from isotropic Gaussian random fields. The paper gives $\tau_{v_0}=-3,\sigma_{v_0}=0.15$ and $\tau_f=-1,\sigma_f=0.4$; samples differ mainly by seed. Current YAML uses keys `smoothness=1.0, scale=0.4, force_smoothness=3.0, force_scale=0.15`; map these implementation names to the paper notation through the generator.

## Boundary conditions

Dirichlet no-slip boundary: velocity is clamped to zero. Current configuration sets `velocity_extrapolation: ZERO` and `force_extrapolation: ZERO`.

## Numerical generation

The paper uses PhiFlow. Current `ns_incomp.yaml` sets `domain_size=[1,1]`, `grid_size=[256,256]`, `NU=0.01`, `n_steps=100000`, `DT=5e-5`, `frame_int=100`, with JAX backend, GPU and JIT.

## Parameters

Equation:

\[
\nabla\cdot\mathbf v=0,
\]
\[
\rho(\partial_t\mathbf v+\mathbf v\cdot\nabla\mathbf v)
=-\nabla p+\eta\Delta\mathbf v+\mathbf f(\mathbf x).
\]

### Released file configs

274 shards share **one** physical config. The name contains `512`, but paper / YAML use **$256\times256$**.

| Data file (pattern) | $\nu$ | Boundary | Per trajectory | Fixed |
|---|---:|---|---|---|
| `ns_incom_inhom_2d_512-{0…274\setminus49}.h5` | $0.01$ | no-slip Dirichlet | velocity GRF, force GRF | domain $[0,1]^2$, $256^2$, $N_t=1000$ |

### Generator-tunable ranges

| Parameter | Tunable range / options | Covered by release? |
|---|---|---|
| $\nu$ (`NU`) | any positive scalar | no (fixed $0.01$) |
| GRF: `smoothness, scale, force_smoothness, force_scale` | editable | no (YAML defaults) |
| `grid_size`, `DT`, `n_steps`, `frame_int` | editable | no (release $256^2$, $N_t=1000$) |
| boundary extrapolation | editable | no (`ZERO` no-slip) |

## Data files

The current official download manifest (`pdebench_data_urls.csv`) lists **274** files; paths are relative to the download root. See [Data format](../00_data_format/).

Shard pattern: `2D/NS_incom/ns_incom_inhom_2d_512-{i}.h5`, indices $0$–$274$, missing index `49`, 274 files total. The `512` token is not the grid resolution.

Filenames:

```
ns_incom_inhom_2d_512-0.h5
ns_incom_inhom_2d_512-1.h5
ns_incom_inhom_2d_512-2.h5
ns_incom_inhom_2d_512-3.h5
ns_incom_inhom_2d_512-4.h5
ns_incom_inhom_2d_512-5.h5
ns_incom_inhom_2d_512-6.h5
ns_incom_inhom_2d_512-7.h5
ns_incom_inhom_2d_512-8.h5
ns_incom_inhom_2d_512-9.h5
ns_incom_inhom_2d_512-10.h5
ns_incom_inhom_2d_512-11.h5
ns_incom_inhom_2d_512-12.h5
ns_incom_inhom_2d_512-13.h5
ns_incom_inhom_2d_512-14.h5
ns_incom_inhom_2d_512-15.h5
ns_incom_inhom_2d_512-16.h5
ns_incom_inhom_2d_512-17.h5
ns_incom_inhom_2d_512-18.h5
ns_incom_inhom_2d_512-19.h5
ns_incom_inhom_2d_512-20.h5
ns_incom_inhom_2d_512-21.h5
ns_incom_inhom_2d_512-22.h5
ns_incom_inhom_2d_512-23.h5
ns_incom_inhom_2d_512-24.h5
ns_incom_inhom_2d_512-25.h5
ns_incom_inhom_2d_512-26.h5
ns_incom_inhom_2d_512-27.h5
ns_incom_inhom_2d_512-28.h5
ns_incom_inhom_2d_512-29.h5
ns_incom_inhom_2d_512-30.h5
ns_incom_inhom_2d_512-31.h5
ns_incom_inhom_2d_512-32.h5
ns_incom_inhom_2d_512-33.h5
ns_incom_inhom_2d_512-34.h5
ns_incom_inhom_2d_512-35.h5
ns_incom_inhom_2d_512-36.h5
ns_incom_inhom_2d_512-37.h5
ns_incom_inhom_2d_512-38.h5
ns_incom_inhom_2d_512-39.h5
ns_incom_inhom_2d_512-40.h5
ns_incom_inhom_2d_512-41.h5
ns_incom_inhom_2d_512-42.h5
ns_incom_inhom_2d_512-43.h5
ns_incom_inhom_2d_512-44.h5
ns_incom_inhom_2d_512-45.h5
ns_incom_inhom_2d_512-46.h5
ns_incom_inhom_2d_512-47.h5
ns_incom_inhom_2d_512-48.h5
ns_incom_inhom_2d_512-50.h5
ns_incom_inhom_2d_512-51.h5
ns_incom_inhom_2d_512-52.h5
ns_incom_inhom_2d_512-53.h5
ns_incom_inhom_2d_512-54.h5
ns_incom_inhom_2d_512-55.h5
ns_incom_inhom_2d_512-56.h5
ns_incom_inhom_2d_512-57.h5
ns_incom_inhom_2d_512-58.h5
ns_incom_inhom_2d_512-59.h5
ns_incom_inhom_2d_512-60.h5
ns_incom_inhom_2d_512-61.h5
ns_incom_inhom_2d_512-62.h5
ns_incom_inhom_2d_512-63.h5
ns_incom_inhom_2d_512-64.h5
ns_incom_inhom_2d_512-65.h5
ns_incom_inhom_2d_512-66.h5
ns_incom_inhom_2d_512-67.h5
ns_incom_inhom_2d_512-68.h5
ns_incom_inhom_2d_512-69.h5
ns_incom_inhom_2d_512-70.h5
ns_incom_inhom_2d_512-71.h5
ns_incom_inhom_2d_512-72.h5
ns_incom_inhom_2d_512-73.h5
ns_incom_inhom_2d_512-74.h5
ns_incom_inhom_2d_512-75.h5
ns_incom_inhom_2d_512-76.h5
ns_incom_inhom_2d_512-77.h5
ns_incom_inhom_2d_512-78.h5
ns_incom_inhom_2d_512-79.h5
ns_incom_inhom_2d_512-80.h5
ns_incom_inhom_2d_512-81.h5
ns_incom_inhom_2d_512-82.h5
ns_incom_inhom_2d_512-83.h5
ns_incom_inhom_2d_512-84.h5
ns_incom_inhom_2d_512-85.h5
ns_incom_inhom_2d_512-86.h5
ns_incom_inhom_2d_512-87.h5
ns_incom_inhom_2d_512-88.h5
ns_incom_inhom_2d_512-89.h5
ns_incom_inhom_2d_512-90.h5
ns_incom_inhom_2d_512-91.h5
ns_incom_inhom_2d_512-92.h5
ns_incom_inhom_2d_512-93.h5
ns_incom_inhom_2d_512-94.h5
ns_incom_inhom_2d_512-95.h5
ns_incom_inhom_2d_512-96.h5
ns_incom_inhom_2d_512-97.h5
ns_incom_inhom_2d_512-98.h5
ns_incom_inhom_2d_512-99.h5
ns_incom_inhom_2d_512-100.h5
ns_incom_inhom_2d_512-101.h5
ns_incom_inhom_2d_512-102.h5
ns_incom_inhom_2d_512-103.h5
ns_incom_inhom_2d_512-104.h5
ns_incom_inhom_2d_512-105.h5
ns_incom_inhom_2d_512-106.h5
ns_incom_inhom_2d_512-107.h5
ns_incom_inhom_2d_512-108.h5
ns_incom_inhom_2d_512-109.h5
ns_incom_inhom_2d_512-110.h5
ns_incom_inhom_2d_512-111.h5
ns_incom_inhom_2d_512-112.h5
ns_incom_inhom_2d_512-113.h5
ns_incom_inhom_2d_512-114.h5
ns_incom_inhom_2d_512-115.h5
ns_incom_inhom_2d_512-116.h5
ns_incom_inhom_2d_512-117.h5
ns_incom_inhom_2d_512-118.h5
ns_incom_inhom_2d_512-119.h5
ns_incom_inhom_2d_512-120.h5
ns_incom_inhom_2d_512-121.h5
ns_incom_inhom_2d_512-122.h5
ns_incom_inhom_2d_512-123.h5
ns_incom_inhom_2d_512-124.h5
ns_incom_inhom_2d_512-125.h5
ns_incom_inhom_2d_512-126.h5
ns_incom_inhom_2d_512-127.h5
ns_incom_inhom_2d_512-128.h5
ns_incom_inhom_2d_512-129.h5
ns_incom_inhom_2d_512-130.h5
ns_incom_inhom_2d_512-131.h5
ns_incom_inhom_2d_512-132.h5
ns_incom_inhom_2d_512-133.h5
ns_incom_inhom_2d_512-134.h5
ns_incom_inhom_2d_512-135.h5
ns_incom_inhom_2d_512-136.h5
ns_incom_inhom_2d_512-137.h5
ns_incom_inhom_2d_512-138.h5
ns_incom_inhom_2d_512-139.h5
ns_incom_inhom_2d_512-140.h5
ns_incom_inhom_2d_512-141.h5
ns_incom_inhom_2d_512-142.h5
ns_incom_inhom_2d_512-143.h5
ns_incom_inhom_2d_512-144.h5
ns_incom_inhom_2d_512-145.h5
ns_incom_inhom_2d_512-146.h5
ns_incom_inhom_2d_512-147.h5
ns_incom_inhom_2d_512-148.h5
ns_incom_inhom_2d_512-149.h5
ns_incom_inhom_2d_512-150.h5
ns_incom_inhom_2d_512-151.h5
ns_incom_inhom_2d_512-152.h5
ns_incom_inhom_2d_512-153.h5
ns_incom_inhom_2d_512-154.h5
ns_incom_inhom_2d_512-155.h5
ns_incom_inhom_2d_512-156.h5
ns_incom_inhom_2d_512-157.h5
ns_incom_inhom_2d_512-158.h5
ns_incom_inhom_2d_512-159.h5
ns_incom_inhom_2d_512-160.h5
ns_incom_inhom_2d_512-161.h5
ns_incom_inhom_2d_512-162.h5
ns_incom_inhom_2d_512-163.h5
ns_incom_inhom_2d_512-164.h5
ns_incom_inhom_2d_512-165.h5
ns_incom_inhom_2d_512-166.h5
ns_incom_inhom_2d_512-167.h5
ns_incom_inhom_2d_512-168.h5
ns_incom_inhom_2d_512-169.h5
ns_incom_inhom_2d_512-170.h5
ns_incom_inhom_2d_512-171.h5
ns_incom_inhom_2d_512-172.h5
ns_incom_inhom_2d_512-173.h5
ns_incom_inhom_2d_512-174.h5
ns_incom_inhom_2d_512-175.h5
ns_incom_inhom_2d_512-176.h5
ns_incom_inhom_2d_512-177.h5
ns_incom_inhom_2d_512-178.h5
ns_incom_inhom_2d_512-179.h5
ns_incom_inhom_2d_512-180.h5
ns_incom_inhom_2d_512-181.h5
ns_incom_inhom_2d_512-182.h5
ns_incom_inhom_2d_512-183.h5
ns_incom_inhom_2d_512-184.h5
ns_incom_inhom_2d_512-185.h5
ns_incom_inhom_2d_512-186.h5
ns_incom_inhom_2d_512-187.h5
ns_incom_inhom_2d_512-188.h5
ns_incom_inhom_2d_512-189.h5
ns_incom_inhom_2d_512-190.h5
ns_incom_inhom_2d_512-191.h5
ns_incom_inhom_2d_512-192.h5
ns_incom_inhom_2d_512-193.h5
ns_incom_inhom_2d_512-194.h5
ns_incom_inhom_2d_512-195.h5
ns_incom_inhom_2d_512-196.h5
ns_incom_inhom_2d_512-197.h5
ns_incom_inhom_2d_512-198.h5
ns_incom_inhom_2d_512-199.h5
ns_incom_inhom_2d_512-200.h5
ns_incom_inhom_2d_512-201.h5
ns_incom_inhom_2d_512-202.h5
ns_incom_inhom_2d_512-203.h5
ns_incom_inhom_2d_512-204.h5
ns_incom_inhom_2d_512-205.h5
ns_incom_inhom_2d_512-206.h5
ns_incom_inhom_2d_512-207.h5
ns_incom_inhom_2d_512-208.h5
ns_incom_inhom_2d_512-209.h5
ns_incom_inhom_2d_512-210.h5
ns_incom_inhom_2d_512-211.h5
ns_incom_inhom_2d_512-212.h5
ns_incom_inhom_2d_512-213.h5
ns_incom_inhom_2d_512-214.h5
ns_incom_inhom_2d_512-215.h5
ns_incom_inhom_2d_512-216.h5
ns_incom_inhom_2d_512-217.h5
ns_incom_inhom_2d_512-218.h5
ns_incom_inhom_2d_512-219.h5
ns_incom_inhom_2d_512-220.h5
ns_incom_inhom_2d_512-221.h5
ns_incom_inhom_2d_512-222.h5
ns_incom_inhom_2d_512-223.h5
ns_incom_inhom_2d_512-224.h5
ns_incom_inhom_2d_512-225.h5
ns_incom_inhom_2d_512-226.h5
ns_incom_inhom_2d_512-227.h5
ns_incom_inhom_2d_512-228.h5
ns_incom_inhom_2d_512-229.h5
ns_incom_inhom_2d_512-230.h5
ns_incom_inhom_2d_512-231.h5
ns_incom_inhom_2d_512-232.h5
ns_incom_inhom_2d_512-233.h5
ns_incom_inhom_2d_512-234.h5
ns_incom_inhom_2d_512-235.h5
ns_incom_inhom_2d_512-236.h5
ns_incom_inhom_2d_512-237.h5
ns_incom_inhom_2d_512-238.h5
ns_incom_inhom_2d_512-239.h5
ns_incom_inhom_2d_512-240.h5
ns_incom_inhom_2d_512-241.h5
ns_incom_inhom_2d_512-242.h5
ns_incom_inhom_2d_512-243.h5
ns_incom_inhom_2d_512-244.h5
ns_incom_inhom_2d_512-245.h5
ns_incom_inhom_2d_512-246.h5
ns_incom_inhom_2d_512-247.h5
ns_incom_inhom_2d_512-248.h5
ns_incom_inhom_2d_512-249.h5
ns_incom_inhom_2d_512-250.h5
ns_incom_inhom_2d_512-251.h5
ns_incom_inhom_2d_512-252.h5
ns_incom_inhom_2d_512-253.h5
ns_incom_inhom_2d_512-254.h5
ns_incom_inhom_2d_512-255.h5
ns_incom_inhom_2d_512-256.h5
ns_incom_inhom_2d_512-257.h5
ns_incom_inhom_2d_512-258.h5
ns_incom_inhom_2d_512-259.h5
ns_incom_inhom_2d_512-260.h5
ns_incom_inhom_2d_512-261.h5
ns_incom_inhom_2d_512-262.h5
ns_incom_inhom_2d_512-263.h5
ns_incom_inhom_2d_512-264.h5
ns_incom_inhom_2d_512-265.h5
ns_incom_inhom_2d_512-266.h5
ns_incom_inhom_2d_512-267.h5
ns_incom_inhom_2d_512-268.h5
ns_incom_inhom_2d_512-269.h5
ns_incom_inhom_2d_512-270.h5
ns_incom_inhom_2d_512-271.h5
ns_incom_inhom_2d_512-272.h5
ns_incom_inhom_2d_512-273.h5
ns_incom_inhom_2d_512-274.h5
```

## Data layout and machine-learning task

A faithful conditional-dynamics task is $(\mathbf v_{0:\ell-1},\mathbf f,\text{boundary/coordinates})\mapsto\mathbf v_{\ell:T-1}$ rather than treating velocity as an unconditional video.

- **Trajectory versus training example:** a complete HDF5 trajectory is not a fixed neural-network input. Autoregressive training normally extracts $\ell$ input frames and a one-step or multi-step target; $\ell$ is controlled by `initial_step` in the training configuration.
- **Source precedence:** equations, initial/boundary conditions and publication-scale statistics follow paper v7 and its supplement; current commands, paths and download categories follow the official GitHub `main` branch. Discrepancies are preserved rather than silently reconciled.

## Download

The current repository recommends `download_direct.py`; the EasyDataverse route is documented as slower and potentially error-prone.

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name ns_incom
```

Files may also be selected manually from the [DaRUS DOI page](https://doi.org/10.18419/darus-2986). After downloading, inspect the actual HDF5 `shape`, coordinate arrays, variable keys and YAML attributes. In particular, do not infer CFD or incompressible-NS resolution solely from a filename.

## Regenerating from the official code

```bash
cd PDEBench
python -m pdebench.data_gen.gen_ns_incomp
# Hydra configuration: pdebench/data_gen/configs/ns_incomp.yaml
```

Generator parameters can be changed through the corresponding Hydra YAML. This generation path writes HDF5 directly and does not require `Data_Merge.py`.

## What is interesting and challenging about the data

Very large volume, long trajectories, incompressibility constraint, nonperiodic no-slip boundaries and heterogeneous layout of dynamic velocity versus static forcing.

## Primary sources

- [PDEBench paper and supplementary material](https://arxiv.org/abs/2210.07182)
- [Official PDEBench repository](https://github.com/pdebench/PDEBench)
- [Official download instructions](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench dataset DOI](https://doi.org/10.18419/darus-2986)
