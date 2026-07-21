---
title: "一维 Kuramoto--Sivashinsky 方程"
dataset_family: PDEArena
dataset_release: Kuramoto-Sivashinsky-1D
equation: "Kuramoto--Sivashinsky equation"
spatial_dimension: 1
coordinate_system: "uniform periodic 1D grid"
task_variant: "fixed- and conditional-viscosity rollout"
official_status: "external Hugging Face release supported by the PDEArena loader"
license: MIT
last_verified: 2026-07-21
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
summary: '一维周期域上的时空混沌标量场数据，包含固定黏性 $\nu=1$ 和条件黏性 $\nu\in[0.5,1.5]$ 两个文件族，并由 PDEArena 数据管道支持。'
description: '一维周期域上的时空混沌标量场数据，包含固定黏性 $\nu=1$ 和条件黏性 $\nu\in[0.5,1.5]$ 两个文件族，并由 PDEArena 数据管道支持。'

---

# 一维 Kuramoto--Sivashinsky 方程

> **一句话说明：** 一维周期域上的时空混沌标量场数据，包含固定黏性 $\nu=1$ 和条件黏性 $\nu\in[0.5,1.5]$ 两个文件族，并由 PDEArena 数据管道支持。

[English version](../en/kuramoto_sivashinsky_1d.md)

## 较长说明

Kuramoto--Sivashinsky（KS）方程同时包含非线性平流、长波不稳定和四阶耗散，是研究混沌 rollout 与参数条件化的经典模型。当前 PDEArena 代码含有 KS loader 和训练配置，但当前 PDEArena Hugging Face 组织只列出四个官方仓库；可访问的 KS 数据实际托管在 `phlippe/Kuramoto-Sivashinsky-1D`。因此本页将其标为 **PDEArena 代码支持的外部数据**。

## 所属数据集与来源

- **代码生态：** PDEArena
- **当前可访问数据仓库：** `phlippe/Kuramoto-Sivashinsky-1D`
- **生成器来源：** [LPSDA](https://github.com/brandstetter-johannes/LPSDA)
- **PDEArena 任务配置：** [configs/kuramotosivashinsky1d.yaml](https://github.com/pdearena/pdearena/blob/main/configs/kuramotosivashinsky1d.yaml)
- **许可证：** MIT
- **状态说明：** 不计入 PDEArena 当前官方组织的四库总量。

## 方程

一种常用的参数化形式为

$$
\frac{\partial u}{\partial t}
+u\frac{\partial u}{\partial x}
+\frac{\partial^2u}{\partial x^2}
+\nu\frac{\partial^4u}{\partial x^4}=0,
$$

配周期边界

$$
u(x+L,t)=u(x,t).
$$

- $u(x,t)$：唯一的标量状态场；
- 二阶项产生长波不稳定；
- 四阶项提供高频耗散；
- 非线性项产生尺度耦合和时空混沌；
- $\nu$：条件版本中变化的系数。

## 数据说明

### PDEArena 任务配置

| 项目 | 规格 |
|---|---|
| 空间维数 | 1D |
| 字段 | 标量 $u$ |
| 通道数 | 1 |
| 轨迹长 | $T=140$ |
| 历史/未来 | 1 帧输入、1 帧输出 |
| padding | circular |
| 参数条件 | fixed: $[\Delta t,\Delta x]$；conditional: $[\Delta t,\Delta x,\nu]$ |

$$
X\in\mathbb R^{1\times1\times N_x},\qquad
Y\in\mathbb R^{1\times1\times N_x}.
$$

PDEArena 配置没有写死唯一 $N_x$；loader 可按用户指定的 `resolution` 对原网格做整数下采样。因此本页不凭文件体积猜测原始空间长度。

### HDF5 与读取方式

loader 读取：

- 一个以 `pde_` 开头的解数组；
- `dt`；
- `dx`；
- 条件黏性文件中的 `v`/黏度字段。

若解数组没有显式通道维，loader 添加单通道维。默认 `time_step=4` 时沿时间下采样；训练模式可随机选取不同起始相位。条件值还会为 Fourier embedding 做数值缩放，这只是模型预处理，不改变物理值。

### 两个文件族

| 文件族 | 黏性 | 变化因素 | 当前文件 |
|---|---|---|---|
| fixed viscosity | $\nu=1$ | 初值、文件中的 $\Delta t,\Delta x$ | train/valid/test 三个 HDF5 |
| conditional viscosity | $\nu\in[0.5,1.5]$ | 初值、$\Delta t,\Delta x,\nu$ | train/valid/test 三个 HDF5 |

当前数据卡明确给出固定黏性 $\nu=1$ 与条件黏性区间 $[0.5,1.5]$。

### 轨迹数与规模

- **仓库总大小：** 3.92 GB
- **文件数：** 6 个 HDF5（fixed/conditional × train/valid/test）
- 历史文件名 `KS_train_2048_large.h5` 和 `KS_train_4096_conditional.h5` 表明两个训练文件分别由 2,048 和 4,096 条轨迹构成；当前简短数据卡没有列出 valid/test 的精确轨迹数，因此本文不猜测。

## 参数：可调、实际变化与固定

| 参数/因素 | fixed 文件族 | conditional 文件族 |
|---|---|---|
| 初始条件 | 变化 | 变化 |
| $\Delta t$ | 作为元数据/条件读取 | 作为元数据/条件读取 |
| $\Delta x$ | 作为元数据/条件读取 | 作为元数据/条件读取 |
| $\nu$ | 固定 1 | **变化于 $[0.5,1.5]$** |
| 边界 | 周期，固定 | 周期，固定 |
| 方程形式 | 固定 | 固定 |
| 模型分辨率 | loader 可下采样 | loader 可下采样 |

## 下载

使用当前可访问的外部仓库：

```bash
git lfs install
git clone https://huggingface.co/datasets/phlippe/Kuramoto-Sivashinsky-1D
```

PDEArena 旧下载文档曾写 `pdearena/Kuramoto-Sivashinsky-1D`，但当前 PDEArena Hugging Face 组织没有列出该仓库；为了可复现，应使用上面的 `phlippe` 地址。

## 有趣与困难之处

- KS 是典型时空混沌系统，短期误差会快速放大；
- 单通道并不意味着简单，四阶导数要求正确处理高频结构；
- 周期平移对称性适合测试等变模型和数据增强；
- 条件黏性版本可测试连续参数插值和外推；
- 不同 $\Delta t,\Delta x$ 条件可用于研究跨离散化泛化。

## 已知限制

当前公开卡片非常简短，未给出所有 split 的轨迹数、唯一原始 $N_x$、生成精度和完整初值分布。此处对这些项目保持“未公开/取决于文件”，不以推测补全。

## 引用

KS 数据由 LPSDA 代码生成/沿用时，可同时引用相关工作：

```bibtex
@article{brandstetter2022lie,
  title={Lie Point Symmetry Data Augmentation for Neural PDE Solvers},
  author={Brandstetter, Johannes and Welling, Max and Worrall, Daniel E.},
  journal={arXiv preprint arXiv:2202.07643},
  year={2022}
}
```

## 资料链接

- [PDEArena KS 配置](https://github.com/pdearena/pdearena/blob/main/configs/kuramotosivashinsky1d.yaml)
- [PDEArena 下载文档](https://github.com/pdearena/pdearena/blob/main/docs/datadownload.md)
- [当前可访问的数据页](https://huggingface.co/datasets/phlippe/Kuramoto-Sivashinsky-1D)
- [LPSDA 代码](https://github.com/brandstetter-johannes/LPSDA)
