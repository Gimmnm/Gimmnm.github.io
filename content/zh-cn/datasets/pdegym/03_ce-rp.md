---
title: "CE-RP：四象限随机 Riemann 问题"
parent_dataset: PDEgym
subset: CE-RP
role: 预训练算子
pde_family: "Compressible Euler"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.compressible.Riemann
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/CE-RP"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: CE-RP
weight: 30
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "二维可压缩 Euler 方程上的随机四象限 Riemann 问题，产生激波、接触间断与稀疏波。"
description: "二维可压缩 Euler 方程上的随机四象限 Riemann 问题，产生激波、接触间断与稀疏波。"

---

# CE-RP：四象限随机 Riemann 问题

**描述：** 二维可压缩 Euler 方程上的随机四象限 Riemann 问题，产生激波、接触间断与稀疏波。 该数据是二维 Sod 激波管类问题的随机推广。每个象限具有独立常状态，模型必须学习多方向间断相互作用。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。
**生成代码或软件：** ALSVINN 高分辨率有限体积法，二次 WENO 重构与 HLLC Riemann solver；$512^2$ 生成后下采样到 $128^2$。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **CE-RP** |
| 角色 | 预训练算子 |
| PDE 类型 | Compressible Euler |
| 空间维数 | 2D |
| 时间依赖 | 是 |
| 官方代码标识 | `fluids.compressible.Riemann` |
| 官方数据页 | [CE-RP](https://huggingface.co/datasets/camlab-ethz/CE-RP) |
| 官方代码 | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| 论文 | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| 许可 | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## 方程

$$
\partial_t\mathbf U+\nabla\cdot\mathbf F(\mathbf U)=0,
\qquad \mathbf U=(\rho,\rho\mathbf v,E)^\top,
$$
$$
\mathbf F(\mathbf U)=\left(\rho\mathbf v,
\rho\mathbf v\otimes\mathbf v+pI,(E+p)\mathbf v\right)^\top,
\qquad E=\frac12\rho\lVert\mathbf v\rVert^2+\frac{p}{\gamma-1}.
$$

其中 $\rho$ 是密度，$\mathbf v=(v_x,v_y)$ 是速度，$p$ 是压力，$E$ 是总能量。除非条目另行说明，PDEgym 的可压缩 Euler 数据使用理想气体参数 $\gamma=1.4$。

单位方形被分成 $2\times2$ 个子域 $D_{ij}$，每个子域初值为常数 $(\rho_{ij},v_{x,ij},v_{y,ij},p_{ij})$。

### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$[\rho,v_x,v_y,p](0)\mapsto[\rho,v_x,v_y,p](t)$。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `data: [10000, 21, 5, 128, 128]` |
| 可用物理场 | $[\rho,v_x,v_y,p,E]$。 |
| 轨迹/样本数 | **10000** |
| Train / Val / Test | **9640 / 120 / 240** |
| 官方仓库总文件大小 | **68.8 GB** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=[0,1]^2\simeq\mathbb T^2$ |
| 初始条件/输入 | 四象限分片常状态。 |
| 边界条件 | 周期边界条件 |
| 保存快照数 | 21 |
| 论文/代码选用快照 | 11 (indices 0,2,…,20) |
| all2all 对数 | 66 pairs per trajectory |
| 总时间范围 | $[0,1]$ |
| 保存时间间隔 | $0.05$ |
| 生成软件/数值方法 | ALSVINN 高分辨率有限体积法，二次 WENO 重构与 HLLC Riemann solver；$512^2$ 生成后下采样到 $128^2$。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $\rho_{ij}$ | 各象限密度；IC / data-distribution parameter | 逐象限、逐轨迹变化 | $\mathcal U[0.1,1]$ |
| $v_{x,ij},v_{y,ij}$ | 各象限速度；IC / data-distribution parameter | 逐象限、逐轨迹变化 | $\mathcal U[-1,1]$ |
| $p_{ij}$ | 各象限压力；IC / data-distribution parameter | 逐象限、逐轨迹变化 | $\mathcal U[0.1,1]$ |
| $p_{\rm grid}$ | 每方向分区数；IC / data-distribution parameter | 固定 | $2$ |
| $\gamma$ | 比热比；PDE coefficient | 固定，不扫描 | $1.4$ |

**汇总：** 可调项包括象限数、状态范围、$\gamma$、边界类型和区域；发布数据只改变初始间断两侧状态。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`data: [10000, 21, 5, 128, 128]`
- 原始通道/变量：$[\rho,v_x,v_y,p,E]$。
- 期望组装文件名：`CE-RP.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[4,128,128] → [4,128,128]`
- 通道定义：模型丢弃可由状态方程重建的 $E$，使用 $[\rho,v_x,v_y,p]$。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

ALSVINN 高分辨率有限体积法，二次 WENO 重构与 HLLC Riemann solver；$512^2$ 生成后下采样到 $128^2$。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/CE-RP --repo-type dataset --local-dir ./CE-RP
```

进入下载目录并运行仓库自带组装脚本：

```bash
cd ./CE-RP
python assemble_data.py --input_dir . --output_file CE-RP.nc
```

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 多方向激波和接触间断相互作用；解具有强不连续性。

## 已知来源差异与复现注意事项

- 论文、官方代码和数据卡在本条目的关键字段上未发现额外冲突。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: CE-RP](https://huggingface.co/datasets/camlab-ethz/CE-RP)。
