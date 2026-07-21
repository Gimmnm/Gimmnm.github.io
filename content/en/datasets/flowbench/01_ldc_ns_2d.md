---
title: "FlowBench: 2-D complex-geometry lid-driven cavity Navier–Stokes"
parent_dataset: FlowBench
subset: LDC_NS_2D
equation_family: "incompressible Navier-Stokes"
spatial_dimension: 2
temporal_regime: steady
task: geometry-and-Reynolds-to-field
geometry_families: ""
license: CC-BY-NC-4.0
last_verified: 2026-07-21
linkTitle: "LDC NS 2D"
weight: 10
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: FlowBench
summary: "Steady incompressible flow is driven by a moving lid in a square cavity containing a stationary complex object."
description: "Steady incompressible flow is driven by a moving lid in a square cavity containing a stationary complex object."

---

# 2-D complex-geometry lid-driven cavity (LDC–NS–2D)

**One-line description:** Steady incompressible flow is driven by a moving lid in a square cavity containing a stationary complex object.

**Longer description:** This subset studies steady solutions of the same incompressible Navier–Stokes equations across Reynolds numbers and complex embedded boundaries. It is the canonical FlowBench geometry-to-field subset and the principal data used by the official Geometry Matters benchmark.

**Dataset team:** FlowBench / Baskar Group, with collaborators from Iowa State University and New York University.  
**Generation software:** Dendro/Dendro-KT finite-element framework with SBM.  



## Parent dataset and links

| Item | Resource |
|---|---|
| Parent benchmark | **FlowBench** |
| Paper | [arXiv:2409.18032](https://arxiv.org/abs/2409.18032) |
| Paper PDF | [PDF](https://arxiv.org/pdf/2409.18032) |
| Official data | [BGLab/FlowBench](https://huggingface.co/datasets/BGLab/FlowBench) |
| Official tools | [baskargroup/flowbench-tools](https://github.com/baskargroup/flowbench-tools) |
| Training/evaluation code | [baskargroup/GeometryMatters](https://github.com/baskargroup/GeometryMatters) |
| Project website | [FlowBench website](https://baskargroup.bitbucket.io/FlowBench/) |
| License | **CC-BY-NC-4.0** |
| Storage format | NumPy compressed archives (`.npz`) |


## Equation

The nondimensional incompressible Navier–Stokes equations are

$$
\frac{\partial \mathbf u}{\partial t}
+(\mathbf u\cdot\nabla)\mathbf u
=-\nabla p+\frac{1}{\mathrm{Re}}\nabla^2\mathbf u+\mathbf f,
$$

$$
\nabla\cdot\mathbf u=0,
$$

with

$$
\mathbf u=(u,v),
\qquad
\mathrm{Re}=\frac{UL}{\nu}.
$$

Here $u$ and $v$ are the $x$- and $y$-velocity components and $p$ is nondimensional pressure. The released sample is the converged **steady field**, so the standard learning map is

$$
(\mathrm{Re},g,s)\longmapsto(u,v,p).
$$

## Domain, coordinates, and boundary conditions

$$
\Omega=[0,2]\times[0,2].
$$

The embedded object is stationary and located in the middle of the cavity. The velocity boundary conditions are

$$
(u,v)=(1,0),\qquad y=2,
$$

$$
(u,v)=(0,0),\qquad x=0,\ x=2,\ y=0,
$$

$$
(u,v)=(0,0),\qquad \partial\Omega_{\rm object}.
$$

Thus, the top wall moves in the $x$ direction with unit speed, while the other outer walls and the object surface are no-slip. The dataset section of the paper does not specify the precise pressure-gauge implementation.


## Geometry conditioning

This subset uses all three two-dimensional FlowBench geometry groups. The paper summarizes the 2-D collection as **300 shapes**, approximately 100 per group.

### G1: parametric NURBS curves

- uniform knot vector;
- fixed quadratic B-spline basis;
- eight control points;
- randomly varied control-point positions;
- curves are constrained to be smooth and free of discontinuities and self-intersections;
- every shape is normalized to the unit square $[0,1]^2$.

A general NURBS curve is

$$
\mathbf C(t)=
\frac{\sum_i N_{i,2}(t)w_i\mathbf P_i}
{\sum_i N_{i,2}(t)w_i}.
$$

The paper explicitly randomizes the control-point positions; it does not list the weights $w_i$ as a sampled dataset parameter.

### G2: harmonic radial curves

The paper calls this family spherical harmonics; the 2-D construction is a Fourier-type radial function:

$$
r(t)=0.5+\sum_{n=1}^{N}
\left(a_n\cos nt+b_n\sin nt\right),
\qquad t\in[0,2\pi].
$$

- $N$ is randomly selected from $\{8,\ldots,15\}$;
- $a_n,b_n\in[0,0.2]$;
- the curve is evaluated at 500 uniformly spaced angular points;
- the radius is normalized by
  $$
  \widehat r(t)=0.5\,\frac{r(t)}{r_{\max}},
  $$
  so that no surface point is farther than $0.5$ from the shape center.

### G3: non-parametric SkelNetOn contours

- animal, insect, bird, and other silhouettes are sampled from the grayscale SkelNetOn collection;
- a Gaussian blur with fixed $\sigma=2$ is applied;
- the filtering removes thin or jagged features that would not be represented consistently across resolutions;
- the resulting contour is scaled into $[0,1]^2$.

G3 is not a low-dimensional continuous parametric family and is therefore especially useful for geometry out-of-distribution testing.

### Grid representations of geometry

The paper defines two geometry inputs at the same resolution as the flow fields:

1. **binary geometry mask** $g(\mathbf x)$: semantically 1 inside the object and 0 outside;
2. **signed distance field** $s(\mathbf x)$: negative inside, positive outside, and zero on the surface.

$$
s(\mathbf x)=
\begin{cases}
<0,&\mathbf x\text{ is inside the object},\\
0,&\mathbf x\text{ is on the object boundary},\\
>0,&\mathbf x\text{ is in the fluid region}.
\end{cases}
$$

**File-level caveat:** some older DataPrep code uses a `0/255` mask and derives it with `SDF > 0`. This is not identical to the semantic convention in the paper. Always plot the downloaded mask and SDF to verify sign and scale.


## About the data

| Property | Value |
|---|---|
| Physical problem | 2-D incompressible Navier–Stokes, complex-geometry LDC |
| Temporal regime | steady |
| Paper sample count | **3000** |
| Geometry count | 300: approximately 100 in each of G1/G2/G3 |
| Conditions per geometry | approximately 10 Reynolds conditions by the 3000/300 design |
| Reynolds range | $\mathrm{Re}\in[10,10^3]$ |
| Trajectory length | one final steady snapshot |
| Released resolutions | $128\times128$, $256\times256$, $512\times512$ |
| Released grid | uniform Cartesian arrays; tree-based FEM for the original solve |
| Current hosted size | approximately **28.3 GB** |
| Repository path | `LDC_NS_2D/` |

### Core field tensors in the paper

$$
X\in\mathbb R^{3000\times3\times N_x\times N_y},
\qquad
X=[\mathrm{Re},g,s],
$$

$$
Y_{\rm field}\in\mathbb R^{3000\times3\times N_x\times N_y},
\qquad
Y_{\rm field}=[u,v,p].
$$

The scalar Reynolds number is broadcast to a constant spatial channel.

### Auxiliary channel in the official preparation README

The official DataPrep README illustrates

```text
Y[3000][u, v, p, C][Nx][Ny]
```

where `C` packages engineering summaries derived from $C_D/C_L$ constants files. It is not a local PDE state. Distinguish the three physical field channels from any optional broadcast summary channel.

## Adjustable, varied, and fixed quantities

| Quantity | Adjustable in a solver | Varied in this subset | Fixed in this subset |
|---|---:|---:|---|
| Reynolds number | yes | yes | — |
| object shape | yes | yes | generation rules fixed |
| object position | yes | no | cavity center/middle |
| lid velocity | yes | no | $(1,0)$ |
| outer-wall BCs | yes | no | three stationary no-slip walls |
| object BC | yes | no | stationary no-slip |
| density and viscosity as separate inputs | yes | no | summarized by nondimensionalization and $\mathrm{Re}$ |
| Mach number/compressibility | outside this subset | no | incompressible |
| time | yes | no | final steady field only |

## Initial conditions and time

The paper treats this as a steady problem and does not release the initialization or convergence trajectory. It should be modeled as a steady operator-learning problem rather than trajectory forecasting.


## Numerical generation and post-processing

- massively parallel quadtree/octree finite-element CFD and multiphysics framework;
- complex boundaries handled with the Shifted Boundary Method (SBM), which weakly imposes the true boundary condition on a surrogate boundary embedded in a fixed tree mesh;
- the 2-D calculations are resolved to approximately the Kolmogorov length scale, while the 3-D calculations target roughly twice that scale;
- ParaView/VTK is used to resample adaptive high-resolution solutions onto uniform tensors;
- PETSc BCGS linear solver with an ASM preconditioner;
- relative solver tolerance $10^{-8}$;
- the paper reports approximately 65K node-hours of total compute.

The lower-resolution releases are post-processed from fully resolved simulations rather than independently rerun coarse CFD simulations, which makes the data useful for multi-resolution and super-resolution studies.


## What is interesting and challenging

- the same PDE is solved on both parametric and non-parametric embedded geometries;
- thin, sharp, and highly curved features create additional separation and recirculation regions;
- low global error can coexist with large near-wall pressure and velocity-gradient errors;
- lift and drag coefficients provide application-level targets;
- the subset supports mask-versus-SDF studies, cross-family geometry OOD tests, multi-resolution generalization, and PDE-residual evaluation.

## Release and file caveats

1. The paper lists $[u,v,p]$ as the core output, whereas older DataPrep code may append an auxiliary `C` channel.
2. The paper defines a 0/1 mask, while some scripts use 0/255.
3. Verify the SDF sign from the actual archive.
4. Files are split by geometry family and resolution.
5. An 80/20 random split is the paper's basic recommendation, but geometry-generalization studies should split by geometry instance or family to prevent Reynolds-condition leakage across the same shape.


## Download

Install the Hugging Face Hub client:

```bash
python -m pip install -U huggingface_hub
```

Download this subset:

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="BGLab/FlowBench",
    repo_type="dataset",
    local_dir="./FlowBench",
    allow_patterns=["LDC_NS_2D/128x128/*"],
)
```

Replace `LDC_NS_2D/128x128/*` with the path shown in the code block. For the larger subsets, download one resolution, geometry family, or geometry instance first rather than the full repository.

### Inspect an `.npz` archive

```python
from pathlib import Path
import numpy as np

path = Path("PATH_TO_FILE.npz")
with np.load(path, allow_pickle=False) as archive:
    print("keys:", archive.files)
    for key in archive.files:
        array = archive[key]
        print(key, array.shape, array.dtype)
```

The tensor formulas in the paper describe **semantic axis order**. Always inspect the actual key, shape, channel order, mask values, and SDF sign before training.



## Citation

Please cite the FlowBench paper when using this data:

```bibtex
@article{tali2024flowbench,
  title   = {FlowBench: A Large Scale Benchmark for Flow Simulation over Complex Geometries},
  author  = {Tali, Ronak and Rabeh, Ali and Yang, Cheng-Hau and Shadkhah, Mehdi
             and Karki, Samundra and Upadhyaya, Abhisek and Dhakshinamoorthy, Suriya
             and Saadati, Marjan and Sarkar, Soumik and Krishnamurthy, Adarsh
             and Hegde, Chinmay and Balu, Aditya and Ganapathysubramanian, Baskar},
  journal = {arXiv preprint arXiv:2409.18032},
  year    = {2024}
}
```

The dataset and official tools are released under **CC-BY-NC-4.0**. Consult the full license text before commercial use.



## Sources and evidence policy

This document cross-checks the following official sources, in descending priority:

1. [FlowBench paper and appendices](https://arxiv.org/abs/2409.18032);
2. [official Hugging Face dataset repository](https://huggingface.co/datasets/BGLab/FlowBench);
3. [official case-generation, downsampling, and tensor-preparation code](https://github.com/baskargroup/flowbench-tools);
4. [official Geometry Matters training/evaluation repository](https://github.com/baskargroup/GeometryMatters);
5. [FlowBench project website](https://baskargroup.bitbucket.io/FlowBench/).

The paper, the older preparation scripts, and the current data repository do not represent exactly the same release. This document therefore distinguishes the **paper specification**, the **preparation-code convention**, and the **current hosted release**.  
Last verified: **2026-07-21**.
