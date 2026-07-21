---
title: "CE-Gauss: Compressible Euler from Gaussian-Vorticity Velocity Fields"
parent_dataset: PDEgym
subset: CE-Gauss
role: "Pretraining operator"
pde_family: "Compressible Euler"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.compressible.Gaussians
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/CE-Gauss"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: CE-Gauss
weight: 60
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "With fixed background density and pressure, the initial velocity is recovered from 100 random Gaussian vorticity blobs and evolved by compressible Euler."
description: "With fixed background density and pressure, the initial velocity is recovered from 100 random Gaussian vorticity blobs and evolved by compressible Euler."

---

# CE-Gauss: Compressible Euler from Gaussian-Vorticity Velocity Fields

**Description:** With fixed background density and pressure, the initial velocity is recovered from 100 random Gaussian vorticity blobs and evolved by compressible Euler. This operator combines localized vortical initial conditions with compressible dynamics, contributing local vortex structure, acoustic coupling, and density/pressure response to pretraining.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.
**Code or software used to generate the data:** ALSVINN; $512^2\to128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **CE-Gauss** |
| Role | Pretraining operator |
| PDE family | Compressible Euler |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `fluids.compressible.Gaussians` |
| Official data page | [CE-Gauss](https://huggingface.co/datasets/camlab-ethz/CE-Gauss) |
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

The initial velocity vorticity uses the same 100-Gaussian superposition as NS-Gauss and the velocity is recovered using the incompressibility relation. Background values are fixed at $\rho^0=0.1$ and $p^0=2.5$.

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$[\rho,v_x,v_y,p](0)\mapsto[\rho,v_x,v_y,p](t)$.

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
| Initial condition / input | Velocity recovered from Gaussian vorticity; constant background density and pressure. |
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
| $\alpha_i$ | Gaussian vorticity strength; IC / data-distribution parameter | varied per trajectory | $\mathcal U[-1,1]$ |
| $\sigma_i$ | Gaussian width; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0.01,0.1]$ |
| $x_i,y_i$ | centers; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0,1]$ |
| $N_g$ | number of Gaussians; IC / data-distribution parameter | fixed | $100$ |
| $\rho^0$ | background density; IC / data-distribution parameter | fixed | $0.1$ |
| $p^0$ | background pressure; IC / data-distribution parameter | fixed | $2.5$ |
| $\gamma$ | ratio of specific heats; PDE coefficient | fixed | $1.4$ |

**Summary:** The Gaussian count, background density/pressure, $\gamma$, and vorticity strength/scale distributions are adjustable; the release varies only the Gaussian-vorticity realization.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `data: [10000, 21, 5, 128, 128]`
- Raw channels/variables: $[\rho,v_x,v_y,p,E]$.
- Expected assembled filename: `CE-Gauss.nc`

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
huggingface-cli download camlab-ethz/CE-Gauss --repo-type dataset --local-dir ./CE-Gauss
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./CE-Gauss
python assemble_data.py --input_dir . --output_file CE-Gauss.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Coupling between localized vortices and compressible density/pressure waves.

## Known source discrepancies and reproduction notes

- No additional conflict was found among the paper, official code, and data card for the key fields in this entry.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: CE-Gauss](https://huggingface.co/datasets/camlab-ethz/CE-Gauss).
