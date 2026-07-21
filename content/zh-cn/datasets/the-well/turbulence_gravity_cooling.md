---
title: 湍流—自引力—冷却星际介质
parent_collection: "The Well"
physical_family: 自引力可压缩流体
spatial_dimension: 3D
coordinate_system: "Cartesian $(x,y,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/turbulence_gravity_cooling/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/turbulence_gravity_cooling"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/turbulence_gravity_cooling"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: turbulence_gravity_cooling
weight: 200
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "自引力湍流气体云在可压缩流体动力学、辐射加热/冷却与引力共同作用下演化。初始温度、密度、金属丰度及湍流随机实现覆盖类似银河系、矮星系和原初/绝热环境。"
description: "自引力湍流气体云在可压缩流体动力学、辐射加热/冷却与引力共同作用下演化。初始温度、密度、金属丰度及湍流随机实现覆盖类似银河系、矮星系和原初/绝热环境。"

---

# 湍流—自引力—冷却星际介质

> **所属数据集：** The Well  
> **数据目录：** `turbulence_gravity_cooling`  
> **方程族：** 自引力可压缩流体  
> **文档类型：** 依据官方数据页、论文附录与当前仓库元数据重写的结构化中文文档。

## 1. 所属集合与物理概览

自引力湍流气体云在可压缩流体动力学、辐射加热/冷却与引力共同作用下演化。初始温度、密度、金属丰度及湍流随机实现覆盖类似银河系、矮星系和原初/绝热环境。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。本文始终区分三类信息：方程/生成器理论上可以调整的参数、发布数据中实际扫描的参数，以及该发布版保持固定的参数。

## 2. 控制方程

热力学与 Lagrangian 流体方程同超新星数据属于同一方程族：
$$
P=(\gamma-1)\rho u,\qquad \gamma=\frac53,
$$
$$
\frac{d\rho}{dt}=-\rho\nabla\cdot\mathbf v,
$$
$$
\frac{d^2\mathbf r}{dt^2}
=-\frac{\nabla P}{\rho}+\mathbf a_{\rm visc}-\nabla\Phi,
$$
$$
\frac{du}{dt}
=-\frac{P}{\rho}\nabla\cdot\mathbf v+\frac{\Gamma-\Lambda}{\rho}.
$$

### 变量与物理场

- \(\rho,P,T,u,\mathbf v\)：密度、压强、温度、比内能与速度。
- \(\Phi\)：自引力势。
- \(\Gamma,\Lambda\)：依赖金属丰度的加热/冷却。
- 发布字段为密度、压强、温度和速度；引力及冷却参数属于元数据而非动态输出通道。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 初始温度/密度/金属丰度、气云质量/半径、湍流种子/谱/幅度、冷却加热表、自引力、质量分辨率、状态方程及终止/输出时间。 |
| 数据中实际变化 | 初始温度 \(T_0\in\{10,100,1000\}\) K、氢数密度 \(n_{\rm H}\in\{44.5,4.45,0.445\}\,{\rm cm}^{-3}\)、金属丰度 \(Z\in\{Z_\odot,0.1Z_\odot,0\}\)，每个物理参数组合使用 100 个湍流种子，因此 \(3\times3\times3\times100=2700\) 条轨迹。 |
| 数据中保持固定 | 气云质量 \(10^6M_\odot\)、单原子气体 \(\gamma=5/3\)、湍流谱约定、发布的 \(64^3\) 网格、自引力及 CLOUDY 生成的加热/冷却框架。 |

## 4. 初始条件与边界条件

### 初始条件

球形湍流气云，半径随目标密度调整，随机速度场遵循文档给出的幂律谱。温度、密度、金属丰度与种子共同标记样本。

### 边界条件

采用 ASURA-FDPS 实现的孤立/开放气云盒子与自引力处理；精确边界和网格化写在生成器/发布元数据中。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `turbulence_gravity_cooling` |
| 空间维数 | 3D |
| 坐标系 | Cartesian $(x,y,z)$ |
| 空间分辨率 | $64^3$ |
| 每条轨迹存储帧数 | 50 |
| 轨迹数 | 2700 |
| 展开后的动态通道数 | 6 |
| 动态物理场 | 密度、压强、温度、速度（3） |
| 静态场/标量上下文 | 初始温度、密度、金属丰度与湍流随机种子 |
| 时间范围 | dataset-specific; stored relative to free-fall time |
| 存储时间间隔 | about $0.02$ free-fall time |
| 空间区域 | density-dependent cloud boxes (about 60/129/278 pc) |
| 发布数据量 | 829.4 GB |
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

**文档记录的求解器：** ASURA-FDPS with DISPH, self-gravity and CLOUDY-derived cooling/heating

ASURA-FDPS + DISPH 演化总质量 \(10^6\,M_\odot\) 的湍流气云。初始湍流遵循文档给出的幂律谱，并通过改变气云半径实现三档密度。由 CLOUDY 生成的金属丰度依赖冷却/加热函数覆盖 \(10\)–\(10^9\) K。论文记录总生成约 577 小时。

## 7. 推荐机器学习任务与诊断

丝状结构形成、引力坍缩统计、多参数泛化、冷却区域迁移、长期稳定性、模拟加速及多相星际介质结构的潜表示学习。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

金属丰度主要充当冷却/加热强度轴；文档发布中 \(Z=0\) 实际对应绝热/原初极限。采样间隔相对于自由落体时间表示，因此物理时间依赖密度。

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
the-well-download --base-path ./the_well_data --dataset turbulence_gravity_cooling --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset turbulence_gravity_cooling --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="turbulence_gravity_cooling",
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
    well_dataset_name="turbulence_gravity_cooling",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。


## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/turbulence_gravity_cooling/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/turbulence_gravity_cooling> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/turbulence_gravity_cooling> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. 引用与来源说明

推荐引用：Hirashima 等工作，以及 The Well 附录中的 ASURA-FDPS/CLOUDY 文献。

同时引用 The Well 总论文：

> Ohana 等，**The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**，NeurIPS 2024 Datasets and Benchmarks。

本文不是官网逐字镜像，而是依据官方数据页、论文附录和当前仓库元数据做的结构化整理、翻译与校勘。英文配套文档是忠实于来源的重新组织版本；中文文档加入了参数层次、通道和输入输出形状等便于多数据集统一管理的信息。
