---
title: "NS-BB: Brownian-Bridge Rough Random Initial Conditions"
parent_dataset: PDEgym
subset: NS-BB
role: "Downstream task: rough random initial conditions"
pde_family: "Incompressible Navier–Stokes / near-inviscid flow"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.incompressible.BrownianBridge
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/NS-BB"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: NS-BB
weight: 80
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Brownian-bridge random fields are generated in Fourier space, pre-evolved from $t=-0.5$ to 0, and then used as initial data."
description: "Brownian-bridge random fields are generated in Fourier space, pre-evolved from $t=-0.5$ to 0, and then used as initial data."

---

# NS-BB: Brownian-Bridge Rough Random Initial Conditions

**Description:** Brownian-bridge random fields are generated in Fourier space, pre-evolved from $t=-0.5$ to 0, and then used as initial data. This construction provides rougher turbulence-like random fields than smooth Fourier initial conditions and tests statistical-flow learning and robustness to low-regularity inputs.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.
**Code or software used to generate the data:** AZEBAN; $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **NS-BB** |
| Role | Downstream task: rough random initial conditions |
| PDE family | Incompressible Navier–Stokes / near-inviscid flow |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `fluids.incompressible.BrownianBridge` |
| Official data page | [NS-BB](https://huggingface.co/datasets/camlab-ethz/NS-BB) |
| Official code | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| Paper | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| License | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## Equation

$$
\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u+\nabla p
=\nu\Delta\mathbf u,\qquad \nabla\cdot\mathbf u=0,
$$

where $\mathbf u=(u_x,u_y)$ is the Cartesian velocity field and $p$ is pressure. In the released PDEgym incompressible-flow simulations, spectral hyperviscosity is used only on sufficiently high Fourier modes. With $N=128$, $m_N=\sqrt N$, and $\varepsilon_N=0.05/N$, the effective viscosity scale is approximately $\nu\simeq4\times10^{-4}$. This is a stabilization choice intended to approximate the inviscid limit; it is not a viscosity sweep in the published data.

The Brownian bridge is built in Fourier space with $\lVert k\rVert_2^{-3/2}$ decay and random sine/cosine combinations. It is pre-evolved by the discrete Navier–Stokes system from $t=-0.5$ to $t=0$; the resulting velocity is the recorded trajectory initial condition.

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$[u_x,u_y](0)\mapsto[u_x,u_y](t)$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `velocity: [20000, 21, 3, 128, 128]` |
| Available physical fields | The HF card lists $[u_x,u_y,\text{passive tracer}]$; the official paper task and loader use only velocity. |
| Number of trajectories / samples | **20000** |
| Train / Val / Test | **19640 / 120 / 240** |
| Official repository total file size | **82.6 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=[0,1]^2$ |
| Initial condition / input | Pre-evolved Brownian-bridge velocity fields. |
| Boundary conditions | Periodic boundary conditions |
| Stored snapshots | 21 |
| Snapshots selected by paper/code | 8 (indices 0,2,…,14) |
| all2all pairs | 36 pairs per trajectory |
| Total time range | $[0,1]$; benchmark horizon $[0,0.7]$ |
| Stored time separation | $0.05$ raw; selected interval $0.1$ |
| Generation software / numerical method | AZEBAN; $128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $\alpha_k^{(mn\ell)}$ | random Fourier coefficients; IC / data-distribution parameter | varied per trajectory | $\mathcal U[-1,1]$ |
| $3/2$ | spectral decay exponent; IC / data-distribution parameter | fixed | $3/2$ |
| pre-evolution | pre-evolution interval; IC / data-distribution parameter | fixed | $[-0.5,0]$ |
| $\nu$ | effective spectral viscosity; PDE/numerical coefficient | fixed | $\simeq4\times10^{-4}$ |

**Summary:** The spectral/Hurst exponent, pre-evolution time, viscosity, and coefficient distribution are adjustable; the release varies only the Fourier coefficients.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `velocity: [20000, 21, 3, 128, 128]`
- Raw channels/variables: The HF card lists $[u_x,u_y,\text{passive tracer}]$; the official paper task and loader use only velocity.
- Expected assembled filename: `NS-BB.nc`

### Official POSEIDON model interface

- One input/output pair: `[4,128,128] → [4,128,128]`
- Channel definition: $[1,u_x,u_y,0]$.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

AZEBAN; $128^2$.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/NS-BB --repo-type dataset --local-dir ./NS-BB
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./NS-BB
python assemble_data.py --input_dir . --output_file NS-BB.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Low-regularity, broadband random initial data are more demanding for long-horizon errors and statistics.

## Known source discrepancies and reproduction notes

- The official loader explicitly disallows BrownianBridge tracer mode although the HF card lists a third channel.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: NS-BB](https://huggingface.co/datasets/camlab-ethz/NS-BB).
