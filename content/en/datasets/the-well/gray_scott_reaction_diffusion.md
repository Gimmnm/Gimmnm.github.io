---
title: "Gray–Scott Reaction–Diffusion"
parent_collection: "The Well"
physical_family: Reaction–diffusion
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,y)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/gray_scott_reaction_diffusion/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/gray_scott_reaction_diffusion"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/gray_scott_reaction_diffusion"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: gray_scott_reaction_diffusion
weight: 100
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "The Gray–Scott model is a two-species reaction–diffusion system. A small set of feed/kill-rate pairs produces qualitatively different pattern families, including gliders, bubble…"
description: "The Gray–Scott model is a two-species reaction–diffusion system. A small set of feed/kill-rate pairs produces qualitatively different pattern families, including gliders, bubble…"

---

# Gray–Scott Reaction–Diffusion

> **Parent collection:** The Well  
> **Directory:** `gray_scott_reaction_diffusion`  
> **Equation family:** Reaction–diffusion  
> **Documentation type:** source-faithful structured rewrite of the official dataset page, paper appendix and current repository metadata.

## 1. Scope and physical overview

The Gray–Scott model is a two-species reaction–diffusion system. A small set of feed/kill-rate pairs produces qualitatively different pattern families, including gliders, bubbles, mazes, worms, spirals and spots.

The Well treats each downloadable directory as a self-documenting HDF5 dataset. This page separates three notions that are often conflated: parameters that are theoretically adjustable in the equations/generator, parameters actually varied in the released ensemble, and parameters fixed in this release.

## 2. Governing equations

$$
\frac{\partial A}{\partial t}
=\delta_A\Delta A-AB^2+f(1-A),
$$
$$
\frac{\partial B}{\partial t}
=\delta_B\Delta B+AB^2-(f+k)B.
$$

### Variables and physical fields

- \(A,B\): concentrations of the two chemical species.
- \(\delta_A,\delta_B\): diffusion constants.
- \(f\): feed rate of species \(A\).
- \(k\): removal/kill rate of species \(B\).

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Diffusion constants, feed/kill rates, domain, boundary conditions, initial concentration fields, perturbation scale, integration interval and sampling cadence. |
| Actually varied in this release | Six \((f,k)\) pairs define six pattern regimes: Gliders \((0.014,0.054)\), Bubbles \((0.098,0.057)\), Maze \((0.029,0.057)\), Worms \((0.058,0.065)\), Spirals \((0.018,0.051)\), and Spots \((0.030,0.062)\). Each pair has 200 initial conditions: 100 random Fourier-series fields and 100 randomly placed Gaussian fields. |
| Fixed in this release | \(\delta_A=2\times10^{-5}\), \(\delta_B=1\times10^{-5}\); periodic domain \([-1,1]^2\); \(128^2\) Fourier representation; 1 s internal step; 10 s output cadence; 10,000 s integration horizon. |

## 4. Initial and boundary conditions

### Initial conditions

Two initialization families are balanced within each parameter regime: random Fourier series and randomly placed Gaussian perturbations.

### Boundary conditions

Periodic in both directions.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `gray_scott_reaction_diffusion` |
| Spatial dimension | 2D |
| Coordinate system | Cartesian $(x,y)$ |
| Spatial resolution | $128\times128$ |
| Stored steps per trajectory | 1001 |
| Number of trajectories | 1200 |
| Dynamic channels after component expansion | 2 |
| Dynamic fields | species concentrations $A,B$ |
| Static fields / scalar context | parameter pair $(f,k)$ |
| Time range | $[0,10000]$ s |
| Stored time spacing | $10$ s between stored snapshots |
| Spatial domain | $[-1,1]^2$, doubly periodic |
| Estimated release size | 153.8 GB |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,2)\);
- standard 4-frame history: \((B,4,L_1,L_2,2)\);
- standard 1-frame target: \((B,1,L_1,L_2,2)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** Chebfun Fourier spectral method; ETDRK4; internal step 1 s

The system is simulated on the doubly periodic domain \([-1,1]^2\) with a \(128\times128\) Fourier representation in Chebfun. An implicit–explicit fourth-order exponential time-differencing Runge–Kutta method handles the stiff system. Internal steps are 1 s and snapshots are saved every 10 steps.

## 7. Recommended ML tasks and diagnostics

Pattern-regime classification, parameter-conditioned forecasting, long-horizon pattern formation, steady-state prediction, and extrapolation to unseen \((f,k)\) regions.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

Some secondary text versions contain a sign typo in the \(B\) equation. The correct Gray–Scott reaction term is \(+AB^2\) in the \(B\) equation, as shown in the paper appendix. The six parameter pairs multiply 200 initial conditions to give 1200 trajectories.

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
the-well-download --base-path ./the_well_data --dataset gray_scott_reaction_diffusion --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset gray_scott_reaction_diffusion --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="gray_scott_reaction_diffusion",
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
    well_dataset_name="gray_scott_reaction_diffusion",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.


## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/gray_scott_reaction_diffusion/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/gray_scott_reaction_diffusion> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/gray_scott_reaction_diffusion> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. Citation and provenance

The Well paper does not require an additional dataset-specific citation; the original Gray–Scott model and numerical-method references are listed in its appendix.

Also cite the collection paper:

> Ohana et al., **The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**, NeurIPS 2024 Datasets and Benchmarks.

This English page is a structured, source-faithful synthesis, not a byte-for-byte mirror of the website. Equations and numerical values are reconciled from the official dataset documentation, the paper appendix and current repository metadata. The paired Chinese document is an annotated translation and reorganization.
