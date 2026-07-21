---
title: "Acoustic Scattering — Maze"
parent_collection: "The Well"
physical_family: "Variable-coefficient acoustics"
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,y)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/acoustic_scattering_maze/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/acoustic_scattering_maze"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/acoustic_scattering_maze"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: acoustic_scattering_maze
weight: 50
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "These datasets solve a first-order variable-coefficient acoustic system. A pressure disturbance travels through materials whose density changes sharply in space. The three relea…"
description: "These datasets solve a first-order variable-coefficient acoustic system. A pressure disturbance travels through materials whose density changes sharply in space. The three relea…"

---

# Acoustic Scattering — Maze

> **Parent collection:** The Well  
> **Directory:** `acoustic_scattering_maze`  
> **Equation family:** Variable-coefficient acoustics  
> **Documentation type:** source-faithful structured rewrite of the official dataset page, paper appendix and current repository metadata.

## 1. Scope and physical overview

These datasets solve a first-order variable-coefficient acoustic system. A pressure disturbance travels through materials whose density changes sharply in space. The three releases share the same PDE and solver but use different families of coefficient fields: a single discontinuous interface, randomly placed inclusions, or a maze-like high-contrast medium.

The Well treats each downloadable directory as a self-documenting HDF5 dataset. This page separates three notions that are often conflated: parameters that are theoretically adjustable in the equations/generator, parameters actually varied in the released ensemble, and parameters fixed in this release.

## 2. Governing equations

$$
\begin{aligned}
\frac{\partial p}{\partial t}
+K(x,y)\left(\frac{\partial u}{\partial x}+\frac{\partial v}{\partial y}\right)&=0,\\
\frac{\partial u}{\partial t}
+\frac{1}{\rho(x,y)}\frac{\partial p}{\partial x}&=0,\\
\frac{\partial v}{\partial t}
+\frac{1}{\rho(x,y)}\frac{\partial p}{\partial y}&=0.
\end{aligned}
$$

The local acoustic speed is \(c(x,y)=\sqrt{K(x,y)/\rho(x,y)}\).

### Variables and physical fields

- \(p(x,y,t)\): acoustic pressure.
- \(u(x,y,t),v(x,y,t)\): Cartesian velocity components.
- \(
ho(x,y)\): time-independent material density.
- \(K(x,y)\): bulk modulus.
- \(c(x,y)\): derived, time-independent speed of sound.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Material density \(
ho(x,y)\), bulk modulus \(K(x,y)\), source count/position/radius/amplitude, coefficient geometry, interface contrast, boundary conditions, spatial and temporal resolution. |
| Actually varied in this release | Maze topology and pressure sources vary. A coarse maze with initial wall/path width between 6 and 16 pixels is nearest-neighbor upsampled to \(256^2\). Walls use \(\rho=10^6\), paths use \(\rho=3\). Each trajectory has 1–6 pressure rings placed on paths, with amplitude \(\mathcal U(3,5)\) and radius \(\mathcal U(0.01,0.04)\); overlap with walls is removed. |
| Fixed in this release | Bulk modulus \(K=4\); wall/path density values; grid, domain, boundaries and CFL rule. |

## 4. Initial and boundary conditions

### Initial conditions

Flat pressure background plus 1–6 path-constrained rings; zero initial velocity.

### Boundary conditions

Open in \(y\); reflective in \(x\).

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `acoustic_scattering_maze` |
| Spatial dimension | 2D |
| Coordinate system | Cartesian $(x,y)$ |
| Spatial resolution | $256\times256$ |
| Stored steps per trajectory | 201 |
| Number of trajectories | 2000 |
| Dynamic channels after component expansion | 3 |
| Dynamic fields | $p,u_x,u_y$ |
| Static fields / scalar context | material density $\rho(x,y)$; sound speed $c(x,y)$ |
| Time range | $[0,4]$ |
| Stored time spacing | $4/201$ (documented storage interval) |
| Spatial domain | $[-1,1]\times[-1,1]$ |
| Estimated release size | 311.3 GB |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,3)\);
- standard 4-frame history: \((B,4,L_1,L_2,3)\);
- standard 1-frame target: \((B,1,L_1,L_2,3)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** Clawpack; explicit finite volume, TVD/MC limiter, CFL-controlled time step

Clawpack solves the hyperbolic conservation-law form using an explicit finite-volume method, a total-variation-diminishing reconstruction/monotonized-central limiter, and a time step selected by the CFL condition. Released arrays are temporally sampled and stored in fp32 even though generation is documented as double precision.

## 7. Recommended ML tasks and diagnostics

Autoregressive wave forecasting, inverse scattering/material reconstruction, source localization or optimization, learning across discontinuous coefficients, and robustness to irregular geometry represented by coefficient fields.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

The maze trajectories are twice as long as the other acoustic variants: 201 stored frames over \([0,4]\). The paper overview groups acoustic data together and therefore does not expose this distinction.

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
the-well-download --base-path ./the_well_data --dataset acoustic_scattering_maze --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset acoustic_scattering_maze --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="acoustic_scattering_maze",
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
    well_dataset_name="acoustic_scattering_maze",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.


## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/acoustic_scattering_maze/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/acoustic_scattering_maze> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/acoustic_scattering_maze> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. Citation and provenance

Recommended simulation citation: Mandli et al., *Clawpack: building an open source ecosystem for solving hyperbolic PDEs* (2016).

Also cite the collection paper:

> Ohana et al., **The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**, NeurIPS 2024 Datasets and Benchmarks.

This English page is a structured, source-faithful synthesis, not a byte-for-byte mirror of the website. Equations and numerical values are reconciled from the official dataset documentation, the paper appendix and current repository metadata. The paired Chinese document is an annotated translation and reorganization.
