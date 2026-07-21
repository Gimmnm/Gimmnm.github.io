---
title: "CFDBench — Cylinder flow and Karman vortex street"
dataset: CFDBench
problem_id: cylinder_flow
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
linkTitle: "Cylinder Flow"
weight: 40
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: CFDBench
summary: "Fluid enters a two-dimensional channel containing a fixed circular cylinder, producing boundary-layer separation and periodic vortex shedding at suitable Reynolds numbers; inlet…"
description: "Fluid enters a two-dimensional channel containing a fixed circular cylinder, producing boundary-layer separation and periodic vortex shedding at suitable Reynolds numbers; inlet…"

---

# CFDBench — Cylinder flow and Kármán vortex street

![Cylinder flow schematic and parameter ranges](./cylinder-flow.png)

**Description:** Fluid enters a two-dimensional channel containing a fixed circular cylinder, producing boundary-layer separation and periodic vortex shedding at suitable Reynolds numbers; inlet speed, density/viscosity, and cylinder/domain geometry are varied separately. Flow around a cylinder is a classical problem for bluff-body wakes, separation, and Kármán vortex streets. CFDBench filters physical-property combinations to the paper's stated range $20\le\mathrm{{Re}}\le1000$, covering relatively steady wakes through strong periodic shedding. With 205,620 frames—about 68.2% of the complete benchmark—this is the largest configuration and is particularly useful for evaluating long-horizon autoregressive error accumulation and periodic-structure learning.

- Parent dataset: **CFDBench**
- Dataset authors: Yining Luo, Yingfa Chen, and Zhen Zhang
- Generator: ANSYS Fluent 2021R1; SST $k$--$\omega$ closure when required
- Official loader: [`src/dataset/cylinder.py`](https://github.com/luo-yining/CFDBench/blob/main/src/dataset/cylinder.py)

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

> **Scope of the written equations.** The incompressible Navier--Stokes system above is the mathematical system explicitly written in the paper. The Fluent setups for Tube and Dam additionally use a VOF multiphase model, and some Cylinder cases use an SST $k$--$\omega$ turbulence closure. The paper does not provide the complete auxiliary VOF/SST equations and constants.

The paper does not list the complete SST $k$--$\omega$ transport equations and constants, and $k,\omega$ are not target channels in the interpolated release.

## Physical domain, coordinates, and boundary conditions

The $x$ direction follows the inflow from left to right and $y$ is transverse. The left boundary is a velocity inlet, the right boundary is a pressure outlet, the top and bottom are no-slip walls, and the cylinder is a fixed no-slip obstacle.

The paper denotes the distances from the cylinder center to the left, right, bottom, and top boundaries by $x_1,x_2,y_1,y_2$, and denotes a cylinder scale by $d$. If the center is placed at the origin, the outer domain can be represented as

$$
D_\mathrm{{outer}}=[-x_1,x_2]\times[-y_1,y_2],
$$

with the cylinder interior removed. Boundary conditions are

$$
\mathbf u(-x_1,y,t)=(u_\mathrm{{in}},0),
$$

$$
p(x_2,y,t)=p_\mathrm{{out}},
$$

and $\mathbf u=\mathbf0$ on the top/bottom walls and the cylinder surface.

## About the data

| Item | Value or description |
|---|---|
| Spatial dimension | 2D |
| Flow character | Single-phase separation, wake, and periodic vortex shedding |
| Interpolated arrays | `u.npy`, `v.npy`: $(T_i,64,64)$ |
| Current corrected loader | `load_case_data_fix` builds a cylinder/boundary mask on the same grid, approximately $(T_i,3,64,64)$ |
| Legacy code paths | The file retains older padded functions/comments, and some utilities may still assume $66\times65$ |
| Case vector | 8 scalars: `vel_in,density,viscosity,height,width,center_x,center_y,radius` |
| Cases/trajectories | 185 = 50 BC + 115 PROP + 20 GEO |
| Total frames | 205,620 |
| Mean frames per case | 1,111.46; not a fixed length |
| Time interval | Paper and autoregressive loader: $0.001\,\mathrm s$; non-autoregressive class contains $0.1\,\mathrm s$ metadata |
| Common $t_{\mathrm{max}}$ | Not reliably uniform; recover it from case arrays and resolved time metadata |
| Raw size per frame in paper | Approximately 4.4 MB |
| Generation time in paper | Approximately 1.18 s/frame |
| Current archives | `cylinder/` approximately 12 GB: BC 2.94 GB, GEO 2.41 GB, PROP 6.67 GB (2026-07-21) |

## Baseline configuration

$$
\rho=10\,\mathrm{{kg\,m^{{-3}}}},\qquad
\mu=10^{{-3}}\,\mathrm{{Pa\,s}},\qquad
u_\mathrm{{in}}=1\,\mathrm{{m/s}},
$$

$$
d=0.02\,\mathrm m,
$$

$$
x_1=y_1=y_2=0.06\,\mathrm m,
\qquad x_2=0.16\,\mathrm m.
$$

The paper filters PROP cases using

$$
\mathrm{{Re}}=\frac{{\rho u_\mathrm{{in}}d}}{{\mu}}
$$

and retains cases in $[20,1000]$.

## Parameters

Cases are generated in mutually exclusive subsets: each subset varies one operating-condition family while the others stay at the baseline above. Values follow paper Table 5.

| Subset | Cases | Varied parameters and values | Held fixed (baseline) |
|---|---:|---|---|
| BC | 50 | $u_{\mathrm{in}}=u_{\mathcal{B}}\in\{0.1,0.2,0.3,\ldots,5\}\,\mathrm{m/s}$ (step $0.1$) | $\rho=10\,\mathrm{kg\,m^{-3}}$, $\mu=10^{-3}\,\mathrm{Pa\cdot s}$, $d=0.02\,\mathrm{m}$, $x_1=y_1=y_2=0.06\,\mathrm{m}$, $x_2=0.16\,\mathrm{m}$ |
| PROP | 115 | $\rho\in\{0.1,0.2,\ldots,1\}\cup\{1.5,2.5,\ldots,4.5,5\}\cup\{6,7,\ldots,10\}\cup\{20,30,\ldots,250\}\cup\{300,400,500\}\,\mathrm{kg\,m^{-3}}$; $\mu\in\{10^{-4},5\times10^{-4},10^{-3},5\times10^{-3},10^{-2}\}\,\mathrm{Pa\cdot s}$; keep only combinations with $\mathrm{Re}\in[20,1000]$ (not a full grid) | $u_{\mathrm{in}}=1\,\mathrm{m/s}$, $d=0.02\,\mathrm{m}$, $x_1=y_1=y_2=0.06\,\mathrm{m}$, $x_2=0.16\,\mathrm{m}$ |
| GEO | 20 | $d\in\{0.01,0.02,0.03,0.04,0.05\}\,\mathrm{m}$; $x_1,y_1,y_2\in\{0.02,0.04,0.06,0.08,0.1\}\,\mathrm{m}$; $x_2\in\{0.12,0.14,0.16,0.18,0.2\}\,\mathrm{m}$ (text also mixes $d$/radius naming for the cylinder scale) | $u_{\mathrm{in}}=1\,\mathrm{m/s}$, $\rho=10\,\mathrm{kg\,m^{-3}}$, $\mu=10^{-3}\,\mathrm{Pa\cdot s}$ |

> GEO and PROP are not full Cartesian products; resolve $d$ versus radius from `case.json` and the mask geometry.

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
hf download chen-yingfa/CFDBench \\
  cylinder/bc.zip cylinder/geo.zip cylinder/prop.zip \\
  --repo-type dataset \\
  --local-dir ./downloads/CFDBench

mkdir -p ./data/cylinder
unzip ./downloads/CFDBench/cylinder/bc.zip   -d ./data/cylinder
unzip ./downloads/CFDBench/cylinder/geo.zip  -d ./data/cylinder
unzip ./downloads/CFDBench/cylinder/prop.zip -d ./data/cylinder
```

## What is interesting and challenging

- The Kármán street is periodic and phase-sensitive, making it useful for frequency-domain methods and long rollouts.
- Separation and wake dynamics require both local high-gradient resolution and global coherent structure modeling.
- It contains the longest trajectories and most frames, so error accumulation is especially visible.
- PROP is an irregular Reynolds-filtered region rather than a Cartesian parameter grid.
- GEO requires the mask and scalar geometry metadata to work together.

## Known caveats

- **Time-interval conflict:** paper/autoregressive code use $0.001\,\mathrm s$, while the current non-autoregressive class still contains $0.1\,\mathrm s$. This may be downsampling or stale metadata and must be checked before training.
- **Loader code drift:** `cylinder.py` retains multiple loader versions. The current class calls `load_case_data_fix`, but other utilities may assume the older padded shape. Pin a commit and run shape tests.
- **Diameter/radius conflict:** trust actual `case.json` values and the reconstructed mask geometry.
- Raw Fluent exports can include pressure and velocity magnitude; interpolated targets are standardized as $u,v$.

## Source locations

- Paper: Sections 3.1 and 3.5, Tables 5 and 6, Section 3.6, Appendix E.1.
- Code: `src/dataset/cylinder.py` and the Cylinder Fluent Scheme.
