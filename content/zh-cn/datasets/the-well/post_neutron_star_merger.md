---
title: 中子星并合后吸积盘
parent_collection: "The Well"
physical_family: "广义相对论 MHD + 中微子输运"
spatial_dimension: 3D
coordinate_system: "quasi-spherical $(\\log r,\\theta,\\phi)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/post_neutron_star_merger/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/post_neutron_star_merger"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/post_neutron_star_merger"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: post_neutron_star_merger
weight: 130
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "该数据模拟双中子星并合后形成的高温吸积盘与外流。理想广义相对论磁流体动力学与电子丰度/轻子数守恒及 Monte Carlo 中微子输运耦合，是 The Well 中计算代价最高的系统之一。"
description: "该数据模拟双中子星并合后形成的高温吸积盘与外流。理想广义相对论磁流体动力学与电子丰度/轻子数守恒及 Monte Carlo 中微子输运耦合，是 The Well 中计算代价最高的系统之一。"

---

# 中子星并合后吸积盘

![电子丰度 Ye](/the-well/post_neutron_star_merger__Ye_good_normalized.gif)


> **所属数据集：** The Well
> **数据目录：** `post_neutron_star_merger`
> **方程族：** 广义相对论 MHD + 中微子输运

## 1. 所属集合与物理概览

该数据模拟双中子星并合后形成的高温吸积盘与外流。理想广义相对论磁流体动力学与电子丰度/轻子数守恒及 Monte Carlo 中微子输运耦合，是 The Well 中计算代价最高的系统之一。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。

## 2. 控制方程

采用论文记号，
$$
\partial_t(\sqrt{g}\,\rho_0 u^t)+\partial_i(\sqrt{g}\,\rho_0 u^i)=0,
$$
$$
\partial_t\big[\sqrt{g}\,(T^t{}_{\nu}+\rho_0 u^t\delta^t{}_{\nu})\big]
+\partial_i\big[\sqrt{g}\,(T^i{}_{\nu}+\rho_0 u^i\delta^t{}_{\nu})\big]
=\sqrt{g}\,(T^\kappa{}_{\lambda}\Gamma^\lambda{}_{\nu\kappa}+G_\nu),
$$
$$
\partial_t(\sqrt{g}\,B^i)
+\partial_j\big[\sqrt{g}\,(b^j u^i-b^i u^j)\big]=0,
$$
$$
\partial_t(\sqrt{g}\,\rho_0 Y_e u^t)
+\partial_i(\sqrt{g}\,\rho_0 Y_e u^i)=\sqrt{g}\,G_{Y_e},
$$
中微子强度沿零测地线满足相对论输运方程：
$$
\frac{D}{d\lambda}\Bigl(\frac{h^3 I_{\nu,f}}{\epsilon^3}\Bigr)=\frac{h^2\eta_{\nu,f}}{\epsilon^2}-\frac{\epsilon\chi_{\nu,f}}{h}\Bigl(\frac{h^3 I_{\nu,f}}{\epsilon^3}\Bigr).
$$

### 变量与物理场

- \(\rho_0,u^\mu,T^\mu{}_{\nu}\)：静质量密度、流体四速度与应力—能量张量。
- \(\sqrt{g}\)：时空度规行列式绝对值的平方根（体积因子）；\(\Gamma^\lambda{}_{\mu\nu}\)：Christoffel 符号。
- \(B^i,b^\mu\)：磁场三向量/四向量。
- \(Y_e\)：电子丰度。
- \(G_\nu,G_{Y_e}\)：辐射四力与轻子交换源项。
- \(I_{\nu,f},\eta_{\nu,f},\chi_{\nu,f}\)：各味中微子强度、发射率与不透明度。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 黑洞质量/自旋、环面质量与角动量、内半径和最大压强半径、熵、电子丰度、密度标度、等离子体 \(\beta\)、磁场拓扑、核物质状态方程、中微子不透明度表及网格分辨率。 |
| 数据中实际变化 | 8 条模拟之间可改变黑洞自旋 \(a\in[0,1]\)、黑洞质量、环面质量/角动量、无量纲内半径 \(R_{\rm in}\)、最大压强半径 \(R_{\max}\)、初始电子丰度 \(Y_e\)、熵、密度标度及等离子体 \(\beta\)。论文没有公开完整的 8 行参数表，不应猜测缺失数值。 |
| 数据中保持固定 | SFHo 有限温核物质状态方程；Fornax 中微子不透明度；理想 GRMHD 假设；\(\nu\)bhlight 数值框架；各运行的度规/网格约定；发布张量分辨率。 |

## 4. 初始条件与边界条件

### 初始条件

由 `torus_cbc` 在旋转黑洞周围构造静水平衡环面，并指定弱磁场及热力学/组分参数。

### 边界条件

内区采用 horizon-penetrating 几何、外区为准球面区域；具体流入/流出及人工大气处理遵循 \(\nu\)bhlight 生成代码和所引用的 drift-frame 方法。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `post_neutron_star_merger` |
| 空间维数 | 3D |
| 坐标系 | quasi-spherical $(\log r,\theta,\phi)$ |
| 空间分辨率 | $192\times128\times66$ |
| 每条轨迹存储帧数 | 181 |
| 轨迹数 | 8 |
| 展开后的动态通道数 | 12 |
| 动态物理场 | 密度、内能、压强、温度、电子丰度、熵、速度（3）、磁场（3） |
| 静态场/标量上下文 | 逆变时空度规张量 |
| 时间范围 | simulation-specific relativistic time |
| 存储时间间隔 | uniform in released sequence |
| 空间区域 | horizon-penetrating quasi-spherical grid around a rotating black hole |
| 发布数据量 | 110.1 GB |
| 存储格式 | HDF5；The Well 统一 schema；发布数组为 fp32 |
| 默认划分口径 | 通常按轨迹/初态作 80/10/10 划分；轨迹很少的数据可能采用不重叠时间块。应检查下载文件元数据。 |

### 原始形状与模型输入输出

原始 HDF5 把标量、向量和张量场分别存储。典型动态标量场的概念形状为

\[
(N_{\rm traj},N_t,L_1,L_2[,L_3]),
\]

向量/张量场在末尾继续增加分量轴。`WellDataset` 可把所有动态物理分量展平到最后一个通道轴。批量大小为 \(B\) 时，本目录可概念性表示为：

- 完整序列：\((B,T,L_1,L_2,L_3,12)\)；
- 标准 4 帧历史输入：\((B,4,L_1,L_2,L_3,12)\)；
- 标准 1 帧预测目标：\((B,1,L_1,L_2,L_3,12)\)。

字段和分量的精确顺序必须读取 HDF5 元数据，不能只依赖本文列举顺序。静态几何/系数场通常作为模型输入，但不应作为时间预测目标。

## 6. 数值生成方法

**文档记录的求解器：** $\nu$bhlight: finite-volume GRMHD + constrained transport + Monte Carlo neutrino transport

\(\nu\)bhlight 采用有限体积 GRMHD、约束输运和 Monte Carlo 中微子辐射，并以一阶算子分裂耦合。网格在 horizon-penetrating 坐标中为径向对数的准球面网格。文档设置使用 SFHo 核物质状态方程与 Fornax 不透明度表。单条模拟约需 300 个 CPU 核运行三周。

## 7. 推荐机器学习任务与诊断

极高代价模拟加速、耦合多场预测、电子丰度跟踪、稳定相对论 rollout、跨黑洞/环面参数迁移以及中微子—MHD 相互作用降阶建模。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

仅有 8 条轨迹，划分可能采用时间块或谨慎分配，而不能视作参数空间充分的轨迹级随机划分。度规张量不随时间变化，通常应作为几何/上下文输入，而非预测目标。

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
the-well-download --base-path ./the_well_data --dataset post_neutron_star_merger --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset post_neutron_star_merger --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="post_neutron_star_merger",
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
    well_dataset_name="post_neutron_star_merger",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。

## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/post_neutron_star_merger/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/post_neutron_star_merger> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/post_neutron_star_merger> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |
