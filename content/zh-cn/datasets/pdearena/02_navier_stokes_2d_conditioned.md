---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 02_navier_stokes_2d_conditioned
spatial_dimension: 2
time_dependent: true
data_format: HDF5
paper: "arXiv:2209.15616v2"
download_key: NavierStokes-2D-conditoned
last_verified: 2026-07-21
title: 二维不可压 Navier–Stokes（参数条件化版）
linkTitle: "NS-2D conditioned"
weight: 20
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "与标准 NS 同方程与网格；扫描竖直浮力，并把浮力与预测时间窗作为条件。"
description: "与标准 NS 同方程与网格；扫描竖直浮力，并把浮力与预测时间窗作为条件。"
---

# 二维不可压 Navier–Stokes（参数条件化版）

与标准版相同的三通道烟雾浮力系统，但训练数据扫描竖直浮力 $b_y$，并把 $(b_y,\Delta t_{\mathrm{pred}})$ 作为连续条件，用于测试跨 PDE 参数与跨时间尺度泛化。官方仓库名拼写为 `NavierStokes-2D-conditoned`（少一个 `i`），下载须用该实际名称。

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEArena** |
| 数据集论文 | [Towards Multi-spatiotemporal-scale Generalized PDE Modeling](https://arxiv.org/abs/2209.15616) |
| 论文 PDF | [arXiv PDF](https://arxiv.org/pdf/2209.15616) |
| 官方代码库 | [pdearena/pdearena](https://github.com/pdearena/pdearena) |
| Hugging Face | [pdearena/NavierStokes-2D-conditoned](https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned) |
| 数据量 | 81.7 GB |
| 任务配置 | [configs/cond_navierstokes2d.yaml](https://github.com/pdearena/pdearena/blob/main/configs/cond_navierstokes2d.yaml) |
| 数值软件 | [PhiFlow](https://github.com/tum-pbs/PhiFlow) |
| 许可证 | MIT |
| 文档核对日期 | 2026-07-21 |

## 控制方程

\[
\frac{\partial s}{\partial t}+\mathbf{v}\cdot\nabla s=0,
\]
\[
\frac{\partial \mathbf{v}}{\partial t}+(\mathbf{v}\cdot\nabla)\mathbf{v}=-\nabla p+\nu\nabla^{2}\mathbf{v}+s\begin{pmatrix}0\\b_y\end{pmatrix},\qquad\nabla\cdot\mathbf{v}=0.
\]

发布中 $\nu=0.01$ 固定，$b_y$ 变化。条件可写为 $c=(b_y,\Delta t_{\mathrm{pred}})$；$\Delta t_{\mathrm{pred}}$ 是任务时间窗，不是新的 PDE 系数。

## 变量与坐标

与[标准版](../01_navier_stokes_2d_standard/)相同：$s,v_x,v_y$；网格 $128\times128$。额外条件通道/嵌入：$b_y$、$\Delta t_{\mathrm{pred}}$。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 2 |
| 含时间 | 是 |
| 网格 | $128\times128$ 均匀笛卡尔 |
| 空间分辨率 | $128\times128$ |
| 时间点数 | $T=56$（任务/生成配置） |
| 轨迹数 | train 6,656 / valid 1,664 / test 1,664（合计 9,984） |
| 通道 | 3：$s$、$v_x$、$v_y$（另加条件 $b_y,\Delta t$） |
| 数据量 | 81.7 GB |
| 格式 | HDF5 |

## 初始条件

初始速度为零；初始烟雾为随机平滑噪声（与标准版同族）。

## 边界条件

速度无滑移 Dirichlet；标量零法向导数 / boundary extrapolation。

## 数值生成方法

与标准版相同的 PhiFlow 烟雾推进；条件化批处理见 `navierstokes_cond_jobs.sh`（每 seed：train 128 / valid 32 / test 32）。

## 参数

| 参数 | 变化方式 | 取值 |
|---|---|---|
| 竖直浮力 $b_y$ | 不同文件 / 轨迹扫描 | 训练范围约 $[0.2,0.5]$（写在文件名中）；发布合计 9,984 条 |
| 预测时间窗 $\Delta t_{\mathrm{pred}}$ | 任务构造（帧间隔） | 按轨迹内 `dt` 与所选帧跨度；配置注释可见 `eval_dts` 如 $[1,2,4,8,16]$ 步 |
| 初始烟雾种子 | 每轨迹随机 | 同标准噪声族 |
| 黏度 $\nu$、$b_x$ | 固定 | $0.01$、$0$ |
| 网格 / 边界 / 初速 | 固定 | 同标准版 |

## 发布配置

- 任务配置 `cond_navierstokes2d.yaml`：`trajlen=56`；条件化生成 `sample_rate=1`。
- 完整发布：train 6,656 / valid 1,664 / test 1,664。
- 时间与条件以各 HDF5 的 `dt`、`buo_y` 及任务 dataloader 为准（不以论文 0.375 s 叙述覆盖发布数据）。

## 数据文件

命名示例：

`NavierStokes2D_{split}_{seed}_{buoyancy}.h5`  
`NavierStokes2D_train_{seed}_{buoyancy}_32.h5`

浮力写在文件名中。详见 [数据格式](../00_data_format/)。

## 数据布局与机器学习输入输出

字段键与标准版相同。典型条件化样本为单帧→单帧（具体 history/future 以所用训练配置为准）：

\[
X\in\mathbb{R}^{1\times3\times128\times128}\to Y\in\mathbb{R}^{1\times3\times128\times128},
\]

条件 $(b_y,\Delta t)$ 经嵌入注入网络（Addition / AdaGN / Spatial–Spectral 等为模型设计，非数据新通道）。

## 下载

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned
```

## 从官方代码重新生成

```bash
./pdedatagen/scripts/navierstokes_cond_jobs.sh
```

## 数据的兴趣点与挑战

连续浮力插值/外推；时间窗改变一步映射难度；将跨参数与跨时间尺度泛化放在同一受控系统中。

## 主要来源

- [PDEArena 论文](https://arxiv.org/abs/2209.15616)
- [条件化任务配置](https://github.com/pdearena/pdearena/blob/main/configs/cond_navierstokes2d.yaml)
- [数据生成说明](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Hugging Face 数据页](https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned)
