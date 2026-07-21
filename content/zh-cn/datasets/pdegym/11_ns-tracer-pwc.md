---
title: NS-Tracer-PwC：不可压流中的被动标量输运
parent_dataset: PDEgym
subset: NS-Tracer-PwC
role: 下游任务：新增被动标量物理
pde_family: "Incompressible Navier–Stokes + advection–diffusion"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.incompressible.PiecewiseConstants.tracer
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/NS-PwC"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: NS-Tracer-PwC
weight: 110
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "NS-PwC 速度场单向驱动一个被动浓度场的对流–扩散。"
description: "NS-PwC 速度场单向驱动一个被动浓度场的对流–扩散。"

---

# NS-Tracer-PwC：不可压流中的被动标量输运

**描述：** NS-PwC 速度场单向驱动一个被动浓度场的对流–扩散。 该任务在预训练流体方程上增加了新的物理量和方程。示踪剂随流输运但不反作用于速度，可代表污染物或染料。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。
**生成代码或软件：** 速度由 AZEBAN 生成；被动标量与同一流场共同保存。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **NS-Tracer-PwC** |
| 角色 | 下游任务：新增被动标量物理 |
| PDE 类型 | Incompressible Navier–Stokes + advection–diffusion |
| 空间维数 | 2D |
| 时间依赖 | 是 |
| 官方代码标识 | `fluids.incompressible.PiecewiseConstants.tracer` |
| 官方数据页 | [NS-PwC](https://huggingface.co/datasets/camlab-ethz/NS-PwC) |
| 官方代码 | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| 论文 | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| 许可 | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## 方程

$$
\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u+\nabla p
=\nu\Delta\mathbf u,\qquad \nabla\cdot\mathbf u=0,
$$

其中 $\mathbf u=(u_x,u_y)$ 是笛卡尔速度场，$p$ 是压力。PDEgym 发布的不可压流模拟只在足够高的 Fourier 模态上施加谱超黏性；取 $N=128$、$m_N=\sqrt N$、$\varepsilon_N=0.05/N$，对应有效黏性尺度约 $\nu\simeq4\times10^{-4}$。它是用于逼近无黏极限的数值稳定化设置，并不是发布数据中的黏度参数扫描。

被动标量 $c$ 满足
$$
\partial_t c+\mathbf u\cdot\nabla c=\kappa\Delta c.
$$
初值为中心圆盘
$$
c_0(x,y)=\mathbf 1_{B_{1/4}(1/2,1/2)}(x,y).
$$

### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$[u_x,u_y,c](0)\mapsto[u_x,u_y,c](t)$；耦合是单向的。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `velocity: [20000, 21, 3, 128, 128] (shared NS-PwC file)` |
| 可用物理场 | $[u_x,u_y,c]$。 |
| 轨迹/样本数 | **20000** |
| Train / Val / Test | **19640 / 120 / 240** |
| 官方仓库总文件大小 | **No additional storage; shares the 82.6 GB NS-PwC repository** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=[0,1]^2$ |
| 初始条件/输入 | 速度初值同 NS-PwC；浓度初值为固定中心圆盘。 |
| 边界条件 | 速度与浓度均采用周期边界 |
| 保存快照数 | 21 |
| 论文/代码选用快照 | 8 (indices 0,2,…,14) |
| all2all 对数 | 36 pairs per trajectory |
| 总时间范围 | $[0,1]$; benchmark horizon $[0,0.7]$ |
| 保存时间间隔 | $0.05$ raw; selected interval $0.1$ |
| 生成软件/数值方法 | 速度由 AZEBAN 生成；被动标量与同一流场共同保存。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $c_{ij}$ | NS-PwC 初始涡量块值；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[-1,1]$ |
| $\kappa$ | 示踪剂扩散率；PDE coefficient | 固定 | set equal to the artificial viscosity scale |
| disk center | 示踪剂圆心；IC / data-distribution parameter | 固定 | $(1/2,1/2)$ |
| disk radius | 示踪剂半径；IC / data-distribution parameter | 固定 | $1/4$ |
| tracer amplitude | 初始浓度幅值；IC / data-distribution parameter | 固定 | $1$ |

**汇总：** 数学上可改变 $\kappa$、示踪剂位置/形状/幅值、加入源汇或双向耦合；发布数据只通过随机速度初值改变输运。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`velocity: [20000, 21, 3, 128, 128] (shared NS-PwC file)`
- 原始通道/变量：$[u_x,u_y,c]$。
- 期望组装文件名：`NS-PwC.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[5,128,128] → [5,128,128]`
- 通道定义：$[1,u_x,u_y,0,c]_{t_i}\to[1,u_x,u_y,0,c]_{t_j}$。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

速度由 AZEBAN 生成；被动标量与同一流场共同保存。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/NS-PwC --repo-type dataset --local-dir ./NS-PwC
```

进入下载目录并运行仓库自带组装脚本：

```bash
cd ./NS-PwC
python assemble_data.py --input_dir . --output_file NS-PwC.nc
```

注意：逻辑任务 NS-Tracer-PwC 仍下载 `NS-PwC` 仓库，并在官方加载器中启用 `.tracer`。

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 需要同时预测速度向量和具有尖锐界面的标量浓度，并维持一向耦合结构。

## 已知来源差异与复现注意事项

- 官方没有独立的 `NS-Tracer-PwC` HF 仓库；必须下载 `camlab-ethz/NS-PwC`。
- 官方 README 的映射表曾出现 `incomressible` 拼写错误；实际使用时应以当前 selector/config 为准。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: NS-PwC](https://huggingface.co/datasets/camlab-ethz/NS-PwC)。
