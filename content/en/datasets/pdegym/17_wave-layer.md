---
title: "Wave-Layer: Waves in Random Layered Media"
parent_dataset: PDEgym
subset: Wave-Layer
role: "Downstream task: layered discontinuous PDE coefficient"
pde_family: "Variable-coefficient wave equation"
spatial_dimension: 2
time_dependent: true
official_code_identifier: wave.Layer
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/Wave-Layer"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: Wave-Layer
weight: 170
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Gaussian initial wave sources propagate through vertically layered media with random curved interfaces and piecewise-constant wave speeds."
description: "Gaussian initial wave sources propagate through vertically layered media with random curved interfaces and piecewise-constant wave speeds."

---

# Wave-Layer: Waves in Random Layered Media

**Description:** Gaussian initial wave sources propagate through vertically layered media with random curved interfaces and piecewise-constant wave speeds. Compared with the smooth coefficient in Wave-Gauss, this task contains coefficient discontinuities and random layer interfaces, resembling layered subsurface media.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.
**Code or software used to generate the data:** Finite-difference method; $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **Wave-Layer** |
| Role | Downstream task: layered discontinuous PDE coefficient |
| PDE family | Variable-coefficient wave equation |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `wave.Layer` |
| Official data page | [Wave-Layer](https://huggingface.co/datasets/camlab-ethz/Wave-Layer) |
| Official code | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| Paper | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| License | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## Equation

$$
\partial_{tt}u-c(x,y)^2\Delta u=0.
$$

For the operator-learning formulation this can be augmented to first order as
$$
u_t=v,\qquad v_t=c^2\Delta u,\qquad c_t=0,$$
but the released Wave-Gauss and Wave-Layer files explicitly store only the displacement trajectory $u$ and the static coefficient field $c$.

Initial Gaussian-source rules are the same as Wave-Gauss. The speed $c(x,y)$ is constant within each randomly curved layer; interfaces are built from ten sine modes and rescaled to prevent crossings.

### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$[u(t_i),c]\mapsto[u(t_j),c]$, evaluated on $u$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `solution: [10512, 15, 128, 128]; c: [10512, 128, 128]` |
| Available physical fields | `solution` is $u$ and `c` is the static layered wave speed. |
| Number of trajectories / samples | **10512** |
| Train / Val / Test | **10212 / 60 / 240** |
| Official repository total file size | **15.2 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=(0,1)^2$ |
| Initial condition / input | Random Gaussian displacement sources as in Wave-Gauss. |
| Boundary conditions | Absorbing boundary conditions |
| Stored snapshots | 15 |
| Snapshots selected by paper/code | 8 (indices 0,2,…,14) |
| all2all pairs | 36 pairs per trajectory |
| Total time range | HF card: $[0,1]$; paper benchmark uses index 14 as $t=0.7$ |
| Stored time separation | source conflict; follow code/indexing for reproduction |
| Generation software / numerical method | Finite-difference method; $128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $n_{layer}$ | number of medium layers; PDE coefficient geometry | varied per trajectory | $\mathcal U\{3,4,5,6\}$ |
| interface modes | sine modes per layer interface; IC / data-distribution parameter | fixed construction | $10$ |
| interface coefficients | random layer-interface coefficients/offsets; PDE coefficient geometry | varied then rescaled per trajectory | sampled in $(0,1)$ |
| $c_i$ | constant speed in each layer; PDE coefficient | varied by layer and trajectory | $\mathcal U[2000,5000]$ |
| $n$ | number of initial Gaussian sources; IC / data-distribution parameter | varied per trajectory | $\mathcal U\{2,3,4,5,6\}$ |
| $s_i$ | source width; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0.039,0.156]$ |

**Summary:** Layer count, layer speed, interface shape, and source geometry vary; anisotropy, initial velocity, absorbing-layer parameters, and interface physics are not swept.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `solution: [10512, 15, 128, 128]; c: [10512, 128, 128]`
- Raw channels/variables: `solution` is $u$ and `c` is the static layered wave speed.
- Expected assembled filename: `Wave-Layer.nc`

### Official POSEIDON model interface

- One input/output pair: `[2,128,128] → [2,128,128]`
- Channel definition: $[u(t_i),c]\to[u(t_j),c]$.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

Finite-difference method; $128^2$.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/Wave-Layer --repo-type dataset --local-dir ./Wave-Layer
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./Wave-Layer
python assemble_data.py --input_dir . --output_file Wave-Layer.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Discontinuous layer speeds and randomly curved interfaces create reflections, transmissions, and complex wavefronts.

## Known source discrepancies and reproduction notes

- Appendix B.2.11 says 21 snapshots, whereas the official HF card gives 15; the raw shape follows the actual release.
- The first-order auxiliary channel $v=u_t$ is not stored.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: Wave-Layer](https://huggingface.co/datasets/camlab-ethz/Wave-Layer).
