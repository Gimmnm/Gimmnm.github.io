---
title: "CFDBench — Lid-driven cavity flow"
dataset: CFDBench
problem_id: cavity_flow
equation_family: "2D incompressible Navier-Stokes"
time_dependent: true
data_origin: "ANSYS Fluent numerical simulation"
interpolated_grid: "64 x 64"
license: "Apache-2.0 (Hugging Face dataset card)"
paper: "https://arxiv.org/abs/2310.05963"
code: "https://github.com/luo-yining/CFDBench"
interpolated_data: "https://huggingface.co/datasets/chen-yingfa/CFDBench"
raw_data: "https://huggingface.co/datasets/chen-yingfa/CFDBench-raw"
last_verified: 2026-07-21
subsets: ["bc", "prop", "geo"]
linkTitle: "Cavity Flow"
weight: 10
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: CFDBench
summary: "A two-dimensional closed rectangular cavity is driven by a moving top wall, producing a primary recirculating vortex and smaller corner vortices; the dataset separately varies l…"
description: "A two-dimensional closed rectangular cavity is driven by a moving top wall, producing a primary recirculating vortex and smaller corner vortices; the dataset separately varies l…"

---

# CFDBench — Lid-driven cavity flow

**One-line description:** A two-dimensional closed rectangular cavity is driven by a moving top wall, producing a primary recirculating vortex and smaller corner vortices; the dataset separately varies lid speed, density/viscosity, and cavity dimensions.

**Longer description:** Lid-driven cavity flow is a classical CFD verification problem. It combines a moving no-slip wall, three stationary no-slip walls, and a discontinuous boundary condition where the lid meets the side walls. CFDBench uses it to evaluate inference-time generalization to unseen boundary speeds, fluid properties, and rectangular geometries. The BC, PROP, and GEO subsets are generated separately rather than as one five-dimensional Cartesian product.

- Parent dataset: **CFDBench**
- Dataset authors: Yining Luo, Yingfa Chen, and Zhen Zhang (Tsinghua University)
- Generator: ANSYS Fluent 2021R1; mesh and batch-generation scripts are under `generation-code/`
- Official loader: [`src/dataset/cavity.py`](https://github.com/luo-yining/CFDBench/blob/main/src/dataset/cavity.py)


## Governing equations

The paper uses the two-dimensional incompressible Newtonian Navier--Stokes equations as the common governing system for all four problems. In conservative form,

$$
\nabla\cdot(\rho\mathbf u)=0,
$$

$$
\frac{\partial(\rho\mathbf u)}{\partial t}
+\nabla\cdot(\rho\mathbf u\otimes\mathbf u)
=-\nabla p
+\nabla\cdot\left\{\mu\left[\nabla\mathbf u+(\nabla\mathbf u)^{\mathsf T}\right]\right\}
+\rho\mathbf g,
$$

where $\mathbf u=(u,v)^{\mathsf T}$, $u$ and $v$ are the velocity components in the $x$ and $y$ directions, $p$ is pressure, $\rho$ is density, and $\mu$ is dynamic viscosity. Except for the dam problem, $\mathbf g$ can be taken as zero. For constant $\rho$ and $\mu$, the component form is

$$
\frac{\partial u}{\partial x}+\frac{\partial v}{\partial y}=0,
$$

$$
\frac{\partial u}{\partial t}
+u\frac{\partial u}{\partial x}
+v\frac{\partial u}{\partial y}
=-\frac{1}{\rho}\frac{\partial p}{\partial x}
+\frac{\mu}{\rho}\left(
\frac{\partial^2u}{\partial x^2}+\frac{\partial^2u}{\partial y^2}
\right)+g_x,
$$

$$
\frac{\partial v}{\partial t}
+u\frac{\partial v}{\partial x}
+v\frac{\partial v}{\partial y}
=-\frac{1}{\rho}\frac{\partial p}{\partial y}
+\frac{\mu}{\rho}\left(
\frac{\partial^2v}{\partial x^2}+\frac{\partial^2v}{\partial y^2}
\right)+g_y.
$$

> **Scope of the written equations.** The incompressible Navier--Stokes system above is the mathematical system explicitly written in the paper. The Fluent setups for Tube and Dam additionally use a VOF multiphase model, and some Cylinder cases use an SST $k$--$\omega$ turbulence closure. The paper does not provide the complete auxiliary VOF/SST equations and constants, so they are not presented here as if they were explicitly documented target equations.


## Physical domain, coordinates, and boundary conditions

The domain is

$$
D=[0,l]\times[0,w],
$$

with $x$ pointing right and $y$ upward. The top wall moves in the $+x$ direction with speed $u_\mathrm{{top}}$, while the other walls are stationary:

$$
\mathbf u(x,w,t)=(u_\mathrm{{top}},0),\qquad
\mathbf u(x,0,t)=\mathbf 0,
$$

$$
\mathbf u(0,y,t)=\mathbf 0,\qquad
\mathbf u(l,y,t)=\mathbf 0.
$$

The generation Scheme initializes pressure and velocity at rest and then applies the moving lid. The velocity discontinuity at the lid/side-wall junction is an important numerical feature.

## About the data

| Item | Value or description |
|---|---|
| Spatial dimension | 2D |
| Temporal character | Transient; supports one-step and multi-step prediction |
| Interpolated arrays | `u.npy`, `v.npy`: $(T_i,64,64)$ |
| Current loader features | $(T_i,3,64,64)$ with $(u,v,\mathrm{{mask}})$; mask is all ones |
| Physical targets | $u$ and $v$; pressure is not a standardized target in the interpolated archives |
| Grid | Uniform Cartesian after interpolation; physical cell size changes with $l,w$ |
| Cases/trajectories | 159 = 50 BC + 84 PROP + 25 GEO |
| Total frames | 34,582 |
| Mean frames per case | 217.50; this is not a fixed trajectory length |
| Stored interval | Both paper and loader use $\Delta t=0.1\,\mathrm s$ |
| Common $t_\max$ | Not reported; derive it per case from `u.npy.shape[0]` and $\Delta t$ |
| Raw size per frame in paper | Approximately 5.2 MB |
| Generation time in paper | Approximately 0.92 s/frame |
| Current archive | `cavity.zip`, approximately 786 MB (2026-07-21) |

## Baseline configuration

$$
\rho=1\,\mathrm{{kg\,m^{{-3}}}},\qquad
\mu=10^{{-5}}\,\mathrm{{Pa\,s}},
$$

$$
l=w=0.01\,\mathrm m,\qquad
u_\mathrm{{top}}=10\,\mathrm{{m\,s^{{-1}}}}.
$$

The code orders the case parameters as

```text
[vel_top, density, viscosity, height, width]
```

## Parameter sweep: varied versus fixed

| Subset | Cases | Parameters actually varied | Conditions held fixed |
|---|---:|---|---|
| BC | 50 | $u_\mathrm{{top}}\in\{{1,2,\ldots,50\}}\,\mathrm{{m/s}}$ | $\rho=1$, $\mu=10^{{-5}}$, $l=w=0.01$; initialization and wall types fixed |
| PROP | 84 | $\rho\in\{{0.1,0.5,1,2,\ldots,10\}}\,\mathrm{{kg/m^3}}$; $\mu\in\{{10^{{-5}},5\times10^{{-5}},10^{{-4}},5\times10^{{-4}},10^{{-3}},5\times10^{{-3}},10^{{-2}}\}}\,\mathrm{{Pa\,s}}$; all $12\times7$ combinations | $u_\mathrm{{top}}=10$, $l=w=0.01$; boundary types and initialization fixed |
| GEO | 25 | $l,w\in\{{0.01,0.02,0.03,0.04,0.05\}}\,\mathrm m$, all $5\times5$ combinations | $u_\mathrm{{top}}=10$, $\rho=1$, $\mu=10^{{-5}}$; wall types fixed |

**Adjustable but not jointly swept:** $u_\mathrm{{top}},\rho,\mu,l,w$ are all adjustable in the PDE or geometry, but CFDBench varies them by subset. Lid direction, wall types, initialization, two-dimensional assumption, and numerical scheme are fixed.


## Numerical generation setup

- Generator: ANSYS Fluent 2021R1. Mesh-generation and batch-generation assets are under `generation-code/`, including ICEM RPL and Fluent Scheme files.
- Laminar/turbulent treatment: the laminar model is used for laminar cases; SST $k$--$\omega$ is used when turbulence closure is required.
- Pressure--velocity coupling: Coupled Scheme for single-phase flow and SIMPLE for two-phase flow.
- Spatial discretization: second-order pressure interpolation; PRESTO! for VOF; second-order upwind for momentum.
- Time discretization: first-order implicit.
- Interpolation: least squares; released fields are mapped to a $64\times64$ Cartesian grid.
- Near-wall mesh: the first near-wall layer is refined to approximately $10^{-5}\,\mathrm m$.
- Convergence: the paper sets the global residual criterion to $10^{-9}$; final velocity residuals reach at least approximately the $10^{-6}$ level.
- Generation hardware: AMD Ryzen Threadripper 3990X with 30 solver processes.
- Numerical precision: the paper does not state single versus double precision; the dtype of the released NumPy arrays should not be used to infer Fluent solver precision.



## Learning tasks, inputs, and outputs

CFDBench supports two task formulations.

### Non-autoregressive coordinate query

$$
\widehat{q}(x,y,t)=f_\theta\big((x,y,t),\Omega\big),
$$

where $\Omega$ contains boundary, physical-property, and geometry conditions. The FFN/DeepONet experiments in the paper commonly predict one scalar velocity component at each query point, while the files still store both $u$ and $v$.

### Autoregressive field propagation

$$
\widehat{\mathbf u}^{\,n+1}
=f_\theta\big(\mathbf u^n,\Omega,\mathrm{mask}\big).
$$

A typical input consists of the current two-component velocity field, a case-parameter vector, and a geometry/boundary mask; the label is the next $u,v$ field. The official loaders stack `u`, `v`, and `mask` into `(T,3,H,W)` features. The mask is a static condition rather than a conserved physical variable and should not be normalized like a velocity channel.

### Splits

Each base subset is divided into train/validation/test at an 8:1:1 ratio by case. Frames from one trajectory are not distributed across different splits, ensuring that test operating conditions remain unseen during training. Exact reproduction requires a fixed code revision, random seed, and resolved case list.



## Download and directory layout

### Official links

- Paper: [https://arxiv.org/abs/2310.05963](https://arxiv.org/abs/2310.05963)
- Official code: [https://github.com/luo-yining/CFDBench](https://github.com/luo-yining/CFDBench)
- Interpolated data: [https://huggingface.co/datasets/chen-yingfa/CFDBench](https://huggingface.co/datasets/chen-yingfa/CFDBench)
- Raw Fluent data: [https://huggingface.co/datasets/chen-yingfa/CFDBench-raw](https://huggingface.co/datasets/chen-yingfa/CFDBench-raw)
- Baidu Drive mirror for raw data: [https://pan.baidu.com/s/1p0q60cv2hFZ7UcIf3XKSaw?pwd=cfd4](https://pan.baidu.com/s/1p0q60cv2hFZ7UcIf3XKSaw?pwd=cfd4), extraction code `cfd4`
- Documentation style reference: [https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/](https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/)

The repository README describes the interpolated release as approximately 13.4 GB; the Hugging Face page reported approximately 14.4 GB on **2026-07-21**. The README describes the complete raw data as approximately 460 GB, while the current raw Hugging Face page reports about 205 GB and notes that parts of Cylinder are still being uploaded. Reproducible work should record the download date and repository revision.

### Command-line download

Install the current Hugging Face CLI:

```bash
python -m pip install -U huggingface_hub
```

Download the complete interpolated repository:

```bash
hf download chen-yingfa/CFDBench \
  --repo-type dataset \
  --local-dir ./downloads/CFDBench
```

The complete raw repository can require hundreds of gigabytes. Inspect it first:

```bash
hf download chen-yingfa/CFDBench-raw \
  --repo-type dataset \
  --local-dir ./downloads/CFDBench-raw \
  --dry-run
```

### Code repository

```bash
git clone https://github.com/luo-yining/CFDBench.git
cd CFDBench
python -m pip install -r requirements.txt
```

Recommended extracted layout:

```text
data/
├── cavity/
│   ├── bc/caseXXXX/{case.json,u.npy,v.npy}
│   ├── geo/caseXXXX/{case.json,u.npy,v.npy}
│   └── prop/caseXXXX/{case.json,u.npy,v.npy}
├── tube/
├── dam/
└── cylinder/
```


### Download only this problem

```bash
hf download chen-yingfa/CFDBench cavity.zip \\
  --repo-type dataset \\
  --local-dir ./downloads/CFDBench
unzip ./downloads/CFDBench/cavity.zip -d ./data
```

## What is interesting and challenging

- The lid/side-wall junction creates a discontinuous boundary condition.
- The primary vortex is global, while corner vortices require local spatial resolution.
- BC, PROP, and GEO changes all modify effective Reynolds numbers through different physical mechanisms.
- A common $64\times64$ array hides the changing physical grid spacing across cavity sizes; models using only pixel coordinates may confuse numerical and physical scale.

## Known caveats

- The abstract mentions velocity and pressure fields, but the interpolated release and current loader consistently use $u,v$. Pressure requires processing the raw Fluent exports.
- Trajectory length is not constant. Do not replace each true $T_i$ with the ratio 34,582/159.
- The current cavity mask is all ones; moving-wall information is primarily carried by the case vector and boundary handling rather than a complete spatial boundary-value channel.

## Citation

```bibtex
@article{CFDBench,
  title  = {CFDBench: A Large-Scale Benchmark for Machine Learning Methods in Fluid Dynamics},
  author = {Luo, Yining and Chen, Yingfa and Zhang, Zhen},
  year   = {2023},
  url    = {https://arxiv.org/abs/2310.05963}
}
```

## Source locations

- Paper: Sections 3.1--3.2, Tables 2 and 6, Section 3.6, Appendix E.1.
- Code: `src/dataset/cavity.py`, `generation-code/fluent-scheme/`.
