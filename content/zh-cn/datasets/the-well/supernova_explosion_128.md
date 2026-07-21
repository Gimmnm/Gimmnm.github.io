---
title: 超新星爆炸——$128^3$
parent_collection: "The Well"
physical_family: "可压缩 SPH 流体 + 冷却"
spatial_dimension: 3D
coordinate_system: "Cartesian $(x,y,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/supernova_explosion_128/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/supernova_explosion_128"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/supernova_explosion_128"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: supernova_explosion_128
weight: 180
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "超新星在具有湍流结构和辐射冷却的星际介质中注入能量，爆炸波在致密丝状结构中各向异性传播。数据提供两种空间分辨率，但轨迹数不同，因此不能默认全部轨迹都能一一配对。"
description: "超新星在具有湍流结构和辐射冷却的星际介质中注入能量，爆炸波在致密丝状结构中各向异性传播。数据提供两种空间分辨率，但轨迹数不同，因此不能默认全部轨迹都能一一配对。"

---

# 超新星爆炸——$128^3$

> **所属数据集：** The Well  
> **数据目录：** `supernova_explosion_128`  
> **方程族：** 可压缩 SPH 流体 + 冷却  
> **文档类型：** 依据官方数据页、论文附录与当前仓库元数据重写的结构化中文文档。

## 1. 所属集合与物理概览

超新星在具有湍流结构和辐射冷却的星际介质中注入能量，爆炸波在致密丝状结构中各向异性传播。数据提供两种空间分辨率，但轨迹数不同，因此不能默认全部轨迹都能一一配对。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。本文始终区分三类信息：方程/生成器理论上可以调整的参数、发布数据中实际扫描的参数，以及该发布版保持固定的参数。

## 2. 控制方程

对单原子理想气体， \(\gamma=5/3\),
$$
P=(\gamma-1)\rho u.
$$
附录使用的 Lagrangian 形式为
$$
\frac{d\rho}{dt}=-\rho\nabla\cdot\mathbf v,
$$
$$
\frac{d^2\mathbf r}{dt^2}
=-\frac{\nabla P}{\rho}+\mathbf a_{\rm visc}-\nabla\Phi,
$$
$$
\frac{du}{dt}
=-\frac{P}{\rho}\nabla\cdot\mathbf v
+\frac{\Gamma-\Lambda}{\rho}.
$$
作为比较，球对称 Sedov 标度为
$$
R(t)=\xi\left(\frac{E}{\rho}\right)^{1/5}t^{2/5}.
$$

### 变量与物理场

- \(\rho,P,u,\mathbf v,\mathbf r\)：密度、压强、比内能、速度与位置。
- \(\Phi\)：引力势。
- \(\mathbf a_{\rm visc}\)：SPH 形式中的数值/物理黏性加速度。
- \(\Gamma,\Lambda\)：单位体积辐射加热与冷却。
- \(E\)：超新星注入能量。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 爆炸能量/位置、环境密度/温度/金属丰度、湍流实现与谱、冷却/加热函数、引力、质量/空间分辨率、盒子大小和输出间隔。 |
| 数据中实际变化 | 发布活动改变环境湍流随机实现以及分辨率对应的样本成员。在 \(128^3\) 分辨率下有 260 条轨迹。 论文明确给出的物理设置固定为：初始温度 \(T_0=100\) K、氢数密度 \(n_{\rm H}=44.5\,{\rm cm}^{-3}\)、太阳金属丰度 \(Z=Z_\odot\)，以及标准超新星能量尺度。 |
| 数据中保持固定 | 单原子理想气体 \(\gamma=5/3\)、上述环境热力学参数、冷却模型/金属丰度、超新星能量注入约定、59 帧输出长度，以及本目录指定的分辨率。 |

## 4. 初始条件与边界条件

### 初始条件

在湍流、丝状星际介质实现中局部注入超新星热能。精确湍流种子与爆炸位置属于样本元数据。

### 边界条件

采用 ASURA-FDPS 模拟定义的开放/流出型盒子处理；粒子到网格的精确后处理应查生成器元数据。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `supernova_explosion_128` |
| 空间维数 | 3D |
| 坐标系 | Cartesian $(x,y,z)$ |
| 空间分辨率 | $128^3$ |
| 每条轨迹存储帧数 | 59 |
| 轨迹数 | 260 |
| 展开后的动态通道数 | 6 |
| 动态物理场 | 密度、压强、温度、速度（3） |
| 静态场/标量上下文 | 固定环境热力学/金属丰度设置及实现元数据 |
| 时间范围 | approximately $0$–$0.2$ Myr |
| 存储时间间隔 | uniform in released trajectory |
| 空间区域 | approximately 60 pc box |
| 发布数据量 | 754 GB |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,L_3,6)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,L_3,6)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,L_3,6)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** ASURA-FDPS N-body/SPH with density-independent SPH (DISPH)

ASURA-FDPS 使用 N-body/SPH，并采用 density-independent SPH（DISPH）改善接触间断与激波处理。发布的超新星设置使用太阳金属丰度。两种分辨率的总生成代价均为数千 CPU 小时，最高并行到 1040 核。

## 7. 推荐机器学习任务与诊断

爆炸波预测、激波/壳层保持、各向异性膨胀、跨分辨率迁移、超分辨率、形态/统计量预测以及星系尺度子网格模型加速。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

高分辨率集合远小于 \(64^3\) 集合。跨分辨率实验应在可用时显式匹配轨迹标识，而不能按行号配对。

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
the-well-download --base-path ./the_well_data --dataset supernova_explosion_128 --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset supernova_explosion_128 --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="supernova_explosion_128",
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
    well_dataset_name="supernova_explosion_128",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。


## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/supernova_explosion_128/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/supernova_explosion_128> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/supernova_explosion_128> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. 引用与来源说明

推荐引用 The Well 列出的 Hirashima 等超新星代理模型论文及 ASURA-FDPS/DISPH 文献。

同时引用 The Well 总论文：

> Ohana 等，**The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**，NeurIPS 2024 Datasets and Benchmarks。

本文不是官网逐字镜像，而是依据官方数据页、论文附录和当前仓库元数据做的结构化整理、翻译与校勘。英文配套文档是忠实于来源的重新组织版本；中文文档加入了参数层次、通道和输入输出形状等便于多数据集统一管理的信息。
