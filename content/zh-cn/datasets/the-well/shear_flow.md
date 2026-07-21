---
title: 不可压缩剪切流
parent_collection: "The Well"
physical_family: "不可压缩 Navier–Stokes + 示踪剂"
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/shear_flow/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/shear_flow"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/shear_flow"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: shear_flow
weight: 170
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "二维不可压缩剪切流由若干水平流层以相反方向运动初始化。Kelvin–Helmholtz 型不稳定性卷起涡旋并输运被动示踪剂；Reynolds 数与 Schmidt 数分别控制动量扩散和质量扩散。"
description: "二维不可压缩剪切流由若干水平流层以相反方向运动初始化。Kelvin–Helmholtz 型不稳定性卷起涡旋并输运被动示踪剂；Reynolds 数与 Schmidt 数分别控制动量扩散和质量扩散。"

---

# 不可压缩剪切流

> **所属数据集：** The Well  
> **数据目录：** `shear_flow`  
> **方程族：** 不可压缩 Navier–Stokes + 示踪剂  
> **文档类型：** 依据官方数据页、论文附录与当前仓库元数据重写的结构化中文文档。

## 1. 所属集合与物理概览

二维不可压缩剪切流由若干水平流层以相反方向运动初始化。Kelvin–Helmholtz 型不稳定性卷起涡旋并输运被动示踪剂；Reynolds 数与 Schmidt 数分别控制动量扩散和质量扩散。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。本文始终区分三类信息：方程/生成器理论上可以调整的参数、发布数据中实际扫描的参数，以及该发布版保持固定的参数。

## 2. 控制方程

$$
\frac{\partial\mathbf u}{\partial t}
-\nu\Delta\mathbf u+\nabla p
=-\mathbf u\cdot\nabla\mathbf u,
\qquad \nabla\cdot\mathbf u=0,
$$
$$
\frac{\partial s}{\partial t}
-D\Delta s=-\mathbf u\cdot\nabla s,
$$
with
$$
\nu=\mathrm{Re}^{-1},\qquad
D=(\mathrm{Re}\,\mathrm{Sc})^{-1}.
$$
涡量可由下式导出：
$$
\omega=\partial_xu_z-\partial_zu_x.
$$

### 变量与物理场

- \(\mathbf u=(u_x,u_z)\)：不可压缩速度。
- \(p\)：采用零均值规范的压强。
- \(s\)：被动示踪剂。
- \(\nu,D\)：动量扩散率与示踪剂扩散率。
- \(\mathrm{Re},\mathrm{Sc}\)：Reynolds 数与 Schmidt 数。
- \(\omega\)：可由速度导出的涡量；标准元数据中并非单独动态目标。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | Reynolds/Schmidt 数、剪切层数量/宽度/速度跃变、示踪剂团块数量/形状/位置、区域长宽比、扰动、边界条件和谱分辨率。 |
| 数据中实际变化 | 完整笛卡尔积：\(\mathrm{Re}\in\{10^4,5\times10^4,10^5,5\times10^5\}\)、\(\mathrm{Sc}\in\{0.1,0.2,0.5,1,2,5,10\}\)、剪切层数 \(n_{\rm shear}\in\{2,4\}\)、示踪团块数 \(n_{\rm blobs}\in\{2,3,4,5\}\)、剪切宽度因子 \(w\in\{0.25,0.5,1,2,4\}\)，共 \(4\times7\times2\times4\times5=1120\) 条轨迹。 |
| 数据中保持固定 | 方程族、周期区域设置、发布的 \(256\times512\) 分辨率、\([0,20]\) 上 200 帧、压强规范，以及生成器中的速度/示踪剂幅度约定。 |

## 4. 初始条件与边界条件

### 初始条件

交替方向的水平速度层叠加 2–5 个被动示踪团块。剪切层数与宽度是显式数据轴，其他随机位置/相位遵循生成器。

### 边界条件

文档描述为二维周期流；各维具体边界仍应读取 HDF5 元数据确认。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `shear_flow` |
| 空间维数 | 2D |
| 坐标系 | Cartesian $(x,z)$ |
| 空间分辨率 | $256\times512$ |
| 每条轨迹存储帧数 | 200 |
| 轨迹数 | 1120 |
| 展开后的动态通道数 | 4 |
| 动态物理场 | 被动示踪剂 $s$、压强 $p$、速度 $(u_x,u_z)$ |
| 静态场/标量上下文 | Reynolds 数、Schmidt 数及初始条件标签 |
| 时间范围 | $[0,20]$ |
| 存储时间间隔 | $0.1$ |
| 空间区域 | 2D periodic domain |
| 发布数据量 | 547 GB |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,4)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,4)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,4)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** Dedalus mixed Fourier–Chebyshev pseudo-spectral method with adaptive time stepping

Dedalus 使用 Fourier–Chebyshev 混合伪谱离散与自适应时间步。早期页面曾给出较小分辨率/体量或误标参数，实际使用时应优先采用当前数据元数据。

## 7. 推荐机器学习任务与诊断

湍流转捩预测、示踪剂输运、跨 \((\mathrm{Re},\mathrm{Sc})\) 参数泛化、对剪切几何的敏感性、涡量/谱诊断及稳定 rollout。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

当前元数据为 \(256\times512\)、1120 条轨迹、约 547 GB。早期文字版本曾出现 \(128\times256\)/115 GB 或把参数误标为 Rayleigh 的情况，不应作为现行张量规格。

当前仓库状态： **active**。本文核对日期为 2026-07-21。实际实验必须检查 `dataset_name.yaml`、`stats.yaml`、HDF5 坐标及 release notes，以确定所用文件的精确版本。

## 下载与读取

### 安装接口

```bash
python -m venv .venv
source .venv/bin/activate
pip install the_well
```

### 下载一个划分

```bash
the-well-download --base-path ./the_well_data --dataset shear_flow --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset shear_flow --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="shear_flow",
    well_split_name="train",
)
loader = DataLoader(trainset, batch_size=1, shuffle=True)

sample = trainset[0]
print(sample.keys())
```

### Hugging Face 流式读取

当前集合中该目录可通过 Hub 读取：

```python
from the_well.data import WellDataset

trainset = WellDataset(
    well_base_path="hf://datasets/polymathic-ai/",
    well_dataset_name="shear_flow",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。


## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/shear_flow/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/shear_flow> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/shear_flow> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. 引用与来源说明

推荐引用 Dedalus 以及 The Well 附录列出的剪切流/Kelvin–Helmholtz 文献。

同时引用 The Well 总论文：

> Ohana 等，**The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**，NeurIPS 2024 Datasets and Benchmarks。

本文不是官网逐字镜像，而是依据官方数据页、论文附录和当前仓库元数据做的结构化整理、翻译与校勘。英文配套文档是忠实于来源的重新组织版本；中文文档加入了参数层次、通道和输入输出形状等便于多数据集统一管理的信息。
