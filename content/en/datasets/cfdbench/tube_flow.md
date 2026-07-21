---
title: "CFDBench — Water-air tube flow"
dataset: CFDBench
problem_id: tube_flow
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
linkTitle: "Tube Flow"
weight: 20
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: CFDBench
summary: "Water enters a two-dimensional axial section of a tube initially filled with air, forming a near-wall viscous boundary layer and a moving phase interface; inlet velocity, workin…"
description: "Water enters a two-dimensional axial section of a tube initially filled with air, forming a near-wall viscous boundary layer and a moving phase interface; inlet velocity, workin…"

---

# CFDBench — Water--air tube flow

**One-line description:** Water enters a two-dimensional axial section of a tube initially filled with air, forming a near-wall viscous boundary layer and a moving phase interface; inlet velocity, working-fluid properties, and tube geometry are varied separately.

**Longer description:** This problem tests whether a model can represent inlet development, wall-induced velocity profiles, a pressure outlet, and a water--air interface at the same time. The paper calls it circular-tube flow, while the data supplied to two-dimensional models are fields on an axial section. Fluent uses a VOF multiphase model, but the official interpolated archives standardize only $u,v$ and do not expose volume fraction as a common learning channel.

- Parent dataset: **CFDBench**
- Dataset authors: Yining Luo, Yingfa Chen, and Zhen Zhang
- Generator: ANSYS Fluent 2021R1 with a VOF multiphase model
- Official loader: [`src/dataset/tube.py`](https://github.com/luo-yining/CFDBench/blob/main/src/dataset/tube.py)


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


### Multiphase auxiliary variable

The Fluent setup uses a water volume fraction $\alpha$. With no interphase mass transfer, the standard VOF transport relation is commonly written as

$$
\frac{\partial\alpha}{\partial t}+\nabla\cdot(\alpha\mathbf u)=0.
$$

This is a standard interpretation of the documented VOF setup, not an additional target equation explicitly written in the paper. The interpolated archives do not consistently publish $\alpha$.

## Physical domain, coordinates, and boundary conditions

The $x$ direction follows the tube axis from left to right, and $y$ spans the tube diameter. An idealized domain is

$$
D=[0,l]\times[0,d].
$$

Boundary conditions are

$$
\mathbf u(0,y,t)=(u_\mathrm{{in}},0),
$$

$$
\mathbf u(x,0,t)=\mathbf u(x,d,t)=\mathbf 0,
$$

$$
p(l,y,t)=p_\mathrm{{out}}.
$$

The generation Scheme initializes mixture pressure and velocity at rest, fills the domain with the air phase, and injects water from the left inlet.

## About the data

| Item | Value or description |
|---|---|
| Spatial dimension | 2D axial section |
| Phases | Water--air, VOF |
| Interpolated arrays | `u.npy`, `v.npy`: $(T_i,64,64)$ |
| Current loader features | After adding a left inlet column and top/bottom wall rows, approximately $(T_i,3,66,65)$ with $(u,v,\mathrm{{mask}})$ |
| Appendix example | Explicitly mentions top/bottom padding to $66\times64$ only; this differs from the current extra left column |
| Physical targets | $u,v$; raw exports may also include water volume fraction and pressure |
| Cases/trajectories | 175 = 50 BC + 100 PROP + 25 GEO |
| Total frames | 39,553 |
| Mean frames per case | 226.02; not a fixed length |
| Time interval | Paper: $0.01\,\mathrm s$; current loader contains `data_delta_time=0.1` |
| Common $t_\max$ | Not reported; derive it from each trajectory and resolved time metadata |
| Raw size per frame in paper | Approximately 4.8 MB |
| Generation time in paper | Approximately 1.08 s/frame |
| Current archive | `tube.zip`, approximately 213 MB (2026-07-21) |

## Baseline configuration

$$
\rho=100\,\mathrm{{kg\,m^{{-3}}}},\qquad
\mu=0.1\,\mathrm{{Pa\,s}},
$$

$$
u_\mathrm{{in}}=1\,\mathrm{{m/s}},\qquad
d=0.1\,\mathrm m,\qquad l=1\,\mathrm m.
$$

Code parameter order:

```text
[vel_in, density, viscosity, height, width]
```

`height/width` refer to the physical dimensions of the interpolated domain. Their correspondence to paper notation $d,l$ should be checked in each `case.json`.

## Parameter sweep: varied versus fixed

| Subset | Cases | Parameters actually varied | Conditions held fixed |
|---|---:|---|---|
| BC | 50 | $u_\mathrm{{in}}=0.1,0.2,\ldots,5.0\,\mathrm{{m/s}}$ | $\rho=100$, $\mu=0.1$, $d=0.1$, $l=1$; phase model, initial air fill, and boundary types fixed |
| PROP | 100 | $\rho=\{{10,120,230,340,450,560,670,780,890,1000\}}\,\mathrm{{kg/m^3}}$; $\mu=\{{0.01,0.12,0.23,0.34,0.45,0.56,0.67,0.78,0.89,1.00\}}\,\mathrm{{Pa\,s}}$; all $10\times10$ combinations | $u_\mathrm{{in}}=1$, $d=0.1$, $l=1$; boundaries and initial phase distribution fixed |
| GEO | 25 | The text says five diameters are selected from $\{{0.01,0.05,0.1,0.3,0.5\}}\,\mathrm m$ and five diameter/length relations are chosen for each, with $0.1\le l\le10$ | $u_\mathrm{{in}}=1$, $\rho=100$, $\mu=0.1$; inlet, outlet, walls, and phase model fixed |

> **Ambiguity in Tube GEO.** The main text states that 25 geometries are generated. Table 3 lists five size values and ten $d/l$ candidates; a full product would yield 50. The paper does not provide the final list of 25 $(d,l)$ pairs. Do not invent the product; use the downloaded `case.json` files.

**Adjustable but not swept:** outlet pressure, air-phase properties, contact angle/surface tension, initial interface, and gravity are adjustable in a more general two-phase formulation, but the public CFDBench sweep focuses on inlet velocity, one working-fluid $\rho/\mu$ pair, and a finite geometry set.


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
hf download chen-yingfa/CFDBench tube.zip \\
  --repo-type dataset \\
  --local-dir ./downloads/CFDBench
unzip ./downloads/CFDBench/tube.zip -d ./data
```

## What is interesting and challenging

- The model must capture both the phase interface and steep near-wall velocity gradients.
- A pressure outlet, velocity inlet, and no-slip walls are non-periodic boundaries, unlike many regular PDE benchmarks.
- Geometry changes alter both physical grid spacing and development length.
- Publishing only $u,v$ removes a direct phase-interface label; the interface must be inferred indirectly or reconstructed from raw VOF exports.

## Known caveats

- **Time-interval conflict:** the paper states $0.01\,\mathrm s$, while current `tube.py` contains $0.1\,\mathrm s$ metadata. Check case metadata, generation Scheme, and actual timestamps before training.
- **Padding conflict:** Appendix E.1 gives a $66\times64$ example, while the current loader may add a left inlet column and return $66\times65$. Always print the actual tensor shape.
- **Incomplete GEO enumeration:** the 25 geometries can only be recovered reliably from case metadata.
- Pressure and water VOF are not standardized channels in the interpolated archives.

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

- Paper: Sections 3.1 and 3.3, Tables 3 and 6, Section 3.6, Appendix E.1.
- Code: `src/dataset/tube.py` and the Tube Fluent Scheme.
