---
title: "FlowBench: 2-D transient Navier–Stokes flow past complex objects"
parent_dataset: FlowBench
subset: FPO_NS_2D_1024x256
equation_family: "time-dependent incompressible Navier-Stokes"
spatial_dimension: 2
temporal_regime: transient
task: "sequence-to-sequence or geometry-conditioned trajectory"
geometry_families: ""
license: CC-BY-NC-4.0
last_verified: 2026-07-21
linkTitle: "FPO NS 2D"
weight: 40
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: FlowBench
summary: "Incompressible flow passes a stationary complex bluff body, producing high-resolution velocity and pressure trajectories with vortex shedding."
description: "Incompressible flow passes a stationary complex bluff body, producing high-resolution velocity and pressure trajectories with vortex shedding."

---

# 2-D flow past complex objects (FPO–NS–2D)

**Description:** Incompressible flow passes a stationary complex bluff body, producing high-resolution velocity and pressure trajectories with vortex shedding. FPO is the only publicly released transient FlowBench family. A complex object is placed upstream in a long channel and generates periodic or aperiodic wakes. The data can be used for past-to-future sequence prediction or augmented with Reynolds number, mask, and SDF for geometry-conditioned trajectory modeling.

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

$$
\frac{\partial \mathbf u}{\partial t}
+(\mathbf u\cdot\nabla)\mathbf u
=-\nabla p+\frac{1}{\mathrm{Re}}\nabla^2\mathbf u+\mathbf f,
$$

$$
\nabla\cdot\mathbf u=0,
\qquad
\mathbf u=(u,v).
$$

The time-dependent state is

$$
\mathbf q(t,x,y)=(u,v,p),
$$

and a common learning problem is

$$
\mathbf q_{t_0:t_k}
\longmapsto
\mathbf q_{t_{k+1}:t_{k+m}}.
$$

## Domain, object position, and boundary conditions

The full CFD domain is

$$
\Omega=[0,64]\times[0,16],
$$

with object center

$$
(x_c,y_c)=(6,8).
$$

- left boundary: parabolic velocity inlet;
- top and bottom boundaries: no-slip Dirichlet conditions;
- right boundary: zero-pressure outlet;
- object surface: stationary no-slip boundary.

The paper states that a region with physical span approximately $[0,16]\times[0,4]$ is cropped for release. Treat this as the reported cropped span; verify the array origin and orientation from the files or downsampling script.

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
| Physical system | 2-D transient incompressible Navier–Stokes external flow |
| Nominal paper/code count | **1150 simulations** |
| Current exact count | corrupted files have been removed; enumerate current `Re_*.npz` files |
| Reynolds range | $\mathrm{Re}\in[10^2,10^3]$ |
| Raw frames | **242** in the current data card and code |
| Common usable frames | **240** after ignoring the first two |
| Per-frame channels | $[u,v,p]$ |
| Current resolution | $1024\times256$ |
| Older paper release description | also listed $512\times128$ |
| Current hosted size | approximately **1.59 TB** |
| Repository path | `FPO_NS_2D_1024x256/` |
| Organization | geometry family / geometry ID / `Re_<value>.npz` |

### Time sampling

The appendix reports:

- solver step $\Delta t_{\rm solve}=0.01$;
- output begins near nondimensional time $t=392$;
- output interval $\Delta t_{\rm out}=0.05$;
- output continues to approximately $t=404$;
- each retained sample contains at least two vortex-shedding cycles;
- the output frequency was selected to provide roughly at least 100 snapshots per shedding cycle.

### Tensor representation

The paper's semantic representation is

$$
Y\in\mathbb R^{1150\times240\times3\times N_x\times N_y},
\qquad
Y=[u,v,p].
$$

The hosted repository exposes complete 242-frame simulations and leaves the input/output windows to the user. The official `fpo2d.py` script builds

$$
X\in\mathbb R^{N\times T_{in}\times3\times N_x\times N_y},
$$

$$
Y\in\mathbb R^{N\times T_{out}\times3\times N_x\times N_y}.
$$

The script initializes `[N,T,C,Ny,Nx]` and transposes to `[N,T,C,Nx,Ny]`. Older README text contains a different order, so inspect the actual archive.

### Is geometry an input?

Two task definitions are possible:

1. **official example Seq2Seq:** only past $u,v,p$ frames are used; the script comments state that geometry is not separately supplied;
2. **geometry-conditioned trajectory modeling:** add $\mathrm{Re},g,s$ and predict a full or future trajectory.

The second task is physically meaningful but is not the default packaging of `fpo2d.py`.

## Adjustable, varied, and fixed quantities

| Quantity | Treatment |
|---|---|
| geometry | varied |
| Reynolds number | varied |
| temporal state | varied |
| object position | fixed at $(6,8)$ |
| mean flow direction | fixed along $x$ |
| inlet type | fixed parabolic profile |
| top/bottom walls | fixed no-slip |
| outlet | fixed zero pressure |
| solver time step | fixed at 0.01 |
| output interval | fixed at 0.05 |
| temperature | absent |
| compressibility | incompressible |

## Derived vorticity

The paper frequently visualizes

$$
\omega_z=
\frac{\partial v}{\partial x}
-\frac{\partial u}{\partial y}.
$$

Vorticity is derived from velocity and is not a core Appendix Table 9 channel.

## Adaptive mesh

The appendix describes five circular refinement regions around $(6,8)$ with radii 0.71, 0.8, 1, 2.5, and 3 and levels 13, 12, 11, 10, and 9, respectively. The immediate object neighborhood reaches level 14, and two rectangular wake regions are also refined.

- approximately 117,978 mesh nodes;
- approximately 353,934 velocity/pressure degrees of freedom;
- an equivalent finest-level uniform mesh would require about 201M degrees of freedom.

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

- geometry, Reynolds number, and long temporal dynamics vary simultaneously;
- low-Re wakes can be nearly periodic, while higher-Re wakes are more irregular;
- long rollouts accumulate phase, frequency, and amplitude errors;
- near-object and far-wake regions have very different resolution requirements;
- approximately 1.59 TB of data creates substantial I/O and caching challenges;
- useful for sequence models, autoregressive rollout, latent dynamics, and geometry-conditioned field/video prediction.

## Release and file caveats

1. The paper table uses 240 frames; the current card uses 242 and the code says to ignore the first two.
2. The stated interval from 392 to 404 at spacing 0.05 would yield 241 points if both endpoints were included; use file-level time information as authoritative.
3. The $512\times128$ release was removed on 2025-02-02 because the geometry was not properly resolved; the hosted release retains $1024\times256$.
4. Corrupted harmonics and NURBS samples were removed, so the current file count may be below the nominal 1150.
5. Dataset-card prose has mentioned three conditions per geometry, while current example folders can contain five `Re_*.npz` files. Enumerate files rather than assuming a fixed count.
6. SkelNetOn folder spelling varies across releases (`skelneton`, `skelenton`, and related variants).

## Download

Start with one geometry instance rather than the full 1.59 TB subset:

```bash
python -m pip install -U huggingface_hub
```

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="BGLab/FlowBench",
    repo_type="dataset",
    local_dir="./FlowBench",
    allow_patterns=["FPO_NS_2D_1024x256/nurbs/36/*"],
)
```

To request a full geometry family:

```python
allow_patterns=["FPO_NS_2D_1024x256/nurbs/*"]
```

Inspect every `Re_*.npz` key and shape after download.

## Sources and evidence policy

This document cross-checks the following official sources, in descending priority:

1. [FlowBench paper and appendices](https://arxiv.org/abs/2409.18032);
2. [official Hugging Face dataset repository](https://huggingface.co/datasets/BGLab/FlowBench);
3. [official case-generation, downsampling, and tensor-preparation code](https://github.com/baskargroup/flowbench-tools);
4. [official Geometry Matters training/evaluation repository](https://github.com/baskargroup/GeometryMatters);
5. [FlowBench project website](https://baskargroup.bitbucket.io/FlowBench/).

The paper, the older preparation scripts, and the current data repository do not represent exactly the same release.
Last verified: **2026-07-21**.
