---
title: "FlowBench: 3-D complex-geometry lid-driven cavity Navier–Stokes"
parent_dataset: FlowBench
subset: LDC_NS_3D
equation_family: "3-D incompressible Navier-Stokes"
spatial_dimension: 3
temporal_regime: steady
task: "3-D geometry-and-Reynolds-to-field"
geometry_families: ""
license: CC-BY-NC-4.0
last_verified: 2026-07-21
linkTitle: "LDC NS 3D"
weight: 50
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: FlowBench
summary: "A moving top face drives incompressible flow in a cubic cavity containing a stationary 3-D object, and the steady solution is released on a uniform $128^3$ grid."
description: "A moving top face drives incompressible flow in a cubic cavity containing a stationary 3-D object, and the steady solution is released on a uniform $128^3$ grid."

---

# 3-D complex-geometry lid-driven cavity (LDC–NS–3D)

**One-line description:** A moving top face drives incompressible flow in a cubic cavity containing a stationary 3-D object, and the steady solution is released on a uniform $128^3$ grid.

**Longer description:** This subset extends the lid-driven cavity to three dimensions with adaptive octree refinement near the embedded object. The paper release contained 500 ellipsoid/torus cases; the current official repository has been updated to 1000 samples and lists ellipsoids, toroids, boxes, and cylinders.

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
\mathbf u=(u,v,w).
$$

In components,

$$
\frac{\partial u}{\partial x}
+\frac{\partial v}{\partial y}
+\frac{\partial w}{\partial z}=0.
$$

The steady operator is

$$
(\mathrm{Re},g,s)\longmapsto(u,v,w,p).
$$

## Domain and boundary conditions

$$
\Omega=[0,2]\times[0,2]\times[0,2].
$$

The top face moves in the $x$ direction:

$$
(u,v,w)=(1,0,0).
$$

All other five outer faces and the object surface are stationary no-slip boundaries:

$$
(u,v,w)=(0,0,0).
$$

The object is fixed in the middle of the cavity.

## Three-dimensional geometries

### Paper and early-code release

- 500 samples in the paper;
- ellipsoids and tori/rings;
- varying major-to-minor axis ratio for ellipsoids;
- varying inner-to-outer radius ratio for rings;
- the paper also describes varying aspect ratios and orientations;
- the CaseGenerator README describes an early collection of 50 3-D shapes with multiple Reynolds conditions.

The complete parameter ranges for axis ratios, radius ratios, and rotations are not published.

### Current hosted release

The current Hugging Face card lists

- ellipsoids;
- toroids;
- boxes;
- cylinders;

and states **1000 samples at $128^3$**. The hosted release is therefore an expanded version rather than a frozen copy of the paper's original 500 samples.

### Geometry channels

The semantic inputs remain a broadcast Reynolds field, binary mask $g(x,y,z)$, and SDF $s(x,y,z)$. The paper uses negative-inside SDF and an inside-one mask. Older 3-D DataPrep code constructs a 0/255 mask from `SDF > 0`, so verify the actual file convention visually.

## About the data

| Property | Value |
|---|---|
| Physical system | 3-D steady incompressible Navier–Stokes LDC |
| Paper sample count | 500 |
| Current sample count | **1000** |
| Reynolds range | overall paper range $[10,10^3]$ |
| Resolution | $128\times128\times128$ |
| Trajectory length | one final steady snapshot |
| Current hosted size | approximately **33.4 GB** |
| Input file | `LDC_3d_X.npz`, approximately 7.25 GB |
| Output file | `LDC_3d_Y.npz`, approximately 26.2 GB |
| Repository path | `LDC_NS_3D/` |

### Abbreviated tensor in the paper

The appendix writes

$$
X\in\mathbb R^{500\times3\times N_x\times N_y\times N_z},
\qquad
X=[\mathrm{Re},g,s],
$$

$$
Y\in\mathbb R^{500\times3\times N_x\times N_y\times N_z},
\qquad
Y=[u,v,p].
$$

The output expression omits the third velocity component $w$.

### Physical channels in the official preparation code

The 3-D script explicitly reads source columns

```text
x, y, z, u, v, w, p
```

and writes four physical fields:

$$
[u,v,w,p].
$$

It also creates a fifth auxiliary channel whose two spatial halves contain broadcast $C_D$ and $C_L$. Thus the older scripted output is effectively

$$
Y_{\rm script}=[u,v,w,p,C],
$$

where $C$ is not a local PDE state. Inspect the current hosted file to determine whether it retains this packaging.

## Adjustable, varied, and fixed quantities

| Quantity | Treatment |
|---|---|
| Reynolds number | varied |
| 3-D geometry class | varied |
| aspect/radius ratio | varied |
| orientation | described as varied; exact range unpublished |
| object position | fixed in the cavity middle |
| lid velocity | fixed at $(1,0,0)$ |
| other faces and object | fixed no-slip |
| domain | fixed at $[0,2]^3$ |
| time | final steady field only |
| temperature | absent |
| compressibility | incompressible |

## Mesh and degrees of freedom

- refinement level 9 near the object, with nominal scale $2/2^9$;
- progressive coarsening to level 7 away from the object, with nominal scale $2/2^7$;
- approximately 2.5M degrees of freedom in the original problem;
- target resolution of roughly twice the Kolmogorov scale;
- final uniform resampling to $128^3$.


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

- 3-D input/output tensors are large and constrain batch size;
- all three velocity components and pressure must be recovered;
- orientation and aspect ratio produce genuinely three-dimensional recirculation structures;
- the expanded release includes geometry classes not listed in the paper;
- surface-near velocity and pressure gradients are highly sensitive to geometry representation and resolution.

## Release and file caveats

1. The paper and older DataPrep documentation use 500 samples; the current repository uses 1000.
2. The paper emphasizes ellipsoids and tori, while the current card also lists boxes and cylinders.
3. The paper table omits $w$; the official code explicitly reads and writes it.
4. Older code may append a fifth $C_D/C_L$ auxiliary channel.
5. Incomplete/old default values such as `num_geometry=25` and `num_Reynolds=10` in the script must not be treated as the composition of the current 1000-sample release.
6. Reserve additional local space beyond the hosted 33.4 GB for caches and training tensors.


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
    allow_patterns=["LDC_NS_3D/*"],
)
```

Replace `LDC_NS_3D/*` with the path shown in the code block. For the larger subsets, download one resolution, geometry family, or geometry instance first rather than the full repository.

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
