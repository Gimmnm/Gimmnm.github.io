---
title: "CE-RM: Richtmyer–Meshkov Instability"
parent_dataset: PDEgym
subset: CE-RM
role: "Downstream task: shock–interface instability"
pde_family: "Compressible Euler"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.compressible.RichtmyerMeshkov
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/CE-RM"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: CE-RM
weight: 140
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Richtmyer–Meshkov trajectories in which a shock interacts with a randomly perturbed density interface."
description: "Richtmyer–Meshkov trajectories in which a shock interacts with a randomly perturbed density interface."

---

# CE-RM: Richtmyer–Meshkov Instability

**Description:** Richtmyer–Meshkov trajectories in which a shock interacts with a randomly perturbed density interface. This classical instability produces interface growth, mixing, and multiscale structure. It differs from pretraining Euler data in generator, time scale, and dataset size.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.
**Code or software used to generate the data:** FISH high-resolution finite-volume hydrodynamics code; released at $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **CE-RM** |
| Role | Downstream task: shock–interface instability |
| PDE family | Compressible Euler |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `fluids.compressible.RichtmyerMeshkov` |
| Official data page | [CE-RM](https://huggingface.co/datasets/camlab-ethz/CE-RM) |
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

The appendix specifies
$$
p_0(x,y)=\begin{cases}20,&\sqrt{x^2+y^2}<0.1,\\1,&\text{otherwise},\end{cases}\qquad
\rho_0(x,y)=\begin{cases}2,&|x|<I(x,y,\omega),\\1,&\text{otherwise},\end{cases}
$$
$$
v_x^0=v_y^0=0,\qquad I=0.25+\epsilon\sum_{j=1}^{10}a_j\sin\bigl(2\pi((x,y)+b_j)\bigr).
$$

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$[\rho,v_x,v_y,p](0)\mapsto[\rho,v_x,v_y,p](t)$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `solution: [1260, 21, 5, 128, 128]` |
| Available physical fields | HF card: $[\rho,v_x,v_y,p,\text{passive tracer}]$; the paper and official loader use the first four channels. |
| Number of trajectories / samples | **1260** |
| Train / Val / Test | **1030 / 100 / 130** |
| Official repository total file size | **8.67 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=[0,1]^2$ |
| Initial condition / input | Localized high pressure and a randomly perturbed density interface, with zero initial velocity. |
| Boundary conditions | Periodic boundaries in the paper |
| Stored snapshots | 21 |
| Snapshots selected by paper/code | paper evaluation at raw index 14; standard downstream pairing uses selected snapshots through index 14 |
| all2all pairs | up to 36 pairs under the standard 8-snapshot setup |
| Total time range | $[0,2]$; evaluated at $t=1.4$ |
| Stored time separation | $0.1$ |
| Generation software / numerical method | FISH high-resolution finite-volume hydrodynamics code; released at $128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $a_j$ | interface perturbation weights; IC / data-distribution parameter | varied and normalized per trajectory | $\mathcal U[0,1]$, $\sum_j a_j=1$ |
| $b_j$ | interface perturbation phases/offsets; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0,1]$ |
| $K$ | number of perturbation modes; IC / data-distribution parameter | fixed | $10$ |
| $\epsilon$ | interface perturbation amplitude; IC / data-distribution parameter | stated only as $>0$; value not given | not specified |
| density ratio | two-side densities; IC / data-distribution parameter | fixed | $2/1$ |
| pressure levels | shock/background pressure; IC / data-distribution parameter | fixed | $20/1$ |

**Summary:** Shock strength, density ratio, $\epsilon$, $K$, $\gamma$, and boundaries are adjustable; the release mainly varies the interface perturbation spectrum.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `solution: [1260, 21, 5, 128, 128]`
- Raw channels/variables: HF card: $[\rho,v_x,v_y,p,\text{passive tracer}]$; the paper and official loader use the first four channels.
- Expected assembled filename: `CE-RM.nc`

### Official POSEIDON model interface

- One input/output pair: `[4,128,128] → [4,128,128]`
- Channel definition: $[\rho,v_x,v_y,p]$.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

FISH high-resolution finite-volume hydrodynamics code; released at $128^2$.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/CE-RM --repo-type dataset --local-dir ./CE-RM
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./CE-RM
python assemble_data.py --input_dir . --output_file CE-RM.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Shock-driven interface instability, mixing, and complex small scales, with far fewer trajectories than most PDEgym subsets.

## Known source discrepancies and reproduction notes

- The appendix notation for the vector-valued sine in $I(x,y,\omega)$ and the coordinate origin is terse; exact reproduction should follow the generator.
- The appendix does not give the value of $\epsilon$.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: CE-RM](https://huggingface.co/datasets/camlab-ethz/CE-RM).
