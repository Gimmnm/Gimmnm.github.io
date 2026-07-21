---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 04_shallow_water_2d_vorticity
spatial_dimension: 2
time_dependent: true
data_format: Zarr
paper: "arXiv:2209.15616v2"
download_key: ShallowWater-2D
last_verified: 2026-07-21
title: 二维球面浅水方程（涡度形式）
linkTitle: "SWE vorticity"
weight: 40
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "同一浅水轨迹上的涡度任务视图：压力/自由表面 + 垂直涡度，2-day 预测。"
description: "同一浅水轨迹上的涡度任务视图：压力/自由表面 + 垂直涡度，2-day 预测。"
---

# 二维球面浅水方程（涡度形式）

论文中的 vorticity–stream-function **任务表示**：对同一 `ShallowWater-2D` 速度轨迹，将风场转为球面法向涡度 $\zeta$，模型只接收两个标量通道。不是第二个 124 GB 独立发布。

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEArena** |
| 底层发布 | [pdearena/ShallowWater-2D](https://huggingface.co/datasets/pdearena/ShallowWater-2D) |
| 数据集论文 | [Towards Multi-spatiotemporal-scale Generalized PDE Modeling](https://arxiv.org/abs/2209.15616) |
| 配套速度文档 | [速度形式](../03_shallow_water_2d_velocity/) |
| 数据量 | 共享 124 GB（不额外计量） |
| 许可证 | MIT |
| 文档核对日期 | 2026-07-21 |

## 控制方程

底层动力学同速度形式。球面垂直涡度

\[
\zeta=(\nabla_s\times\mathbf{v})\cdot\hat{\mathbf{r}}
\]

（局部笛卡尔近似下 $\zeta\approx\partial_x v-\partial_y u$）。任务使用 $[p,\zeta]$，不是位涡 $(\zeta+f_c)/h$，也不单独保存流函数输出通道。

## 变量与坐标

- $p$：压力/自由表面标量；
- $\zeta$：垂直涡度（由 $(u,v)$ 导出）；
- 网格与坐标同[速度形式](../03_shallow_water_2d_velocity/)。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 2（球面） |
| 含时间 | 是 |
| 空间分辨率 | $192\times96$ |
| 任务时间窗 | 2 days / 48 h |
| 轨迹长 | $T=11$ |
| 轨迹数 | 与底层相同 8,400（5,600/1,400/1,400） |
| 通道 | 2：$p$、$\zeta$ |
| 数据量 | 不额外计量 |
| 格式 | 同底层 Zarr；涡度由管道导出 |

## 初始条件

与速度形式完全相同（`random2` 等）。

## 边界条件

同速度形式。

## 数值生成方法

同速度形式；涡度在同一动力学轨迹上由风场计算。附录说明 pressure 与 vorticity 训练前归一化。

## 参数

| 参数 | 变化方式 | 取值 |
|---|---|---|
| 初值随机量 | 每轨迹随机 | 同速度形式 |
| $\zeta$ | 由 $(u,v)$ 导出 | 非独立随机参数 |
| 网格 / 物理常数 / 20-day 设置 | 固定 | 同速度形式 |
| 时间任务 | 论文明确 2-day 涡度任务 | 无独立 1-day 涡度仓库证据 |

## 发布配置

- 2-day 涡度任务：2 帧历史 → 1 帧未来；底层轨迹与速度形式相同。
- 完整发布规模同 `ShallowWater-2D`（8,400 条，124 GB 共享）。

## 数据文件

下载同一 `ShallowWater-2D`；无单独 “ShallowWater-Vorticity” 官方仓库。文件布局见[速度形式](../03_shallow_water_2d_velocity/)与[数据格式](../00_data_format/)。

## 数据布局与机器学习输入输出

\[
X\in\mathbb{R}^{2\times2\times96\times192}\to Y\in\mathbb{R}^{1\times2\times96\times192}
\]

（时间并入通道：$[4,96,192]\to[2,96,192]$）。

## 下载

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/ShallowWater-2D
```

下载后按 PDEArena 数据管道构造涡度视图。

## 从官方代码重新生成

同[速度形式](../03_shallow_water_2d_velocity/)；再在任务侧由风场计算 $\zeta$。

## 数据的兴趣点与挑战

涡度突出旋转与小尺度结构；二维速度压成单标量改变学习难度；与速度形式共享轨迹，适合公平比较场表示。

## 主要来源

- [PDEArena 论文](https://arxiv.org/abs/2209.15616)
- [速度形式配套文档](../03_shallow_water_2d_velocity/)
- [Hugging Face 底层数据页](https://huggingface.co/datasets/pdearena/ShallowWater-2D)
