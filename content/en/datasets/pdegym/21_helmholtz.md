---
title: "Helmholtz: Random Media and Boundary Values to Frequency-Domain Waves"
parent_dataset: PDEgym
subset: Helmholtz
role: "Downstream task: steady coefficient operator"
pde_family: "Helmholtz equation"
spatial_dimension: 2
time_dependent: false
official_code_identifier: elliptic.Helmholtz(.time)
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/Helmholtz"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: Helmholtz
weight: 210
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Maps a per-sample medium coefficient field and constant Dirichlet boundary value to a frequency-domain Helmholtz solution."
description: "Maps a per-sample medium coefficient field and constant Dirichlet boundary value to a frequency-domain Helmholtz solution."

---

# Helmholtz: Random Media and Boundary Values to Frequency-Domain Waves

**Description:** Maps a per-sample medium coefficient field and constant Dirichlet boundary value to a frequency-domain Helmholtz solution. This task varies both the PDE coefficient $a(x,y)$ and the boundary parameter $b$, while frequency is fixed. It is a representative steady wave-coefficient operator in PDEgym.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.
**Code or software used to generate the data:** Finite-difference method similar to DeVITO; $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **Helmholtz** |
| Role | Downstream task: steady coefficient operator |
| PDE family | Helmholtz equation |
| Spatial dimension | 2-D |
| Time dependent | No (steady) |
| Official code identifier | `elliptic.Helmholtz(.time)` |
| Official data page | [Helmholtz](https://huggingface.co/datasets/camlab-ethz/Helmholtz) |
| Official code | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| Paper | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| License | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## Equation

$$
-\Delta u-\omega^2a(x,y)u=0\quad\text{in }D,
\qquad u=b\quad\text{on }\partial D,
$$
$$
\omega=\frac{5\pi}{2}.
$$
First generate
$$
\bar a(x,y)=-\sum_{i=1}^{n}A_i\exp\!\left[-\frac{(x-x_i)^2+(y-y_i)^2}{2\sigma_i^2}\right],
$$
then min–max normalize $a=(\bar a-\min\bar a)/(\max\bar a-\min\bar a)$.

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$(a,b)\mapsto u$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `HDF5: 19675 groups Sample_i, each with a[128,128], scalar bc, u[128,128]` |
| Available physical fields | Medium field $a$, scalar boundary value $bc$, and solution $u$. |
| Number of trajectories / samples | **19675** |
| Train / Val / Test | **19035 / 128 / 512** |
| Official repository total file size | **5.2 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=(0,1)^2$ |
| Initial condition / input | Steady problem; inputs are medium field and boundary value. |
| Boundary conditions | Per-sample constant Dirichlet condition $u=b$ |
| Stored snapshots | steady |
| Snapshots selected by paper/code | not applicable; `.time` wrapper can assign lead time 1 |
| all2all pairs | not a physical trajectory pairing |
| Total time range | steady state / frequency domain |
| Stored time separation | not applicable |
| Generation software / numerical method | Finite-difference method similar to DeVITO; $128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $b$ | constant Dirichlet boundary value; boundary parameter | varied per sample | $\mathcal U[0.25,0.5]$ |
| $n$ | number of medium Gaussians; PDE coefficient construction | varied per sample | $\mathcal U\{2,3,4,5,6,7\}$ |
| $A_i$ | medium-Gaussian amplitude; PDE coefficient construction | varied per sample | $\mathcal U[0.5,10]$ |
| $\sigma_i$ | medium-Gaussian width; PDE coefficient construction | varied per sample | $\mathcal U[0.05,0.1]$ |
| $x_i,y_i$ | medium-Gaussian centers; PDE coefficient construction | varied per sample | $\mathcal U[0.2,0.8]$ |
| $\omega$ | angular frequency; PDE coefficient | fixed | $5\pi/2$ |

**Summary:** Frequency, spatial boundary profile, complex damping, domain, and medium construction are adjustable; the release varies $a(x,y)$ and scalar $b$ while fixing $\omega$.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `HDF5: 19675 groups Sample_i, each with a[128,128], scalar bc, u[128,128]`
- Raw channels/variables: Medium field $a$, scalar boundary value $bc$, and solution $u$.
- Expected assembled filename: `Helmholtz.h5`

### Official POSEIDON model interface

- One input/output pair: `[2,128,128] → [1,128,128]`
- Channel definition: The loader broadcasts $b$ to a constant field and concatenates it with $a$ as a two-channel input; output is one-channel $u$. It also preprocesses $a$ as `a - 1`.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

Finite-difference method similar to DeVITO; $128^2$.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/Helmholtz --repo-type dataset --local-dir ./Helmholtz
```

The official card publishes this as an already assembled file and does not require `assemble_data.py`.

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Both medium coefficient and boundary value vary, solutions can be oscillatory/resonant, and the raw format uses one HDF5 group per sample.

## Known source discrepancies and reproduction notes

- No additional conflict was found among the paper, official code, and data card for the key fields in this entry.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: Helmholtz](https://huggingface.co/datasets/camlab-ethz/Helmholtz).
