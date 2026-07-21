---
title: "FlowBench: 2-D thermally coupled lid-driven cavity with variable Reynolds number"
parent_dataset: FlowBench
subset: LDC_NSHT_2D_variable-Re
equation_family: "incompressible Navier-Stokes + heat transfer, Boussinesq coupling"
spatial_dimension: 2
temporal_regime: steady
task: geometry-Reynolds-Richardson-to-coupled-fields
geometry_families: ""
license: CC-BY-NC-4.0
last_verified: 2026-07-21
linkTitle: "LDC NSHT 2D (var Re)"
weight: 30
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: FlowBench
summary: "Complex geometry, Reynolds number, and the buoyancy-to-inertia ratio are varied jointly to produce steady velocity, pressure, and temperature fields."
description: "Complex geometry, Reynolds number, and the buoyancy-to-inertia ratio are varied jointly to produce steady velocity, pressure, and temperature fields."

---

# 2-D thermally coupled lid-driven cavity: variable Reynolds number

**Description:** Complex geometry, Reynolds number, and the buoyancy-to-inertia ratio are varied jointly to produce steady velocity, pressure, and temperature fields. This subset uses the same coupled equations and boundary conditions as the constant-Re NSHT subset, but scans both inertial/viscous and buoyancy effects. It is therefore the broader multi-parameter operator-learning problem.

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

## Equations

$$
\frac{\partial \mathbf u}{\partial t}
+(\mathbf u\cdot\nabla)\mathbf u
=-\nabla p
+\frac{1}{\mathrm{Re}}\nabla^2\mathbf u
+\mathrm{Ri}\,\theta\,\mathbf e_g
+\mathbf f,
$$

$$
\nabla\cdot\mathbf u=0,
$$

$$
\frac{\partial\theta}{\partial t}
+\mathbf u\cdot\nabla\theta
=\frac{1}{\mathrm{Pe}}\nabla^2\theta,
$$

with

$$
\mathrm{Ri}=\frac{\mathrm{Gr}}{\mathrm{Re}^2},
\qquad
\mathrm{Gr}=\mathrm{Ri}\,\mathrm{Re}^2,
\qquad
\mathrm{Pe}=0.7\,\mathrm{Re}.
$$

Therefore $\mathrm{Ri}$ and $\mathrm{Re}$ contain enough information to reconstruct $\mathrm{Gr}$.

## Domain and boundary conditions

$$
\Omega=[0,2]\times[0,2].
$$

Velocity:

- top wall: $(u,v)=(1,0)$;
- other three outer walls and object surface: $(u,v)=(0,0)$.

Temperature:

- bottom wall: $\theta=1$;
- top wall: $\theta=0$;
- left and right walls: $\partial_n\theta=0$;
- object surface: $\theta=0$.

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
| Physical system | 2-D incompressible NS + heat transfer with Boussinesq coupling |
| Temporal regime | steady |
| Sample count | **3000** |
| Geometry count | approximately 300 |
| Conditions per geometry | approximately 10 |
| Reynolds range | overall paper range $[10,10^3]$ |
| Grashof range | overall paper range $[10,10^7]$ |
| Resolutions | $128^2$, $256^2$, $512^2$ |
| Trajectory length | one final steady snapshot |
| Current hosted size | approximately **34.6 GB** |
| Repository path | `LDC_NSHT_2D_variable-Re/` |

### Tensors

The official split-specific preparation convention is

$$
X\in\mathbb R^{3000\times4\times N_x\times N_y},
\qquad
X=[\mathrm{Ri},\mathrm{Re},g,s],
$$

$$
Y_{\rm field}\in\mathbb R^{3000\times4\times N_x\times N_y},
\qquad
Y_{\rm field}=[u,v,p,\theta].
$$

Older preparation documentation may append a `C*` summary channel containing $C_D,C_L,$ and $\mathrm{Nu}$ information.

## Parameter design

| Parameter | Varied? | Relation/range |
|---|---:|---|
| geometry | yes | G1/G2/G3 |
| $\mathrm{Re}$ | yes | overall paper range 10–$10^3$ |
| $\mathrm{Ri}$ | yes | buoyancy/inertia ratio |
| $\mathrm{Gr}$ | induced | $\mathrm{Gr}=\mathrm{Ri}\mathrm{Re}^2$ |
| $\mathrm{Pe}$ | coupled to Re | $0.7\mathrm{Re}$ |
| $\mathrm{Pr}$ | no | 0.7 |
| domain and object position | no | fixed |
| velocity and thermal BCs | no | fixed |
| time | no | steady |

The paper illustrates parameter pairs such as $(\mathrm{Ri},\mathrm{Re})=(0.321,16)$, $(1.76,640)$, $(2.847,720)$, and $(9.452,952)$. These are examples, not the complete parameter list.

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

- geometry shift, Reynolds shift, and convection-regime shift occur simultaneously;
- equal Richardson number does not imply identical boundary-layer thickness at different Reynolds numbers;
- increasing Reynolds number weakens relative viscosity, whereas increasing Richardson number strengthens buoyant circulation;
- the model must predict four coupled fields while respecting incompressibility and thermal transport;
- the subset is useful for parameter encodings, nondimensional-condition tokens, and multiphysics foundation models.

## Release and file caveats

1. The paper's combined table uses `[Re, Gr, g, s]`; the split-specific DataPrep convention uses `[Ri, Re, g, s]`.
2. The parameterizations are information-equivalent, but preprocessing must not mix them silently.
3. `C*` may be present as a packaged auxiliary channel rather than a local field.
4. Verify mask and SDF conventions from the actual files.
5. Geometry-generalization tests should split by geometry ID, not by arbitrary sample.

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
    allow_patterns=["LDC_NSHT_2D_variable-Re/128x128/*"],
)
```

Replace `LDC_NSHT_2D_variable-Re/128x128/*` with the path shown in the code block. For the larger subsets, download one resolution, geometry family, or geometry instance first rather than the full repository.

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

## Sources and evidence policy

This document cross-checks the following official sources, in descending priority:

1. [FlowBench paper and appendices](https://arxiv.org/abs/2409.18032);
2. [official Hugging Face dataset repository](https://huggingface.co/datasets/BGLab/FlowBench);
3. [official case-generation, downsampling, and tensor-preparation code](https://github.com/baskargroup/flowbench-tools);
4. [official Geometry Matters training/evaluation repository](https://github.com/baskargroup/GeometryMatters);
5. [FlowBench project website](https://baskargroup.bitbucket.io/FlowBench/).

The paper, the older preparation scripts, and the current data repository do not represent exactly the same release.
Last verified: **2026-07-21**.
