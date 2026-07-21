---
title: 磁流体湍流——$64^3$
parent_collection: "The Well"
physical_family: 理想等温磁流体动力学
spatial_dimension: 3D
coordinate_system: "Cartesian $(x,y,z)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/MHD_64/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/MHD_64"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/MHD_64"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: MHD_64
weight: 20
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: '该数据模拟受大尺度随机驱动的等温、无自引力磁流体湍流，具有尺度自由性质。声速马赫数和 Alfvén 马赫数覆盖亚声速/超声速以及强磁场/弱磁场区域。配对的 \(256^3\) 与抗混叠 \(64^3\) 数据同时支持动力学预测和超分辨率研究。'
description: '该数据模拟受大尺度随机驱动的等温、无自引力磁流体湍流，具有尺度自由性质。声速马赫数和 Alfvén 马赫数覆盖亚声速/超声速以及强磁场/弱磁场区域。配对的 \(256^3\) 与抗混叠 \(64^3\) 数据同时支持动力学预测和超分辨率研究。'

---

# 磁流体湍流——$64^3$

> **所属数据集：** The Well  
> **数据目录：** `MHD_64`  
> **方程族：** 理想等温磁流体动力学  
> **文档类型：** 依据官方数据页、论文附录与当前仓库元数据重写的结构化中文文档。

## 1. 所属集合与物理概览

该数据模拟受大尺度随机驱动的等温、无自引力磁流体湍流，具有尺度自由性质。声速马赫数和 Alfvén 马赫数覆盖亚声速/超声速以及强磁场/弱磁场区域。配对的 \(256^3\) 与抗混叠 \(64^3\) 数据同时支持动力学预测和超分辨率研究。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。本文始终区分三类信息：方程/生成器理论上可以调整的参数、发布数据中实际扫描的参数，以及该发布版保持固定的参数。

## 2. 控制方程

$$
\frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf v)=0,
$$
$$
\frac{\partial(\rho\mathbf v)}{\partial t}
+\nabla\cdot\left[
\rho\mathbf v\mathbf v+
\left(p+\frac{B^2}{8\pi}\right)I-\frac{\mathbf B\mathbf B}{4\pi}
\right]=\mathbf f,
$$
$$
\frac{\partial\mathbf B}{\partial t}
-\nabla\times(\mathbf v\times\mathbf B)=0,
\qquad p=c_s^2\rho.
$$

### 变量与物理场

- \(\rho\)：密度。
- \(\mathbf v\)：速度。
- \(\mathbf B\)：磁场。
- \(p=c_s^2\rho\)：等温状态方程给出的压强。
- \(\mathbf f\)：波数约 \(k\approx2.5\) 的大尺度无散驱动。
- \(M_s=|\mathbf v|/c_s\)：声速马赫数。
- \(M_A=|\mathbf v|/\langle v_A\rangle\)：Alfvén 马赫数。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 声速/Alfvén 马赫数、驱动幅度/谱/相关时间、声速、平均磁场、初始扰动、自引力、状态方程、盒子物理尺度与分辨率。 |
| 数据中实际变化 | 声速马赫数 \(M_s\in\{0.5,0.7,1.5,2.0,7.0\}\)，Alfvén 马赫数 \(M_A\in\{0.7,2.0\}\)。每个参数对有 10 个实现，共 \(5\times2\times10=100\) 条轨迹。 |
| 数据中保持固定 | 周期立方体；等温状态方程；无自引力；在 \(k\approx2.5\) 附近连续施加大尺度无散驱动；100 个输出帧；代码单位归一化。 |

## 4. 初始条件与边界条件

### 初始条件

每个 \((M_s,M_A)\) 参数对包含不同湍流随机实现/驱动相位。超 Alfvén 情形的初始 \(M_A\) 可更大（文档为 7），小尺度发电机饱和后落到标注的最终区域 \(M_A\approx2\)。

### 边界条件

三个空间方向均为周期边界。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `MHD_64` |
| 空间维数 | 3D |
| 坐标系 | Cartesian $(x,y,z)$ |
| 空间分辨率 | $64^3$ |
| 每条轨迹存储帧数 | 100 |
| 轨迹数 | 100 |
| 展开后的动态通道数 | 7 |
| 动态物理场 | 密度（1）、速度（3）、磁场（3） |
| 静态场/标量上下文 | 马赫数标签与驱动配置 |
| 时间范围 | $[0,1]$ (code units) |
| 存储时间间隔 | $\approx0.01$ |
| 空间区域 | periodic cube |
| 发布数据量 | 71.6 GB |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,L_3,7)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,L_3,7)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,L_3,7)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** third-order hybrid ENO ideal-MHD solver; anti-aliased low-pass downsampling from $256^3$

采用三阶 hybrid ENO 格式在周期立方体的 \(256^3\) 网格上求解理想 MHD。\(64^3\) 版本先对高分辨率轨迹做理想低通滤波，再进行抗混叠降采样。论文记录单条高分辨率模拟在 64 个 CPU 核上约需 48 h。

## 7. 推荐机器学习任务与诊断

三维湍流预测、跨马赫数泛化、磁场约束的守恒学习、谱诊断、\(64^3\!\to256^3\) 超分辨率及跨分辨率迁移。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

这是与 `MHD_256` 配对的抗混叠低分辨率表示，适合作为超分辨率实验的低分辨率输入/目标。

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
the-well-download --base-path ./the_well_data --dataset MHD_64 --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset MHD_64 --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="MHD_64",
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
    well_dataset_name="MHD_64",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。


## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/MHD_64/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/MHD_64> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/MHD_64> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. 引用与来源说明

推荐同时引用 The Well 附录中列出的 MHD 模拟与 CATS 数据库文献。

同时引用 The Well 总论文：

> Ohana 等，**The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**，NeurIPS 2024 Datasets and Benchmarks。

本文不是官网逐字镜像，而是依据官方数据页、论文附录和当前仓库元数据做的结构化整理、翻译与校勘。英文配套文档是忠实于来源的重新组织版本；中文文档加入了参数层次、通道和输入输出形状等便于多数据集统一管理的信息。
