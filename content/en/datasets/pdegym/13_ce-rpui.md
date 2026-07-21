---
title: "CE-RPUI: Strong Riemann Problems with Uncertain Interfaces"
parent_dataset: PDEgym
subset: CE-RPUI
role: "Downstream task: new interface distribution"
pde_family: "Compressible Euler"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.compressible.RiemannKelvinHelmholtz
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/CE-RPUI"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: CE-RPUI
weight: 130
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Four-quadrant Riemann problems with strong random states and high-frequency, small-amplitude uncertain interfaces."
description: "Four-quadrant Riemann problems with strong random states and high-frequency, small-amplitude uncertain interfaces."

---

# CE-RPUI: Strong Riemann Problems with Uncertain Interfaces

> **One-line description:** Four-quadrant Riemann problems with strong random states and high-frequency, small-amplitude uncertain interfaces.

## Longer description

This is a difficult out-of-distribution variant of CE-RP: jumps are stronger and interface location/shape are random, combining shocks with small-scale vortex roll-up.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.  
**Code or software used to generate the data:** ALSVINN; $512^2\to128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **CE-RPUI** |
| Role | Downstream task: new interface distribution |
| PDE family | Compressible Euler |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `fluids.compressible.RiemannKelvinHelmholtz` |
| Official data page | [CE-RPUI](https://huggingface.co/datasets/camlab-ethz/CE-RPUI) |
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

Interface perturbations are
$$
\sigma_x=\sum_{i,j=1}^{p}\alpha_{x,ij}\sin\!\left(2\pi(i+2p^2)x+(j+2p^2)y+\beta_{x,ij}\right),
$$
$$
\sigma_y=\sum_{i,j=1}^{p}\alpha_{y,ij}\sin\!\left(2\pi(i+2p^2)x+(j+2p^2)y+\beta_{y,ij}\right),
$$
followed by random constant states in the curved partitions.


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
| Spatial domain | $D=[0,1]^2\simeq\mathbb T^2$ |
| Initial condition / input | Strong random discontinuous states on uncertain curved interfaces. |
| Boundary conditions | Periodic boundary conditions |
| Stored snapshots | 21 |
| Snapshots selected by paper/code | 8 (indices 0,2,…,14) |
| all2all pairs | 36 pairs per trajectory |
| Total time range | $[0,1]$; benchmark horizon $[0,0.7]$ |
| Stored time separation | $0.05$ raw; selected interval $0.1$ |
| Generation software / numerical method | ALSVINN; $512^2\to128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $\alpha_{k,ij}$ | interface perturbation amplitude; IC / data-distribution parameter | varied per trajectory | $\mathcal U[-0.01,0.01]$ |
| $\beta_{k,ij}$ | interface perturbation phase; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0,1]$ |
| $\rho_{ij}$ | density; IC / data-distribution parameter | varied by partition | $\mathcal U[1,3]$ |
| $v_{x,ij},v_{y,ij}$ | velocity; IC / data-distribution parameter | varied by partition | $\mathcal U[-10,10]$ |
| $p_{ij}$ | pressure; IC / data-distribution parameter | varied by partition | $\mathcal U[5,7]$ |
| $p$ | partition parameter; IC / data-distribution parameter | release value not stated | not specified |
| $\gamma$ | ratio of specific heats; PDE coefficient | fixed | $1.4$ |

**Summary:** Interface spectrum, state strength, partition count, $\gamma$, and boundaries are adjustable; the release varies both interface geometry and state values.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `data: [10000, 21, 5, 128, 128]`
- Raw channels/variables: $[\rho,v_x,v_y,p,E]$.
- Expected assembled filename: `CE-RPUI.nc`

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
huggingface-cli download camlab-ethz/CE-RPUI --repo-type dataset --local-dir ./CE-RPUI
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./CE-RPUI
python assemble_data.py --input_dir . --output_file CE-RPUI.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Strong shocks, curved discontinuities, and small vortices coexist, making this a difficult OOD fluid task.

## Known source discrepancies and reproduction notes

- The appendix subsection does not state the release value of the partition parameter $p$.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: CE-RPUI](https://huggingface.co/datasets/camlab-ethz/CE-RPUI).
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
