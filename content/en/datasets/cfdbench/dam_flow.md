---
title: "CFDBench — Gravity-driven two-phase flow over an obstacle"
dataset: CFDBench
problem_id: dam_flow
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
multiphase: true
gravity: true
linkTitle: "Dam Flow"
weight: 30
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: CFDBench
summary: "Water enters a rectangular air-filled domain through a low left velocity inlet, crosses a fixed vertical obstacle, and forms a jet, recirculation, and wall impact under gravity;…"
description: "Water enters a rectangular air-filled domain through a low left velocity inlet, crosses a fixed vertical obstacle, and forms a jet, recirculation, and wall impact under gravity;…"

---

# CFDBench — Gravity-driven two-phase flow over an obstacle

**One-line description:** Water enters a rectangular air-filled domain through a low left velocity inlet, crosses a fixed vertical obstacle, and forms a jet, recirculation, and wall impact under gravity; inlet speed, density/viscosity, and obstacle geometry are varied separately.

**Longer description:** The paper simplifies a dam-break/overflow scenario into a two-dimensional water--air flow over a vertical step. At low Reynolds number, viscous effects dominate and the fluid descends along the obstacle; at higher inlet velocity, inertia produces an over-obstacle jet that falls under gravity and impacts the bottom wall. The problem combines a source term, a phase interface, mixed inlet boundaries, and an explicit obstacle. It has the highest reported per-frame generation time among the four configurations.

- Parent dataset: **CFDBench**
- Dataset authors: Yining Luo, Yingfa Chen, and Zhen Zhang
- Generator: ANSYS Fluent 2021R1 with VOF and gravity
- Official loader: [`src/dataset/dam.py`](https://github.com/luo-yining/CFDBench/blob/main/src/dataset/dam.py)


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


For this problem, $\mathbf g=(0,-g)^{\mathsf T}$. Fluent also solves a VOF phase fraction; its standard no-mass-transfer form is

$$
\frac{\partial\alpha}{\partial t}+\nabla\cdot(\alpha\mathbf u)=0,
$$

but $\alpha$ is not a standardized target in the interpolated archives.

## Physical domain, coordinates, and boundary conditions

The outer domain is $1.5\,\mathrm m$ long and $0.4\,\mathrm m$ high. The $x$ direction points right, $y$ points upward, and gravity is downward. The lower $0.1\,\mathrm m$ segment of the left boundary is a velocity inlet; the upper $0.3\,\mathrm m$ segment is a pressure inlet. The right boundary is a pressure outlet, and the top and bottom are walls. The left face of the vertical obstacle is $0.5\,\mathrm m$ from the inlet; its height and width are $h,w$.

A simplified boundary representation is

$$
\mathbf u(0,y,t)=(u_\mathrm{{in}},0)
\quad\text{{on the lower inlet segment}},
$$

$$
p=p_\mathrm{{in}}
\quad\text{{on the upper-left pressure inlet}},
\qquad
p=p_\mathrm{{out}}
\quad\text{{on the right outlet}},
$$

with no-slip conditions on solid walls and the obstacle.

## About the data

| Item | Value or description |
|---|---|
| Spatial dimension | 2D |
| Phases and source | Water--air VOF; gravity in $-y$ |
| Outer domain | $1.5\,\mathrm m\times0.4\,\mathrm m$ |
| Interpolated arrays | `u.npy`, `v.npy`: $(T_i,64,64)$ |
| Current loader features | Approximately $(T_i,3,66,65)$ with $(u,v,\mathrm{{mask}})$ after adding a left inlet column and top/bottom wall rows |
| Geometry encoding | The obstacle is encoded by the mask; the current five-scalar vector retains outer-domain `height/width`, not obstacle $h,w$ |
| Cases/trajectories | 220 = 70 BC + 100 PROP + 50 GEO |
| Total frames | 21,916 |
| Mean frames per case | 99.62; not a fixed length |
| Time interval | $\Delta t=0.1\,\mathrm s$ |
| Common $t_\max$ | Not reported; determine it from each array length |
| Raw size per frame in paper | Approximately 2.0 MB |
| Generation time in paper | Approximately 3.98 s/frame |
| Current archive | `dam.zip`, approximately 1.35 GB (2026-07-21) |

## Baseline configuration

$$
\rho=100\,\mathrm{{kg\,m^{{-3}}}},\qquad
\mu=0.1\,\mathrm{{Pa\,s}},\qquad
u_\mathrm{{in}}=1\,\mathrm{{m/s}},
$$

$$
h=0.1\,\mathrm m,\qquad
w=0.05\,\mathrm m,
$$

$$
L_x=1.5\,\mathrm m,\qquad L_y=0.4\,\mathrm m.
$$

Current loader parameter order:

```text
[velocity, density, viscosity, height, width]
```

Here `height=0.4` and `width=1.5` are outer-domain dimensions. The varying obstacle geometry in the GEO subset is primarily supplied through the mask.

## Parameter sweep: varied versus fixed

| Subset | Cases | Parameters actually varied | Conditions held fixed |
|---|---:|---|---|
| BC | 70 | $u_\mathrm{{in}}\in\{{0.05,0.10,\ldots,1.00\}}\cup\{{1.02,1.04,\ldots,2.00\}}\,\mathrm{{m/s}}$, giving $20+50$ values | $\rho=100$, $\mu=0.1$, $h=0.1$, $w=0.05$; outer domain, gravity, and boundary types fixed |
| PROP | 100 | Main text and generation scripts agree on $\rho=\{{10,120,230,340,450,560,670,780,890,1000\}}$ and $\mu=\{{0.01,0.12,0.23,0.34,0.45,0.56,0.67,0.78,0.89,1.00\}}$, all $10\times10$ combinations | $u_\mathrm{{in}}=1$, $h=0.1$, $w=0.05$; outer domain, gravity, and boundaries fixed |
| GEO | Paper total: 50 | $h\in\{{0.11,0.12,0.13,0.14,0.15\}}\,\mathrm m$; $w\in\{{0.01,0.02,\ldots,0.09\}}\,\mathrm m$ | $u_\mathrm{{in}}=1$, $\rho=100$, $\mu=0.1$; outer domain, obstacle position, gravity, and boundary types fixed |

> **Two internal conflicts in the Dam description.**
>
> 1. Table 4 prints a low-density/low-viscosity set resembling Cavity, while the main text and official generation scripts agree on the $10\times10$ grid above. This page follows the mutually supported text/code version.
> 2. Five heights times nine widths give 45 full combinations, whereas the summary table reports 50 GEO cases. The public text does not identify the additional five, so the downloaded `case.json` files are authoritative.

**Adjustable but held fixed:** gravitational acceleration, pressure-inlet/outlet values, obstacle position, outer-domain dimensions, air-phase properties, surface tension, and initial phase distribution are fixed or not exposed as explicit sweep parameters.


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
hf download chen-yingfa/CFDBench dam.zip \\
  --repo-type dataset \\
  --local-dir ./downloads/CFDBench
unzip ./downloads/CFDBench/dam.zip -d ./data
```

## What is interesting and challenging

- Gravity, a VOF interface, a jet, recirculation, and a solid obstacle occur in one problem.
- Changing obstacle dimensions preserves topology but strongly changes the passable region and impact location.
- GEO information is mainly spatially encoded by a mask; the current scalar parameter vector does not explicitly retain obstacle $h,w$.
- It has fewer/shorter trajectories, yet the highest reported Fluent generation time per frame.

## Known caveats

- PROP values and the GEO count contain internal paper inconsistencies; do not reconstruct the case list from tables alone.
- Current loader `height,width` are outer-domain dimensions, not the obstacle dimensions varied in the paper.
- Stored arrays are $64\times64$, while loader padding may produce $66\times65$.
- Raw data may include VOF and pressure; standardized interpolated targets remain $u,v$.

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

- Paper: Sections 3.1 and 3.4, Tables 4 and 6, Section 3.6, Appendix E.1.
- Code: `src/dataset/dam.py` and the Dam Fluent Scheme.
