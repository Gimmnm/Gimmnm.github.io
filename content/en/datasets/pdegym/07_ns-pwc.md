---
title: "NS-PwC: Piecewise-Constant Vorticity Initial Conditions"
parent_dataset: PDEgym
subset: NS-PwC
role: "Downstream task: new initial-condition distribution"
pde_family: "Incompressible Navier–Stokes / near-inviscid flow"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.incompressible.PiecewiseConstants
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/NS-PwC"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: NS-PwC
weight: 70
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: 'The initial vorticity is piecewise constant on a $10\times10$ grid, after which the velocity is recovered and evolved.'
description: 'The initial vorticity is piecewise constant on a $10\times10$ grid, after which the velocity is recovered and evolved.'

---

# NS-PwC: Piecewise-Constant Vorticity Initial Conditions

> **One-line description:** The initial vorticity is piecewise constant on a $10\times10$ grid, after which the velocity is recovered and evolved.

## Longer description

This task resembles many simultaneous Riemann discontinuities in vorticity and tests transfer to rough, out-of-pretraining initial data.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.  
**Code or software used to generate the data:** AZEBAN; $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **NS-PwC** |
| Role | Downstream task: new initial-condition distribution |
| PDE family | Incompressible Navier–Stokes / near-inviscid flow |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `fluids.incompressible.PiecewiseConstants` |
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

$$
\omega_0(x,y)=c_{ij},\qquad (x,y)\in[x_{i-1},x_i]\times[y_{j-1},y_j],\qquad x_i=y_i=i/10.
$$

The initial velocity is recovered from vorticity and incompressibility.

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$[u_x,u_y](0)\mapsto[u_x,u_y](t)$; this logical task does not read the tracer.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `velocity: [20000, 21, 3, 128, 128]` |
| Available physical fields | $[u_x,u_y,c_{tr}]$; the same physical file also serves NS-Tracer-PwC. |
| Number of trajectories / samples | **20000** |
| Train / Val / Test | **19640 / 120 / 240** |
| Official repository total file size | **82.6 GB (shared with NS-Tracer-PwC)** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=[0,1]^2$ |
| Initial condition / input | $10\times10$ piecewise-constant vorticity. |
| Boundary conditions | Periodic boundary conditions |
| Stored snapshots | 21 |
| Snapshots selected by paper/code | 8 (indices 0,2,…,14) |
| all2all pairs | 36 pairs per trajectory |
| Total time range | $[0,1]$; paper benchmark horizon $[0,0.7]$ |
| Stored time separation | $0.05$ raw; selected interval $0.1$ |
| Generation software / numerical method | AZEBAN; $128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $c_{ij}$ | initial vorticity in each cell; IC / data-distribution parameter | varied by cell and trajectory | $\mathcal U[-1,1]$ |
| $p$ | partition count per direction; IC / data-distribution parameter | fixed | $10$ |
| $\nu$ | effective spectral viscosity; PDE/numerical coefficient | fixed | $\simeq4\times10^{-4}$ |

**Summary:** The partition count, vorticity range, viscosity, and boundary conditions are adjustable; the release varies only $c_{ij}$.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `velocity: [20000, 21, 3, 128, 128]`
- Raw channels/variables: $[u_x,u_y,c_{tr}]$; the same physical file also serves NS-Tracer-PwC.
- Expected assembled filename: `NS-PwC.nc`

### Official POSEIDON model interface

- One input/output pair: `[4,128,128] → [4,128,128]`
- Channel definition: $[1,u_x,u_y,0]_{t_i}\to[1,u_x,u_y,0]_{t_j}$.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

AZEBAN; $128^2$.

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

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Rough piecewise-constant vorticity creates many small interfaces and complex vortex interactions.

## Known source discrepancies and reproduction notes

- NS-PwC and NS-Tracer-PwC share the same repository and NetCDF file; do not double-count storage.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: NS-PwC](https://huggingface.co/datasets/camlab-ethz/NS-PwC).
5. The page structure is inspired by [The Well dataset documentation](https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/), while the content is grounded in the PDEgym paper, code, and data cards.

## Citation

```bibtex
@misc{herde2024poseidon,
  title        = {POSEIDON: Efficient Foundation Models for PDEs},
  author       = {Maximilian Herde and Bogdan Raoni\'{c} and Tobias Rohner and
                  Roger K\"appeli and Roberto Molinaro and Emmanuel de B\'{e}zenac
                  and Siddhartha Mishra},
  year         = {2024},
  eprint       = {2405.19101},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG}
}
```
