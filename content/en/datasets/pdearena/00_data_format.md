---
title: "Data format"
linkTitle: "data format"
weight: 5
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "PDEArena storage: HDF5 / Zarr, field keys, splits, and model tensors."
description: "PDEArena storage: HDF5 / Zarr, field keys, splits, and model tensors."
---

# Data format

This page follows the official [`docs/data.md`](https://github.com/pdearena/pdearena/blob/main/docs/data.md) / [`docs/datadownload.md`](https://github.com/pdearena/pdearena/blob/main/docs/datadownload.md), and the current Hugging Face layouts. Each equation card also lists concrete naming and sizes.

## Releases and splits

- Data are hosted under [Hugging Face `pdearena`](https://huggingface.co/pdearena); download with `git lfs` + `git clone`.
- Four organization releases: `NavierStokes-2D`, `NavierStokes-2D-conditoned` (missing an `i`), `ShallowWater-2D`, `Maxwell-3D`.
- Splits are usually `train` / `valid` / `test`. NS and Maxwell ship as flat directories of per-seed `.h5` shards; shallow water uses `train|valid|test/seed=*` directories (Zarr after NetCDF conversion).

## Storage by task

| Task | Format | Typical state keys | Notes |
|---|---|---|---|
| Navier–Stokes 2D | HDF5 (`.h5`) | `u`, `vx`, `vy` | plus `t`,`x`,`y`,`dt`,`dx`,`dy`,`buo_y` |
| ShallowWater-2D | NetCDF → Zarr | pressure/free-surface + winds | ships `normstats.pt`; vorticity derived from winds |
| Maxwell-3D | HDF5 | `d_field`, `h_field` | generator writes `E`/`H` into these keys |
| KS-1D | HDF5 | `pde_*` solution array | plus `dt`,`dx`; conditional files carry viscosity |

## Arrays and model tensors

Raw 2D trajectories are often written

\[
U\in\mathbb{R}^{N\times T\times C\times H\times W},
\]

and 3D as $N\times T\times C\times D\times H\times W$. A full trajectory is not a fixed network input; training slices history frames → future frames per task config (e.g. standard NS often 4→1, shallow water 2→1, conditioned NS often 1→1).

## Naming (summary)

- Standard NS: `NavierStokes2D_{split}_{seed}_0.50000.h5`
- Conditioned NS: `NavierStokes2D_{split}_{seed}_{buoyancy}[_{n}].h5`
- Maxwell: `Maxwell3D_{split}_{seed}.h5`
- Shallow water: `{split}/seed={seed}/` (Zarr groups)
- KS (external): `KS_{split}_{fixed|conditional}_viscosity.h5`

After download, verify `shape`, keys and metadata; do not infer resolution or $\Delta t$ from filenames alone.

## Primary sources

- [PDEArena paper](https://arxiv.org/abs/2209.15616)
- [Official repository](https://github.com/pdearena/pdearena)
- [Data generation docs](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Download docs](https://github.com/pdearena/pdearena/blob/main/docs/datadownload.md)
