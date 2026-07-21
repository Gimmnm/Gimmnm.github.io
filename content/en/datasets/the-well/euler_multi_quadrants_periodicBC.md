---
title: "Euler Multi-Quadrants — Periodic Boundary"
parent_collection: "The Well"
physical_family: "Compressible inviscid Euler equations"
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,y)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/euler_multi_quadrants_periodicBC/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/euler_multi_quadrants_periodicBC"
huggingface_dataset: ""
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: euler_multi_quadrants_periodicBC
weight: 90
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "This benchmark generalizes the classical two-dimensional quadrant Riemann problem. Piecewise-constant initial states create shocks, rarefaction waves and contact discontinuities…"
description: "This benchmark generalizes the classical two-dimensional quadrant Riemann problem. Piecewise-constant initial states create shocks, rarefaction waves and contact discontinuities…"

---

# Euler Multi-Quadrants — Periodic Boundary

> **Parent collection:** The Well  
> **Directory:** `euler_multi_quadrants_periodicBC`  
> **Equation family:** Compressible inviscid Euler equations  
> **Documentation type:** source-faithful structured rewrite of the official dataset page, paper appendix and current repository metadata.

## 1. Scope and physical overview

This benchmark generalizes the classical two-dimensional quadrant Riemann problem. Piecewise-constant initial states create shocks, rarefaction waves and contact discontinuities, and the additional quadrant structure forces these waves to interact. The two downloadable directories differ only in the external boundary treatment.

The Well treats each downloadable directory as a self-documenting HDF5 dataset. This page separates three notions that are often conflated: parameters that are theoretically adjustable in the equations/generator, parameters actually varied in the released ensemble, and parameters fixed in this release.

## 2. Governing equations

For conserved state
$$
U=(\rho,\rho u,\rho v,\rho E)^\top,
$$
the integral conservation law is
$$
\frac{d}{dt}\iint_\Omega U\,dA
+\oint_{\partial\Omega}(\mathbf F\,\hat{\mathbf i}+\mathbf G\,\hat{\mathbf j})\cdot\hat{\mathbf n}\,dS=0,
$$
where
$$
\mathbf F=
\begin{pmatrix}
\rho u\\ \rho u^2+p\\ \rho uv\\ u(\rho E+p)
\end{pmatrix},\qquad
\mathbf G=
\begin{pmatrix}
\rho v\\ \rho uv\\ \rho v^2+p\\ v(\rho E+p)
\end{pmatrix},
$$
and
$$
\rho E=\frac{p}{\gamma-1}+\frac12\rho(u^2+v^2).
$$

### Variables and physical fields

- \(\rho\): mass density.
- \(u,v\): Cartesian velocity components.
- \(p\): pressure.
- \(\rho E\): total energy density.
- \(\gamma\): ratio of specific heats.
- The released momentum field stores \((\rho u,\rho v)\).

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Adiabatic index \(\gamma\), all piecewise-constant quadrant states \((\rho,u,v,p)\), discontinuity layout, boundary type, domain size, grid resolution, Riemann solver/limiter and sampling cadence. |
| Actually varied in this release | The adiabatic index is swept over \(\gamma\in\{1.13,1.22,1.30,1.33,1.365,1.40,1.404,1.453,1.597,1.76\}\). For each value, approximately 500 randomized piecewise-constant multi-quadrant initial states are generated, giving 5000 trajectories in this boundary-condition directory. |
| Fixed in this release | Grid resolution, integration horizon, conservative variables, equation family and the boundary type named by this directory. |

## 4. Initial and boundary conditions

### Initial conditions

Randomized piecewise-constant density, velocity and pressure states arranged in multiple quadrants/discontinuous regions. The exact generator is authoritative for state ranges and admissibility filters.

### Boundary conditions

Periodic external boundaries.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `euler_multi_quadrants_periodicBC` |
| Spatial dimension | 2D |
| Coordinate system | Cartesian $(x,y)$ |
| Spatial resolution | $512\times512$ |
| Stored steps per trajectory | 100 |
| Number of trajectories | 5000 |
| Dynamic channels after component expansion | 5 |
| Dynamic fields | density $\rho$, energy, pressure, momentum $(\rho u,\rho v)$ |
| Static fields / scalar context | adiabatic index $\gamma$ and boundary-condition metadata |
| Time range | $[0,1.5]$ |
| Stored time spacing | $\approx0.015$ |
| Spatial domain | uniform square grid |
| Estimated release size | part of 5.17 TB combined Euler release |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,5)\);
- standard 4-frame history: \((B,4,L_1,L_2,5)\);
- standard 1-frame target: \((B,1,L_1,L_2,5)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** Clawpack; explicit finite-volume hyperbolic solver

Clawpack applies an explicit finite-volume method for hyperbolic conservation laws. Initial data are randomized piecewise-constant multi-quadrant states. The paper reports generation in fp64, approximately 80 aggregate hours on 160 CPU cores.

## 7. Recommended ML tasks and diagnostics

Shock-aware forecasting, conservation-law learning, robustness to discontinuities, transfer between open and periodic boundaries, interpolation/extrapolation in \(\gamma\), and long-rollout stability.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

The paper reports 10,000 Euler trajectories in total; the current repository exposes two 5000-trajectory directories split by boundary condition. Some metadata versions may show 101 coordinate values including endpoints while benchmark tables summarize 100 time steps; inspect the actual HDF5 `time` array.

Current repository status: **active**. This document was checked against the repository state/release information available on 2026-07-21. Always inspect `dataset_name.yaml`, `stats.yaml`, HDF5 coordinates and release notes for the exact files used in an experiment.

## Download and loading

### Install the interface

```bash
python -m venv .venv
source .venv/bin/activate
pip install the_well
```

### Download one split

```bash
the-well-download --base-path ./the_well_data --dataset euler_multi_quadrants_periodicBC --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset euler_multi_quadrants_periodicBC --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="euler_multi_quadrants_periodicBC",
    well_split_name="train",
)
loader = DataLoader(trainset, batch_size=1, shuffle=True)

sample = trainset[0]
print(sample.keys())
```

### Hugging Face status

This directory is not currently listed among the commonly available The Well Hugging Face streams. Use the official download CLI/Flatiron-hosted files and re-check the collection before assuming Hub availability.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.


## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/euler_multi_quadrants_periodicBC/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/euler_multi_quadrants_periodicBC> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. Citation and provenance

Recommended citations: Clawpack and the two-dimensional Riemann-problem literature cited by The Well.

Also cite the collection paper:

> Ohana et al., **The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**, NeurIPS 2024 Datasets and Benchmarks.

This English page is a structured, source-faithful synthesis, not a byte-for-byte mirror of the website. Equations and numerical values are reconciled from the official dataset documentation, the paper appendix and current repository metadata. The paired Chinese document is an annotated translation and reorganization.
