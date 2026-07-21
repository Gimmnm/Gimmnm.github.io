---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 05_maxwell_3d
spatial_dimension: 3
time_dependent: true
data_format: HDF5
paper: "Clifford Neural Layers (associated); not in PDEArena 2022 main experiments"
download_key: Maxwell-3D
last_verified: 2026-07-21
title: 三维 Maxwell 时域电磁场
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
dataset_family: PDEArena
summary: "三维周期均匀介质中 FDTD 电磁轨迹；中心 $32^3$ 区域 8 帧；扫描随机平面源。"
description: "三维周期均匀介质中 FDTD 电磁轨迹；中心 $32^3$ 区域 8 帧；扫描随机平面源。"
---

# 三维 Maxwell 时域电磁场

官方 PDEArena 扩展发布（关联 *Clifford Neural Layers for PDE Modeling*），不属于 2022 PDEArena 论文的 NS/浅水主实验。在 $64^3$ 周期网格上放置 18 个随机平面源，burn-in 后裁剪中心 $32^3$ 保存 8 帧电磁场。

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEArena**（扩展） |
| 关联论文 | [Clifford Neural Layers for PDE Modeling](https://arxiv.org/abs/2209.04934) |
| 官方代码库 | [pdearena/pdearena](https://github.com/pdearena/pdearena) |
| Hugging Face | [pdearena/Maxwell-3D](https://huggingface.co/datasets/pdearena/Maxwell-3D) |
| 数据量 | 121 GB |
| 生成入口 | [pdedatagen/maxwell.py](https://github.com/pdearena/pdearena/blob/main/pdedatagen/maxwell.py) |
| 数值软件 | [Python 3D FDTD Simulator](https://github.com/flaport/fdtd) |
| 许可证 | MIT |
| 文档核对日期 | 2026-07-21 |

## 控制方程

\[
\nabla\cdot\mathbf{D}=\rho,\qquad\nabla\cdot\mathbf{B}=0,
\]
\[
\frac{\partial\mathbf{D}}{\partial t}=\nabla\times\mathbf{H}-\mathbf{J},\qquad
\frac{\partial\mathbf{B}}{\partial t}=-\nabla\times\mathbf{E},
\]
\[
\mathbf{D}=\epsilon\mathbf{E},\qquad\mathbf{B}=\mu\mathbf{H}.
\]

随机 PlaneSource 提供外部激励。

## 变量与坐标

- 单帧 6 通道：$[E_x,E_y,E_z,H_x,H_y,H_z]$；
- HDF5 键名为 `d_field`、`h_field`，但当前代码把 `grid.E` / `grid.H` 写入二者，第一组应按 $\mathbf{E}$ 理解；
- 求解网格 $64^3$，保存中心 $32^3$；域长 $L=3.2\times10^{-5}$ m。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 3 |
| 含时间 | 是 |
| 网格 | 均匀笛卡尔，周期边界 |
| 保存区域 | 中心 $32\times32\times32$ |
| 时间点数 | 8（burn-in 250 步，每 25 步存一帧） |
| 轨迹数 | train 6,400 / valid 1,600 / test 1,600（合计 9,600） |
| 通道 | 6：$\mathbf{E}$、$\mathbf{H}$ 各 3 |
| 数据量 | 121 GB |
| 格式 | HDF5 |

## 初始条件

由 18 个 PlaneSource（XY/XZ/YZ 各 6）激发：边长 $\in\{2,3,4,5\}$ 格、位置/振幅/相位/偏振/周期随机。

## 边界条件

$x,y,z$ 三向周期。

## 数值生成方法

FDTD；配置见 `pdedatagen/configs/maxwell3d.yaml`。生成脚本对 64 个 seed 各写 train 100 / valid 25 / test 25。

## 参数

| 参数 | 变化方式 | 取值 |
|---|---|---|
| 源位置/尺寸/方向/振幅/相位/周期 | 每轨迹随机 | 见生成器；周期 $T=\lambda q/c$，$q\sim\mathrm{Unif}[10^{-3},10^3]$ |
| 源数 | 固定 | 18 |
| $\epsilon_r,\mu_r$ | 固定 | 10、1 |
| 波长 / 光速 / 域长 | 固定 | $10^{-5}$ m；$c$；$L=3.2\times10^{-5}$ m |
| 网格 / crop / 帧数 | 固定 | $64^3\to32^3$；$T=8$ |

## 发布配置

当前仓库未给出唯一的 Maxwell `time_history`/`time_future` 标准任务配置；1→1 或多帧切片应在下游实验中明确，勿冒充唯一官方 I/O。

## 数据文件

命名：`Maxwell3D_{train|valid|test}_{seed}.h5`  
原始数组：`d_field`,`h_field` $\in\mathbb{R}^{N\times8\times32\times32\times32\times3}$。详见 [数据格式](../00_data_format/)。

## 数据布局与机器学习输入输出

拼接后 $U\in\mathbb{R}^{N\times8\times6\times32\times32\times32}$。历史/未来帧数由实验自定。

## 下载

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/Maxwell-3D
```

## 从官方代码重新生成

```bash
python scripts/generate_data.py base=pdedatagen/configs/maxwell3d.yaml \
  experiment=maxwell mode=train samples=100 seed=$SEED \
  dirname=pdearena_data/maxwell3d/
python scripts/compute_normalization.py --dataset maxwell pdearena_data/maxwell3d
```

## 数据的兴趣点与挑战

三维向量场体积大；多源干涉与多尺度频率；键名与实际 $\mathbf{E}/\mathbf{H}$ 语义需谨慎。

## 主要来源

- [PDEArena 代码库与 README](https://github.com/pdearena/pdearena)
- [Maxwell 生成代码](https://github.com/pdearena/pdearena/blob/main/pdedatagen/maxwell.py)
- [Hugging Face 数据页](https://huggingface.co/datasets/pdearena/Maxwell-3D)
