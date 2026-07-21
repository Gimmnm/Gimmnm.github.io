---
title: 二维球面浅水方程（速度形式）
dataset_family: PDEArena
dataset_release: ShallowWater-2D
equation: "Rotating shallow-water equations"
spatial_dimension: 2
coordinate_system: "global longitude-latitude / spherical spectral grid"
task_variant: "velocity-form 1-day and 2-day tasks"
official_status: "official PDEArena release and benchmark task view"
license: MIT
last_verified: 2026-07-21
linkTitle: "Shallow Water (velocity)"
weight: 30
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
summary: "在全球经纬度网格上模拟旋转浅水方程，保存一个压力/自由表面标量以及纬向和经向风速，并构造 1-day 与 2-day 两种时间预测任务。"
description: "在全球经纬度网格上模拟旋转浅水方程，保存一个压力/自由表面标量以及纬向和经向风速，并构造 1-day 与 2-day 两种时间预测任务。"

---

# 二维球面浅水方程（速度形式）

> **一句话说明：** 在全球经纬度网格上模拟旋转浅水方程，保存一个压力/自由表面标量以及纬向和经向风速，并构造 1-day 与 2-day 两种时间预测任务。

[English version](../en/shallow_water_2d_velocity.md)

## 较长说明

浅水方程描述垂直尺度远小于水平尺度、近似处于静水平衡的薄层流体。PDEArena 使用修改后的 SpeedyWeather.jl 在全球球面上生成轨迹。速度形式的单帧状态由一个压力/位势高度/自由表面相关标量和二维切向风场组成。

`ShallowWater2DVel-1Day` 与 `ShallowWater2DVel-2Day` 不是两套独立物理模拟：它们是同一批浅水轨迹采用不同时间抽样得到的 benchmark 视图。

## 所属数据集与来源

- **所属数据集：** PDEArena
- **官方发布名：** `pdearena/ShallowWater-2D`
- **任务视图：** `ShallowWater2DVel-1Day`、`ShallowWater2DVel-2Day`
- **原始工作：** *Towards Multi-spatiotemporal-scale Generalized PDE Modeling*
- **许可证：** MIT
- **数值软件：** [SpeedyWeather.jl](https://github.com/SpeedyWeather/SpeedyWeather.jl)

## 方程

原论文解释了浅水模型和字段，但没有在正文中打印一套完整的球面浅水方程。用于数据目录的一种等价标准向量形式为

$$
\frac{\partial h}{\partial t}+\nabla_s\cdot(h\mathbf v)=0,
$$

$$
\frac{\partial\mathbf v}{\partial t}
+(\mathbf v\cdot\nabla_s)\mathbf v
+f_c\,\hat{\mathbf r}\times\mathbf v
+g\nabla_s h=\mathcal D.
$$

其中 $\nabla_s$ 是球面微分算子，$f_c$ 是科氏参数，$\mathcal D$ 代表求解器中的耗散/数值闭合。

### 变量和坐标

- $h$ 或 $p$：自由表面位移、位势高度或论文所称 pressure field；
- $u$：zonal velocity，沿经线坐标方向的东西向/纬向风；
- $v$：meridional velocity，南北向/经向风；
- $(\lambda,\phi)$：经度和纬度。

## 生成代码与数值配置

- [浅水生成代码目录](https://github.com/pdearena/pdearena/tree/main/pdedatagen/shallowwater)
- [生成器配置](https://github.com/pdearena/pdearena/blob/main/pdedatagen/configs/shallowwater.yaml)
- [1-day 任务配置](https://github.com/pdearena/pdearena/blob/main/configs/shallowwater2d_1day.yaml)
- [2-day 任务配置](https://github.com/pdearena/pdearena/blob/main/configs/shallowwater2d_2day.yaml)

当前生成调用的核心设置包括：

```julia
run_speedy(Float32;
  n_days=20,
  model=:shallowwater,
  output=true,
  trunc=62,
  Δt_at_T85=40,
  initial_conditions=:random2)
```

## 数据说明

### 空间网格

| 项目 | 规格 |
|---|---|
| 物理空间 | 全球球面 |
| 经度点数 | 192 |
| 纬度点数 | 96 |
| 论文写法 | $192\times96$，$\Delta x=1.875^\circ$、$\Delta y=3.75^\circ$ |
| 常见数组尾维 | $[96,192]=[N_{\rm lat},N_{\rm lon}]$ |
| 网格/方法 | 规则经纬网格输出，球面谱方法求解 |

经度方向周期；极点由球面谱表示处理。论文把实验概括为 regular grid with periodic boundary conditions，不应把球面简单理解为平面矩形四条边完全相同地卷绕。

### 字段和通道

单帧状态为

$$
[p,u,v]\quad\text{或等价地}\quad[h,u,v],
$$

共 3 个通道：1 个标量场和 1 个二维向量场。

### 2-day 任务

| 项目 | 规格 |
|---|---|
| 轨迹长 | $T=11$ |
| 历史帧 | 2 |
| 未来帧 | 1 |
| 配置注释 | $n_t=88$、`sample_rate=8` |
| 论文预测窗口 | 48 h |

$$
X\in\mathbb R^{2\times3\times96\times192},\qquad
Y\in\mathbb R^{1\times3\times96\times192}.
$$

展平时间维后：

$$
[6,96,192]\longrightarrow[3,96,192].
$$

### 1-day 任务

| 项目 | 规格 |
|---|---|
| 轨迹长 | $T=21$ |
| 历史帧 | 2 |
| 未来帧 | 1 |
| 配置注释 | $n_t=84$、`sample_rate=4` |

$$
X\in\mathbb R^{2\times3\times96\times192},\qquad
Y\in\mathbb R^{1\times3\times96\times192}.
$$

空间和通道形状不变，区别在于时间抽样更细。

### 轨迹数与规模

| split | 轨迹数 |
|---|---:|
| train | 5,600 |
| validation | 1,400 |
| test | 1,400 |
| **总计**| **8,400** |

- **官方仓库总大小：** 124 GB
- 1-day、2-day、速度、涡度视图共享这批发布轨迹，不能重复相加。
- 论文中的 448/5,600 与 256/2,800 是实验训练子集设置。

### 初始条件

`random2` 初值随机化：

$$
\mathrm{offset}\sim\mathrm{Unif}\{80,\ldots,120\},
$$

$$
a_1\sim\mathrm{Unif}\{-20,\ldots,30\},\qquad
a_2,a_3\sim\mathrm{Unif}\{-20,\ldots,40\}.
$$

近似的初始 zonal wind 为

$$
u_0(\lambda,\phi)=a_1r(\lambda,\phi)\cos\phi-a_2\cos^2\phi+a_3\sin\phi\cos\phi+\mathrm{offset},
$$

其中 $r$ 为逐格独立均匀随机量。代码还加入固定结构的波扰动

$$
A=10^{-4},\quad m=6,\quad\theta_0=45^\circ,\quad\theta_w=10^\circ,
$$

以及幅度 $5\times10^{-6}$ 的随机谱微扰来打破对称性。

### 存储与预处理

生成流程使用 NetCDF；官方文档随后提供 NetCDF 到 Zarr 的转换和归一化统计计算。论文附录明确说明浅水输入使用前 2 个时间点，并对 pressure 与 vorticity 字段进行训练归一化。

## 参数：可调、实际变化与固定

| 参数/因素 | 发布数据中的处理 |
|---|---|
| 随机种子 | **逐轨迹变化** |
| `offset`, $a_1,a_2,a_3$ | **在固定离散范围内随机** |
| 逐格随机量 $r$ | **变化** |
| 谱微扰 realization | **变化**；幅度固定 |
| 波扰动 $A,m,\theta_0,\theta_w$ | 固定 |
| 模拟时长 | 固定 20 days |
| 谱截断 | 固定 `trunc=62` |
| 步长设置 | 固定 `Δt_at_T85=40` |
| 网格 | 固定 $192\times96$ |
| 1-day/2-day sample rate | **任务视图之间变化** |
| 重力、行星半径、科氏设置、耗散 | PDEArena 未报告扫描，按求解器版本固定/default 处理 |
| 球面拓扑/边界 | 固定 |

## 下载

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/ShallowWater-2D
```

仅克隆指针：

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/pdearena/ShallowWater-2D
```

## 有趣与困难之处

- 全球球面上的局部天气结构和大尺度环流同时存在；
- 经度周期、极区几何与球面微分使平面卷积假设不完全成立；
- 1-day 与 2-day 任务可以隔离时间尺度变化的影响；
- 初值具有强随机性，但物理常数和几何保持统一，适合比较多尺度网络结构。

## 已知限制

该数据没有系统扫描重力、旋转率、行星半径、流体深度、边界或网格分辨率。它主要是多初值、固定物理系统的数据集。


## 引用

PDEArena 的 Navier--Stokes 与浅水方程数据应引用：

```bibtex
@article{gupta2022towards,
  title={Towards Multi-spatiotemporal-scale Generalized PDE Modeling},
  author={Gupta, Jayesh K. and Brandstetter, Johannes},
  journal={arXiv preprint arXiv:2209.15616},
  year={2022}
}
```

## 资料链接

- [原论文](https://arxiv.org/abs/2209.15616)
- [官方代码库](https://github.com/pdearena/pdearena)
- [数据生成文档](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Hugging Face 数据页](https://huggingface.co/datasets/pdearena/ShallowWater-2D)
