---
title: "ACE: Allen–Cahn Reaction–Diffusion Phase Field"
parent_dataset: PDEgym
subset: ACE
role: "Downstream task: new PDE and phase-transition physics"
pde_family: "Allen–Cahn reaction–diffusion"
spatial_dimension: 2
time_dependent: true
official_code_identifier: reaction_diffusion.AllenCahn
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/ACE"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: ACE
weight: 180
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Nonlinear Allen–Cahn phase-transition trajectories on a two-dimensional periodic domain."
description: "Nonlinear Allen–Cahn phase-transition trajectories on a two-dimensional periodic domain."

---

# ACE: Allen–Cahn Reaction–Diffusion Phase Field

> **One-line description:** Nonlinear Allen–Cahn phase-transition trajectories on a two-dimensional periodic domain.

## Longer description

This task differs strongly from the convection-dominated pretraining fluids: diffusion, bistable reaction, and interface motion dominate the dynamics.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.  
**Code or software used to generate the data:** Finite-difference method; $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **ACE** |
| Role | Downstream task: new PDE and phase-transition physics |
| PDE family | Allen–Cahn reaction–diffusion |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `reaction_diffusion.AllenCahn` |
| Official data page | [ACE](https://huggingface.co/datasets/camlab-ethz/ACE) |
| Official code | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| Paper | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| License | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## Equation


$$
\partial_tu=\Delta u-\epsilon^2u(u^2-1).
$$
Initial condition
$$
u_0(x,y)=\frac1{K^2}\sum_{i,j=1}^{K}a_{ij}(i^2+j^2)^{-r}\sin(\pi ix)\sin(\pi jy).
$$


### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$u_0\mapsto u(t)$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `solution: [15000, 20, 128, 128]` |
| Available physical fields | Single-channel phase field/concentration $u$. |
| Number of trajectories / samples | **15000** |
| Train / Val / Test | **14700 / 60 / 240** |
| Official repository total file size | **19.7 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=(0,1)^2$ |
| Initial condition / input | Random decaying Fourier sine series. |
| Boundary conditions | Periodic boundary conditions |
| Stored snapshots | 20 |
| Snapshots selected by paper/code | 8 (indices 0,2,…,14) |
| all2all pairs | 36 pairs per trajectory |
| Total time range | $[0,0.0002]$ |
| Stored time separation | nominal endpoint-inclusive interval $0.0002/19$ |
| Generation software / numerical method | Finite-difference method; $128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $K$ | initial spectral cutoff; IC / data-distribution parameter | varied per trajectory | uniform integer in $[16,32]$ |
| $r$ | spectral decay exponent; IC / data-distribution parameter | varied per trajectory | $\mathcal U[0.7,1.0]$ |
| $a_{ij}$ | random initial coefficients; IC / data-distribution parameter | varied per trajectory | $\mathcal U[-1,1]$ |
| $\epsilon$ | reaction parameter; PDE coefficient | fixed | $220$ in the paper text |
| diffusion coefficient | diffusion coefficient; PDE coefficient | fixed | $1$ |

**Summary:** Diffusion coefficient, reaction rate/interface width, potential, and boundary conditions are adjustable; the release varies only the initial spectrum.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `solution: [15000, 20, 128, 128]`
- Raw channels/variables: Single-channel phase field/concentration $u$.
- Expected assembled filename: `ACE.nc`

### Official POSEIDON model interface

- One input/output pair: `[1,128,128] → [1,128,128]`
- Channel definition: $u(t_i)\to u(t_j)$.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

Finite-difference method; $128^2$.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/ACE --repo-type dataset --local-dir ./ACE
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./ACE
python assemble_data.py --input_dir . --output_file ACE.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Thin-interface motion, nonlinear bistable reaction, and a very short physical time scale.

## Known source discrepancies and reproduction notes

- The text calls the reaction rate $\epsilon=220$, while the displayed equation contains $\epsilon^2$; exact reproduction should inspect the generator to avoid squaring twice.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: ACE](https://huggingface.co/datasets/camlab-ethz/ACE).
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
