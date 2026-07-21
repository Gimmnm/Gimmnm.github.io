---
title: "二维不可压 Navier--Stokes 烟雾浮力流（标准版）"
dataset_family: PDEArena
dataset_release: NavierStokes-2D
equation: "Incompressible Navier--Stokes + advected scalar"
spatial_dimension: 2
coordinate_system: "uniform Cartesian grid"
task_variant: "standard rollout"
official_status: "official PDEArena release"
license: MIT
last_verified: 2026-07-21
linkTitle: "NS-2D Standard"
weight: 10
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
summary: "在封闭二维方形域内，用不可压 Navier--Stokes 方程推进速度场，同时平流一个烟雾/粒子浓度标量，并让该标量通过固定的竖直浮力反馈到速度场。"
description: "在封闭二维方形域内，用不可压 Navier--Stokes 方程推进速度场，同时平流一个烟雾/粒子浓度标量，并让该标量通过固定的竖直浮力反馈到速度场。"

---

# 二维不可压 Navier--Stokes 烟雾浮力流（标准版）

> **一句话说明：** 在封闭二维方形域内，用不可压 Navier--Stokes 方程推进速度场，同时平流一个烟雾/粒子浓度标量，并让该标量通过固定的竖直浮力反馈到速度场。

[English version](../en/navier_stokes_2d_standard.md)

## 较长说明

该数据用于学习规则网格上的非稳态流体演化。每条轨迹包含一个标量浓度场 $s(x,y,t)$ 和二维速度场 $\mathbf v=(v_x,v_y)$。标量由速度平流；标量又通过竖直浮力项驱动速度。发布数据不把压力作为监督通道保存，压力只在不可压投影中作为约束变量出现。

标准版只改变随机初始烟雾形态和随机种子，黏度、浮力强度、计算域、网格与边界条件均固定，因此它主要测试对不同初值的轨迹预测，而不是跨物理参数泛化。

## 所属数据集与来源

- **所属数据集：** PDEArena
- **官方发布名：** `pdearena/NavierStokes-2D`
- **原始工作：** *Towards Multi-spatiotemporal-scale Generalized PDE Modeling*
- **作者/维护者：** Jayesh K. Gupta、Johannes Brandstetter；当前代码由 PDEArena 仓库维护
- **领域专家：** 原论文没有单独列出一个 “domain expert” 字段，本文不额外推断
- **许可证：** 当前代码库和 Hugging Face 数据页标注为 MIT

## 生成代码与数值软件

- [PDEArena 当前代码库](https://github.com/pdearena/pdearena)
- [数据生成说明](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [Navier--Stokes 生成器](https://github.com/pdearena/pdearena/blob/main/pdedatagen/navier_stokes.py)
- [生成器配置](https://github.com/pdearena/pdearena/blob/main/pdedatagen/configs/navierstokes2dsmoke.yaml)
- 数值软件：[PhiFlow](https://github.com/tum-pbs/PhiFlow)

代码中的一步推进顺序为：

1. 用 semi-Lagrangian 方法平流标量；
2. 构造 $s(0,b_y)^\mathsf T$ 浮力；
3. semi-Lagrangian 平流速度并加入浮力；
4. 显式黏性扩散；
5. 进行不可压投影。

## 方程

速度形式的不可压 Navier--Stokes 方程为

$$
\frac{\partial \mathbf v}{\partial t}
+ (\mathbf v\cdot\nabla)\mathbf v
= -\nabla p + \nu\nabla^2\mathbf v + \mathbf f,
\qquad \nabla\cdot\mathbf v=0.
$$

PDEArena 的烟雾数据还包含平流标量

$$
\frac{\partial s}{\partial t}+\mathbf v\cdot\nabla s=0,
$$

并令

$$
\mathbf f=s\begin{pmatrix}b_x\\b_y\end{pmatrix},
\qquad (b_x,b_y)=(0,0.5)
$$

用于标准发布。

### 变量

- $s$：烟雾或粒子浓度，标量场；
- $\mathbf v=(v_x,v_y)$：二维速度场；
- $p$：压力/不可压投影的拉格朗日乘子，不作为发布数据通道；
- $\nu$：运动黏度；
- $(b_x,b_y)$：单位浓度对应的浮力系数。

## 数据说明

### 离散维度

| 项目 | 规格 |
|---|---|
| 空间维数 | 2D |
| 网格 | $128\times128$ 均匀笛卡尔网格 |
| 论文网格间距 | $\Delta x=\Delta y=0.25$ |
| 代码域长 | $L_x=L_y=32$ |
| 单帧字段 | $s,v_x,v_y$ |
| 单帧通道数 | 3 |
| 论文轨迹长度 | 14 个保存时间点 |
| 基准模型历史/未来 | 4 帧输入、1 帧输出 |

原始物理场可统一写成

$$
U\in\mathbb R^{N\times14\times3\times128\times128}.
$$

模型样本为

$$
X\in\mathbb R^{4\times3\times128\times128},\qquad
Y\in\mathbb R^{1\times3\times128\times128}.
$$

将时间维并入通道后为

$$
[12,128,128]\longrightarrow[3,128,128].
$$

### 字段和 HDF5 键

| HDF5 键 | 含义 | 典型形状 |
|---|---|---|
| `u` | 标量浓度 $s$ | $[N,T,128,128]$ |
| `vx` | $x$ 方向速度 | $[N,T,128,128]$ |
| `vy` | $y$ 方向速度 | $[N,T,128,128]$ |
| `t` | 时间坐标 | $[N,T]$ |
| `x`, `y` | 空间坐标 | $[N,128]$ |
| `dt`, `dx`, `dy` | 时间/空间间距元数据 | $[N]$ |
| `buo_y` | 竖直浮力系数 | $[N]$ |

### 轨迹数与规模

| split | 轨迹数 |
|---|---:|
| train | 5,200 |
| validation | 1,300 |
| test | 1,300 |
| **总计**| **7,800** |

- **官方仓库总大小：** 43 GB
- 论文中的 2,080 条训练轨迹是数据效率实验子集，不是完整训练集。

### 初始条件

- 标量：`abs(Noise(scale=11.0, smoothness=6.0))`；随机种子随轨迹变化；
- 速度：$\mathbf v_0=0$，在 staggered grid 上表示。

### 边界条件

- 速度：封闭域、无滑移 Dirichlet 条件 $\mathbf v=0$；
- 标量：论文给出零法向导数 Neumann 条件；生成器使用 boundary extrapolation。

### 时间分辨率与版本差异

原论文附录把该任务描述为模拟 21 s、每 1.5 s 采样、共 14 个时间点。当前主分支生成器配置则常写 $t_\min=18$、$t_\max=102$、$n_t=56$，基础步长为 1.5 s；标准批处理脚本再设 `sample_rate=4`，得到 14 帧和 6 s 的保存间隔。两者不能无说明地合并：复现实验时应明确采用论文版本还是当前生成脚本版本。

## 参数：可调、实际变化与固定

| 参数 | 代码层面 | 官方标准数据中的做法 |
|---|---|---|
| $t_\min,t_\max,n_t$ | 可调 | 固定 |
| `sample_rate`, `skip_nt` | 可调 | 固定；当前标准脚本使用 `sample_rate=4` |
| $L_x,L_y,n_x,n_y$ | 可调 | 固定为 $32,32,128,128$ |
| 黏度 $\nu$ | 可调 | 固定为 0.01 |
| 浮力 $b_x,b_y$ | 可调 | 固定为 0 和 0.5 |
| 初始标量随机种子 | 可调 | **逐轨迹变化** |
| 噪声尺度/平滑度 | 改代码可调 | 固定为 11/6 |
| 初始速度 | 改代码可调 | 固定为零 |
| 边界条件/几何 | 理论上可改 | 发布中固定 |
| `correction_strength`, `force_strength`, `force_frequency` | dataclass 暴露 | 当前 smoke 推进路径没有实际使用，不能视为被扫描参数 |

## 下载

```bash
# 安装并初始化 Git LFS
git lfs install

# 下载完整数据仓库
git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D
```

只克隆指针而不立即拉取大文件：

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/pdearena/NavierStokes-2D
```

## 有趣与困难之处

- 标量和速度双向耦合，标量既是被输运量又是驱动力；
- 不可压约束使速度分量之间存在全局耦合；
- 涡旋平移、卷吸和细丝化要求模型同时处理局部小尺度与全局流动；
- 固定物理参数但多初值的设置适合研究长期 rollout 稳定性和数据效率。

## 已知限制

该发布不覆盖变化的黏度、几何、边界条件、分辨率或多种初始速度分布；因此不能把在该数据上的成功直接解释为对任意 Navier--Stokes 系统的泛化。


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
- [下载文档](https://github.com/pdearena/pdearena/blob/main/docs/datadownload.md)
- [Hugging Face 数据页](https://huggingface.co/datasets/pdearena/NavierStokes-2D)
