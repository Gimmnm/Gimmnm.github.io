---
title: "PDEArena"
linkTitle: PDEArena
weight: 30
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
math: true
summary: "面向算子学习的 PDE 基准：Navier–Stokes、浅水、Maxwell-3D 与 KS 等。"
description: "面向算子学习的 PDE 基准：Navier–Stokes、浅水、Maxwell-3D 与 KS 等。"
dataset_family: PDEArena
---

# PDEArena

## 问题定义

算子学习（operator learning）把定义在不同域上的解 $u:\mathcal{X}\to\mathbb{R}^{n}$ 与 $u':\mathcal{X}'\to\mathbb{R}^{n'}$ 通过算子 $\mathcal{G}$ 联系起来：

\[
\mathcal{G}:(u\in\mathcal{U})\mapsto(u'\in\mathcal{U}'),
\]

其中 $\mathcal{U}$、$\mathcal{U}'$ 分别为相应解空间。实践中，神经 PDE 代理通常取同一网格上若干历史时间帧，映射到未来一帧或多帧。

PDEArena 强调跨初值、跨 PDE 参数与跨时间窗 $\Delta t$ 的泛化。条件化实验中，解对 $\{u,u'\}$ 可来自不同力项刻画的解空间；同时要求映射 $u\mapsto u'$ 能泛化到不同时间窗。力项与 $\Delta t$ 均为连续标量，可用正弦 Fourier 嵌入编码后注入网络。

基准设计原则包括：任务由领域求解器生成、足够困难、速度/涡度等表示多样，并能探测时间尺度与参数泛化。

## 方程目录

先读 [数据格式](./00_data_format/)；各方程页另列该类下载文件与命名约定。

| # | 方程文档 | Hugging Face 发布 | 当前标称体积 |
|---:|---|---|---:|
| — | [数据格式](./00_data_format/) | — | — |
| 1 | [二维不可压 NS 烟雾浮力流（标准版）](./01_navier_stokes_2d_standard/) | `NavierStokes-2D` | 43 GB |
| 2 | [二维不可压 NS（参数条件化版）](./02_navier_stokes_2d_conditioned/) | `NavierStokes-2D-conditoned` | 81.7 GB |
| 3 | [球面浅水方程（速度形式）](./03_shallow_water_2d_velocity/) | `ShallowWater-2D` | 124 GB（共享） |
| 4 | [球面浅水方程（涡度形式）](./04_shallow_water_2d_vorticity/) | 同一 `ShallowWater-2D` 任务视图 | 不额外计量 |
| 5 | [三维 Maxwell 时域电磁场](./05_maxwell_3d/) | `Maxwell-3D` | 121 GB |
| 6 | [一维 Kuramoto–Sivashinsky](./06_kuramoto_sivashinsky_1d/) | 外部 `phlippe/...`（loader 支持） | 3.92 GB |

## 统一口径

- 当前 PDEArena 组织官方四库合计约 **369.7 GB**、**35,784** 条轨迹；浅水速度/涡度与 1-day/2-day 共用同一发布，不能重复相加。KS 单独统计。
- 轨迹数、时间点数、采样、文件布局与体积以 **Hugging Face 发布 + 官方生成/任务配置** 为准；与论文表述冲突时以实际数据集为准。
- 原始二维轨迹常写为 $[N,T,C,H,W]$；三维为 $[N,T,C,D,H,W]$。模型样本由历史帧切到未来帧，具体 $\ell$ 由任务配置决定。
- Maxwell-3D 为官方扩展发布；KS 为代码支持的外部数据，不计入四库总量。
