---
title: "Poisson-Gauss: Gaussian Sources to Steady Poisson Solutions"
parent_dataset: PDEgym
subset: Poisson-Gauss
role: "Downstream task: steady elliptic operator"
pde_family: "Poisson equation"
spatial_dimension: 2
time_dependent: false
official_code_identifier: elliptic.poisson.Gaussians(.time)
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/Poisson-Gauss"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: Poisson-Gauss
weight: 200
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Steady mapping from a random superposition of Gaussian sources to the homogeneous-Dirichlet Poisson solution."
description: "Steady mapping from a random superposition of Gaussian sources to the homogeneous-Dirichlet Poisson solution."

---

# Poisson-Gauss: Gaussian Sources to Steady Poisson Solutions

**Description:** Steady mapping from a random superposition of Gaussian sources to the homogeneous-Dirichlet Poisson solution. This elliptic diffusion/smoothing operator is very different from fluid pretraining and tests transfer from a source field to a steady solution.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.
**Code or software used to generate the data:** FEniCS finite-element method; released as $128^2$ fields.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **Poisson-Gauss** |
| Role | Downstream task: steady elliptic operator |
| PDE family | Poisson equation |
| Spatial dimension | 2-D |
| Time dependent | No (steady) |
| Official code identifier | `elliptic.poisson.Gaussians(.time)` |
| Official data page | [Poisson-Gauss](https://huggingface.co/datasets/camlab-ethz/Poisson-Gauss) |
| Official code | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| Paper | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| License | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## Equation

$$
-\Delta u=f\quad\text{in }(0,1)^2,\qquad u=0\quad\text{on }\partial D,
$$
$$
f(x,y)=\sum_{i=1}^{N_g}\exp\!\left[-\frac{(x-\mu_{x,i})^2+(y-\mu_{y,i})^2}{2\sigma_i^2}\right].
$$

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$f\mapsto u$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `source: [20000,128,128]; solution: [20000,128,128]` |
| Available physical fields | One source channel and one solution channel. |
| Number of trajectories / samples | **20000** |
| Train / Val / Test | **19640 / 120 / 240** |
| Official repository total file size | **2.62 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=(0,1)^2$ |
| Initial condition / input | Steady problem; input is a Gaussian source field. |
| Boundary conditions | Homogeneous Dirichlet: $u=0$ |
| Stored snapshots | steady |
| Snapshots selected by paper/code | not applicable |
| all2all pairs | not a physical trajectory pairing |
| Total time range | steady state |
| Stored time separation | not applicable |
| Generation software / numerical method | FEniCS finite-element method; released as $128^2$ fields. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $N_g$ | number of Gaussian sources; source parameter | varied per sample | $\mathrm{Geom}(0.4)$ |
| $\mu_{x,i},\mu_{y,i}$ | source centers; source parameter | varied per sample | $\mathcal U[0,1]$ |
| $\sigma_i$ | source width; source parameter | varied per sample | $\mathcal U[0.025,0.1]$ |
| Gaussian amplitude | amplitude of each Gaussian; source parameter | fixed | $1$ |
| elliptic coefficient | Laplacian coefficient; PDE coefficient | fixed | $1$ |
| boundary value | boundary value; boundary parameter | fixed | $0$ |

**Summary:** Spatially varying diffusivity, nonhomogeneous boundaries, domain shape, and reaction terms are adjustable; the release varies only the source.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `source: [20000,128,128]; solution: [20000,128,128]`
- Raw channels/variables: One source channel and one solution channel.
- Expected assembled filename: `Poisson-Gauss.nc`

### Official POSEIDON model interface

- One input/output pair: `[1,128,128] → [1,128,128]`
- Channel definition: $f\to u$; the `.time` wrapper sets lead time to one.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

FEniCS finite-element method; released as $128^2$ fields.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/Poisson-Gauss --repo-type dataset --local-dir ./Poisson-Gauss
```

The official card publishes this as an already assembled file and does not require `assemble_data.py`.

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Local sources produce global smooth solutions; steadiness, ellipticity, and Dirichlet boundaries all differ from pretraining.

## Known source discrepancies and reproduction notes

- No additional conflict was found among the paper, official code, and data card for the key fields in this entry.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: Poisson-Gauss](https://huggingface.co/datasets/camlab-ethz/Poisson-Gauss).
