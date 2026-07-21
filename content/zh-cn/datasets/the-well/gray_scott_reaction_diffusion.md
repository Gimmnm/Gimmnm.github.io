---
title: "Gray–Scott 反应扩散"
parent_collection: "The Well"
physical_family: 反应扩散
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,y)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/gray_scott_reaction_diffusion/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/gray_scott_reaction_diffusion"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/gray_scott_reaction_diffusion"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: gray_scott_reaction_diffusion
weight: 100
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "Gray–Scott 模型是两物种耦合反应扩散系统。少量进料率/消除率参数对即可产生性质明显不同的图样族，包括 gliders、bubbles、maze、worms、spirals 与 spots。"
description: "Gray–Scott 模型是两物种耦合反应扩散系统。少量进料率/消除率参数对即可产生性质明显不同的图样族，包括 gliders、bubbles、maze、worms、spirals 与 spots。"

---

# Gray–Scott 反应扩散

![浓度 A](/the-well/gray_scott_reaction_diffusion__concentration_A_normalized.gif)


> **所属数据集：** The Well
> **数据目录：** `gray_scott_reaction_diffusion`
> **方程族：** 反应扩散

## 1. 所属集合与物理概览

Gray–Scott 模型是两物种耦合反应扩散系统。少量进料率/消除率参数对即可产生性质明显不同的图样族，包括 gliders、bubbles、maze、worms、spirals 与 spots。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。

## 2. 控制方程

$$
\frac{\partial A}{\partial t}
=\delta_A\Delta A-AB^2+f(1-A),
$$
$$
\frac{\partial B}{\partial t}
=\delta_B\Delta B+AB^2-(f+k)B.
$$

### 变量与物理场

- \(A,B\)：两种化学物种浓度。
- \(\delta_A,\delta_B\)：扩散常数。
- \(f\)：物种 \(A\) 的进料率。
- \(k\)：物种 \(B\) 的移除/消除率。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 扩散常数、进料率与消除率、区域、边界条件、初始浓度场、扰动尺度、积分时长和采样间隔。 |
| 数据中实际变化 | 六组 \((f,k)\) 产生六类图样：Gliders \((0.014,0.054)\)、Bubbles \((0.098,0.057)\)、Maze \((0.029,0.057)\)、Worms \((0.058,0.065)\)、Spirals \((0.018,0.051)\)、Spots \((0.030,0.062)\)。每组参数有 200 个初态：100 个随机 Fourier 级数场与 100 个随机放置 Gaussian 场。 |
| 数据中保持固定 | \(\delta_A=2\times10^{-5}\)、\(\delta_B=1\times10^{-5}\)；周期区域 \([-1,1]^2\)；\(128^2\) Fourier 表示；内部步长 1 s；每 10 s 输出；总积分 10,000 s。 |

## 4. 初始条件与边界条件

### 初始条件

每个参数区域中均衡使用两类初态：随机 Fourier 级数与随机放置的 Gaussian 扰动。

### 边界条件

两个方向均为周期边界。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `gray_scott_reaction_diffusion` |
| 空间维数 | 2D |
| 坐标系 | Cartesian $(x,y)$ |
| 空间分辨率 | $128\times128$ |
| 每条轨迹存储帧数 | 1001 |
| 轨迹数 | 1200 |
| 展开后的动态通道数 | 2 |
| 动态物理场 | 两种化学物种浓度 $A,B$ |
| 静态场/标量上下文 | 参数对 $(f,k)$ |
| 时间范围 | $[0,10000]$ s |
| 存储时间间隔 | $10$ s between stored snapshots |
| 空间区域 | $[-1,1]^2$, doubly periodic |
| 发布数据量 | 153.8 GB |
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

**文档记录的求解器：** Chebfun Fourier spectral method; ETDRK4; internal step 1 s

系统在双周期区域 \([-1,1]^2\) 上以 Chebfun 的 \(128\times128\) Fourier 表示求解。使用四阶隐显式指数时间差分 Runge–Kutta 方法处理刚性系统；内部步长为 1 s，每 10 步保存一次快照。

## 7. 推荐机器学习任务与诊断

图样区域分类、参数条件预测、长期图样形成、稳态预测，以及向未见 \((f,k)\) 区域外推。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

部分次级文档版本在 \(B\) 方程反应项符号上有排版错误；正确形式按论文附录为 \(+AB^2\)。六组参数各 200 个初态，共 1200 条轨迹。

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
the-well-download --base-path ./the_well_data --dataset gray_scott_reaction_diffusion --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset gray_scott_reaction_diffusion --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="gray_scott_reaction_diffusion",
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
    well_dataset_name="gray_scott_reaction_diffusion",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。

## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/gray_scott_reaction_diffusion/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/gray_scott_reaction_diffusion> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/gray_scott_reaction_diffusion> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |
