---
title: "CE-KH: Kelvin–Helmholtz Shear Instability"
parent_dataset: PDEgym
subset: CE-KH
role: "Pretraining operator"
pde_family: "Compressible Euler"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.compressible.KelvinHelmholtz
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/CE-KH"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: CE-KH
weight: 50
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Compressible Kelvin–Helmholtz shear layers with randomly perturbed interfaces."
description: "Compressible Kelvin–Helmholtz shear layers with randomly perturbed interfaces."

---

# CE-KH: Kelvin–Helmholtz Shear Instability

> **One-line description:** Compressible Kelvin–Helmholtz shear layers with randomly perturbed interfaces.

## Longer description

Two fluid layers have different densities and opposite horizontal velocities. Small random interface perturbations trigger roll-up and mixing, supplying a canonical shear instability to pretraining.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.  
**Code or software used to generate the data:** ALSVINN; $512^2\to128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **CE-KH** |
| Role | Pretraining operator |
| PDE family | Compressible Euler |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `fluids.compressible.KelvinHelmholtz` |
| Official data page | [CE-KH](https://huggingface.co/datasets/camlab-ethz/CE-KH) |
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

The initial state is
$$
(\rho,v_x,v_y,p)|_{t=0}=\begin{cases}
(1,0.5,0,2.5),&y<0.25+\sigma_0(x)\ \text{or}\ y>0.75+\sigma_1(x),\\
(2,-0.5,0,2.5),&\text{otherwise},
\end{cases}
$$
$$
\sigma_i(x)=\varepsilon\frac{\sum_{j=1}^{p}\alpha_{ij}\cos(2\pi j(x+\beta_{ij}))}{\sum_{j=1}^{p}\alpha_{ij}},\qquad \varepsilon=0.05.
$$


### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

Randomly perturbed shear-layer initial state $\mapsto [\rho,v_x,v_y,p](t)$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `data: [10000, 21, 5, 128, 128]` |
| Available physical fields | $[\rho,v_x,v_y,p,E]$. |
| Number of trajectories / samples | **10000** |
| Train / Val / Test | **9640 / 120 / 240** |
| Official repository total file size | **68.8 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=[0,1]^2$ |
| Initial condition / input | Double shear layer with random Fourier interface perturbations. |
| Boundary conditions | Periodic boundary conditions |
| Stored snapshots | 21 |
| Snapshots selected by paper/code | 11 (indices 0,2,…,20) |
| all2all pairs | 66 pairs per trajectory |
| Total time range | $[0,1]$ |
| Stored time separation | $0.05$ |
| Generation software / numerical method | ALSVINN; $512^2\to128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $\alpha_{ij}$ | interface-mode weights; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0,1]$ |
| $\beta_{ij}$ | interface-mode phases; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0,1]$ |
| $\varepsilon$ | overall interface-perturbation amplitude; IC / data-distribution parameter | fixed | $0.05$ |
| $p$ | number of perturbation modes; IC / data-distribution parameter | release value not stated | not specified |
| $\rho_1,\rho_2$ | layer densities; IC / data-distribution parameter | fixed | $1,2$ |
| $v_{x,1},v_{x,2}$ | layer horizontal velocities; IC / data-distribution parameter | fixed | $0.5,-0.5$ |
| $\gamma$ | ratio of specific heats; PDE coefficient | fixed | $1.4$ |

**Summary:** Density ratio, velocity jump, pressure, interface thickness/amplitude, mode count, and $\gamma$ are adjustable; the release randomizes only the interface-mode weights and phases.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `data: [10000, 21, 5, 128, 128]`
- Raw channels/variables: $[\rho,v_x,v_y,p,E]$.
- Expected assembled filename: `CE-KH.nc`

### Official POSEIDON model interface

- One input/output pair: `[4,128,128] → [4,128,128]`
- Channel definition: $[\rho,v_x,v_y,p]$.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

ALSVINN; $512^2\to128^2$.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/CE-KH --repo-type dataset --local-dir ./CE-KH
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./CE-KH
python assemble_data.py --input_dir . --output_file CE-KH.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Strong nonlinear roll-up, mixing-layer growth, and multiscale vortex formation.

## Known source discrepancies and reproduction notes

- The appendix formula contains a mode count $p$, but the subsection does not state the release value.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: CE-KH](https://huggingface.co/datasets/camlab-ethz/CE-KH).
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
