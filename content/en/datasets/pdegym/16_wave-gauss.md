---
title: "Wave-Gauss: Variable-Coefficient Waves in Gaussian Media"
parent_dataset: PDEgym
subset: Wave-Gauss
role: "Downstream task: per-sample PDE coefficient"
pde_family: "Variable-coefficient wave equation"
spatial_dimension: 2
time_dependent: true
official_code_identifier: wave.Gaussians
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/Wave-Gauss"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: Wave-Gauss
weight: 160
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Multiple Gaussian initial wave sources propagate through a random smooth Gaussian wave-speed medium."
description: "Multiple Gaussian initial wave sources propagate through a random smooth Gaussian wave-speed medium."

---

# Wave-Gauss: Variable-Coefficient Waves in Gaussian Media

> **One-line description:** Multiple Gaussian initial wave sources propagate through a random smooth Gaussian wave-speed medium.

## Longer description

The spatial wave speed $c(x,y)$ is a per-sample PDE coefficient, modeling acoustic/seismic propagation through a heterogeneous smooth medium.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.  
**Code or software used to generate the data:** Finite-difference method similar to DeVITO; $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **Wave-Gauss** |
| Role | Downstream task: per-sample PDE coefficient |
| PDE family | Variable-coefficient wave equation |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `wave.Gaussians` |
| Official data page | [Wave-Gauss](https://huggingface.co/datasets/camlab-ethz/Wave-Gauss) |
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

Initial displacement
$$
u_0(x,y)=\sum_{i=1}^{n}\exp\!\left[-\frac{(x-x_{c,i})^2+(y-y_{c,i})^2}{2s_i^2}\right].$$
Medium wave speed
$$c(x,y)=c_0+\sum_{i=1}^{4}v_i\exp\!\left[-\frac{(x-x_i-dx_i)^2+(y-y_i-dy_i)^2}{2\sigma_i^2}\right].$$


### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

Released interface: $[u(t_i),c]\mapsto[u(t_j),c]$; evaluation is on $u$ only.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `solution: [10512, 15, 128, 128]; c: [10512, 128, 128]` |
| Available physical fields | Dynamic variable `solution` is $u$; static variable `c` is wave speed. |
| Number of trajectories / samples | **10512** |
| Train / Val / Test | **10212 / 60 / 240** |
| Official repository total file size | **11.7 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=(0,1)^2$ |
| Initial condition / input | Two to six unit-amplitude Gaussian displacement sources with a separation constraint. |
| Boundary conditions | Absorbing boundary conditions |
| Stored snapshots | 15 |
| Snapshots selected by paper/code | 8 (indices 0,2,…,14) |
| all2all pairs | 36 pairs per trajectory |
| Total time range | HF card: $[0,1]$; paper benchmark identifies raw index 14 with $t=0.7$ |
| Stored time separation | source conflict; do not infer a unique physical $\Delta t$ without checking the generator/loader |
| Generation software / numerical method | Finite-difference method similar to DeVITO; $128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $n$ | number of initial Gaussian sources; IC / data-distribution parameter | varied per trajectory | $\mathcal U\{2,3,4,5,6\}$ |
| $x_{c,i},y_{c,i}$ | source centers; IC / data-distribution parameter | varied per trajectory | $\mathcal U[1/6,5/6]$ |
| $s_i$ | source width; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0.039,0.156]$ |
| source amplitude | source amplitude; IC / data-distribution parameter | fixed | $1$ |
| $c_0$ | background wave speed; PDE coefficient | varied per trajectory | $\mathcal U[1500,2500]$ |
| $dx_i,dy_i$ | offsets of four medium anomalies; PDE coefficient | varied per trajectory | $\mathcal U[-0.3125,0.3125]$ |
| $v_i$ | medium-anomaly amplitude; PDE coefficient | varied per trajectory | $\mathcal U[1000,2500]$ |
| $\sigma_i$ | medium-anomaly width; PDE coefficient | varied per trajectory | $\mathcal U[1/12,1/6]$ |
| anchor points | four base anomaly anchors; IC / data-distribution parameter | fixed | $(0.25,0.25),(0.25,0.75),(0.75,0.25),(0.75,0.75)$ |

**Summary:** Source amplitude, initial velocity, absorbing layer, and wave-speed ranges are adjustable; the release randomizes source geometry and the full coefficient field $c(x,y)$.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `solution: [10512, 15, 128, 128]; c: [10512, 128, 128]`
- Raw channels/variables: Dynamic variable `solution` is $u$; static variable `c` is wave speed.
- Expected assembled filename: `Wave-Gauss.nc`

### Official POSEIDON model interface

- One input/output pair: `[2,128,128] → [2,128,128]`
- Channel definition: $[u(t_i),c]\to[u(t_j),c]$; the first-order auxiliary $v=u_t$ is absent from the release.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

Finite-difference method similar to DeVITO; $128^2$.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/Wave-Gauss --repo-type dataset --local-dir ./Wave-Gauss
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./Wave-Gauss
python assemble_data.py --input_dir . --output_file Wave-Gauss.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Wavefront propagation, absorbing boundaries, and per-sample continuous medium coefficients vary together.

## Known source discrepancies and reproduction notes

- The paper states total simulation time $T=1$ but also calls the 14th index $t=0.7$; the HF release has 15 frames. Reproduction should follow code time normalization and raw indices.
- The theoretical first-order state $[u,v,c]$ differs from the actual released/loaded $[u,c]$.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: Wave-Gauss](https://huggingface.co/datasets/camlab-ethz/Wave-Gauss).
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
