---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 01_navier_stokes_2d_standard
spatial_dimension: 2
time_dependent: true
data_format: HDF5
paper: "arXiv:2209.15616v2"
download_key: NavierStokes-2D
last_verified: 2026-07-21
title: 二维不可压 Navier–Stokes 烟雾浮力流（标准版）
linkTitle: "NS-2D standard"
weight: 10
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "封闭方域内不可压 NS + 烟雾标量；固定黏度与浮力，仅随机初值。"
description: "封闭方域内不可压 NS + 烟雾标量；固定黏度与浮力，仅随机初值。"
---

# 二维不可压 Navier–Stokes 烟雾浮力流（标准版）

在封闭二维方形域内，用不可压 Navier–Stokes 推进速度场，同时平流烟雾/粒子浓度标量；标量通过固定竖直浮力反馈到速度。发布数据不保存压力通道。标准版只改变随机初始烟雾，黏度、浮力、域、网格与边界均固定，主要测试多初值轨迹预测。

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEArena** |
| 数据集论文 | [Towards Multi-spatiotemporal-scale Generalized PDE Modeling](https://arxiv.org/abs/2209.15616) |
| 论文 PDF | [arXiv PDF](https://arxiv.org/pdf/2209.15616) |
| 官方代码库 | [pdearena/pdearena](https://github.com/pdearena/pdearena) |
| Hugging Face | [pdearena/NavierStokes-2D](https://huggingface.co/datasets/pdearena/NavierStokes-2D) |
| 数据量 | 43 GB |
| 生成入口 | [pdedatagen/navier_stokes.py](https://github.com/pdearena/pdearena/blob/main/pdedatagen/navier_stokes.py) |
| 数值软件 | [PhiFlow](https://github.com/tum-pbs/PhiFlow) |
| 许可证 | MIT |
| 文档核对日期 | 2026-07-21 |

## 控制方程

\[
\frac{\partial \mathbf{v}}{\partial t}+(\mathbf{v}\cdot\nabla)\mathbf{v}=-\nabla p+\nu\nabla^{2}\mathbf{v}+\mathbf{f},\qquad\nabla\cdot\mathbf{v}=0,
\]
\[
\frac{\partial s}{\partial t}+\mathbf{v}\cdot\nabla s=0,\qquad
\mathbf{f}=s\begin{pmatrix}b_x\\b_y\end{pmatrix},\qquad(b_x,b_y)=(0,0.5).
\]

（论文式 (5) 中黏度符号为 $\mu$，发布与代码中取 $\nu=0.01$。）

## 变量与坐标

**状态变量**
- $s$：烟雾/粒子浓度（标量）；
- $\mathbf{v}=(v_x,v_y)$：二维速度；
- $p$：压力（不可压投影乘子，不作为发布通道）。

**参数**
- $\nu$：运动黏度；$b_y$：竖直浮力系数。

**坐标与定义域**
- 空间：$128\times128$ 均匀笛卡尔网格；域长 $L_x=L_y=32$（$\Delta x=\Delta y=0.25$）；
- 时间：生成器 $t\in[18,102]$，$n_t=56$ 为基础步，标准发布 `sample_rate=4` → 保存 **14** 帧。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 2 |
| 含时间 | 是 |
| 网格 | 均匀笛卡尔 $128\times128$ |
| 空间域 | 封闭方域，$L_x=L_y=32$ |
| 时间范围 | 生成窗口 $[18,102]$；保存 14 帧（`sample_rate=4`） |
| 空间分辨率 | $128\times128$ |
| 时间点数 | 14 |
| 轨迹数 | train 5,200 / valid 1,300 / test 1,300（合计 7,800） |
| 通道 | 3：$s$、$v_x$、$v_y$ |
| 单样本形状（轨迹） | $14\times3\times128\times128$ |
| 数据量 | 43 GB |
| 格式 | HDF5 |

## 初始条件

- 标量：`abs(Noise(scale=11.0, smoothness=6.0))`，随机种子随轨迹变化；
- 速度：$\mathbf{v}_0=0$（staggered grid）。

## 边界条件

- 速度：封闭域无滑移 Dirichlet $\mathbf{v}=0$；
- 标量：Neumann $\partial_n s=0$（生成器为 boundary extrapolation）。

## 数值生成方法

PhiFlow；一步顺序为：semi-Lagrangian 平流标量 → 构造浮力 → 平流速度并加浮力 → 显式黏性扩散 → 不可压投影。

## 参数

| 参数 | 变化方式 | 取值 |
|---|---|---|
| 初始烟雾种子 | 每轨迹随机 | Noise scale=11，smoothness=6 |
| 黏度 $\nu$ | 固定 | 0.01 |
| 浮力 $(b_x,b_y)$ | 固定 | $(0,0.5)$ |
| 网格 / 域长 | 固定 | $128^2$，$L=32$ |
| 初始速度 | 固定 | $\mathbf{0}$ |
| 边界 | 固定 | 速度无滑移；标量零法向导数 |

## 发布配置

- 任务配置 `navierstokes2d.yaml`：`time_history=4`，`time_future=1`，`trajlen=14`。
- 完整发布：train 5,200 / valid 1,300 / test 1,300。
- 实际间隔以各 HDF5 内 `dt` 为准（生成脚本基础步约 1.5 s，再按 `sample_rate=4` 抽帧）。

## 数据文件

Hugging Face 扁平目录；命名

`NavierStokes2D_{train|valid|test}_{seed}_0.50000.h5`

由官方 `navierstokes_jobs.sh` 对 52 个 seed 各生成 train 100 / valid 25 / test 25 条轨迹。详见 [数据格式](../00_data_format/)。

## 数据布局与机器学习输入输出

HDF5 键：`u`（$s$）、`vx`、`vy`，以及 `t`,`x`,`y`,`dt`,`dx`,`dy`,`buo_y`。

典型模型样本：

\[
X\in\mathbb{R}^{4\times3\times128\times128}\to Y\in\mathbb{R}^{1\times3\times128\times128}
\]

（时间并入通道时为 $[12,128,128]\to[3,128,128]$）。

## 下载

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D
# 仅指针：GIT_LFS_SKIP_SMUDGE=1 git clone ...
```

## 从官方代码重新生成

```bash
./pdedatagen/scripts/navierstokes_jobs.sh
# 或按 docs/data.md 对多 seed 调用
# python scripts/generate_data.py base=pdedatagen/configs/navierstokes2dsmoke.yaml \
#   experiment=smoke mode=train samples=100 seed=$SEED \
#   pdeconfig.init_args.sample_rate=4 dirname=pdearena_data/navierstokes/
```

## 数据的兴趣点与挑战

标量—速度双向耦合；不可压约束带来全局速度耦合；固定物理参数下的多初值设定适合测长期 rollout 与数据效率。

## 主要来源

- [PDEArena 论文](https://arxiv.org/abs/2209.15616)
- [官方代码库](https://github.com/pdearena/pdearena)
- [数据生成说明](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Hugging Face 数据页](https://huggingface.co/datasets/pdearena/NavierStokes-2D)
