---
title: "Incompressible Shear Flow"
parent_collection: "The Well"
physical_family: "Incompressible Navier–Stokes + tracer"
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/shear_flow/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/shear_flow"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/shear_flow"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: shear_flow
weight: 170
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "A two-dimensional incompressible shear flow is initialized with horizontal layers moving in opposite directions. Kelvin–Helmholtz-type instabilities roll up into vortices and tr…"
description: "A two-dimensional incompressible shear flow is initialized with horizontal layers moving in opposite directions. Kelvin–Helmholtz-type instabilities roll up into vortices and tr…"

---

# Incompressible Shear Flow

![Passive tracer](/the-well/shear_flow__tracer_normalized.gif)


> **Parent collection:** The Well
> **Directory:** `shear_flow`
> **Equation family:** Incompressible Navier–Stokes + tracer

## 1. Scope and physical overview

A two-dimensional incompressible shear flow is initialized with horizontal layers moving in opposite directions. Kelvin–Helmholtz-type instabilities roll up into vortices and transport a passive tracer. Reynolds and Schmidt numbers separately control momentum and tracer diffusion.

The Well treats each downloadable directory as a self-documenting HDF5 dataset.

## 2. Governing equations

$$
\frac{\partial\mathbf u}{\partial t}
-\nu\Delta\mathbf u+\nabla p
=-\mathbf u\cdot\nabla\mathbf u,
\qquad \nabla\cdot\mathbf u=0,
$$
$$
\frac{\partial s}{\partial t}
-D\Delta s=-\mathbf u\cdot\nabla s,
$$
with
$$
\nu=\mathrm{Re}^{-1},\qquad
D=(\mathrm{Re}\,\mathrm{Sc})^{-1}.
$$
Vorticity may be derived as
$$
\omega=\partial_xu_z-\partial_zu_x.
$$

### Variables and physical fields

- \(\mathbf u=(u_x,u_z)\): incompressible velocity.
- \(p\): pressure with zero-mean gauge.
- \(s\): passive tracer.
- \(\nu,D\): momentum and tracer diffusivities.
- \(\mathrm{Re},\mathrm{Sc}\): Reynolds and Schmidt numbers.
- \(\omega\): derived vorticity; it is discussed but not a separate released dynamic target in the standard metadata.

## 3. Parameter audit

| Category | Released-data interpretation |
|---|---|
| Theoretically adjustable | Reynolds and Schmidt numbers, shear-layer count/width/velocity jump, tracer-blob count/shape/location, domain aspect ratio, perturbations, boundary conditions and spectral resolution. |
| Actually varied in this release | Full Cartesian product: \(\mathrm{Re}\in\{10^4,5\times10^4,10^5,5\times10^5\}\), \(\mathrm{Sc}\in\{0.1,0.2,0.5,1,2,5,10\}\), shear-layer count \(n_{\rm shear}\in\{2,4\}\), tracer-blob count \(n_{\rm blobs}\in\{2,3,4,5\}\), and shear-width factor \(w\in\{0.25,0.5,1,2,4\}\). This gives \(4\times7\times2\times4\times5=1120\) trajectories. |
| Fixed in this release | Equation family, periodic-domain setup, released \(256\times512\) resolution, 200 snapshots over \([0,20]\), pressure gauge and the generator's velocity/tracer amplitude conventions. |

## 4. Initial and boundary conditions

### Initial conditions

Alternating horizontal velocity layers plus 2–5 passive-tracer blobs. Layer count and width vary as explicit data axes; other random placements/phases follow the generator.

### Boundary conditions

Documented as a two-dimensional periodic flow; verify per-dimension boundary metadata in the HDF5 file.

## 5. Data specification

| Property | Value |
|---|---|
| Parent collection | The Well |
| Download directory | `shear_flow` |
| Spatial dimension | 2D |
| Coordinate system | Cartesian $(x,z)$ |
| Spatial resolution | $256\times512$ |
| Stored steps per trajectory | 200 |
| Number of trajectories | 1120 |
| Dynamic channels after component expansion | 4 |
| Dynamic fields | passive tracer $s$, pressure $p$, velocity $(u_x,u_z)$ |
| Static fields / scalar context | Reynolds, Schmidt and initialization labels |
| Time range | $[0,20]$ |
| Stored time spacing | $0.1$ |
| Spatial domain | 2D periodic domain |
| Estimated release size | 547 GB |
| Storage | HDF5, shared The Well schema, released arrays in fp32 |
| Default split convention | Usually 80/10/10 over trajectories/initial conditions; small-trajectory datasets may use blocked time segments. Inspect the downloaded metadata. |

### Raw and model-facing shapes

The raw HDF5 schema stores scalar, vector and tensor fields separately. A typical dynamic scalar field has conceptual shape

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

while vector/tensor fields append their component axes. `WellDataset` can flatten physical components into a final channel axis. With batch size \(B\), this directory is represented conceptually as:

- full sequence: \((B,T,L_1,L_2,4)\);
- standard 4-frame history: \((B,4,L_1,L_2,4)\);
- standard 1-frame target: \((B,1,L_1,L_2,4)\).

The order of fields/components should be read from the HDF5 metadata rather than inferred from this conceptual list. Time-independent geometry/coefficient fields are normally model inputs but not prediction targets.

## 6. Numerical generation

**Documented solver:** Dedalus mixed Fourier–Chebyshev pseudo-spectral method with adaptive time stepping

Dedalus solves the PDEs with a mixed Fourier–Chebyshev pseudo-spectral discretization and adaptive time stepping. The current dataset metadata should be preferred over early documentation that listed a smaller resolution/size or mislabeled one parameter.

## 7. Recommended ML tasks and diagnostics

Turbulent-transition forecasting, tracer transport, parameter generalization over \((\mathrm{Re},\mathrm{Sc})\), sensitivity to shear geometry, vorticity/spectral diagnostics and stable rollouts.

Useful evaluation should go beyond aggregate RMSE when possible: report per-field errors, long-rollout stability, conservation or balance diagnostics, and spectral/scale-resolved error for turbulent or wave systems.

## 8. Version reconciliation and cautions

Current metadata gives \(256\times512\), 1120 trajectories and roughly 547 GB. Earlier text variants contained a \(128\times256\)/115 GB description or mislabeled a parameter as Rayleigh; those are not the current released tensor specification.

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
the-well-download --base-path ./the_well_data --dataset shear_flow --split train
```

Download all standard splits:

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset shear_flow --split "$split"
done
```

Omitting both `--dataset` and `--split` requests the full collection and should not be done accidentally because The Well is about 15 TB.

### Load local data

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="shear_flow",
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
    well_dataset_name="shear_flow",
    well_split_name="train",
)
```

For large training runs, local download is normally faster and more reproducible than network streaming.

### Other distribution route

The paper also describes direct Flatiron-hosted distribution and a Globus endpoint. Endpoint details can change, so use the current repository/download documentation rather than hard-coding an old endpoint.

## 9. Links

| Resource | URL |
|---|---|
| Official dataset page | <https://polymathic-ai.org/the_well/datasets/shear_flow/> |
| Repository directory | <https://github.com/PolymathicAI/the_well/tree/master/datasets/shear_flow> |
| Hugging Face dataset | <https://huggingface.co/datasets/polymathic-ai/shear_flow> |
| The Well repository | <https://github.com/PolymathicAI/the_well> |
| Paper | <https://arxiv.org/abs/2412.00568> |
| Data-format documentation | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face collection | <https://huggingface.co/collections/polymathic-ai/the-well> |
