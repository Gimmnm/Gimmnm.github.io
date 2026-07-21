---
title: "Viscoelastic Instability — Corrected v2"
parent_collection: "The Well"
physical_family: "FENE-P viscoelastic flow"
spatial_dimension: 2D
coordinate_system: "Cartesian streamwise/wall-normal coordinates"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: ""
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/viscoelastic_instability_v2"
huggingface_dataset: ""
paper: "https://arxiv.org/abs/2412.00568"
status: active-corrected
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: viscoelastic_instability_v2
weight: 240
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "Two-dimensional FENE-P channel flow supports multiple coexisting attractors: laminar flow, steady and chaotic arrowhead states, elasto-inertial turbulence, and edge states separ…"
description: "Two-dimensional FENE-P channel flow supports multiple coexisting attractors: laminar flow, steady and chaotic arrowhead states, elasto-inertial turbulence, and edge states separ…"

---

# Viscoelastic Instability — Corrected v2

> **Parent collection:** The Well  
> **Directory:** `viscoelastic_instability_v2`  
> **Equation family:** FENE-P viscoelastic flow  
> **Documentation type:** source-faithful structured rewrite of the official dataset page, paper appendix and current repository metadata.

## 1. Scope and physical overview

Two-dimensional FENE-P channel flow supports multiple coexisting attractors: laminar flow, steady and chaotic arrowhead states, elasto-inertial turbulence, and edge states separating basins of attraction. The legacy processed release is deprecated; the corrected `viscoelastic_instability_v2` should be preferred for new work.

The Well treats each downloadable directory as a self-documenting HDF5 dataset. This page separates three notions that are often conflated: parameters that are theoretically adjustable in the equations/generator, parameters actually varied in the released ensemble, and parameters fixed in this release.

## 2. Governing equations

$$
\mathrm{Re}\left(\frac{\partial\mathbf u}{\partial t}
+\mathbf u\cdot\nabla\mathbf u\right)+\nabla p
=\beta\Delta\mathbf u+(1-\beta)\nabla\cdot T(C),
$$
$$
\nabla\cdot\mathbf u=0,
$$
$$
T(C)=\frac1{\mathrm{Wi}}
\left[
\frac{C}{1-(\operatorname{tr}C-3)/L_{\max}^2}-I
\right],
$$
$$
\frac{\partial C}{\partial t}
+(\mathbf u\cdot\nabla)C+T(C)
=C\cdot\nabla\mathbf u+(\nabla\mathbf u)^\top\cdot C+\epsilon\Delta C.
$$

### Variables and physical fields

- \(\mathbf u=(u,v)\), \(p\): velocity and pressure.
- \(C\): polymer conformation tensor.
- \(T(C)\): FENE-P polymer stress.
- \(\mathrm{Re}\): Reynolds number.
- \(\mathrm{Wi}\): Weissenberg number.
- \(\beta=\nu_s/\nu\): solvent-to-total viscosity ratio.
- \(\epsilon\): dimensionless polymer-stress diffusivity.
- \(L_{\max}\): maximum polymer extensibility.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Reynolds/Weissenberg numbers, viscosity ratio, extensibility, stress diffusivity, pressure gradient/flow rate, channel size, perturbation and attractor/edge-state initialization, spatial resolution and sampling window. |
| Actually varied in this release | The physical coefficients are not swept: \(\mathrm{Re}=1000\), \(\mathrm{Wi}=50\), \(\beta=0.9\), \(\epsilon=2\times10^{-6}\), \(L_{\max}=70\). Variation comes from dynamical regime and initial condition: laminar, steady arrowhead (SAR), chaotic arrowhead (CAR), elasto-inertial turbulence (EIT), and two edge-state families. |
| Fixed in this release | All FENE-P coefficients above, channel geometry, streamwise periodicity, no-slip walls, resolution and the underlying Dedalus simulations. |

## 4. Initial and boundary conditions

### Initial conditions

States sampled from/coherent with the named attractors. Edge states are found by bisection between initial conditions known to approach different attractors.

### Boundary conditions

Periodic in the streamwise direction; no velocity at the two parallel walls.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `viscoelastic_instability_v2` |
| Spatial dimension | 2D |
| Coordinate system | Cartesian streamwise/wall-normal coordinates |
| Spatial resolution | $512\times512$ |
| Stored steps per trajectory | 20 or 60 depending on attractor/segment |
| Number of trajectories | 260 |
| Dynamic channels after component expansion | 8 |
| Dynamic fields | pressure; velocity (2); conformation components $C_{xx},C_{xy},C_{yx},C_{yy},C_{zz}$ |
| Static fields / scalar context | fixed FENE-P dimensionless parameters and attractor labels |
| Time range | segment-dependent |
| Stored time spacing | uniform within each segment |
| Spatial domain | channel; periodic streamwise, no-slip walls |
| Estimated release size | approximately 66 GB; not separately tabulated in the paper |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,8)\);
- standard 4-frame history: \((B,4,L_1,L_2,8)\);
- standard 1-frame target: \((B,1,L_1,L_2,8)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** Dedalus DNS; corrected extraction/processing of the same simulations

Dedalus performs direct numerical simulation between two parallel walls with streamwise periodicity and no-slip walls. Edge states are generated by bisection between initial states known to reach different attractors. The paper reports about one day for roughly 50 snapshots on 32 or 64 cores and around three months for the campaign.

## 7. Recommended ML tasks and diagnostics

Attractor classification, transition/edge-state forecasting, multistability, rare-event prediction, long-horizon chaotic dynamics and learning tensor-valued positive-definite fields.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

Corrected processing of the same underlying physical simulations. Prefer this directory for new experiments. It is present in the repository but does not yet have a separate official website page or common Hugging Face stream entry.

Current repository status: **active-corrected**. This document was checked against the repository state/release information available on 2026-07-21. Always inspect `dataset_name.yaml`, `stats.yaml`, HDF5 coordinates and release notes for the exact files used in an experiment.

## Download and loading

### Install the interface

```bash
python -m venv .venv
source .venv/bin/activate
pip install the_well
```

### Download one split

```bash
the-well-download --base-path ./the_well_data --dataset viscoelastic_instability_v2 --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset viscoelastic_instability_v2 --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="viscoelastic_instability_v2",
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
| Official dataset page | No separate page / 尚无独立页面 |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/viscoelastic_instability_v2> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. Citation and provenance

Recommended citation: Beneitez et al., *Multistability of elasto-inertial two-dimensional channel flow* (2024).

Also cite the collection paper:

> Ohana et al., **The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**, NeurIPS 2024 Datasets and Benchmarks.

This English page is a structured, source-faithful synthesis, not a byte-for-byte mirror of the website. Equations and numerical values are reconciled from the official dataset documentation, the paper appendix and current repository metadata. The paired Chinese document is an annotated translation and reorganization.
