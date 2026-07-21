---
title: "Active Matter"
parent_collection: "The Well"
physical_family: "Active-fluid kinetic theory"
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,y)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/active_matter/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/active_matter"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/active_matter"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: active_matter
weight: 60
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: 'A continuum kinetic model describes active elongated particles suspended in a viscous Stokes fluid. The high-dimensional orientational distribution \(\Psi(\mathbf x,\mathbf p,t)…'
description: 'A continuum kinetic model describes active elongated particles suspended in a viscous Stokes fluid. The high-dimensional orientational distribution \(\Psi(\mathbf x,\mathbf p,t)…'

---

# Active Matter

> **Parent collection:** The Well  
> **Directory:** `active_matter`  
> **Equation family:** Active-fluid kinetic theory  
> **Documentation type:** source-faithful structured rewrite of the official dataset page, paper appendix and current repository metadata.

## 1. Scope and physical overview

A continuum kinetic model describes active elongated particles suspended in a viscous Stokes fluid. The high-dimensional orientational distribution \(\Psi(\mathbf x,\mathbf p,t)\) is evolved, while low-order moments—concentration, orientation, velocity and strain—are stored for machine learning.

The Well treats each downloadable directory as a self-documenting HDF5 dataset. This page separates three notions that are often conflated: parameters that are theoretically adjustable in the equations/generator, parameters actually varied in the released ensemble, and parameters fixed in this release.

## 2. Governing equations

The Smoluchowski equation is
$$
\frac{\partial\Psi}{\partial t}
+\nabla_{\mathbf x}\!\cdot(\dot{\mathbf x}\Psi)
+\nabla_{\mathbf p}\!\cdot(\dot{\mathbf p}\Psi)=0,
$$
with conformational fluxes
$$
\dot{\mathbf x}=\mathbf u-d_T\nabla_{\mathbf x}\log\Psi,\qquad
\dot{\mathbf p}=(I-\mathbf p\mathbf p)\cdot(\nabla\mathbf u+2\zeta D)\cdot\mathbf p
-d_R\nabla_{\mathbf p}\log\Psi.
$$
It is coupled to incompressible Stokes flow,
$$
-\Delta\mathbf u+\nabla P=\nabla\cdot\Sigma,\qquad \nabla\cdot\mathbf u=0,
$$
with
$$
\Sigma=\alpha D+\beta\,S:E-2\zeta\beta(D\cdot D-S:D).
$$

### Variables and physical fields

- \(\Psi(\mathbf x,\mathbf p,t)\): particle distribution in position and orientation.
- \(c=\langle1
angle\): concentration.
- \(D=\langle\mathbf p\mathbf p
angle\): second orientation moment; the released orientation tensor is normalized according to the generator convention.
- \(S=\langle\mathbf p\mathbf p\mathbf p\mathbf p
angle\): fourth moment.
- \(\mathbf u,P,E\): fluid velocity, pressure and rate-of-strain tensor.
- \(lpha\): active dipole strength; \(eta\): density/rigidity parameter; \(\zeta\): steric-alignment strength; \(d_T,d_R\): diffusivities.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Active strength \(lpha\), alignment \(\zeta\), density parameter \(eta\), translational/rotational diffusion \(d_T,d_R\), domain size, spatial/orientational modes, initial distribution and forcing. |
| Actually varied in this release | The released parameter grid uses \(\alpha\in\{-1,-2,-3,-4,-5\}\) and \(\zeta\in\{1,3,5,7,9,11,13,15,17\}\), with repeated initial conditions. Current documentation/parameter arithmetic indicates 5 initial realizations per pair, giving \(5\times9\times5=225\) trajectories. |
| Fixed in this release | \(\beta=0.8\); periodic square \(L=10\); spatial and orientation resolutions; the generator's translational/rotational diffusion and integration configuration; 81 stored snapshots. |

## 4. Initial and boundary conditions

### Initial conditions

Five initial realizations are used for each \((\alpha,\zeta)\) pair in the current release organization. Exact random-field construction should be read from the generator/repository when reproducing the data bit-for-bit.

### Boundary conditions

Periodic in both spatial directions.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `active_matter` |
| Spatial dimension | 2D |
| Coordinate system | Cartesian $(x,y)$ |
| Spatial resolution | $256\times256$ |
| Stored steps per trajectory | 81 |
| Number of trajectories | 225 (current parameter product; paper table reports 360) |
| Dynamic channels after component expansion | 11 |
| Dynamic fields | concentration (1), velocity (2), orientation tensor (4), strain-rate tensor (4) |
| Static fields / scalar context | none in the default dynamic target; parameters are stored as scalars |
| Time range | $[0,20]$ |
| Stored time spacing | $0.25$ |
| Spatial domain | periodic square, side length $L=10$ |
| Estimated release size | 51.3 GB |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,11)\);
- standard 4-frame history: \((B,4,L_1,L_2,11)\);
- standard 1-frame target: \((B,1,L_1,L_2,11)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** Fourier pseudo-spectral discretization in space/orientation; SBDF2, internal $\Delta t\approx4\times10^{-4}$

Fourier pseudo-spectral differentiation is used in physical space and orientation. Linear terms are treated implicitly and nonlinear terms explicitly with SBDF2. The simulation uses a periodic square of side \(L=10\), 256 spatial modes in each direction and 256 orientational modes. The source paper reports roughly 20 minutes per run on an A100 80 GB GPU in fp64.

## 7. Recommended ML tasks and diagnostics

Moment-closure learning, long-horizon forecasting of active turbulence, parameter interpolation/extrapolation over \(lpha,\zeta\), and learning stable low-order dynamics without resolving the full orientation distribution.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

The paper table reports 360 trajectories, while the current official parameter product gives 225. This documentation records both and uses 225 as the current-directory count; inspect downloaded HDF5 metadata for the exact version in use.

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
the-well-download --base-path ./the_well_data --dataset active_matter --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset active_matter --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="active_matter",
    well_split_name="train",
)
loader = DataLoader(trainset, batch_size=1, shuffle=True)

sample = trainset[0]
print(sample.keys())
```

### Hugging Face streaming

This directory is listed for Hub access in the current collection:

```python
from the_well.data import WellDataset

trainset = WellDataset(
    well_base_path="hf://datasets/polymathic-ai/",
    well_dataset_name="active_matter",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.


## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/active_matter/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/active_matter> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/active_matter> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. Citation and provenance

Recommended citation: Maddu, Weady and Shelley, *Learning fast, accurate, and stable closures of a kinetic theory of an active fluid* (2024).

Also cite the collection paper:

> Ohana et al., **The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**, NeurIPS 2024 Datasets and Benchmarks.

This English page is a structured, source-faithful synthesis, not a byte-for-byte mirror of the website. Equations and numerical values are reconciled from the official dataset documentation, the paper appendix and current repository metadata. The paired Chinese document is an annotated translation and reorganization.
