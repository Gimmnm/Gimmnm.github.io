---
title: "二维不可压 Navier--Stokes 烟雾浮力流（参数条件化版）"
dataset_family: PDEArena
dataset_release: NavierStokes-2D-conditoned
equation: "Incompressible Navier--Stokes + advected scalar"
spatial_dimension: 2
coordinate_system: "uniform Cartesian grid"
task_variant: "buoyancy- and time-conditioned rollout"
official_status: "official PDEArena release; repository name contains a typo"
license: MIT
last_verified: 2026-07-21
linkTitle: "NS-2D Conditioned"
weight: 20
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
summary: "与标准 NS 数据使用相同的三通道烟雾浮力系统，但训练数据扫描竖直浮力系数，并把浮力强度和预测时间跨度作为连续条件输入。"
description: "与标准 NS 数据使用相同的三通道烟雾浮力系统，但训练数据扫描竖直浮力系数，并把浮力强度和预测时间跨度作为连续条件输入。"

---

# 二维不可压 Navier--Stokes 烟雾浮力流（参数条件化版）

> **一句话说明：** 与标准 NS 数据使用相同的三通道烟雾浮力系统，但训练数据扫描竖直浮力系数，并把浮力强度和预测时间跨度作为连续条件输入。

[English version](../en/navier_stokes_2d_conditioned.md)

## 较长说明

该发布专门用于测试单个神经 PDE surrogate 是否能同时跨 **PDE 参数**与 **时间尺度** 泛化。物理参数是竖直浮力 $b_y$；预测时间窗口 $\Delta t_{\rm pred}$ 则是从输入帧到目标帧的时间跨度，属于任务/离散化条件，而不是方程新的物理系数。

官方 Hugging Face 仓库名拼写为 `NavierStokes-2D-conditoned`，其中 `conditioned` 少了一个 `i`。下载和脚本中必须沿用这个实际仓库名。

## 所属数据集与来源

- **所属数据集：** PDEArena
- **官方发布名：** `pdearena/NavierStokes-2D-conditoned`
- **原始工作：** *Towards Multi-spatiotemporal-scale Generalized PDE Modeling*
- **许可证：** MIT
- **与标准版关系：** 方程、空间网格、字段、边界条件和黏度相同；主要增加 $b_y$ 扫描和多时间跨度任务。

## 生成代码与数值软件

- [PDEArena 当前代码库](https://github.com/pdearena/pdearena)
- [条件化任务配置](https://github.com/pdearena/pdearena/blob/main/configs/cond_navierstokes2d.yaml)
- [Navier--Stokes 生成器](https://github.com/pdearena/pdearena/blob/main/pdedatagen/navier_stokes.py)
- 数值软件：[PhiFlow](https://github.com/tum-pbs/PhiFlow)

## 方程

$$
\frac{\partial s}{\partial t}+\mathbf v\cdot\nabla s=0,
$$

$$
\frac{\partial \mathbf v}{\partial t}
+(\mathbf v\cdot\nabla)\mathbf v
=-\nabla p+\nu\nabla^2\mathbf v
+s\begin{pmatrix}0\\b_y\end{pmatrix},
\qquad \nabla\cdot\mathbf v=0.
$$

发布中 $\nu=0.01$ 固定，$b_y$ 变化。

## 连续条件

模型条件可写为

$$
c=(b_y,\Delta t_{\rm pred}).
$$

- 论文训练范围：$0.2\le b_y\le0.5$；
- 训练构造均匀使用 832 个不同的浮力值；
- 评估对 208 个未见浮力值取平均；
- 论文描述的预测时间窗范围：$0.375\text{ s}\le\Delta t_{\rm pred}\le20\text{ s}$；
- 附录集中报告 $0.375,0.75,1.5,3,6$ s。

论文使用正弦嵌入，并比较 Addition、AdaGN 与 Spatial--Spectral 等条件注入方式。它们是模型设计，不是数据的新增物理通道。

## 数据说明

### 离散维度与通道

| 项目 | 规格 |
|---|---|
| 空间网格 | $128\times128$ |
| 坐标系 | 2D 笛卡尔坐标 |
| 单帧通道 | $s,v_x,v_y$ |
| 通道数 | 3 |
| 当前任务配置轨迹长 | $T=56$ |
| 模型历史/未来 | 论文附录使用前 1 帧预测目标帧 |
| 额外条件 | $b_y,\Delta t_{\rm pred}$ |

$$
X\in\mathbb R^{1\times3\times128\times128},\qquad
Y\in\mathbb R^{1\times3\times128\times128}.
$$

原始轨迹可统一写作

$$
U\in\mathbb R^{N\times56\times3\times128\times128}.
$$

### 字段、初值与边界

字段和 HDF5 键与标准版相同：`u`, `vx`, `vy`, `t`, `x`, `y`, `dt`, `dx`, `dy`, `buo_y`。初始速度固定为零，初始烟雾来自随机平滑噪声；速度使用闭域无滑移边界，标量使用零法向导数/边界外推。

### 轨迹数与规模

| split | 轨迹数 |
|---|---:|
| train | 6,656 |
| validation | 1,664 |
| test | 1,664 |
| **总计**| **9,984** |

- **官方仓库总大小：** 81.7 GB
- 论文图中的 1,664 与 6,656 是两种训练规模。

## 参数：可调、实际变化与固定

| 参数/因素 | 数据中是否变化 | 说明 |
|---|---|---|
| 竖直浮力 $b_y$ | **变化** | 核心 PDE 参数，训练范围 $[0.2,0.5]$ |
| 预测时间跨度 $\Delta t_{\rm pred}$ | **变化** | 通过目标帧间隔选择形成，不是新的 PDE 系数 |
| 初始烟雾随机种子 | **变化** | 提供初值多样性 |
| 黏度 $\nu$ | 固定 | 0.01 |
| $b_x$ | 固定 | 0 |
| 网格/域长 | 固定 | $128^2$、约 $32\times32$ |
| 初始速度 | 固定 | 零 |
| 边界条件 | 固定 | 速度无滑移，标量零法向导数 |
| 噪声族 | 固定分布 | scale=11、smoothness=6，随机 realization 变化 |

## 论文与当前主分支的时间口径差异

论文明确把条件化数据称为更高时间分辨率数据，基础间隔为 0.375 s。当前主分支中可见的生成器注释则为 $t_\min=18$、$t_\max=102$、$n_t=56$、`sample_rate=1`，对应 1.5 s。官方数据卡没有提供足以消除这一差异的元数据。因此：

- 复现论文实验时采用论文的 0.375 s 口径；
- 重新运行当前代码时应以实际 YAML 和生成文件内 `dt` 为准；
- 不应在数据库文档中把二者写成同一版本的无冲突事实。

## 下载

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned
```

仅克隆指针：

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned
```

## 有趣与困难之处

- 同一模型需要对连续浮力参数插值，并测试训练区间外外推；
- 时间跨度变化会改变一步映射的难度与误差尺度；
- 速度不可压约束和标量浮力耦合仍然存在；
- 数据将“跨参数泛化”和“跨时间尺度泛化”放在同一个受控系统中。

## 已知限制

该数据只扫描浮力，不扫描黏度、几何、边界条件或材料性质。因此它是单一 PDE 族内部的参数化 benchmark，而不是多方程或多边界条件数据集。


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
- [条件化任务配置](https://github.com/pdearena/pdearena/blob/main/configs/cond_navierstokes2d.yaml)
- [数据生成文档](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Hugging Face 数据页](https://huggingface.co/datasets/pdearena/NavierStokes-2D-conditoned)
