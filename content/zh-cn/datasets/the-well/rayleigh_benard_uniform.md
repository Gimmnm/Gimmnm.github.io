---
title: "Rayleigh–Bénard 热对流——均匀重采样"
parent_collection: "The Well"
physical_family: "Boussinesq 热对流"
spatial_dimension: 2D
coordinate_system: "Cartesian, uniformly resampled"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/rayleigh_benard_uniform/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/rayleigh_benard_uniform"
huggingface_dataset: ""
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: rayleigh_benard_uniform
weight: 150
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "水平周期流体层下热上冷。浮力克服黏性与热扩散驱动对流，形成 Bénard 对流胞；对流胞的位置和后续湍流演化对微小初始扰动高度敏感。"
description: "水平周期流体层下热上冷。浮力克服黏性与热扩散驱动对流，形成 Bénard 对流胞；对流胞的位置和后续湍流演化对微小初始扰动高度敏感。"

---

# Rayleigh–Bénard 热对流——均匀重采样

> **所属数据集：** The Well  
> **数据目录：** `rayleigh_benard_uniform`  
> **方程族：** Boussinesq 热对流  
> **文档类型：** 依据官方数据页、论文附录与当前仓库元数据重写的结构化中文文档。

## 1. 所属集合与物理概览

水平周期流体层下热上冷。浮力克服黏性与热扩散驱动对流，形成 Bénard 对流胞；对流胞的位置和后续湍流演化对微小初始扰动高度敏感。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。本文始终区分三类信息：方程/生成器理论上可以调整的参数、发布数据中实际扫描的参数，以及该发布版保持固定的参数。

## 2. 控制方程

$$
\frac{\partial b}{\partial t}-\kappa\Delta b
=-\mathbf u\cdot\nabla b,
$$
$$
\frac{\partial\mathbf u}{\partial t}
-\nu\Delta\mathbf u+\nabla p-b\mathbf e_z
=-\mathbf u\cdot\nabla\mathbf u,
\qquad \nabla\cdot\mathbf u=0,
$$
with
$$
\kappa=(\mathrm{Ra}\,\mathrm{Pr})^{-1/2},\qquad
\nu=\left(\frac{\mathrm{Ra}}{\mathrm{Pr}}\right)^{-1/2}.
$$

### 变量与物理场

- \(b\)：与温度差相关的浮力标量。
- \(\mathbf u=(u_x,u_z)\)：不可压缩速度。
- \(p\)：采用零均值规范的压强。
- \(\mathrm{Ra}\)：Rayleigh 数。
- \(\mathrm{Pr}\)：Prandtl 数。
- \(\kappa,\nu\)：热扩散率与运动黏度。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | Rayleigh/Prandtl 数、上下板温度、长宽比、无滑移/自由滑移边界、扰动谱与幅度、黏度/扩散率、空间基函数/分辨率和输出间隔。 |
| 数据中实际变化 | Rayleigh 数 \(\mathrm{Ra}\in\{10^6,10^7,10^8,10^9,10^{10}\}\)、Prandtl 数 \(\mathrm{Pr}\in\{0.1,0.2,0.5,1,2,5,10\}\)，以及初始浮力扰动幅度 \(\delta b_0\in\{0.2,0.4,0.6,0.8,1.0\}\)，并配合多次随机扰动。由 \(5\times7\times50=1750\) 可知每个 \((\mathrm{Ra},\mathrm{Pr})\) 参数对有 50 个初始实现。 |
| 数据中保持固定 | 区域长宽比、上下板浮力值、无滑移壁面速度、水平周期性、\([0,50]\) 上 200 帧，以及同一 Dedalus 模拟活动。uniform 目录只改变表示，不改变物理。 |

## 4. 初始条件与边界条件

### 初始条件

导热平衡浮力剖面叠加随机扰动，幅度由 \(\delta b_0\) 控制；速度从生成器规定的静止/扰动状态开始。

### 边界条件

\(x\) 方向周期；在 \(z=0,1\) 处速度无滑移，浮力固定（下热上冷）。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `rayleigh_benard_uniform` |
| 空间维数 | 2D |
| 坐标系 | Cartesian, uniformly resampled |
| 空间分辨率 | $512\times128$ |
| 每条轨迹存储帧数 | 200 |
| 轨迹数 | 1750 |
| 展开后的动态通道数 | 4 |
| 动态物理场 | 浮力 $b$、压强 $p$、速度 $(u_x,u_z)$ |
| 静态场/标量上下文 | 与原生网格版本相同的物理标签 |
| 时间范围 | $[0,50]$ |
| 存储时间间隔 | $0.25$ |
| 空间区域 | $x\in[0,4], z\in[0,1]$ |
| 发布数据量 | not separately reported; similar order to native-grid data |
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

**文档记录的求解器：** post-processed uniform resampling of Dedalus trajectories

Dedalus 在水平方向使用 Fourier 基、竖直方向使用 Chebyshev 基，并采用自适应时间步。水平方向周期，上下板施加无滑移速度与固定浮力。uniform 版本是对相同轨迹的后处理重采样，而不是新的物理模拟。

## 7. 推荐机器学习任务与诊断

初值敏感性、对流胞位置预测、湍流演化、跨 \((\mathrm{Ra},\mathrm{Pr})\) 参数迁移、原生非均匀网格学习以及与均匀重采样数据的对比。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

该目录是对原生轨迹的均匀网格重采样。插值会改变表示，尤其影响最高频模态；不应把它重复计作独立物理模拟。当前常见 Hugging Face 流式列表中未列出。

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
the-well-download --base-path ./the_well_data --dataset rayleigh_benard_uniform --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset rayleigh_benard_uniform --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="rayleigh_benard_uniform",
    well_split_name="train",
)
loader = DataLoader(trainset, batch_size=1, shuffle=True)

sample = trainset[0]
print(sample.keys())
```

### Hugging Face 状态

当前常见 The Well Hugging Face 流式列表中没有该目录。应使用官方下载 CLI/Flatiron 托管文件，并在使用前重新检查集合页面，不能假定 Hub 路径一定存在。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。


## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/rayleigh_benard_uniform/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/rayleigh_benard_uniform> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. 引用与来源说明

推荐引用 Dedalus；物理设置还应参考 The Well 附录列出的 Rayleigh–Bénard 文献。

同时引用 The Well 总论文：

> Ohana 等，**The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**，NeurIPS 2024 Datasets and Benchmarks。

本文不是官网逐字镜像，而是依据官方数据页、论文附录和当前仓库元数据做的结构化整理、翻译与校勘。英文配套文档是忠实于来源的重新组织版本；中文文档加入了参数层次、通道和输入输出形状等便于多数据集统一管理的信息。
