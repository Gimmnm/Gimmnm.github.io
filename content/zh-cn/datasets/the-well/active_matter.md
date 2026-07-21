---
title: 活性物质
parent_collection: "The Well"
physical_family: 活性流体动理学
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,y)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/active_matter/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/active_matter"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/active_matter"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: active_matter
weight: 60
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: '该数据使用连续介质动理学模型描述浸没在黏性 Stokes 流体中的细长活性粒子。求解器演化高维取向分布 \(\Psi(\mathbf x,\mathbf p,t)\)，而发布数据保存浓度、取向、速度和应变等低阶矩。'
description: '该数据使用连续介质动理学模型描述浸没在黏性 Stokes 流体中的细长活性粒子。求解器演化高维取向分布 \(\Psi(\mathbf x,\mathbf p,t)\)，而发布数据保存浓度、取向、速度和应变等低阶矩。'

---

# 活性物质

![浓度场](/the-well/active_matter__concentration_notnormalized.gif)


> **所属数据集：** The Well
> **数据目录：** `active_matter`
> **方程族：** 活性流体动理学

## 1. 所属集合与物理概览

该数据使用连续介质动理学模型描述浸没在黏性 Stokes 流体中的细长活性粒子。求解器演化高维取向分布 \(\Psi(\mathbf x,\mathbf p,t)\)，而发布数据保存浓度、取向、速度和应变等低阶矩。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。

## 2. 控制方程

Smoluchowski 方程为
$$
\frac{\partial\Psi}{\partial t}
+\nabla_{\mathbf x}\!\cdot(\dot{\mathbf x}\Psi)
+\nabla_{\mathbf p}\!\cdot(\dot{\mathbf p}\Psi)=0,
$$
其中构象通量为
$$
\dot{\mathbf x}=\mathbf u-d_T\nabla_{\mathbf x}\log\Psi,\qquad
\dot{\mathbf p}=(I-\mathbf p\mathbf p)\cdot(\nabla\mathbf u+2\zeta D)\cdot\mathbf p
-d_R\nabla_{\mathbf p}\log\Psi.
$$
并与不可压缩 Stokes 流耦合：
$$
-\Delta\mathbf u+\nabla P=\nabla\cdot\Sigma,\qquad \nabla\cdot\mathbf u=0,
$$
with
$$
\Sigma=\alpha D+\beta\,S:E-2\zeta\beta(D\cdot D-S:D).
$$

### 变量与物理场

- \(\Psi(\mathbf x,\mathbf p,t)\)：位置—取向空间中的粒子分布。
- \(c=\langle1
angle\)：浓度。
- \(D=\langle\mathbf p\mathbf p
angle\)：二阶取向矩；发布的取向张量按生成器约定归一化。
- \(S=\langle\mathbf p\mathbf p\mathbf p\mathbf p
angle\)：四阶取向矩。
- \(\mathbf u,P,E\)：流体速度、压强与应变率张量。
- \(\alpha\)：活性偶极强度；\(\beta\)：密度/刚性参数；\(\zeta\)：空间位阻取向强度；\(d_T,d_R\)：扩散系数。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 活性强度 \(\alpha\)、取向耦合 \(\zeta\)、密度参数 \(\beta\)、平移/转动扩散 \(d_T,d_R\)、区域大小、空间/取向模态数、初始分布与外部驱动。 |
| 数据中实际变化 | 发布参数网格为 \(\alpha\in\{-1,-2,-3,-4,-5\}\)、\(\zeta\in\{1,3,5,7,9,11,13,15,17\}\)，并对每个参数对使用多个初态。当前文档与参数笛卡尔积表明每对 5 个初态，因此共有 \(5\times9\times5=225\) 条轨迹。 |
| 数据中保持固定 | \(\beta=0.8\)；周期正方形 \(L=10\)；空间与取向分辨率；生成器中的平移/转动扩散及积分配置；81 个存储快照。 |

## 4. 初始条件与边界条件

### 初始条件

当前发布组织中，每个 \((\alpha,\zeta)\) 参数对使用 5 个初始实现。若需逐位复现，应以生成代码中的随机场构造为准。

### 边界条件

两个空间方向均为周期边界。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `active_matter` |
| 空间维数 | 2D |
| 坐标系 | Cartesian $(x,y)$ |
| 空间分辨率 | $256\times256$ |
| 每条轨迹存储帧数 | 81 |
| 轨迹数 | 225 (current parameter product; paper table reports 360) |
| 展开后的动态通道数 | 11 |
| 动态物理场 | 浓度（1）、速度（2）、取向张量（4）、应变率张量（4） |
| 静态场/标量上下文 | 默认动态目标无额外静态场；物理参数作为标量元数据 |
| 时间范围 | $[0,20]$ |
| 存储时间间隔 | $0.25$ |
| 空间区域 | periodic square, side length $L=10$ |
| 发布数据量 | 51.3 GB |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,11)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,11)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,11)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** Fourier pseudo-spectral discretization in space/orientation; SBDF2, internal $\Delta t\approx4\times10^{-4}$

在物理空间和取向空间都使用 Fourier 伪谱微分；SBDF2 对线性项隐式、非线性项显式处理。区域为边长 \(L=10\) 的周期正方形，两个空间方向各 256 个模态，并使用 256 个取向模态。论文记录单次运行约需 A100 80 GB GPU 20 分钟，生成精度为 fp64。

## 7. 推荐机器学习任务与诊断

矩闭合学习、活性湍流长期预测、对 \(\alpha,\zeta\) 的参数内插/外推，以及在不显式解析完整取向分布的情况下学习稳定低阶动力学。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

论文表格报告 360 条轨迹，而当前官方参数笛卡尔积得到 225 条。本文同时保留两者，并把 225 作为现行目录口径；实际实验应检查下载 HDF5 的元数据。

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
the-well-download --base-path ./the_well_data --dataset active_matter --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset active_matter --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="active_matter",
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
    well_dataset_name="active_matter",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。

## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/active_matter/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/active_matter> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/active_matter> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |
