---
title: "The Well documentation"
linkTitle: "The Well"
weight: 5
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
summary: "Polymathic AI's large-scale multi-physics PDE benchmark spanning acoustics, fluids, MHD, supernovae, and more."
description: "Polymathic AI's large-scale multi-physics PDE benchmark spanning acoustics, fluids, MHD, supernovae, and more."
dataset_family: "The Well"
---

# The Well — bilingual per-equation dataset documentation

This package contains **24 English dataset pages**and **24 paired Chinese pages**. It follows the current repository directory structure, while preserving the paper's interpretation of The Well as 16 physical scenarios. The official website currently exposes 23 dataset pages; the repository additionally contains the corrected `viscoelastic_instability_v2` directory.

## What each page contains

Each file is designed to be reused in a larger PDE/dynamics dataset catalog. It includes:

- parent collection, slug, licenses, official/repository/Hugging Face links;
- physical overview and governing equations;
- variable definitions and channel accounting;
- a three-level parameter audit: theoretically adjustable, actually varied, fixed;
- initial and boundary conditions;
- coordinate system, resolution, trajectory count, sequence length, fields and release size;
- raw HDF5 and model-facing input/output shape conventions;
- generation software and numerical method;
- download commands, local loading and Hub streaming status;
- ML tasks, version discrepancies and cautions.

## Documentation policy

The English files are **source-faithful structured rewrites**, not byte-for-byte copies of the website. The Chinese files are annotated translations and reconciliations. Equations and parameter values are checked against the official dataset pages, the current repository metadata and Appendix C of the paper. Where sources disagree, the disagreement is retained instead of silently choosing a value.

## Directory layout

```text
the_well_markdown_docs/
├── README.md
├── README.zh-CN.md
├── MANIFEST.md
├── SOURCE_NOTES.md
├── TEMPLATE.en.md
├── TEMPLATE.zh-CN.md
├── en/       # 24 English dataset pages
└── zh-CN/    # 24 Chinese dataset pages
```

## Dataset index

| Directory | Equation family | Grid | Steps | Trajectories | Channels | Size | Status |
|---|---|---:|---:|---:|---:|---:|---|
| [`acoustic_scattering_discontinuous`](../acoustic_scattering_discontinuous/) | Variable-coefficient acoustics | $256\times256$ | 101 | 2000 | 3 | 157.7 GB | active |
| [`acoustic_scattering_inclusions`](../acoustic_scattering_inclusions/) | Variable-coefficient acoustics | $256\times256$ | 101 | 4000 | 3 | 283.8 GB | active |
| [`acoustic_scattering_maze`](../acoustic_scattering_maze/) | Variable-coefficient acoustics | $256\times256$ | 201 | 2000 | 3 | 311.3 GB | active |
| [`active_matter`](../active_matter/) | Active-fluid kinetic theory | $256\times256$ | 81 | 225 (current parameter product; paper table reports 360) | 11 | 51.3 GB | active |
| [`convective_envelope_rsg`](../convective_envelope_rsg/) | Radiation hydrodynamics | $256\times128\times256$ | 100 | 29 temporal cuts | 6 | 570 GB | active |
| [`euler_multi_quadrants_openBC`](../euler_multi_quadrants_openBC/) | Compressible inviscid Euler equations | $512\times512$ | 100 | 5000 | 5 | part of 5.17 TB combined Euler release | active |
| [`euler_multi_quadrants_periodicBC`](../euler_multi_quadrants_periodicBC/) | Compressible inviscid Euler equations | $512\times512$ | 100 | 5000 | 5 | part of 5.17 TB combined Euler release | active |
| [`gray_scott_reaction_diffusion`](../gray_scott_reaction_diffusion/) | Reaction–diffusion | $128\times128$ | 1001 | 1200 | 2 | 153.8 GB | active |
| [`helmholtz_staircase`](../helmholtz_staircase/) | Wave / Helmholtz scattering | $1024\times256$ | 50 | 512 | 2 | 52.4 GB | active |
| [`MHD_64`](../MHD_64/) | Ideal isothermal magnetohydrodynamics | $64^3$ | 100 | 100 | 7 | 71.6 GB | active |
| [`MHD_256`](../MHD_256/) | Ideal isothermal magnetohydrodynamics | $256^3$ | 100 | 100 | 7 | 4.58 TB | active |
| [`planetswe`](../planetswe/) | Rotating spherical shallow-water equations | $256\times512$ | 1008 | 120 ML trajectories (from 40 three-year simulations) | 3 | 185.8 GB | active |
| [`post_neutron_star_merger`](../post_neutron_star_merger/) | General-relativistic MHD + neutrino transport | $192\times128\times66$ | 181 | 8 | 12 | 110.1 GB | active |
| [`rayleigh_benard`](../rayleigh_benard/) | Boussinesq convection | $512\times128$ | 200 | 1750 | 4 | approximately 342–358 GB across documentation versions | active |
| [`rayleigh_benard_uniform`](../rayleigh_benard_uniform/) | Boussinesq convection | $512\times128$ | 200 | 1750 | 4 | not separately reported; similar order to native-grid data | active |
| [`rayleigh_taylor_instability`](../rayleigh_taylor_instability/) | Variable-density miscible flow | $128^3$ | 119 on current dataset page (paper table: 120) | 45 | 4 | 255.6 GB | active |
| [`shear_flow`](../shear_flow/) | Incompressible Navier–Stokes + tracer | $256\times512$ | 200 | 1120 | 4 | 547 GB | active |
| [`supernova_explosion_64`](../supernova_explosion_64/) | Compressible SPH hydrodynamics + cooling | $64^3$ | 59 | 740 | 6 | 268.2 GB | active |
| [`supernova_explosion_128`](../supernova_explosion_128/) | Compressible SPH hydrodynamics + cooling | $128^3$ | 59 | 260 | 6 | 754 GB | active |
| [`turbulence_gravity_cooling`](../turbulence_gravity_cooling/) | Self-gravitating compressible hydrodynamics | $64^3$ | 50 | 2700 | 6 | 829.4 GB | active |
| [`turbulent_radiative_layer_2D`](../turbulent_radiative_layer_2D/) | Compressible hydrodynamics + radiative cooling | $128\times384$ | 101 | 90 | 4 | 6.9 GB | active |
| [`turbulent_radiative_layer_3D`](../turbulent_radiative_layer_3D/) | Compressible hydrodynamics + radiative cooling | $128\times128\times256$ | 101 | 90 | 5 | 745 GB | active |
| [`viscoelastic_instability`](../viscoelastic_instability/) | FENE-P viscoelastic flow | $512\times512$ | 20 or 60 depending on attractor/segment | 260 | 8 | 66 GB | deprecated |
| [`viscoelastic_instability_v2`](../viscoelastic_instability_v2/) | FENE-P viscoelastic flow | $512\times512$ | 20 or 60 depending on attractor/segment | 260 | 8 | approximately 66 GB; not separately tabulated in the paper | active-corrected |

## Shared download command

```bash
pip install the_well
the-well-download --base-path ./the_well_data --dataset active_matter --split train
```

The CLI can download a selected dataset/split. Omitting both selectors requests the full collection, which is approximately 15 TB.

## Primary sources

- Official documentation: <https://polymathic-ai.org/the_well/>
- Repository: <https://github.com/PolymathicAI/the_well>
- Paper: <https://arxiv.org/abs/2412.00568>
- Hugging Face collection: <https://huggingface.co/collections/polymathic-ai/the-well>
- Data format: <https://polymathic-ai.org/the_well/data_format/>

Verification date: **2026-07-21**.
