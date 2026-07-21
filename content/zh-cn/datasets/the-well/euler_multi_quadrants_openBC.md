---
title: "Euler 多象限 Riemann 问题——开边界"
parent_collection: "The Well"
physical_family: "可压缩无黏 Euler 方程"
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,y)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/euler_multi_quadrants_openBC/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/euler_multi_quadrants_openBC"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/euler_multi_quadrants_openBC"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: euler_multi_quadrants_openBC
weight: 80
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "该基准把经典二维四象限 Riemann 问题推广为包含更多初始不连续面的多象限问题。分片常数初态产生激波、稀疏波和接触间断，多象限结构使这些波进一步相互作用。两个可下载目录仅外边界处理不同。"
description: "该基准把经典二维四象限 Riemann 问题推广为包含更多初始不连续面的多象限问题。分片常数初态产生激波、稀疏波和接触间断，多象限结构使这些波进一步相互作用。两个可下载目录仅外边界处理不同。"

---

# Euler 多象限 Riemann 问题——开边界

![密度演化（开边界）](/the-well/euler_multi_quadrants_openBC__density_normalized.gif)


> **所属数据集：** The Well
> **数据目录：** `euler_multi_quadrants_openBC`
> **方程族：** 可压缩无黏 Euler 方程

## 1. 所属集合与物理概览

该基准把经典二维四象限 Riemann 问题推广为包含更多初始不连续面的多象限问题。分片常数初态产生激波、稀疏波和接触间断，多象限结构使这些波进一步相互作用。两个可下载目录仅外边界处理不同。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。

## 2. 控制方程

对守恒状态
$$
U=(\rho,\rho u,\rho v,\rho E)^\top,
$$
积分守恒律为
$$
\frac{d}{dt}\iint_\Omega U\,dA
+\oint_{\partial\Omega}(\mathbf F\,\hat{\mathbf i}+\mathbf G\,\hat{\mathbf j})\cdot\hat{\mathbf n}\,dS=0,
$$
where
$$
\mathbf F=
\begin{pmatrix}
\rho u\\ \rho u^2+p\\ \rho uv\\ u(\rho E+p)
\end{pmatrix},\qquad
\mathbf G=
\begin{pmatrix}
\rho v\\ \rho uv\\ \rho v^2+p\\ v(\rho E+p)
\end{pmatrix},
$$
and
$$
\rho E=\frac{p}{\gamma-1}+\frac12\rho(u^2+v^2).
$$

### 变量与物理场

- \(\rho\)：质量密度。
- \(u,v\)：Cartesian 速度分量。
- \(p\)：压强。
- \(\rho E\)：总能量密度。
- \(\gamma\)：比热比。
- 发布的动量向量场保存 \((\rho u,\rho v)\)。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 绝热指数 \(\gamma\)、各分区分片常数状态 \((\rho,u,v,p)\)、间断面布局、边界类型、区域大小、网格分辨率、Riemann 求解器/限制器和采样间隔。 |
| 数据中实际变化 | 绝热指数扫描为 \(\gamma\in\{1.13,1.22,1.30,1.33,1.365,1.40,1.404,1.453,1.597,1.76\}\)。每个 \(\gamma\) 约生成 500 个随机分片常数多象限初态，因此该边界条件目录共有 5000 条轨迹。 |
| 数据中保持固定 | 网格分辨率、积分时长、守恒变量、方程族，以及由目录名称指定的边界类型。 |

## 4. 初始条件与边界条件

### 初始条件

在多个象限/间断区域中随机设置分片常数密度、速度和压强。具体状态范围与可接受性筛选应以生成器为准。

### 边界条件

外部开边界。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `euler_multi_quadrants_openBC` |
| 空间维数 | 2D |
| 坐标系 | Cartesian $(x,y)$ |
| 空间分辨率 | $512\times512$ |
| 每条轨迹存储帧数 | 100 |
| 轨迹数 | 5000 |
| 展开后的动态通道数 | 5 |
| 动态物理场 | 密度 $\rho$、能量、压强、动量 $(\rho u,\rho v)$ |
| 静态场/标量上下文 | 绝热指数 $\gamma$ 与边界条件元数据 |
| 时间范围 | $[0,1.5]$ |
| 存储时间间隔 | $\approx0.015$ |
| 空间区域 | uniform square grid |
| 发布数据量 | part of 5.17 TB combined Euler release |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,5)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,5)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,5)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** Clawpack; explicit finite-volume hyperbolic solver

Clawpack 使用显式有限体积双曲守恒律方法。初态为随机生成的多象限分片常数状态。论文记录数据以 fp64 生成，总计算约为 160 个 CPU 核上的 80 小时。

## 7. 推荐机器学习任务与诊断

激波感知预测、守恒律学习、对间断的鲁棒性、开边界与周期边界之间的迁移、对 \(\gamma\) 的内插/外推，以及长期 rollout 稳定性。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

论文报告 Euler 总计 10,000 条轨迹；当前仓库按边界条件拆为两个各 5000 条的目录。部分元数据版本可能把包含端点的时间坐标写成 101，而基准表概写 100 步；实际应读取 HDF5 的 `time` 数组。

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
the-well-download --base-path ./the_well_data --dataset euler_multi_quadrants_openBC --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset euler_multi_quadrants_openBC --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="euler_multi_quadrants_openBC",
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
    well_dataset_name="euler_multi_quadrants_openBC",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。

## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/euler_multi_quadrants_openBC/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/euler_multi_quadrants_openBC> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/euler_multi_quadrants_openBC> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |
