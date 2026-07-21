---
title: "数据格式"
linkTitle: "data format"
weight: 5
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "PDEArena 的存储约定：HDF5 / Zarr、字段键、切分与模型张量。"
description: "PDEArena 的存储约定：HDF5 / Zarr、字段键、切分与模型张量。"
---

# 数据格式

本节依据官方 [`docs/data.md`](https://github.com/pdearena/pdearena/blob/main/docs/data.md) / [`docs/datadownload.md`](https://github.com/pdearena/pdearena/blob/main/docs/datadownload.md)，以及当前 Hugging Face 发布布局整理。各方程页另列该类具体文件命名与规模。

## 发布与切分

- 数据托管在 [Hugging Face `pdearena`](https://huggingface.co/pdearena)；下载推荐 `git lfs` + `git clone`。
- 官方组织当前四个仓库：`NavierStokes-2D`、`NavierStokes-2D-conditoned`（拼写少一个 `i`）、`ShallowWater-2D`、`Maxwell-3D`。
- 切分一般为 `train` / `valid` / `test`。NS 与 Maxwell 多为扁平目录下按 seed 分片的 `.h5`；浅水为 `train|valid|test/seed=*` 目录（发布为 Zarr，由 NetCDF 转换）。

## 按任务的存储

| 任务 | 格式 | 典型状态键 | 备注 |
|---|---|---|---|
| Navier–Stokes 2D | HDF5 (`.h5`) | `u`, `vx`, `vy` | 另有 `t`,`x`,`y`,`dt`,`dx`,`dy`,`buo_y` |
| ShallowWater-2D | NetCDF → Zarr | 压力/自由表面 + 风场 | 官方提供 `normstats.pt`；涡度由风场导出 |
| Maxwell-3D | HDF5 | `d_field`, `h_field` | 代码将 `E`/`H` 写入上述键，语义以生成器为准 |
| KS-1D | HDF5 | `pde_*` 解数组 | 另有 `dt`,`dx`；条件文件含黏度字段 |

## 数组与模型张量

原始二维轨迹常统一写成

\[
U\in\mathbb{R}^{N\times T\times C\times H\times W},
\]

三维为 $N\times T\times C\times D\times H\times W$。完整轨迹不是固定网络输入；训练按任务配置切出历史帧 $\to$ 未来帧，例如标准 NS 常用 4→1，浅水常用 2→1，条件化 NS 常用 1→1。

## 命名约定（摘要）

- 标准 NS：`NavierStokes2D_{split}_{seed}_0.50000.h5`
- 条件化 NS：`NavierStokes2D_{split}_{seed}_{buoyancy}[_{n}].h5`（浮力写在文件名中）
- Maxwell：`Maxwell3D_{split}_{seed}.h5`
- 浅水：`{split}/seed={seed}/`（Zarr 组）
- KS（外部）：`KS_{split}_{fixed|conditional}_viscosity.h5`

下载后应核对实际 `shape`、键名与元数据；不要仅凭文件名推断分辨率或时间间隔。

## 主要来源

- [PDEArena 论文](https://arxiv.org/abs/2209.15616)
- [官方代码库](https://github.com/pdearena/pdearena)
- [数据生成说明](https://github.com/pdearena/pdearena/blob/main/docs/data.md)
- [下载说明](https://github.com/pdearena/pdearena/blob/main/docs/datadownload.md)
