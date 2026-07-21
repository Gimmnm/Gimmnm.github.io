---
title: "PDEgym docs"
linkTitle: PDEgym
weight: 50
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
summary: "ETH CAMLab pretraining and downstream operator-learning tasks across fluids, waves, and elliptic PDEs."
description: "ETH CAMLab pretraining and downstream operator-learning tasks across fluids, waves, and elliptic PDEs."
dataset_family: PDEgym
---

# PDEgym Per-Subset Markdown Technical Documentation (English)

Following the information architecture of [The Well’s per-dataset page](https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/), this package provides one Markdown page for every PDEgym **logical task/operator**, enriched with parent-dataset identity, official links, download/assembly commands, raw tensors, model-facing interfaces, adjustable/varied/fixed parameters, code identifiers, and source discrepancy notes.

## Scope

- **21 logical tasks**: 6 pretraining operators and 15 downstream tasks.
- **20 physical data repositories**: NS-PwC and NS-Tracer-PwC share the `NS-PwC` repository and NetCDF file. The Hugging Face PDEgym collection displays 21 items because it also includes the paper entry.
- Chinese pages are in `zh-CN/`; English pages are in `en/`.
- The 20 non-duplicated physical repositories contain **299,088**trajectories/steady samples; counting the tracer view as a separate logical task gives **319,088**.
- Summing the current total-file-size values shown by the 20 official Hugging Face data repositories gives approximately **992.07 GB** (decimal GB, about 0.992 TB). This is not the same as decompressed disk usage or training-cache usage.

## Conventions

1. **Raw file dimensions**are separated from **one model training pair**. Raw trajectories are usually `[N,T,C,H,W]`; the all2all loader returns `[C,H,W] → [C,H,W]` plus lead time, and batching adds `B`.
2. **Mathematically adjustable**, **generator-editable**, and **actually sampled in the release** are distinguished.
3. Source conflicts are preserved rather than guessed away, including Wave-Layer’s 21/15-frame conflict, Wave time calibration, ACE’s $\epsilon$ versus $\epsilon^2$ notation, and raw tracer channels not used by several paper tasks.
4. `.time` is only a long-time-limit wrapper for steady tasks and does not imply a raw physical trajectory.

## Index

| # | Subset | Role | PDE | Count | Raw shape | Official size / note |
|---:|---|---|---|---:|---|---|
| 01 | [NS-Sines](../01_ns-sines/) | Pretraining operator | Incompressible Navier–Stokes / near-inviscid flow | 20000 | velocity: [20000, 21, 3, 128, 128] | 82.6 GB |
| 02 | [NS-Gauss](../02_ns-gauss/) | Pretraining operator | Incompressible Navier–Stokes / near-inviscid flow | 20000 | velocity: [20000, 21, 3, 128, 128] | 82.6 GB |
| 03 | [CE-RP](../03_ce-rp/) | Pretraining operator | Compressible Euler | 10000 | data: [10000, 21, 5, 128, 128] | 68.8 GB |
| 04 | [CE-CRP](../04_ce-crp/) | Pretraining operator | Compressible Euler | 10000 | data: [10000, 21, 5, 128, 128] | 68.8 GB |
| 05 | [CE-KH](../05_ce-kh/) | Pretraining operator | Compressible Euler | 10000 | data: [10000, 21, 5, 128, 128] | 68.8 GB |
| 06 | [CE-Gauss](../06_ce-gauss/) | Pretraining operator | Compressible Euler | 10000 | data: [10000, 21, 5, 128, 128] | 68.8 GB |
| 07 | [NS-PwC](../07_ns-pwc/) | Downstream task: new initial-condition distribution | Incompressible Navier–Stokes / near-inviscid flow | 20000 | velocity: [20000, 21, 3, 128, 128] | 82.6 GB (shared with NS-Tracer-PwC) |
| 08 | [NS-BB](../08_ns-bb/) | Downstream task: rough random initial conditions | Incompressible Navier–Stokes / near-inviscid flow | 20000 | velocity: [20000, 21, 3, 128, 128] | 82.6 GB |
| 09 | [NS-SL](../09_ns-sl/) | Downstream task: shear layer | Incompressible Navier–Stokes / near-inviscid flow | 40000 | velocity: [40000, 21, 2, 128, 128] | 110 GB |
| 10 | [NS-SVS](../10_ns-svs/) | Downstream task: sinusoidal vortex sheet | Incompressible Navier–Stokes / near-inviscid flow | 20000 | velocity: [20000, 21, 3, 128, 128] | 82.6 GB |
| 11 | [NS-Tracer-PwC](../11_ns-tracer-pwc/) | Downstream task: added passive-scalar physics | Incompressible Navier–Stokes + advection–diffusion | 20000 | velocity: [20000, 21, 3, 128, 128] (shared NS-PwC file) | No additional storage; shares the 82.6 GB NS-PwC repository |
| 12 | [FNS-KF](../12_fns-kf/) | Downstream task: added external forcing | Forced incompressible Navier–Stokes | 20000 | solution: [20000, 21, 2, 128, 128] | 55.1 GB |
| 13 | [CE-RPUI](../13_ce-rpui/) | Downstream task: new interface distribution | Compressible Euler | 10000 | data: [10000, 21, 5, 128, 128] | 68.8 GB |
| 14 | [CE-RM](../14_ce-rm/) | Downstream task: shock–interface instability | Compressible Euler | 1260 | solution: [1260, 21, 5, 128, 128] | 8.67 GB |
| 15 | [GCE-RT](../15_gce-rt/) | Downstream task: added gravity source and physical parameters | Compressible Euler with gravity | 1260 | solution: [1260, 11, 6, 128, 128] | 5.45 GB |
| 16 | [Wave-Gauss](../16_wave-gauss/) | Downstream task: per-sample PDE coefficient | Variable-coefficient wave equation | 10512 | solution: [10512, 15, 128, 128]; c: [10512, 128, 128] | 11.7 GB |
| 17 | [Wave-Layer](../17_wave-layer/) | Downstream task: layered discontinuous PDE coefficient | Variable-coefficient wave equation | 10512 | solution: [10512, 15, 128, 128]; c: [10512, 128, 128] | 15.2 GB |
| 18 | [ACE](../18_ace/) | Downstream task: new PDE and phase-transition physics | Allen–Cahn reaction–diffusion | 15000 | solution: [15000, 20, 128, 128] | 19.7 GB |
| 19 | [SE-AF](../19_se-af/) | Downstream task: steady geometry-conditioned operator | Steady compressible Euler | 10869 | solution: [10869, 2, 128, 128] | 1.43 GB |
| 20 | [Poisson-Gauss](../20_poisson-gauss/) | Downstream task: steady elliptic operator | Poisson equation | 20000 | source: [20000,128,128]; solution: [20000,128,128] | 2.62 GB |
| 21 | [Helmholtz](../21_helmholtz/) | Downstream task: steady coefficient operator | Helmholtz equation | 19675 | HDF5: 19675 groups Sample_i, each with a[128,128], scalar bc, u[128,128] | 5.2 GB |

## Additional files

- [`manifest.json`](manifest.json): machine-readable index.
- [`manifest.csv`](manifest.csv): tabular index.
- [`TEMPLATE_zh-CN.md`](TEMPLATE_zh-CN.md): reusable Chinese template.
- [`TEMPLATE_en.md`](TEMPLATE_en.md): reusable English template.
- [`SOURCES.md`](SOURCES.md): common sources and version notes.
