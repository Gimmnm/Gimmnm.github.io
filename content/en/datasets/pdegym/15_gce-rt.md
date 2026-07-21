---
title: "GCE-RT: Rayleigh–Taylor Instability in Euler Flow with Gravity"
parent_dataset: PDEgym
subset: GCE-RT
role: "Downstream task: added gravity source and physical parameters"
pde_family: "Compressible Euler with gravity"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.compressible.gravity.RayleighTaylor
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/GCE-RT"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: GCE-RT
weight: 150
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "Compressible Euler with gravitational forcing, modeling a random Rayleigh–Taylor instability in a polytropic neutron-star configuration."
description: "Compressible Euler with gravitational forcing, modeling a random Rayleigh–Taylor instability in a polytropic neutron-star configuration."

---

# GCE-RT: Rayleigh–Taylor Instability in Euler Flow with Gravity

> **One-line description:** Compressible Euler with gravitational forcing, modeling a random Rayleigh–Taylor instability in a polytropic neutron-star configuration.

## Longer description

This is one of the PDEgym tasks that genuinely varies physical parameters per sample: central density, central pressure, and Atwood number change, while gravitational potential is supplied as a static field.

**Dataset authors/maintainers:** The POSEIDON authors, Computational and Applied Mathematics Laboratory, ETH Zurich.  
**Code or software used to generate the data:** Second-order well-balanced finite-volume method; generated at $256^2$ and downsampled to $128^2$.

## Identity

| Item | Value |
|---|---|
| Parent dataset | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| Subset / logical task | **GCE-RT** |
| Role | Downstream task: added gravity source and physical parameters |
| PDE family | Compressible Euler with gravity |
| Spatial dimension | 2-D |
| Time dependent | Yes |
| Official code identifier | `fluids.compressible.gravity.RayleighTaylor` |
| Official data page | [GCE-RT](https://huggingface.co/datasets/camlab-ethz/GCE-RT) |
| Official code | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| Paper | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| License | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## Equation


$$
\partial_t\mathbf U+\nabla\cdot\mathbf F(\mathbf U)=\mathbf S(\rho,\mathbf v,\nabla\phi),
$$
where $\mathbf U=(\rho,\rho\mathbf v,E)^\top$, $\phi$ is gravitational potential, and the data use a $\gamma=2$ polytrope. The radial equilibrium is
$$
p(r)=K_0\left(\rho_0\frac{\sin(\alpha r)}{\alpha r}\right)^2,\qquad
\phi(r)=-2K_0\rho_0\frac{\sin(\alpha r)}{\alpha r},
$$
$$
K_0=p_0/\rho_0^2,\qquad \alpha=\sqrt{\frac{4\pi G}{2K_0}}.
$$

For conserved variables $\mathbf U=(\rho,\rho v_x,\rho v_y,E)^\top$, the gravity source is
$$
\mathbf S=
\begin{bmatrix}0\\-\rho\\0\\-\rho v_x\end{bmatrix}\partial_x\phi+
\begin{bmatrix}0\\0\\-\rho\\-\rho v_y\end{bmatrix}\partial_y\phi.
$$
The initial velocity is fixed to zero. The density profile and heavy/light-fluid interface are
$$
\rho(r)=\sqrt{\frac{K_0}{\widetilde K(r)}}\,\rho_0\frac{\sin(\alpha r)}{\alpha r},
\qquad
\widetilde K(r)=
\begin{cases}
K_0,&r<r_{RT},\\
\left(\dfrac{1-A}{1+A}\right)^2K_0,&r\ge r_{RT},
\end{cases}
$$
$$
r_{RT}=0.25\left[1+a\cos\!\left(\operatorname{atan2}(y,x)+b\right)\right],
$$
$$
\rho_0=1+0.2c,\qquad p_0=1+0.2d,\qquad A=0.05(1+0.2e),
\qquad c,d,e\sim\mathcal U[-1,1].
$$


### Physical quantities

- Coordinates are two-dimensional Cartesian $(x,y)$. Unless stated otherwise, coordinates are implicit in array indices and are not extra channels.
- Raw release fields, paper operator fields, and official model-facing channels can differ; see “Data format and channels.”

## Operator-learning task

$[\rho,v_x,v_y,p,\phi](0)\mapsto[\rho,v_x,v_y,p,\phi](t)$ with static $\phi$.

## About the data

| Field | Value |
|---|---|
| Discretized data dimensions | `solution: [1260, 11, 6, 128, 128]` |
| Available physical fields | $[\rho,v_x,v_y,p,c_{tr},\phi]$. |
| Number of trajectories / samples | **1260** |
| Train / Val / Test | **1030 / 100 / 130** |
| Official repository total file size | **5.45 GB** |
| Grid type | uniform Cartesian Eulerian grid |
| Spatial domain | $D=[-1/2,1/2]^2$ |
| Initial condition / input | Polytropic gravitational equilibrium, zero initial velocity, and a randomly perturbed heavy/light-fluid interface. |
| Boundary conditions | Periodic boundary conditions |
| Stored snapshots | 11 |
| Snapshots selected by paper/code | 8 (indices 0,1,…,7) |
| all2all pairs | 36 pairs per trajectory |
| Total time range | $[0,5]$ |
| Stored time separation | $0.5$ |
| Generation software / numerical method | Second-order well-balanced finite-volume method; generated at $256^2$ and downsampled to $128^2$. |
| Approximate generation time | The paper and official dataset card do not report a per-trajectory generation time. |
| Generation hardware and precision | Generation hardware and precision are not fully reported per subset; the paper specifies the solver and generation/release resolution. |

## Adjustable, varied, and fixed parameters

| Parameter | Meaning / type | Status in the release | Value or distribution |
|---|---|---|---|
| $a$ | RT interface-perturbation amplitude; IC / data-distribution parameter | varied per trajectory | $\mathcal U[-1,1]$ |
| $b$ | RT interface phase; IC / data-distribution parameter | varied per trajectory | $\mathcal U[-\pi,\pi]$ |
| $\rho_0$ | central density; physical parameter | varied per trajectory | $1+0.2c,\ c\sim\mathcal U[-1,1]$ |
| $p_0$ | central pressure; physical parameter | varied per trajectory | $1+0.2d,\ d\sim\mathcal U[-1,1]$ |
| $A$ | Atwood number / density jump; physical parameter | varied per trajectory | $0.05(1+0.2e),\ e\sim\mathcal U[-1,1]$ |
| $\gamma$ | polytropic/specific-heat parameter; PDE coefficient | fixed | $2$ |
| $G$ | gravitational constant; PDE coefficient | fixed | $1$ |
| $r_{RT,0}$ | base interface radius; IC / data-distribution parameter | fixed | $0.25$ |

**Summary:** The release varies $\rho_0,p_0,A$ and interface geometry; $G,\gamma$, and initial velocity are fixed. Potential, boundaries, and polytropic constants are also adjustable in principle.

> “Adjustable” has three distinct meanings: mathematically changeable in the PDE, changeable by editing the generator, and actually sampled in the official release. Random initial-condition parameters are often encoded only in the field realization rather than stored as an explicit metadata vector.

## Data format, input/output sizes, and channels

### Raw release

- Raw shape: `solution: [1260, 11, 6, 128, 128]`
- Raw channels/variables: $[\rho,v_x,v_y,p,c_{tr},\phi]$.
- Expected assembled filename: `GCE-RT.nc`

### Official POSEIDON model interface

- One input/output pair: `[5,128,128] → [5,128,128]`
- Channel definition: The official loader drops the fifth raw passive-tracer channel and uses $[\rho,v_x,v_y,p,\phi]$.
- After batching the model generally sees `[B,C,H,W]`; trajectory files are typically `[N,T,C,H,W]`. These should not be conflated.
- For time-dependent tasks, `BaseTimeDataset` returns two snapshots and a scalar lead time. all2all pairing enumerates all selected pairs with $t_i\le t_j$.

## Numerical generation

Second-order well-balanced finite-volume method; generated at $256^2$ and downsampled to $128^2$.

Normalization is only a training implementation detail: the official loader applies precomputed means and standard deviations, which neither adds physical fields nor constitutes a PDE-parameter variation.

## Download and assembly

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/GCE-RT --repo-type dataset --local-dir ./GCE-RT
```

Enter the downloaded directory and run the included assembly script:

```bash
cd ./GCE-RT
python assemble_data.py --input_dir . --output_file GCE-RT.nc
```

The assembled path can be passed to the official training/inference scripts through `--data_path`. A steady identifier may be suffixed with `.time` to wrap the steady map as a normalized lead-time-one long-time-limit task; this does not create a physical trajectory in the raw file.

## What is interesting and challenging

- Well-balanced gravity, Rayleigh–Taylor instability, and multiple per-sample physical parameters occur simultaneously.

## Known source discrepancies and reproduction notes

- The HF card says “unit square,” while the paper explicitly gives $[-1/2,1/2]^2$; this documentation follows the paper coordinates.
- The official Hugging Face file tree currently reports a total repository size of 5.45 GB, consistent in scale with the float32 payload implied by the raw shape.

## Sources

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101), especially Appendix B.
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon); identifiers and loaders are under [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems).
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651).
4. [Official dataset repository: GCE-RT](https://huggingface.co/datasets/camlab-ethz/GCE-RT).
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
