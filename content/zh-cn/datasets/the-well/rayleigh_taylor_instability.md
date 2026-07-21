---
title: "Rayleigh–Taylor 不稳定性"
parent_collection: "The Well"
physical_family: 变密度可混溶流
spatial_dimension: 3D
coordinate_system: "Cartesian $(x,y,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/rayleigh_taylor_instability/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/rayleigh_taylor_instability"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/rayleigh_taylor_instability"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: rayleigh_taylor_instability
weight: 160
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "重的可混溶流体位于轻流体上方并受重力作用。界面扰动发展为上升气泡和下降尖峰，最终形成湍流混合层。Atwood 数控制密度反差与混合层对称性，初始 Fourier 谱控制结构形态。"
description: "重的可混溶流体位于轻流体上方并受重力作用。界面扰动发展为上升气泡和下降尖峰，最终形成湍流混合层。Atwood 数控制密度反差与混合层对称性，初始 Fourier 谱控制结构形态。"

---

# Rayleigh–Taylor 不稳定性

> **所属数据集：** The Well  
> **数据目录：** `rayleigh_taylor_instability`  
> **方程族：** 变密度可混溶流  
> **文档类型：** 依据官方数据页、论文附录与当前仓库元数据重写的结构化中文文档。

## 1. 所属集合与物理概览

重的可混溶流体位于轻流体上方并受重力作用。界面扰动发展为上升气泡和下降尖峰，最终形成湍流混合层。Atwood 数控制密度反差与混合层对称性，初始 Fourier 谱控制结构形态。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。本文始终区分三类信息：方程/生成器理论上可以调整的参数、发布数据中实际扫描的参数，以及该发布版保持固定的参数。

## 2. 控制方程

$$
\frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf u)=0,
$$
$$
\frac{\partial(\rho\mathbf u)}{\partial t}
+\nabla\cdot(\rho\mathbf u\mathbf u)
=-\nabla p+\nabla\cdot\tau+\rho\mathbf g,
$$
$$
\nabla\cdot\mathbf u
=-\kappa\nabla\cdot\left(\frac{\nabla\rho}{\rho}\right),
$$
$$
\tau=\rho\nu\left[
\nabla\mathbf u+(\nabla\mathbf u)^\top
-\frac23(\nabla\cdot\mathbf u)I
\right].
$$
The density contrast is summarized by
$$
\mathrm{At}=\frac{\rho_h-\rho_l}{\rho_h+\rho_l}.
$$

### 变量与物理场

- \(\rho,\mathbf u,p\)：密度、速度与压强。
- \(\mathbf g\)：重力。
- \(\kappa\)：共同分子扩散系数。
- \(\nu\)：运动黏度；代码中会缩放以使 Kolmogorov 尺度接近网格分辨率。
- \(\mathrm{At}\)：Atwood 数。
- 初始扰动在 Fourier 空间由均值 \(\mu\)、宽度 \(\sigma\) 和相位范围 \(\phi_{\max}\) 描述。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | Atwood 数、重力、分子扩散、黏度/分辨率规则、密度界面厚度、初始谱幅度/相位、区域长宽比、边界条件及输出时间步。 |
| 数据中实际变化 | Atwood 数 \(\mathrm{At}\in\{3/4,1/2,1/4,1/8,1/16\}\)。初始界面谱包括 Gaussian 型幅度包络：\(\mu\in\{1,4,16\}\)、\(\sigma\in\{1/4,1/2,1\}\) 与随机相位；第二类固定 \(\mu=16,\sigma=0.25\)，并令 \(\phi_{\max}\in\{\pi/128,\pi/8,\pi/2,\pi\}\)。发布数据共有 45 条轨迹。 |
| 数据中保持固定 | 网格 \(128^3\)、重力设置、可混溶流体方程族、压强求解器/离散、依赖分辨率的黏度规则，以及每个 Atwood 组内的数据采样设置。 |

## 4. 初始条件与边界条件

### 初始条件

重/轻流体之间的密度界面叠加 Fourier 空间中按文档谱族生成的扰动。

### 边界条件

精确三维边界配置写在发布 HDF5 元数据和 TURMIX3D 设置中，不应在未检查文件时直接假设全周期。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `rayleigh_taylor_instability` |
| 空间维数 | 3D |
| 坐标系 | Cartesian $(x,y,z)$ |
| 空间分辨率 | $128^3$ |
| 每条轨迹存储帧数 | 119 on current dataset page (paper table: 120) |
| 轨迹数 | 45 |
| 展开后的动态通道数 | 4 |
| 动态物理场 | 密度 $\rho$ 与速度（3） |
| 静态场/标量上下文 | Atwood 数与初始谱元数据 |
| 时间范围 | Atwood-dependent nondimensional time |
| 存储时间间隔 | varies with Atwood-number group |
| 空间区域 | uniform cubic cells |
| 发布数据量 | 255.6 GB |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,L_3,4)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,L_3,4)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,L_3,4)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** TURMIX3D; staggered MAC mesh, Lagrange+remap, TVD, SSPRK2, multigrid pressure solve

TURMIX3D 使用交错 Marker-and-Cell 网格和 Lagrange+remap 方法。空间上采用二阶 TVD 与 Van Leer 限制器，时间上采用二阶 SSP Runge–Kutta。变密度修正压强方程由红黑松弛和 V-cycle 多重网格求解。

## 7. 推荐机器学习任务与诊断

质量守恒的湍流混合、Atwood 条件泛化、时间步泛化、气泡/尖峰形态、混合层宽度增长率预测及惯性区谱保真。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

附录描述每个 Atwood 数有 13 类初始化，理论上会得到 65 个组合，而发布表/目录只有 45 条轨迹。当前页面报告 119 帧，论文表格为 120 帧。不同 Atwood 组的时间间隔不同，模型应显式读取时间坐标。

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
the-well-download --base-path ./the_well_data --dataset rayleigh_taylor_instability --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset rayleigh_taylor_instability --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="rayleigh_taylor_instability",
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
    well_dataset_name="rayleigh_taylor_instability",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。


## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/rayleigh_taylor_instability/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/rayleigh_taylor_instability> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/rayleigh_taylor_instability> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. 引用与来源说明

推荐引用 The Well 指定的 Rayleigh–Taylor 模拟文献 [187]，并按需引用 TURMIX3D 方法。

同时引用 The Well 总论文：

> Ohana 等，**The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**，NeurIPS 2024 Datasets and Benchmarks。

本文不是官网逐字镜像，而是依据官方数据页、论文附录和当前仓库元数据做的结构化整理、翻译与校勘。英文配套文档是忠实于来源的重新组织版本；中文文档加入了参数层次、通道和输入输出形状等便于多数据集统一管理的信息。
