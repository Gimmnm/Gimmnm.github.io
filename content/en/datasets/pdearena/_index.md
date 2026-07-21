---
title: "PDEArena Equation Documentation Index"
dataset_family: PDEArena
dataset_release: PDEArena
equation: multiple
spatial_dimension: 0
coordinate_system: multiple
task_variant: catalog
official_status: "documentation index"
license: MIT
last_verified: 2026-07-21
linkTitle: PDEArena
weight: 30
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
summary: "Operator-learning PDE benchmark covering Navier–Stokes, shallow water, Maxwell-3D, and KS."
description: "Operator-learning PDE benchmark covering Navier–Stokes, shallow water, Maxwell-3D, and KS."
---

# PDEArena Equation Documentation Index

This collection follows the organization of a [The Well per-dataset page](https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/) and adds YAML front matter, dataset affiliation, release status, download instructions, explicit model tensors, parameter classifications, and version notes for a multi-benchmark catalog.

## Documents

| Document | System/task | Status | Size |
|---|---|---|---:|
| [Standard Navier--Stokes](../navier_stokes_2d_standard/) | 2D incompressible NS + scalar | official PDEArena release | 43 GB |
| [Conditioned Navier--Stokes](../navier_stokes_2d_conditioned/) | buoyancy/time conditioned | official PDEArena release | 81.7 GB |
| [Shallow water, velocity](../shallow_water_2d_velocity/) | 1-day/2-day, 3 channels | official release/task view | 124 GB shared |
| [Shallow water, vorticity](../shallow_water_2d_vorticity/) | 2-day, 2 scalar channels | view of same release | no additional size |
| [Maxwell-3D](../maxwell_3d/) | 3D electromagnetic fields | official PDEArena extension | 121 GB |
| [Kuramoto--Sivashinsky-1D](../kuramoto_sivashinsky_1d/) | fixed/conditional viscosity | external data supported by loader | 3.92 GB |

## Current four PDEArena Hugging Face releases

| Release | train/valid/test | Total | Size |
|---|---:|---:|---:|
| NavierStokes-2D | 5,200/1,300/1,300 | 7,800 | 43 GB |
| NavierStokes-2D-conditoned | 6,656/1,664/1,664 | 9,984 | 81.7 GB |
| ShallowWater-2D | 5,600/1,400/1,400 | 8,400 | 124 GB |
| Maxwell-3D | 6,400/1,600/1,600 | 9,600 | 121 GB |
| **Total**|  | **35,784**| **369.7 GB** |

Shallow-water velocity/vorticity and 1-day/2-day views reuse one release. KS is counted separately because it is not currently listed under the PDEArena Hugging Face organization.
