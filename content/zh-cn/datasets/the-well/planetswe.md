---
title: 行星球面浅水方程
parent_collection: "The Well"
physical_family: 旋转球面浅水方程
spatial_dimension: "2D on sphere"
coordinate_system: "spherical angular grid $(\\\\theta,\\\\phi)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/planetswe/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/planetswe"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/planetswe"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: planetswe
weight: 120
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "该数据在球面上求解旋转、受迫、超黏浅水方程，用于近似单一大气压力层。初态来自 ERA5 的 500 hPa 场，并加入真实地球地形以及具有日周期和年周期的人工外力，从而包含地理和季节结构。"
description: "该数据在球面上求解旋转、受迫、超黏浅水方程，用于近似单一大气压力层。初态来自 ERA5 的 500 hPa 场，并加入真实地球地形以及具有日周期和年周期的人工外力，从而包含地理和季节结构。"

---

# 行星球面浅水方程

![浅水演化](/the-well/planetswe__planetswe.gif)


> **所属数据集：** The Well
> **数据目录：** `planetswe`
> **方程族：** 旋转球面浅水方程

## 1. 所属集合与物理概览

该数据在球面上求解旋转、受迫、超黏浅水方程，用于近似单一大气压力层。初态来自 ERA5 的 500 hPa 场，并加入真实地球地形以及具有日周期和年周期的人工外力，从而包含地理和季节结构。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。

## 2. 控制方程

$$
\frac{\partial\mathbf u}{\partial t}
=-\mathbf u\cdot\nabla\mathbf u-g\nabla h
-\nu\nabla^4\mathbf u-2\boldsymbol\Omega\times\mathbf u,
$$
$$
\frac{\partial h}{\partial t}
=-H\nabla\cdot\mathbf u-\nabla\cdot(h\mathbf u)
-\nu\nabla^4 h+F(\theta,\phi,t).
$$

### 变量与物理场

- \(\mathbf u\)：球面上的深度平均水平速度。
- \(h\)：压力面/自由表面高度扰动。
- \(H\)：参考层厚度。
- \(g\)：重力加速度。
- \(\boldsymbol\Omega\)：行星自转向量。
- \(\nu=1.76\times10^{-10}\)：文档设置中的固定超黏系数。
- \(F\)：具有模型日周期与模型年周期的外力。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 行星半径/自转、重力、参考层厚度、地形、超黏系数、外力幅度/季节性、初始大气状态、谱分辨率与输出间隔。 |
| 数据中实际变化 | 物理运行之间仅初始大气状态变化。40 个来自 ERA5 并经过平衡调整的初态各模拟三个模型年；机器学习存储时，每条三年运行切成三条一年轨迹，因此得到 120 条、每条 1008 个小时快照。 |
| 数据中保持固定 | 地球地形、行星几何/自转与重力、\(\nu=1.76\times10^{-10}\)、日/年周期外力定义、数值分辨率、小时输出间隔及 burn-in 流程。 |

## 4. 初始条件与边界条件

### 初始条件

把 ERA5 500 hPa 的 \(u,v,z\) 场映射为浅水状态，经过多次短积分/投影趋向平衡，并 burn-in 半个模型年后开始记录。

### 边界条件

全球球面，无物理侧边界；经度周期，极点正则性由球谐谱基处理。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `planetswe` |
| 空间维数 | 2D on sphere |
| 坐标系 | spherical angular grid $(\theta,\phi)$ |
| 空间分辨率 | $256\times512$ |
| 每条轨迹存储帧数 | 1008 |
| 轨迹数 | 120 ML trajectories (from 40 three-year simulations) |
| 展开后的动态通道数 | 3 |
| 动态物理场 | 自由表面高度 $h$ 与水平速度（2） |
| 静态场/标量上下文 | 地球地形/水深及外力定义 |
| 时间范围 | one model year per stored ML trajectory |
| 存储时间间隔 | one model hour |
| 空间区域 | global sphere |
| 发布数据量 | 185.8 GB |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,3)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,3)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,3)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** Dedalus spin-weighted spherical harmonics; 3/2 anti-aliasing; second-order IMEX RK

Dedalus 采用 spin-weighted 球谐方法，并以 3/2 超采样进行抗混叠。ERA5 初态先通过短积分和投影反复调整到较平衡状态，再 burn-in 半个模型年；之后记录三个模型年，每个模型小时保存一次。发布的机器学习数据把每条三年物理模拟切成三条一年轨迹。

## 7. 推荐机器学习任务与诊断

稳定的多年预测、球面算子学习、守恒量与气候统计评估、跨 ERA5 初态迁移，以及地形/外力条件预测。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

不要把 40 条求解器运行与 120 条发布 ML 轨迹混淆。时间单位是模型定义的“日/年”，并非严格校准到物理时间。地形是静态模型输入，而非动态预测目标。

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
the-well-download --base-path ./the_well_data --dataset planetswe --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset planetswe --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="planetswe",
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
    well_dataset_name="planetswe",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。

## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/planetswe/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/planetswe> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/planetswe> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |
