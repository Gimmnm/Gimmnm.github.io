---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 06_kuramoto_sivashinsky_1d
spatial_dimension: 1
time_dependent: true
data_format: HDF5
paper: "LPSDA / external; loader-supported in PDEArena"
download_key: Kuramoto-Sivashinsky-1D
last_verified: 2026-07-21
title: 一维 Kuramoto–Sivashinsky 方程
linkTitle: KS-1D
weight: 60
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "一维周期 KS 混沌标量；固定黏性与条件黏性两族；PDEArena loader 支持的外部数据。"
description: "一维周期 KS 混沌标量；固定黏性与条件黏性两族；PDEArena loader 支持的外部数据。"
---

# 一维 Kuramoto–Sivashinsky 方程

一维周期域上的时空混沌标量方程。PDEArena 含 KS loader 与训练配置，但当前组织四库不含 KS；可访问数据在 `phlippe/Kuramoto-Sivashinsky-1D`。标为 **代码支持的外部数据**，不计入官方四库总量。

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 代码生态 | **PDEArena** |
| 当前数据仓库 | [phlippe/Kuramoto-Sivashinsky-1D](https://huggingface.co/datasets/phlippe/Kuramoto-Sivashinsky-1D) |
| 生成器来源 | [LPSDA](https://github.com/brandstetter-johannes/LPSDA) |
| 任务配置 | [configs/kuramotosivashinsky1d.yaml](https://github.com/pdearena/pdearena/blob/main/configs/kuramotosivashinsky1d.yaml) |
| 数据量 | 3.92 GB |
| 许可证 | MIT |
| 文档核对日期 | 2026-07-21 |

## 控制方程

\[
\frac{\partial u}{\partial t}+u\frac{\partial u}{\partial x}+\frac{\partial^{2}u}{\partial x^{2}}+\nu\frac{\partial^{4}u}{\partial x^{4}}=0,\qquad u(x+L,t)=u(x,t).
\]

二阶项长波不稳定，四阶项高频耗散，非线性项尺度耦合；$\nu$ 在条件版本中变化。

## 变量与坐标

- $u(x,t)$：唯一标量状态；
- 周期一维均匀网格；loader 可按 `resolution` 整数下采样，本页不臆测唯一原始 $N_x$。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 1 |
| 含时间 | 是 |
| 网格 | 均匀周期 1D |
| 轨迹长（任务配置） | $T=140$ |
| 通道 | 1：$u$ |
| 文件族 | fixed $\nu=1$；conditional $\nu\in[0.5,1.5]$ |
| 数据量 | 3.92 GB |
| 格式 | HDF5（6 个文件） |

历史文件名表明 train fixed / conditional 分别约 2,048 / 4,096 条轨迹；valid/test 精确条数数据卡未列全，此处不猜测。

## 初始条件

公开卡片未给出完整初值分布；以文件内轨迹为准。

## 边界条件

周期边界。

## 数值生成方法

LPSDA 生成；PDEArena loader 读取以 `pde_` 开头的解数组及 `dt`、`dx`（条件文件另有黏度字段）。默认 `time_step=4` 可沿时间下采样。

## 参数

| 参数 | 变化方式 | 取值 |
|---|---|---|
| 初始条件 | 每轨迹变化 | 见文件 |
| $\nu$ | fixed 固定；conditional 扫描 | $1$；$[0.5,1.5]$ |
| $\Delta t,\Delta x$ | 作为元数据/条件读取 | 见文件 |
| 边界 / 方程形式 | 固定 | 周期；上式 |

## 发布配置

PDEArena 任务配置：1 帧输入 → 1 帧输出；fixed 条件 $[\Delta t,\Delta x]$，conditional 另加 $\nu$。旧下载文档曾写 `pdearena/Kuramoto-Sivashinsky-1D`，当前组织未列出该库，应以 `phlippe` 地址为准。

## 数据文件

| 文件 | 说明 |
|---|---|
| `KS_train_fixed_viscosity.h5` | 固定黏性训练 |
| `KS_valid_fixed_viscosity.h5` | 固定黏性验证 |
| `KS_test_fixed_viscosity.h5` | 固定黏性测试 |
| `KS_train_conditional_viscosity.h5` | 条件黏性训练 |
| `KS_valid_conditional_viscosity.h5` | 条件黏性验证 |
| `KS_test_conditional_viscosity.h5` | 条件黏性测试 |

详见 [数据格式](../00_data_format/)。

## 数据布局与机器学习输入输出

\[
X\in\mathbb{R}^{1\times1\times N_x}\to Y\in\mathbb{R}^{1\times1\times N_x}.
\]

## 下载

```bash
git lfs install
git clone https://huggingface.co/datasets/phlippe/Kuramoto-Sivashinsky-1D
```

## 从官方代码重新生成

按 [LPSDA](https://github.com/brandstetter-johannes/LPSDA) 流程生成后，用 PDEArena KS loader 读取。

## 数据的兴趣点与挑战

时空混沌使短期误差放大；四阶导数要求正确处理高频；条件黏性可测连续参数插值/外推。

## 主要来源

- [PDEArena KS 配置](https://github.com/pdearena/pdearena/blob/main/configs/kuramotosivashinsky1d.yaml)
- [当前可访问数据页](https://huggingface.co/datasets/phlippe/Kuramoto-Sivashinsky-1D)
- [LPSDA 代码](https://github.com/brandstetter-johannes/LPSDA)
