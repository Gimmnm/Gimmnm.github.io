---
title: "PDEArena 方程数据文档索引"
dataset_family: PDEArena
dataset_release: PDEArena
equation: multiple
spatial_dimension: 0
coordinate_system: multiple
task_variant: catalog
official_status: "documentation index"
license: MIT
last_verified: 2026-07-21
linkTitle: PDEArena
weight: 30
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
summary: "面向算子学习的 PDE 基准：Navier–Stokes、浅水方程、Maxwell-3D 与 KS 等。"
description: "面向算子学习的 PDE 基准：Navier–Stokes、浅水方程、Maxwell-3D 与 KS 等。"
---

# PDEArena 方程数据文档索引

本文档集参考 [The Well 单数据集页面](https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/) 的组织方式，并增加适合跨多个 benchmark 统一整理的 YAML front matter、所属数据集、发布状态、下载方法、输入输出张量、参数三分表以及版本差异。

## 文档列表

| 文档 | 物理系统/任务 | 官方状态 | 数据规模 |
|---|---|---|---:|
| [Navier--Stokes 标准版](../navier_stokes_2d_standard/) | 2D 不可压 NS + 烟雾标量 | PDEArena 官方发布 | 43 GB |
| [Navier--Stokes 条件化版](../navier_stokes_2d_conditioned/) | 浮力与时间尺度条件化 | PDEArena 官方发布 | 81.7 GB |
| [浅水方程速度形式](../shallow_water_2d_velocity/) | 1-day/2-day，3 通道 | PDEArena 官方发布/任务视图 | 124 GB（共享） |
| [浅水方程涡度形式](../shallow_water_2d_vorticity/) | 2-day，2 标量通道 | 同一浅水发布的任务视图 | 不额外计量 |
| [Maxwell-3D](../maxwell_3d/) | 3D 电磁场 | PDEArena 官方扩展 | 121 GB |
| [Kuramoto--Sivashinsky-1D](../kuramoto_sivashinsky_1d/) | fixed/conditional viscosity | PDEArena loader 支持的外部数据 | 3.92 GB |

## 当前 PDEArena 官方 Hugging Face 四库

| 发布 | train/valid/test | 总轨迹 | 大小 |
|---|---:|---:|---:|
| NavierStokes-2D | 5,200/1,300/1,300 | 7,800 | 43 GB |
| NavierStokes-2D-conditoned | 6,656/1,664/1,664 | 9,984 | 81.7 GB |
| ShallowWater-2D | 5,600/1,400/1,400 | 8,400 | 124 GB |
| Maxwell-3D | 6,400/1,600/1,600 | 9,600 | 121 GB |
| **合计**|  | **35,784**| **369.7 GB** |

浅水速度/涡度、1-day/2-day 重用同一发布，不能重复相加。KS 不在当前 PDEArena 组织的四库中，单独统计。

## 统一字段约定

- 原始二维轨迹：$[N,T,C,H,W]$；
- 原始三维轨迹：$[N,T,C,D,H,W]$；
- 模型样本：$[T_{in},C,\ldots]\to[T_{out},C,\ldots]$；
- “物理参数”与“时间/网格条件”分开记录；
- “代码可调”“发布实际变化”“发布固定”分别列出；
- 论文、当前主分支和当前数据库不一致时并列保留，不强行拼成一个版本。
