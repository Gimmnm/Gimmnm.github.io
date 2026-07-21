---
title: 声学散射——单一不连续界面
parent_collection: "The Well"
physical_family: 变系数声学
spatial_dimension: 2D
coordinate_system: "Cartesian $(x,y)$"
storage_format: "HDF5 / The Well unified schema / fp32 release arrays"
dataset_license: CC-BY-4.0
code_license: BSD-3-Clause
official_page: "https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/"
repository_directory: "https://github.com/PolymathicAI/the_well/tree/master/datasets/acoustic_scattering_discontinuous"
huggingface_dataset: "https://huggingface.co/datasets/polymathic-ai/acoustic_scattering_discontinuous"
paper: "https://arxiv.org/abs/2412.00568"
status: active
repository_release_checked: "v1.2.0 / master"
last_verified: 2026-07-21
linkTitle: acoustic_scattering_discontinuous
weight: 30
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: "The Well"
summary: "这组三个数据目录求解一阶变系数声学系统。初始声压扰动在材料密度具有空间突变的介质中传播。三个目录共用同一组 PDE 和数值求解器，仅静态系数场的生成族不同：单一不连续界面、随机夹杂物以及高反差迷宫介质。"
description: "这组三个数据目录求解一阶变系数声学系统。初始声压扰动在材料密度具有空间突变的介质中传播。三个目录共用同一组 PDE 和数值求解器，仅静态系数场的生成族不同：单一不连续界面、随机夹杂物以及高反差迷宫介质。"

---

# 声学散射——单一不连续界面

![密度场 / 材料分布](/the-well/acoustic_scattering_discontinuous__discontinuous_density.png)


> **所属数据集：** The Well
> **数据目录：** `acoustic_scattering_discontinuous`
> **方程族：** 变系数声学

## 1. 所属集合与物理概览

这组三个数据目录求解一阶变系数声学系统。初始声压扰动在材料密度具有空间突变的介质中传播。三个目录共用同一组 PDE 和数值求解器，仅静态系数场的生成族不同：单一不连续界面、随机夹杂物以及高反差迷宫介质。

The Well 把每个可下载目录组织为自描述 HDF5 数据集。

## 2. 控制方程

$$
\begin{aligned}
\frac{\partial p}{\partial t}
+K(x,y)\left(\frac{\partial u}{\partial x}+\frac{\partial v}{\partial y}\right)&=0,\\
\frac{\partial u}{\partial t}
+\frac{1}{\rho(x,y)}\frac{\partial p}{\partial x}&=0,\\
\frac{\partial v}{\partial t}
+\frac{1}{\rho(x,y)}\frac{\partial p}{\partial y}&=0.
\end{aligned}
$$

局部声速为 \(c(x,y)=\sqrt{K(x,y)/\rho(x,y)}\).

### 变量与物理场

- \(p(x,y,t)\)：声压。
- \(u(x,y,t),v(x,y,t)\)：Cartesian 速度分量。
- \(\rho(x,y)\)：不随时间变化的材料密度。
- \(K(x,y)\)：体积模量。
- \(c(x,y)\)：由 \(K, \rho\) 导出的静态声速。

## 3. 参数审计

| 类别 | 本发布版中的含义 |
|---|---|
| 理论上可调 | 材料密度 \(\rho(x,y)\)、体积模量 \(K(x,y)\)、声源数量/位置/半径/强度、系数场几何、界面反差、边界条件、空间与时间分辨率。 |
| 数据中实际变化 | 每条轨迹改变静态密度场和初始声压环。区域由一个不连续界面分为两个子域，每侧独立选择一种平滑密度生成族：（i）Gaussian bump，峰值 \(\mathcal U(1,7)\)、\(\sigma\sim\mathcal U(0.1,5)\)、中心随机；（ii）四角取值 \(\mathcal U(1,7)\) 后双线性插值；（iii）常数 \(\rho\sim\mathcal U(1,7)\)；（iv）背景 \(\mathcal U(1,7)\) 叠加 IID Gaussian 噪声，再以 \(\sigma\sim\mathcal U(5,10)\) 平滑。 |
| 数据中保持固定 | 体积模量 \(K=4\)；Cartesian 区域与 \(256^2\) 网格；\(y\) 向开边界；\(x\) 向反射壁；CFL safety factor 0.25；发布版采样间隔与轨迹时长。 |

## 4. 初始条件与边界条件

### 初始条件

平坦背景声压上随机放置 1–4 个高压环；环强度取自 \(\mathcal U(0.5,2)\)，半径取自 \(\mathcal U(0.06,0.15)\)；文档设置中初始速度为静止/零。

### 边界条件

\(y\) 方向开边界，\(x\) 方向反射壁。

## 5. 数据规格

| 属性 | 数值/说明 |
|---|---|
| 所属集合 | The Well |
| 下载目录 | `acoustic_scattering_discontinuous` |
| 空间维数 | 2D |
| 坐标系 | Cartesian $(x,y)$ |
| 空间分辨率 | $256\times256$ |
| 每条轨迹存储帧数 | 101 |
| 轨迹数 | 2000 |
| 展开后的动态通道数 | 3 |
| 动态物理场 | 声压 $p$；速度 $u_x,u_y$ |
| 静态场/标量上下文 | 材料密度 $\rho(x,y)$；声速 $c(x,y)$ |
| 时间范围 | $[0,2]$ |
| 存储时间间隔 | $2/101$ (documented storage interval) |
| 空间区域 | $[-1,1]\times[-1,1]$ |
| 发布数据量 | 157.7 GB |
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

**文档记录的求解器：** Clawpack; explicit finite volume, TVD/MC limiter, CFL-controlled time step

使用 Clawpack 的显式有限体积双曲守恒律求解器，采用 TVD/monotonized-central 通量限制器，并由 CFL 条件选择内部步长。发布数组经过时间采样并以 fp32 保存，而生成过程记录为双精度。

## 7. 推荐机器学习任务与诊断

自回归声波预测、逆散射/材料重建、声源定位或优化、跨不连续系数泛化，以及把复杂几何编码为系数场时的鲁棒建模。

评估时不宜只报告整体 RMSE；在条件允许时，应同时报告逐物理场误差、长期 rollout 稳定性、守恒/平衡诊断，以及湍流或波动问题的分频段误差。

## 8. 版本差异与注意事项

官网方程第三式曾排成 \(\partial p/\partial v\)；物理上正确且论文附录采用的是 \(y\) 导数 \(\partial p/\partial y\)。论文总览把序列长度概写为 100，而当前专用数据页给出 101 个存储快照。

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
the-well-download --base-path ./the_well_data --dataset acoustic_scattering_discontinuous --split train
```

下载标准的三个划分：

```bash
for split in train valid test; do
  the-well-download --base-path ./the_well_data --dataset acoustic_scattering_discontinuous --split "$split"
done
```

若同时省略 `--dataset` 与 `--split`，命令会请求完整集合；The Well 总量约 15 TB，不应误操作。

### 从本地读取

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="./the_well_data",
    well_dataset_name="acoustic_scattering_discontinuous",
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
    well_dataset_name="acoustic_scattering_discontinuous",
    well_split_name="train",
)
```

大规模训练通常应先下载到本地，以获得更高吞吐与更稳定的可复现性。

### 其他分发方式

论文还说明数据由 Flatiron Institute 直接托管并提供 Globus endpoint。端点信息可能变化，因此应遵循当前仓库的下载文档，不要把旧 endpoint 写死在脚本中。

## 9. 链接

| 资源 | URL |
|---|---|
| 官方数据页 | <https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/> |
| 仓库目录 | <https://github.com/PolymathicAI/the_well/tree/master/datasets/acoustic_scattering_discontinuous> |
| Hugging Face 数据页 | <https://huggingface.co/datasets/polymathic-ai/acoustic_scattering_discontinuous> |
| The Well 总仓库 | <https://github.com/PolymathicAI/the_well> |
| 论文 | <https://arxiv.org/abs/2412.00568> |
| 统一数据格式 | <https://polymathic-ai.org/the_well/data_format/> |
| Hugging Face 集合 | <https://huggingface.co/collections/polymathic-ai/the-well> |
