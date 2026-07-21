---
title: "周期阶梯 Helmholtz 声散射"
parent_collection: "The Well"
physical_family: "波动/Helmholtz 散射"
spatial_dimension: 2D
coordinate_system: "Cartesian $(x_1,x_2)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/helmholtz_staircase/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/helmholtz_staircase"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/helmholtz_staircase"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: helmholtz_staircase
weight: 110
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "点声源位于无限周期、声硬阶梯表面上方。问题在频域中求解，再解析采样一个振荡周期。沿表面传播的俘获模与向外辐射波同时存在，形成两种空间尺度，模型必须辨别真正控制时间相位的源频率。"
description: "点声源位于无限周期、声硬阶梯表面上方。问题在频域中求解，再解析采样一个振荡周期。沿表面传播的俘获模与向外辐射波同时存在，形成两种空间尺度，模型必须辨别真正控制时间相位的源频率。"

---

# 周期阶梯 Helmholtz 声散射

> **所属数据集：** The Well  
> **数据目录：** `helmholtz_staircase`  
> **方程族：** 波动/Helmholtz 散射  
> **文档类型：** 依据官方数据页、论文附录与当前仓库元数据重写的结构化中文文档。

## 1. 所属集合与物理概览

点声源位于无限周期、声硬阶梯表面上方。问题在频域中求解，再解析采样一个振荡周期。沿表面传播的俘获模与向外辐射波同时存在，形成两种空间尺度，模型必须辨别真正控制时间相位的源频率。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。本文始终区分三类信息：方程/生成器理论上可以调整的参数、发布数据中实际扫描的参数，以及该发布版保持固定的参数。

## 2. 控制方程

时域问题为
$$
\frac{\partial^2 U}{\partial t^2}-\Delta U
=\delta(t)\delta(\mathbf x-\mathbf x_0),\qquad
\partial_n U=0\ \text{on }\partial\Omega.
$$
对时间作 Fourier 变换后，
$$
-(\Delta+\omega^2)u=\delta_{\mathbf x_0}\quad\text{in }\Omega,\qquad
\partial_nu=0\quad\text{on }\partial\Omega,
$$
并满足外向辐射条件。时间样本由下式的实部/虚部分量重构： \(u(\mathbf x)e^{-i\omega t}\).

### 变量与物理场

- \(U(t,\mathbf x)\)：时域声场。
- \(u(\mathbf x)\)：复值频域声压。
- \(\omega\)：点声源角频率。
- \(\mathbf x_0\)：声源位置。
- \(\partial_n\)：边界法向导数。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 声源频率与位置、阶梯周期/几何、声速与密度、边界类型、输出窗口范围、空间离散、Floquet–Bloch 求积和相位采样。 |
| 数据中实际变化 | 声源频率取 16 个值：
\[
0.062,0.251,0.439,0.626,0.813,0.998,1.182,1.363,1.541,1.715,1.882,2.042,2.191,2.323,2.433,2.511.
\]
声源位置使用 32 个配置，因此共有 \(16\times32=512\) 个参数组合；每个组合在一个周期内采样 50 个相位。 |
| 数据中保持固定 | 阶梯几何与周期、声硬 Neumann 边界、常密度气体与归一化声速 \(c=1\)、低频/俘获模区域、输出网格分辨率及 50 个相位样本。 |

## 4. 初始条件与边界条件

### 初始条件

在 \(t=0,\mathbf x=\mathbf x_0\) 施加单个脉冲点源，激发前场为静止。发布的频域表示中，\((\omega,\mathbf x_0)\) 完全指定声源。

### 边界条件

阶梯表面满足 Neumann/声硬条件 \(\partial_nu=0\)，表面几何周期，并在无界区域满足外向辐射条件。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `helmholtz_staircase` |
| 空间维数 | 2D |
| 坐标系 | Cartesian $(x_1,x_2)$ |
| 空间分辨率 | $1024\times256$ |
| 每条轨迹存储帧数 | 50 |
| 轨迹数 | 512 |
| 展开后的动态通道数 | 2 |
| 动态物理场 | 声压实部与虚部 |
| 静态场/标量上下文 | 阶梯掩码；声源位置与频率元数据 |
| 时间范围 | one period $T=2\pi/\omega$ per trajectory |
| 存储时间间隔 | $T/50$ |
| 空间区域 | periodic corrugated half-space represented on a finite output window |
| 发布数据量 | 52.4 GB |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,2)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,2)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,2)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** Floquet–Bloch transform + high-order boundary integral equation method

生成器结合 Floquet–Bloch 变换与高阶边界积分方程方法，把二维 PDE 化为一维边界上的积分；专门求积规则处理阶梯拐角与辐射条件。附录记录精度约 7–8 位有效数字，并在 64 个 CPU 核上每个参数组合约耗时 400 s。

## 7. 推荐机器学习任务与诊断

频率/相位条件预测、逆声源定位、逆边界/几何推断、俘获模识别以及跨声源频率泛化。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

附录文字列出的候选 \(x,y\) 坐标集合若做完整笛卡尔积会超过 32 个位置，因此精确的 32 点列表应以 HDF5/生成器元数据为准。50 帧是由频域解解析生成的相位，而不是 50 次独立 PDE 时间推进。

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
the-well-download --base-path ./the_well_data --dataset helmholtz_staircase --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset helmholtz_staircase --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="helmholtz_staircase",
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
    well_dataset_name="helmholtz_staircase",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。


## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/helmholtz_staircase/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/helmholtz_staircase> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/helmholtz_staircase> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. 引用与来源说明

推荐引用：Agocs 与 Barnett，*Trapped acoustic waves and raindrops: high-order accurate integral equation method for localized excitation of a periodic staircase*。

同时引用 The Well 总论文：

> Ohana 等，**The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**，NeurIPS 2024 Datasets and Benchmarks。

本文不是官网逐字镜像，而是依据官方数据页、论文附录和当前仓库元数据做的结构化整理、翻译与校勘。英文配套文档是忠实于来源的重新组织版本；中文文档加入了参数层次、通道和输入输出形状等便于多数据集统一管理的信息。
