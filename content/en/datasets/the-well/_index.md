---
title: "The Well"
linkTitle: "The Well"
weight: 20
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
math: true
summary: "Polymathic AI's large-scale multi-physics PDE benchmark: 15TB across 16 physical scenarios."
description: "Polymathic AI's large-scale multi-physics PDE benchmark: 15TB across 16 physical scenarios."
dataset_family: "The Well"
---

# The Well: 15TB of Physics Simulations

![The Well](/the-well/the_well_color.svg)

The Well is a large-scale collection of machine learning datasets containing numerical simulations of a wide variety of spatiotemporal physical systems. It provides about **15TB** of data across **16** physical scenarios (biological systems, fluid dynamics, acoustic scattering, magnetohydrodynamics, supernova explosions, and more). Datasets can be used individually or as a broader surrogate-model benchmark suite.

Official site: [polymathic-ai.org/the_well](https://polymathic-ai.org/the_well/). The documentation below follows the official dataset pages; when a downloadable directory is split (e.g. acoustic / Euler / MHD / supernova variants, plus `rayleigh_benard_uniform` and `viscoelastic_instability_v2`), each directory has its own card.

## Dataset catalog

One row per downloadable directory. Numbers prefer the official per-dataset pages when they disagree with the overview table.

| Directory | Resolution | Steps | Trajectories | Size | Status |
|---|---|---:|---:|---:|---|
| [`acoustic_scattering_discontinuous`](./acoustic_scattering_discontinuous/) | 256×256 | 101 | 2000 | 157.7 GB | active |
| [`acoustic_scattering_inclusions`](./acoustic_scattering_inclusions/) | 256×256 | 101 | 4000 | 283.8 GB | active |
| [`acoustic_scattering_maze`](./acoustic_scattering_maze/) | 256×256 | 201 | 2000 | 311.3 GB | active |
| [`active_matter`](./active_matter/) | 256×256 | 81 | 225 | 51.3 GB | active |
| [`convective_envelope_rsg`](./convective_envelope_rsg/) | 256×128×256 | 100 | 29 | 570 GB | active |
| [`euler_multi_quadrants_openBC`](./euler_multi_quadrants_openBC/) | 512×512 | 100 | 5000 | part of 5.17 TB | active |
| [`euler_multi_quadrants_periodicBC`](./euler_multi_quadrants_periodicBC/) | 512×512 | 100 | 5000 | part of 5.17 TB | active |
| [`gray_scott_reaction_diffusion`](./gray_scott_reaction_diffusion/) | 128×128 | 1001 | 1200 | 153.8 GB | active |
| [`helmholtz_staircase`](./helmholtz_staircase/) | 1024×256 | 50 | 512 | 52.4 GB | active |
| [`MHD_64`](./MHD_64/) | 64³ | 100 | 100 | 71.6 GB | active |
| [`MHD_256`](./MHD_256/) | 256³ | 100 | 100 | 4.58 TB | active |
| [`planetswe`](./planetswe/) | 256×512 | 1008 | 120 | 185.8 GB | active |
| [`post_neutron_star_merger`](./post_neutron_star_merger/) | 192×128×66 | 181 | 8 | 110.1 GB | active |
| [`rayleigh_benard`](./rayleigh_benard/) | 512×128 | 200 | 1750 | ~342–358 GB | active |
| [`rayleigh_benard_uniform`](./rayleigh_benard_uniform/) | 512×128 | 200 | 1750 | similar order | active |
| [`rayleigh_taylor_instability`](./rayleigh_taylor_instability/) | 128³ | 119 | 45 | 255.6 GB | active |
| [`shear_flow`](./shear_flow/) | 256×512 | 200 | 1120 | 547 GB | active |
| [`supernova_explosion_64`](./supernova_explosion_64/) | 64³ | 59 | 740 | 268.2 GB | active |
| [`supernova_explosion_128`](./supernova_explosion_128/) | 128³ | 59 | 260 | 754 GB | active |
| [`turbulence_gravity_cooling`](./turbulence_gravity_cooling/) | 64³ | 50 | 2700 | 829.4 GB | active |
| [`turbulent_radiative_layer_2D`](./turbulent_radiative_layer_2D/) | 128×384 | 101 | 90 | 6.9 GB | active |
| [`turbulent_radiative_layer_3D`](./turbulent_radiative_layer_3D/) | 128×128×256 | 101 | 90 | 745 GB | active |
| [`viscoelastic_instability`](./viscoelastic_instability/) | 512×512 | variable | 260 | 66 GB | deprecated |
| [`viscoelastic_instability_v2`](./viscoelastic_instability_v2/) | 512×512 | variable | 260 | ~66 GB | active |

## Shared format

Data live on uniform grids at constant time intervals in self-documenting HDF5 files plus `dataset_name.yaml` metadata. Arrays are `fp32` with conceptual shape `(n_traj, n_steps, coord1, coord2[, coord3])`. Fields are split by tensor order: scalars `t0_fields`, vectors `t1_fields`, tensors `t2_fields`. Default trajectory split is 0.8 / 0.1 / 0.1 for train / val / test.

See the official [data format](https://polymathic-ai.org/the_well/data_format/) page.

## Download and load

```bash
pip install the_well
the-well-download --base-path ./the_well_data --dataset active_matter --split train
```

Omit `--dataset` / `--split` to request the full ~15TB collection.

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="path/to/base",
    well_dataset_name="active_matter",
    well_split_name="train",
)
train_loader = DataLoader(trainset)
for batch in train_loader:
    ...
```

Most datasets can also be streamed from Hugging Face with `well_base_path="hf://datasets/polymathic-ai/"`.

## Generation cost (official overview)

| Dataset | Size (GB) | Run time (h) | Hardware | Software |
|---|---:|---:|---|---|
| `acoustic_discontinuous` | 157 | 0.25 | 64 C | Clawpack |
| `acoustic_inclusions` | 283 | 0.25 | 64 C | Clawpack |
| `acoustic_maze` | 311 | 0.33 | 64 C | Clawpack |
| `active_matter` | 51.3 | 0.33 | A100 GPU | Python |
| `convective_envelope_rsg` | 570 | 1460 | 80 C | Athena++ |
| `euler` | 5170 | 80* | 160 C* | ClawPack |
| `helmholtz_staircase` | 52 | 0.11 | 64 C | Python |
| `MHD_256` | 4580 | 48 | 64 C | Fortran MPI |
| `MHD_64` | 72 | — | — | — |
| `gray_scott_reaction_diffusion` | 154 | 33* | 40 C | Matlab |
| `planetswe` | 186 | 0.75 | 64 C | Dedalus |
| `post_neutron_star_merger` | 110 | 505* | 300 C* | νbhlight |
| `rayleigh_benard` | 358 | 60* | 768 C* | Dedalus |
| `rayleigh_taylor_instability` | 256 | 65* | 128 C* | TurMix3D |
| `shear_flow` | 115† | 5* | 448 C* | Dedalus |
| `supernova_explosion_128` | 754 | 4* | 1040 C* | ASURA-FDPS |
| `supernova_explosion_64` | 268 | 4* | 1040 C* | ASURA-FDPS |
| `turbulence_gravity_cooling` | 829 | 577* | 1040 C* | ASURA-FDPS |
| `turbulent_radiative_layer_2D` | 6.9 | 2* | 48 C | Athena++ |
| `turbulent_radiative_layer_3D` | 745 | 271* | 128 C | Athena++ |
| `viscoelastic_instability` | 66 | 34* | 64 C | Dedalus |

\* Totals over all runs. C = CPU cores. † Overview table value; the [shear_flow](./shear_flow/) page reports **547 GB**.

## Primary sources

- Official docs: <https://polymathic-ai.org/the_well/>
- Overview: <https://polymathic-ai.org/the_well/datasets_overview/>
- Repository: <https://github.com/PolymathicAI/the_well>
- Paper: <https://arxiv.org/abs/2412.00568>
- Hugging Face: <https://huggingface.co/collections/polymathic-ai/the-well>
- Data format: <https://polymathic-ai.org/the_well/data_format/>

Verification date: **2026-07-21**.
