---
title: "三维 Maxwell 时域电磁场"
dataset_family: PDEArena
dataset_release: Maxwell-3D
equation: "Maxwell equations"
spatial_dimension: 3
coordinate_system: "uniform Cartesian grid with periodic boundaries"
task_variant: "raw 8-frame electromagnetic trajectories"
official_status: "official PDEArena extension; associated with Clifford Neural Layers"
license: MIT
last_verified: 2026-07-21
linkTitle: Maxwell-3D
weight: 50
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
summary: "在三维周期均匀介质中，用 FDTD 推进由多个随机平面源激发的电场和磁场，并保存中心 $32^3$ 区域的 8 帧序列。"
description: "在三维周期均匀介质中，用 FDTD 推进由多个随机平面源激发的电场和磁场，并保存中心 $32^3$ 区域的 8 帧序列。"

---

# 三维 Maxwell 时域电磁场

> **一句话说明：** 在三维周期均匀介质中，用 FDTD 推进由多个随机平面源激发的电场和磁场，并保存中心 $32^3$ 区域的 8 帧序列。

[English version](../en/maxwell_3d.md)

## 较长说明

Maxwell-3D 是当前 PDEArena 官方发布，但不属于 2022 年 PDEArena 论文的 Navier--Stokes/浅水主实验。官方 README 将它与 *Clifford Neural Layers for PDE Modeling* 关联。生成器在 $64^3$ 周期网格上放置 18 个随机平面源，先 burn-in，再裁剪中心 $32^3$ 区域保存电磁场。

## 所属数据集与来源

- **所属数据集：** PDEArena
- **官方发布名：** `pdearena/Maxwell-3D`
- **关联论文：** *Clifford Neural Layers for PDE Modeling*
- **生成代码：** [pdedatagen/maxwell.py](https://github.com/pdearena/pdearena/blob/main/pdedatagen/maxwell.py)
- **数值软件：** [Python 3D FDTD Simulator](https://github.com/flaport/fdtd)
- **许可证：** MIT

## 方程

$$
\nabla\cdot\mathbf D=\rho,
\qquad
\nabla\cdot\mathbf B=0,
$$

$$
\frac{\partial\mathbf D}{\partial t}=\nabla\times\mathbf H-\mathbf J,
\qquad
\frac{\partial\mathbf B}{\partial t}=-\nabla\times\mathbf E,
$$

$$
\mathbf D=\epsilon\mathbf E,
\qquad
\mathbf B=\mu\mathbf H.
$$

在均匀无自由电荷/电流区域，这些方程描述电磁波传播；随机 PlaneSource 提供外部激励。

### 字段

按代码实际写入内容，单帧 6 通道为

$$
[E_x,E_y,E_z,H_x,H_y,H_z].
$$

生成器创建的 HDF5 键名是 `d_field` 与 `h_field`，但当前代码把 `grid.E` 写入 `d_field`、把 `grid.H` 写入 `h_field`。因此第一组应按代码语义理解为 $\mathbf E$，不能只凭键名认定为 $\mathbf D$。

## 数据说明

### 网格和时间

| 项目 | 规格 |
|---|---|
| 求解网格 | $64\times64\times64$ |
| 保存区域 | 中心 $32\times32\times32$ crop |
| 输出轨迹长 | $T=8$ |
| 单帧通道 | 6 |
| burn-in | 250 个 FDTD 步 |
| 保存间隔 | 每 25 个 FDTD 步保存一帧 |
| 边界条件 | $x,y,z$ 三方向周期 |
| 域长 | $L=3.2\times10^{-5}$ m |
| 求解网格间距 | $L/64=5\times10^{-7}$ m |

两个原始数组为

$$
\texttt{d\_field},\texttt{h\_field}
\in\mathbb R^{N\times8\times32\times32\times32\times3}.
$$

拼接后：

$$
U\in\mathbb R^{N\times8\times6\times32\times32\times32}.
$$

当前仓库没有像 NS/浅水那样给出唯一的 Maxwell `time_history`/`time_future` 标准任务配置。1→1、多帧→1 或序列到序列切片应在下游实验中明确说明，不能冒充唯一官方 I/O。

### 固定物理/数值参数

| 参数 | 值 |
|---|---:|
| 波长 `wavelength` | $10^{-5}$ m |
| 光速 `sol` | 299,792,458 m/s |
| 最大振幅 $A_{\max}$ | 1 |
| 相对介电常数/代码 permittivity | 10 |
| 相对磁导率/代码 permeability | 1 |
| 域长 $L$ | $3.2\times10^{-5}$ m |
| `n_large` | 64 |
| 输出 `n` | 32 |
| `nt` | 8 |
| `skip_nt` | 250 |
| `sample_rate` | 25 |

### 随机源

每条轨迹放置 18 个 PlaneSource：XY、XZ、YZ 三种平面各 6 个。每个源独立随机：

- 边长：2、3、4 或 5 个网格单元；
- 位置：在允许范围内均匀随机；
- 振幅：$\mathrm{Unif}[0,A_{\max})$；
- 相位：$\mathrm{Unif}[0,2\pi)$；
- 偏振：从所在平面的两个坐标轴中离散随机选择；
- 周期：

$$
T_{\rm source}=\frac{\lambda}{c}q,
\qquad q\sim\mathrm{Unif}[10^{-3},10^3].
$$

因此发布中实际变化的是 **源项/激励条件**，不是介电常数、磁导率、几何或边界。

### 轨迹数与规模

| split | 轨迹数 |
|---|---:|
| train | 6,400 |
| validation | 1,600 |
| test | 1,600 |
| **总计**| **9,600** |

- **官方仓库总大小：** 121 GB
- 6 个 float64 场的理论裸数组量与 121 GB 量级相符。

## 参数：可调、实际变化与固定

| 参数/因素 | 代码可调 | 发布实际做法 |
|---|---|---|
| 源位置/尺寸/方向 | 是 | **随机变化** |
| 源振幅/相位/周期 | 是 | **随机变化** |
| 源数 | 改代码可调 | 固定 18 |
| $\epsilon,\mu$ | 配置可调 | 固定 10、1 |
| 波长、光速、域长 | 配置可调 | 固定 |
| 边界条件 | 改代码可调 | 三向周期 |
| 网格/crop | 配置可调 | $64^3\to32^3$ 固定 |
| burn-in/保存间隔/帧数 | 配置可调 | 250/25/8 固定 |

## 下载

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/Maxwell-3D
```

仅克隆指针：

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/pdearena/Maxwell-3D
```

## 有趣与困难之处

- 三维数据量大，单帧就有 $6\times32^3$ 个场值；
- 电场和磁场是具有旋转/反射变换性质的向量场；
- 多源叠加产生干涉、传播和多尺度频率结构；
- 周期边界和中心 crop 使观察域不包含完整源--边界关系；
- HDF5 键名与实际写入变量不完全一致，需要谨慎处理语义。

## 已知限制

材料参数、边界和域几何固定；数据主要覆盖不同电磁源配置。当前发布也没有唯一标准化的 history/future 任务切片。

## 引用

```bibtex
@article{brandstetter2022clifford,
  title={Clifford Neural Layers for PDE Modeling},
  author={Brandstetter, Johannes and van den Berg, Rianne and Welling, Max and Gupta, Jayesh K.},
  journal={arXiv preprint arXiv:2209.04934},
  year={2022}
}
```

## 资料链接

- [PDEArena README 与引用说明](https://github.com/pdearena/pdearena)
- [Maxwell 生成代码](https://github.com/pdearena/pdearena/blob/main/pdedatagen/maxwell.py)
- [Maxwell 生成配置](https://github.com/pdearena/pdearena/blob/main/pdedatagen/configs/maxwell3d.yaml)
- [Hugging Face 数据页](https://huggingface.co/datasets/pdearena/Maxwell-3D)
