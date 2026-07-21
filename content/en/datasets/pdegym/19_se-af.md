---
title: "SE-AF: Airfoil Geometry to Steady Euler Density"
parent_dataset: PDEgym
subset: SE-AF
role: "Downstream task: steady geometry-conditioned operator"
pde_family: "Steady compressible Euler"
spatial_dimension: 2
time_dependent: false
official_code_identifier: fluids.compressible.steady.Airfoil(.time)
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/SE-AF"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: SE-AF
weight: 190
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Maps the shape mask of a randomly Hicks–Henne-perturbed airfoil to the steady compressible-Euler density field."
description: "Maps the shape mask of a randomly Hicks–Henne-perturbed airfoil to the steady compressible-Euler density field."

---

# SE-AF: Airfoil Geometry to Steady Euler Density

**Description:** Maps the shape mask of a randomly Hicks–Henne-perturbed airfoil to the steady compressible-Euler density field. This is not trajectory prediction but a steady geometry-to-field operator. The original solve uses a body-fitted elliptic mesh and is then interpolated to a Cartesian grid.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.
**Code or software used to generate the data:** NEWTUN/NUWTUN steady Euler solver; body-fitted $243\times43$ mesh interpolated to $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **SE-AF** |
| Role | Downstream task: steady geometry-conditioned operator |
| PDE family | Steady compressible Euler |
| Spatial dimension | 2-D |
| Time dependent | No (steady) |
| Official code identifier | `fluids.compressible.steady.Airfoil(.time)` |
| Official data page | [SE-AF](https://huggingface.co/datasets/camlab-ethz/SE-AF) |
| Official code | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| Paper | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| License | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## Equation

$$
\partial_t\mathbf U+\nabla\cdot\mathbf F(\mathbf U)=0,
\qquad \mathbf U=(\rho,\rho\mathbf v,E)^\top,
$$
$$
\mathbf F(\mathbf U)=\left(\rho\mathbf v,
\rho\mathbf v\otimes\mathbf v+pI,(E+p)\mathbf v\right)^\top,
\qquad E=\frac12\rho\lVert\mathbf v\rVert^2+\frac{p}{\gamma-1}.
$$

Here $\rho$ is density, $\mathbf v=(v_x,v_y)$ is velocity, $p$ is pressure, and $E$ is total energy. Unless stated otherwise, the PDEgym compressible-Euler datasets use the ideal-gas value $\gamma=1.4$.

At steady state $\partial_t\mathbf U=0$. Fifteen Hicks–Henne bumps are added to each surface of the RAE2822 reference airfoil:
$$
y^{L/U}(\xi)=y_{ref}^{L/U}(\xi)+\sum_{i=1}^{15}a_i^{L/U}B_i(\xi),\qquad B_i(\xi)=\sin^3(\pi\xi^{q_i}).
$$
The input is the airfoil indicator $f=\chi_S$ and the output is steady density $\rho$.

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$f(x,y)=\chi_S(x,y)\mapsto\rho_{steady}(x,y)$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `solution: [10869, 2, 128, 128]` |
| Available physical fields | Channel 1 is the airfoil shape mask and channel 2 is density. |
| Number of trajectories / samples | **10869** |
| Train / Val / Test | **10509 / 120 / 240** |
| Official repository total file size | **1.43 GB** |
| Grid type | Original $243\times43$ body-fitted elliptic mesh; released on a $128^2$ Cartesian grid |
| Spatial domain | $D=[-0.75,1.75]^2$ after interpolation |
| Initial condition / input | Steady problem with no time initial condition; the input is a geometry shape function. |
| Boundary conditions | Fixed free-stream boundary conditions with a solid airfoil boundary |
| Stored snapshots | steady (2 fields, no time axis) |
| Snapshots selected by paper/code | not applicable; `.time` wrapper assigns normalized lead time 1 |
| all2all pairs | not a physical trajectory pairing |
| Total time range | steady state |
| Stored time separation | not applicable |
| Generation software / numerical method | NEWTUN/NUWTUN steady Euler solver; body-fitted $243\times43$ mesh interpolated to $128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $\psi\in[0,1]^{30}$ | 30 Hicks–Henne bump parameters; geometry parameter | varied per sample | uniform on $[0,1]^{30}$ |
| $M_\infty$ | free-stream Mach number; physical parameter | fixed | $0.729$ |
| $\alpha$ | angle of attack; physical parameter | fixed | $2.31^\circ$ |
| $T_\infty$ | free-stream temperature; physical parameter | fixed | $1$ |
| $p_\infty$ | free-stream pressure; physical parameter | fixed | $1$ |
| reference airfoil | reference airfoil; geometry parameter | fixed | RAE2822 |

**Summary:** Mach number, angle of attack, free-stream state, airfoil family, and bump ranges are adjustable; the release sweeps only the 30-dimensional geometry.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `solution: [10869, 2, 128, 128]`
- Raw channels/variables: Channel 1 is the airfoil shape mask and channel 2 is density.
- Expected assembled filename: `SE-AF.nc`

### Official POSEIDON model interface

- One input/output pair: `[1,128,128] → [1,128,128]`
- Channel definition: shape mask $\to$ density; the official pixel mask excludes the airfoil interior, where density is set to one.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

NEWTUN/NUWTUN steady Euler solver; body-fitted $243\times43$ mesh interpolated to $128^2$.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/SE-AF --repo-type dataset --local-dir ./SE-AF
```

The official card publishes this as an already assembled file and does not require `assemble_data.py`.

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Non-Cartesian source geometry, interpolation to a regular grid, and geometry-conditioned transonic steady flow.

## Known source discrepancies and reproduction notes

- The paper describes 30 bump parameters; the displayed indexing for upper/lower surfaces is easy to misread, so exact geometry generation should follow official data/code.
- Training and evaluation error is computed only outside the airfoil.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: SE-AF](https://huggingface.co/datasets/camlab-ethz/SE-AF).
