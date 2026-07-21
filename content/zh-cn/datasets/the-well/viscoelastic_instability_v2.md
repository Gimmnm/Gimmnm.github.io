---
title: "黏弹性不稳定性——修正版 v2"
parent_collection: "The Well"
physical_family: "FENE-P 黏弹性流"
spatial_dimension: 2D
coordinate_system: "Cartesian streamwise/wall-normal coordinates"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: ""
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/viscoelastic_instability_v2"
huggingface_dataset: ""
paper: "https://arxiv.org/abs/2412.00568"
status: active-corrected
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: viscoelastic_instability_v2
weight: 240
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "二维 FENE-P 通道流存在多个共存吸引子：层流、稳态/混沌箭头态、弹性—惯性湍流，以及分隔不同吸引域的 edge states。旧版处理数据已弃用；新研究应优先使用修正后的 `viscoelastic_instability_v2`。"
description: "二维 FENE-P 通道流存在多个共存吸引子：层流、稳态/混沌箭头态、弹性—惯性湍流，以及分隔不同吸引域的 edge states。旧版处理数据已弃用；新研究应优先使用修正后的 `viscoelastic_instability_v2`。"

---

# 黏弹性不稳定性——修正版 v2

> **所属数据集：** The Well  
> **数据目录：** `viscoelastic_instability_v2`  
> **方程族：** FENE-P 黏弹性流  
> **文档类型：** 依据官方数据页、论文附录与当前仓库元数据重写的结构化中文文档。

## 1. 所属集合与物理概览

二维 FENE-P 通道流存在多个共存吸引子：层流、稳态/混沌箭头态、弹性—惯性湍流，以及分隔不同吸引域的 edge states。旧版处理数据已弃用；新研究应优先使用修正后的 `viscoelastic_instability_v2`。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。本文始终区分三类信息：方程/生成器理论上可以调整的参数、发布数据中实际扫描的参数，以及该发布版保持固定的参数。

## 2. 控制方程

$$
\mathrm{Re}\left(\frac{\partial\mathbf u}{\partial t}
+\mathbf u\cdot\nabla\mathbf u\right)+\nabla p
=\beta\Delta\mathbf u+(1-\beta)\nabla\cdot T(C),
$$
$$
\nabla\cdot\mathbf u=0,
$$
$$
T(C)=\frac1{\mathrm{Wi}}
\left[
\frac{C}{1-(\operatorname{tr}C-3)/L_{\max}^2}-I
\right],
$$
$$
\frac{\partial C}{\partial t}
+(\mathbf u\cdot\nabla)C+T(C)
=C\cdot\nabla\mathbf u+(\nabla\mathbf u)^\top\cdot C+\epsilon\Delta C.
$$

### 变量与物理场

- \(\mathbf u=(u,v)\)、\(p\)：速度与压强。
- \(C\)：聚合物构象张量。
- \(T(C)\)：FENE-P 聚合物应力。
- \(\mathrm{Re}\)：Reynolds 数。
- \(\mathrm{Wi}\)：Weissenberg 数。
- \(\beta=\nu_s/\nu\)：溶剂黏度占总黏度比例。
- \(\epsilon\)：无量纲聚合物应力扩散率。
- \(L_{\max}\)：聚合物最大伸长。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | Reynolds/Weissenberg 数、黏度比、最大伸长、应力扩散率、压强梯度/流量、通道尺寸、扰动及吸引子/edge-state 初态、空间分辨率与采样窗口。 |
| 数据中实际变化 | 物理系数没有扫描：\(\mathrm{Re}=1000\)、\(\mathrm{Wi}=50\)、\(\beta=0.9\)、\(\epsilon=2\times10^{-6}\)、\(L_{\max}=70\)。变化来自动力学状态与初态：层流、稳态箭头态（SAR）、混沌箭头态（CAR）、弹性—惯性湍流（EIT）以及两类 edge state。 |
| 数据中保持固定 | 上述全部 FENE-P 系数、通道几何、流向周期性、无滑移壁面、分辨率及底层 Dedalus 模拟。 |

## 4. 初始条件与边界条件

### 初始条件

从各命名吸引子采样或与其相容的状态。Edge states 通过在通向不同吸引子的初态之间进行二分搜索获得。

### 边界条件

流向周期；两平行壁面速度为零（无滑移）。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `viscoelastic_instability_v2` |
| 空间维数 | 2D |
| 坐标系 | Cartesian streamwise/wall-normal coordinates |
| 空间分辨率 | $512\times512$ |
| 每条轨迹存储帧数 | 20 or 60 depending on attractor/segment |
| 轨迹数 | 260 |
| 展开后的动态通道数 | 8 |
| 动态物理场 | 压强；速度（2）；构象张量分量 $C_{xx},C_{xy},C_{yx},C_{yy},C_{zz}$ |
| 静态场/标量上下文 | 固定 FENE-P 无量纲参数与吸引子标签 |
| 时间范围 | segment-dependent |
| 存储时间间隔 | uniform within each segment |
| 空间区域 | channel; periodic streamwise, no-slip walls |
| 发布数据量 | approximately 66 GB; not separately tabulated in the paper |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,8)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,8)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,8)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** Dedalus DNS; corrected extraction/processing of the same simulations

Dedalus 在两平行壁面之间进行直接数值模拟，流向周期、壁面无滑移。Edge states 通过对通向不同吸引子的初态做二分搜索获得。论文记录约 32/64 核运行一天得到约 50 帧，整个生成过程约三个月。

## 7. 推荐机器学习任务与诊断

吸引子分类、转捩/edge-state 预测、多稳态、稀有事件预测、长期混沌动力学，以及正定张量场学习。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

对同一批底层物理模拟进行修正后的处理，新实验应优先使用本目录。它存在于仓库，但尚无独立官网页面，也未列入常见 Hugging Face 流式入口。

当前仓库状态： **active-corrected**。本文核对日期为 2026-07-21。实际实验必须检查 `dataset_name.yaml`、`stats.yaml`、HDF5 坐标及 release notes，以确定所用文件的精确版本。

## 下载与读取

### 安装接口

```bash
python -m venv .venv
source .venv/bin/activate
pip install the_well
```

### 下载一个划分

```bash
the-well-download --base-path ./the_well_data --dataset viscoelastic_instability_v2 --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset viscoelastic_instability_v2 --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="viscoelastic_instability_v2",
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
| 官方数据页 | No separate page / 尚无独立页面 |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/viscoelastic_instability_v2> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |

## 10. 引用与来源说明

推荐引用：Beneitez 等，*Multistability of elasto-inertial two-dimensional channel flow*（2024）。

同时引用 The Well 总论文：

> Ohana 等，**The Well: a Large-Scale Collection of Diverse Physics Simulations for Machine Learning**，NeurIPS 2024 Datasets and Benchmarks。

本文不是官网逐字镜像，而是依据官方数据页、论文附录和当前仓库元数据做的结构化整理、翻译与校勘。英文配套文档是忠实于来源的重新组织版本；中文文档加入了参数层次、通道和输入输出形状等便于多数据集统一管理的信息。
