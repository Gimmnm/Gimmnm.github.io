---
title: "NS-Tracer-PwC: Passive-Scalar Transport in Incompressible Flow"
parent_dataset: PDEgym
subset: NS-Tracer-PwC
role: "Downstream task: added passive-scalar physics"
pde_family: "Incompressible Navier–Stokes + advection–diffusion"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.incompressible.PiecewiseConstants.tracer
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/NS-PwC"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: NS-Tracer-PwC
weight: 110
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "An NS-PwC velocity field drives a passive concentration through one-way coupled advection–diffusion."
description: "An NS-PwC velocity field drives a passive concentration through one-way coupled advection–diffusion."

---

# NS-Tracer-PwC: Passive-Scalar Transport in Incompressible Flow

**Description:** An NS-PwC velocity field drives a passive concentration through one-way coupled advection–diffusion. This task adds a new physical variable and equation to the pretraining fluid dynamics. The tracer is transported by the flow without feedback, representing a pollutant or dye.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.
**Code or software used to generate the data:** Velocity generated with AZEBAN; the passive scalar is stored with the same flow.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **NS-Tracer-PwC** |
| Role | Downstream task: added passive-scalar physics |
| PDE family | Incompressible Navier–Stokes + advection–diffusion |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `fluids.incompressible.PiecewiseConstants.tracer` |
| Official data page | [NS-PwC](https://huggingface.co/datasets/camlab-ethz/NS-PwC) |
| Official code | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| Paper | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| License | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## Equation

$$
\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u+\nabla p
=\nu\Delta\mathbf u,\qquad \nabla\cdot\mathbf u=0,
$$

where $\mathbf u=(u_x,u_y)$ is the Cartesian velocity field and $p$ is pressure. In the released PDEgym incompressible-flow simulations, spectral hyperviscosity is used only on sufficiently high Fourier modes. With $N=128$, $m_N=\sqrt N$, and $\varepsilon_N=0.05/N$, the effective viscosity scale is approximately $\nu\simeq4\times10^{-4}$. This is a stabilization choice intended to approximate the inviscid limit; it is not a viscosity sweep in the published data.

The passive scalar $c$ satisfies
$$
\partial_t c+\mathbf u\cdot\nabla c=\kappa\Delta c.
$$
Its initial condition is the central disk
$$
c_0(x,y)=\mathbf 1_{B_{1/4}(1/2,1/2)}(x,y).
$$

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$[u_x,u_y,c](0)\mapsto[u_x,u_y,c](t)$ with one-way coupling.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `velocity: [20000, 21, 3, 128, 128] (shared NS-PwC file)` |
| Available physical fields | $[u_x,u_y,c]$. |
| Number of trajectories / samples | **20000** |
| Train / Val / Test | **19640 / 120 / 240** |
| Official repository total file size | **No additional storage; shares the 82.6 GB NS-PwC repository** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=[0,1]^2$ |
| Initial condition / input | Velocity initial data as in NS-PwC; fixed central-disk tracer. |
| Boundary conditions | Periodic boundaries for velocity and concentration |
| Stored snapshots | 21 |
| Snapshots selected by paper/code | 8 (indices 0,2,…,14) |
| all2all pairs | 36 pairs per trajectory |
| Total time range | $[0,1]$; benchmark horizon $[0,0.7]$ |
| Stored time separation | $0.05$ raw; selected interval $0.1$ |
| Generation software / numerical method | Velocity generated with AZEBAN; the passive scalar is stored with the same flow. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $c_{ij}$ | NS-PwC initial vorticity cell values; IC / data-distribution parameter | varied per trajectory | $\mathcal U[-1,1]$ |
| $\kappa$ | tracer diffusivity; PDE coefficient | fixed | set equal to the artificial viscosity scale |
| disk center | tracer-disk center; IC / data-distribution parameter | fixed | $(1/2,1/2)$ |
| disk radius | tracer-disk radius; IC / data-distribution parameter | fixed | $1/4$ |
| tracer amplitude | initial concentration amplitude; IC / data-distribution parameter | fixed | $1$ |

**Summary:** One may change $\kappa$, tracer position/shape/amplitude, add sources/sinks, or introduce two-way coupling; the release varies transport only through random velocity initial data.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `velocity: [20000, 21, 3, 128, 128] (shared NS-PwC file)`
- Raw channels/variables: $[u_x,u_y,c]$.
- Expected assembled filename: `NS-PwC.nc`

### Official POSEIDON model interface

- One input/output pair: `[5,128,128] → [5,128,128]`
- Channel definition: $[1,u_x,u_y,0,c]_{t_i}\to[1,u_x,u_y,0,c]_{t_j}$.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

Velocity generated with AZEBAN; the passive scalar is stored with the same flow.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/NS-PwC --repo-type dataset --local-dir ./NS-PwC
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./NS-PwC
python assemble_data.py --input_dir . --output_file NS-PwC.nc
```

Note: the logical NS-Tracer-PwC task downloads the `NS-PwC` repository and enables `.tracer` in the official loader.

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Requires joint prediction of vector velocity and a scalar with sharp interfaces while respecting one-way coupling.

## Known source discrepancies and reproduction notes

- There is no separate `NS-Tracer-PwC` HF repository; download `camlab-ethz/NS-PwC`.
- The official README mapping has contained the misspelling `incomressible`; use the current selector/config implementation as authoritative.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: NS-PwC](https://huggingface.co/datasets/camlab-ethz/NS-PwC).
