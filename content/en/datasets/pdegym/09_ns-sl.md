---
title: "NS-SL: Random Double Shear Layers"
parent_dataset: PDEgym
subset: NS-SL
role: "Downstream task: shear layer"
pde_family: "Incompressible Navier–Stokes / near-inviscid flow"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.incompressible.ShearLayer
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/NS-SL"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: NS-SL
weight: 90
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Double-shear-layer initial conditions with random thickness, shift, and Fourier perturbations."
description: "Double-shear-layer initial conditions with random thickness, shift, and Fourier perturbations."

---

# NS-SL: Random Double Shear Layers

**Description:** Double-shear-layer initial conditions with random thickness, shift, and Fourier perturbations. The double shear layer rapidly undergoes Kelvin–Helmholtz-type roll-up, making it a classic incompressible-flow test of instability, vortex formation, and long rollouts.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.
**Code or software used to generate the data:** AZEBAN; $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **NS-SL** |
| Role | Downstream task: shear layer |
| PDE family | Incompressible Navier–Stokes / near-inviscid flow |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `fluids.incompressible.ShearLayer` |
| Official data page | [NS-SL](https://huggingface.co/datasets/camlab-ethz/NS-SL) |
| Official code | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| Paper | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| License | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## Equation

$$
\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u+\nabla p
=\nu\Delta\mathbf u,\qquad \nabla\cdot\mathbf u=0,
$$

where $\mathbf u=(u_x,u_y)$ is the Cartesian velocity field and $p$ is pressure. In the released PDEgym incompressible-flow simulations, spectral hyperviscosity is used only on sufficiently high Fourier modes. With $N=128$, $m_N=\sqrt N$, and $\varepsilon_N=0.05/N$, the effective viscosity scale is approximately $\nu\simeq4\times10^{-4}$. This is a stabilization choice intended to approximate the inviscid limit; it is not a viscosity sweep in the published data.

$$
u_x^0(x,y)=\begin{cases}
\tanh\!\left(2\pi\frac{y-0.25}{\rho_s}\right),&y+\sigma_\delta(x)\le1/2,\\
\tanh\!\left(2\pi\frac{0.75-y}{\rho_s}\right),&\text{otherwise},
\end{cases}\qquad u_y^0=0,
$$
$$
\sigma_\delta(x)=\xi+\delta\sum_{k=1}^{p}\alpha_k\sin(2\pi kx-\beta_k).
$$

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$[u_x,u_y](0)\mapsto[u_x,u_y](t)$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `velocity: [40000, 21, 2, 128, 128]` |
| Available physical fields | $[u_x,u_y]$. |
| Number of trajectories / samples | **40000** |
| Train / Val / Test | **39640 / 120 / 240** |
| Official repository total file size | **110 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=[0,1]^2$ |
| Initial condition / input | Random double shear layer. |
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
| $p$ | number of perturbation modes; IC / data-distribution parameter | varied per trajectory | $\mathcal U\{7,8,\ldots,12\}$ |
| $\alpha_k$ | mode amplitudes; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0,1]$ |
| $\beta_k$ | mode phases; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0,2\pi]$ |
| $\rho_s$ | shear-layer thickness; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0.08,0.12]$ |
| $\xi$ | global vertical shift; IC / data-distribution parameter | varied per trajectory | $\mathcal U[-0.0625,0.0625]$ |
| $\delta$ | overall perturbation amplitude; IC / data-distribution parameter | fixed | $0.025$ |
| $\nu$ | effective spectral viscosity; PDE/numerical coefficient | fixed | $\simeq4\times10^{-4}$ |

**Summary:** Thickness, shift, mode count, and interface perturbations vary; viscosity and total perturbation amplitude are fixed. Velocity jump and number of layers are also mathematically adjustable.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `velocity: [40000, 21, 2, 128, 128]`
- Raw channels/variables: $[u_x,u_y]$.
- Expected assembled filename: `NS-SL.nc`

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
huggingface-cli download camlab-ethz/NS-SL --repo-type dataset --local-dir ./NS-SL
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./NS-SL
python assemble_data.py --input_dir . --output_file NS-SL.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Largest trajectory count in PDEgym; roll-up creates sharp multiscale vortices and time-accumulating errors.

## Known source discrepancies and reproduction notes

- No additional conflict was found among the paper, official code, and data card for the key fields in this entry.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: NS-SL](https://huggingface.co/datasets/camlab-ethz/NS-SL).
