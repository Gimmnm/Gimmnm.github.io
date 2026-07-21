---
title: 湍流辐射混合层——3D
parent_collection: "The Well"
physical_family: "可压缩流体 + 辐射冷却"
spatial_dimension: 3D
coordinate_system: "Cartesian $(x,y,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/turbulent_radiative_layer_3D/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/turbulent_radiative_layer_3D"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/turbulent_radiative_layer_3D"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: turbulent_radiative_layer_3D
weight: 220
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "冷而致密的气体相与热而稀薄的气体相相对运动。界面湍流混合产生中间温度气体，随后通过辐射冷却并并入冷相。2D 与 3D 版本共享同一物理参数扫描，可用于跨维数迁移。"
description: "冷而致密的气体相与热而稀薄的气体相相对运动。界面湍流混合产生中间温度气体，随后通过辐射冷却并并入冷相。2D 与 3D 版本共享同一物理参数扫描，可用于跨维数迁移。"

---

# 湍流辐射混合层——3D

> **所属数据集：** The Well  
> **数据目录：** `turbulent_radiative_layer_3D`  
> **方程族：** 可压缩流体 + 辐射冷却  
> **文档类型：** 依据官方数据页、论文附录与当前仓库元数据重写的结构化中文文档。

## 1. 所属集合与物理概览

冷而致密的气体相与热而稀薄的气体相相对运动。界面湍流混合产生中间温度气体，随后通过辐射冷却并并入冷相。2D 与 3D 版本共享同一物理参数扫描，可用于跨维数迁移。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。本文始终区分三类信息：方程/生成器理论上可以调整的参数、发布数据中实际扫描的参数，以及该发布版保持固定的参数。

## 2. 控制方程

$$
\frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf v)=0,
$$
$$
\frac{\partial(\rho\mathbf v)}{\partial t}
+\nabla\cdot(\rho\mathbf v\mathbf v+P I)=0,
$$
$$
\frac{\partial E}{\partial t}
+\nabla\cdot[(E+P)\mathbf v]
=-\frac{E}{t_{\rm cool}},
$$
$$
E=\frac{P}{\gamma-1},\qquad \gamma=\frac53.
$$
相应标度关系为
$$
\dot E_{\rm cool}\propto\dot M
\propto v_{\rm rel}^{3/4}t_{\rm cool}^{-1/4}.
$$

### 变量与物理场

- \(\rho,\mathbf v,P,E\)：密度、速度、压强与热能密度。
- \(t_{\rm cool}\)：冷却时间。
- \(v_{\rm rel}\)：两相相对速度。
- \(\dot M\)：热相向冷相的净质量转移率。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 冷却时间/函数、密度和温度反差、相对速度、扰动谱/随机种子、空间维数、区域长宽比、边界条件、状态方程及分辨率。 |
| 数据中实际变化 | 冷却时间 \(t_{\rm cool}\in\{0.03,0.06,0.10,0.18,0.32,0.56,1.00,1.78,3.16\}\)，每个值 10 个随机实现，共 90 条轨迹。 |
| 数据中保持固定 | 状态方程 \(\gamma=5/3\)、冷热两相及相对流动设置、三维几何、发布分辨率、101 个快照和 Athena++ 求解器配置。 |

## 4. 初始条件与边界条件

### 初始条件

冷而致密与热而稀薄两相之间的扰动界面，并指定相对速度；每个冷却时间使用 10 个随机种子。

### 边界条件

采用 Athena++ 设置定义的混合层边界；周期/流出方向应读取 HDF5 元数据确认。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `turbulent_radiative_layer_3D` |
| 空间维数 | 3D |
| 坐标系 | Cartesian $(x,y,z)$ |
| 空间分辨率 | $128\times128\times256$ |
| 每条轨迹存储帧数 | 101 |
| 轨迹数 | 90 |
| 展开后的动态通道数 | 5 |
| 动态物理场 | 密度、压强、速度（3） |
| 静态场/标量上下文 | 冷却时间标签 $t_{\rm cool}$ |
| 时间范围 | nondimensional mixing-layer time |
| 存储时间间隔 | uniform in released trajectories |
| 空间区域 | 3D mixing-layer box |
| 发布数据量 | 745 GB |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,L_3,5)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,L_3,5)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,L_3,5)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** Athena++; compressible finite-volume hydrodynamics with radiative energy sink

Athena++ 使用可压缩有限体积流体求解器并加入辐射能量汇。2D 数据总计约 100 CPU-core-hours，3D 数据约 34,560 CPU-core-hours。两个版本均包含 9 个冷却时间和多次随机实现。

## 7. 推荐机器学习任务与诊断

跨维数迁移、冷却条件预测、多相界面跟踪、质量增长/冷却率统计、长期稳定性以及由 2D 预训练迁移到 3D。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

这是跨维数迁移对中昂贵的 3D 成员。90 条轨迹复用 2D 参数设计，但属于独立维数模拟，不是逐帧精确配对。

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
the-well-download --base-path ./the_well_data --dataset turbulent_radiative_layer_3D --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset turbulent_radiative_layer_3D --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="turbulent_radiative_layer_3D",
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
    well_dataset_name="turbulent_radiative_layer_3D",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。


## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/turbulent_radiative_layer_3D/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/turbulent_radiative_layer_3D> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/turbulent_radiative_layer_3D> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. 引用与来源说明

推荐引用：Fielding 等，*Multiphase Gas and the Fractal Nature of Radiative Turbulent Mixing Layers*（2020）。

同时引用 The Well 总论文：

> Ohana 等，**The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**，NeurIPS 2024 Datasets and Benchmarks。

本文不是官网逐字镜像，而是依据官方数据页、论文附录和当前仓库元数据做的结构化整理、翻译与校勘。英文配套文档是忠实于来源的重新组织版本；中文文档加入了参数层次、通道和输入输出形状等便于多数据集统一管理的信息。
