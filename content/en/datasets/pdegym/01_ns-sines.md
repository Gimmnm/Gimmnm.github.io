---
title: "NS-Sines: Incompressible Flow from Sinusoidal Initial Conditions"
parent_dataset: PDEgym
subset: NS-Sines
role: "Pretraining operator"
pde_family: "Incompressible Navier–Stokes / near-inviscid flow"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.incompressible.Sines
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/NS-Sines"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: NS-Sines
weight: 10
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Two-dimensional incompressible Navier–Stokes trajectories initialized by random sine and cosine Fourier modes."
description: "Two-dimensional incompressible Navier–Stokes trajectories initialized by random sine and cosine Fourier modes."

---

# NS-Sines: Incompressible Flow from Sinusoidal Initial Conditions

**Description:** Two-dimensional incompressible Navier–Stokes trajectories initialized by random sine and cosine Fourier modes. This distribution excites the dynamics with smooth, global, multiscale periodic velocity fields. It is one of the six POSEIDON pretraining operators and supplies representations of transport, vortical structure, and periodic flow.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.
**Code or software used to generate the data:** AZEBAN spectral-hyperviscosity solver; released at $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **NS-Sines** |
| Role | Pretraining operator |
| PDE family | Incompressible Navier–Stokes / near-inviscid flow |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `fluids.incompressible.Sines` |
| Official data page | [NS-Sines](https://huggingface.co/datasets/camlab-ethz/NS-Sines) |
| Official code | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| Paper | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| License | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## Equation

$$
\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u+\nabla p
=\nu\Delta\mathbf u,\qquad \nabla\cdot\mathbf u=0,
$$

where $\mathbf u=(u_x,u_y)$ is the Cartesian velocity field and $p$ is pressure. In the released PDEgym incompressible-flow simulations, spectral hyperviscosity is used only on sufficiently high Fourier modes. With $N=128$, $m_N=\sqrt N$, and $\varepsilon_N=0.05/N$, the effective viscosity scale is approximately $\nu\simeq4\times10^{-4}$. This is a stabilization choice intended to approximate the inviscid limit; it is not a viscosity sweep in the published data.

The initial velocity is
$$
 u_x^0=\sum_{i,j=1}^{p}\frac{\alpha_{ij}}{\sqrt{2\pi(i+j)}}\sin(2\pi ix+\beta_{ij})\sin(2\pi jy+\gamma_{ij}),
$$
$$
 u_y^0=\sum_{i,j=1}^{p}\frac{\alpha_{ij}}{\sqrt{2\pi(i+j)}}\cos(2\pi ix+\beta_{ij})\cos(2\pi jy+\gamma_{ij}).
$$

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$\mathcal S(t;u_x^0,u_y^0)=(u_x(t),u_y(t))$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `velocity: [20000, 21, 3, 128, 128]` |
| Available physical fields | HF card: $[u_x,u_y,\text{passive tracer}]$; the paper task and loader use only the first two channels. |
| Number of trajectories / samples | **20000** |
| Train / Val / Test | **19640 / 120 / 240** |
| Official repository total file size | **82.6 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=[0,1]^2$ |
| Initial condition / input | Random Fourier sine/cosine velocity field. |
| Boundary conditions | Periodic boundary conditions |
| Stored snapshots | 21 |
| Snapshots selected by paper/code | 11 (indices 0,2,…,20) |
| all2all pairs | 66 pairs per trajectory |
| Total time range | $[0,1]$ |
| Stored time separation | $0.05$ |
| Generation software / numerical method | AZEBAN spectral-hyperviscosity solver; released at $128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $\alpha_{ij}$ | Fourier-mode amplitude; IC / data-distribution parameter | varied per trajectory | $\mathcal U[-1,1]$ |
| $\beta_{ij},\gamma_{ij}$ | mode phases; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0,2\pi]$ |
| $p$ | mode cutoff in each direction; IC / data-distribution parameter | fixed | $p=10$ |
| $\nu$ | effective high-mode spectral viscosity; PDE/numerical coefficient | fixed; not swept | $\simeq4\times10^{-4}$ |

**Summary:** Mathematically one may change $\nu$, the mode cutoff $p$, amplitude spectrum, domain scale, or boundary conditions; the release varies only initial-mode amplitudes and phases.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `velocity: [20000, 21, 3, 128, 128]`
- Raw channels/variables: HF card: $[u_x,u_y,\text{passive tracer}]$; the paper task and loader use only the first two channels.
- Expected assembled filename: `NS-Sines.nc`

### Official POSEIDON model interface

- One input/output pair: `[4,128,128] → [4,128,128]`
- Channel definition: $[1,u_x,u_y,0]_{t_i}\to[1,u_x,u_y,0]_{t_j}$; dummy density is one and dummy pressure is zero/masked.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

AZEBAN spectral-hyperviscosity solver; released at $128^2$.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/NS-Sines --repo-type dataset --local-dir ./NS-Sines
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./NS-Sines
python assemble_data.py --input_dir . --output_file NS-Sines.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Smooth but spectrally multiscale; useful for testing periodic transport and vortex interactions.

## Known source discrepancies and reproduction notes

- The HF card lists a third passive-tracer channel, but the official loader explicitly rejects `Sines(tracer=True)`; that channel is not part of the paper-defined NS-Sines operator.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: NS-Sines](https://huggingface.co/datasets/camlab-ethz/NS-Sines).
