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
dataset_family: PDEBench
summary: "PDEBench 的 HDF5 存储约定：数组维序、文件命名、坐标与 YAML 属性。"
description: "PDEBench 的 HDF5 存储约定：数组维序、文件命名、坐标与 YAML 属性。"
---

# 数据格式

本节依据当前可下载 HDF5、官方 dataloader / 下载清单，以及 DaRUS 数据说明整理。各方程页另列该类具体文件。

![PDEBench 数据格式示意](./DataFormat.png)

上图以密度（标量时序场）、速度（向量时序场）与潜在外力（可无时间维的条件场）为例，说明同一物理系统可拆成多个 HDF5 dataset；并非每个 PDE 都同时具备这三项。

## 存储与命名

- 格式：HDF5（`.hdf5` / `.h5`）。
- 命名：发布文件名多为下划线分隔，例如 `1D_Advection_Sols_beta0.4.hdf5`、`2D_diff-react_NA_NA.h5`；具体清单以官方 `pdebench_data_urls.csv` 为准。
- 每个文件通常含一个逻辑组，组内可有多个 dataset（对应不同物理量张量）；具体键名以生成代码与官方 dataloader 为准。
- 仿真参数以 **YAML 字符串**写在 HDF5 attributes 中（UTF-8）。

## 数组维序

通用约定：

\[
(b,\, t,\, x_1,\ldots,x_d,\, v)
\]

| 维 | 含义 |
|---|---|
| $b$ | 样本 / 轨迹数 |
| $t$ | 时间（含初值快照；以实际 `shape` 为准） |
| $x_1,\ldots,x_d$ | 空间维（1D/2D/3D） |
| $v$ | 状态通道维（标量场为 1；二维速度可为 2） |

并非所有维都出现：时间无关场（如某些外力 / Darcy 系数）可没有 $t$。官方坐标数组常见键为 `x-coordinate` / `y-coordinate` / `z-coordinate`（或不可压 NS 分片里的 `grid/x`、`grid/y`）。

## 通道与分 dataset 存储

- 多数标量 / 少通道任务把场放在名为 `tensor` 的 dataset 中，形状遵循上表。
- **可压缩 Navier–Stokes**：密度、压力、速度分量常存为独立 dataset（如 `density`、`pressure`、`Vx`、`Vy`、`Vz`），而不是拼成单一通道维 $v$，便于按空间子采样做 I/O。
- **不可压 NS**：速度与（静态）外力等可分键存储；分片文件名中的 `512` 不能直接当作网格分辨率。

## 机器学习用法

完整 HDF5 轨迹不是固定网络输入。官方训练通常按 `initial_step` 切出 $\ell$ 帧输入与下一步 / 多步目标。读取示例与 PyTorch Dataset 见官方仓库 [`pdebench/models`](https://github.com/pdebench/PDEBench/tree/main/pdebench/models)（如 FNO `utils.py` 中对 `tensor` 与 CFD 分键的分支）。

## 下载清单口径

当前一键下载文件列表以仓库 [`pdebench/data_download/pdebench_data_urls.csv`](https://github.com/pdebench/PDEBench/blob/main/pdebench/data_download/pdebench_data_urls.csv) 为准；各方程页列出该类下的相对路径与文件名。下载后仍应核对实际 `shape`、坐标与 attributes。

## 主要来源

- [PDEBench 官方代码库](https://github.com/pdebench/PDEBench)
- [官方下载说明与 URL 清单](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench 数据集 DOI](https://doi.org/10.18419/darus-2986)
