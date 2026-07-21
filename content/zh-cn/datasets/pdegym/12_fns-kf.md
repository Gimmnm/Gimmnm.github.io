---
title: "FNS-KF：Kolmogorov 强迫不可压流"
parent_dataset: PDEgym
subset: FNS-KF
role: 下游任务：新增外部强迫
pde_family: "Forced incompressible Navier–Stokes"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.incompressible.forcing.KolmogorovFlow
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/FNS-KF"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: FNS-KF
weight: 120
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "具有固定正弦 Kolmogorov 外力的不可压 Navier–Stokes 轨迹。"
description: "具有固定正弦 Kolmogorov 外力的不可压 Navier–Stokes 轨迹。"

---

# FNS-KF：Kolmogorov 强迫不可压流

**描述：** 具有固定正弦 Kolmogorov 外力的不可压 Navier–Stokes 轨迹。 该任务把外部强迫作为静态 conditioning 场加入解算子。初始速度分布与 NS-PwC 相同，但持续强迫改变后续动力学。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。
**生成代码或软件：** AZEBAN 流体求解；forcing 由官方加载代码生成。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **FNS-KF** |
| 角色 | 下游任务：新增外部强迫 |
| PDE 类型 | Forced incompressible Navier–Stokes |
| 空间维数 | 2D |
| 时间依赖 | 是 |
| 官方代码标识 | `fluids.incompressible.forcing.KolmogorovFlow` |
| 官方数据页 | [FNS-KF](https://huggingface.co/datasets/camlab-ethz/FNS-KF) |
| 官方代码 | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| 论文 | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| 许可 | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## 方程

$$
\partial_t\mathbf u+(\mathbf u\cdot\nabla)\mathbf u+\nabla p-\nu\Delta\mathbf u=\mathbf f,
\qquad \nabla\cdot\mathbf u=0,
$$
论文采用静态场
$$
f(x,y)=0.1\sin(2\pi(x+y)).
$$
官方算子实现把该场作为额外通道，并附加 $f_t=0$。

### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$[u_x,u_y,f](0)\mapsto[u_x,u_y,f](t)$；评价只计算速度。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `solution: [20000, 21, 2, 128, 128]` |
| 可用物理场 | 只存 $[u_x,u_y]$；forcing 在加载时按解析式重建。 |
| 轨迹/样本数 | **20000** |
| Train / Val / Test | **19640 / 120 / 240** |
| 官方仓库总文件大小 | **55.1 GB** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=[0,1]^2$ |
| 初始条件/输入 | 速度初值与 NS-PwC 相同。 |
| 边界条件 | 周期边界条件 |
| 保存快照数 | 21 |
| 论文/代码选用快照 | 8 (indices 0,2,…,14) |
| all2all 对数 | 36 pairs per trajectory |
| 总时间范围 | $[0,1]$; benchmark horizon $[0,0.7]$ |
| 保存时间间隔 | $0.05$ raw; selected interval $0.1$ |
| 生成软件/数值方法 | AZEBAN 流体求解；forcing 由官方加载代码生成。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $c_{ij}$ | 初始分片常数涡量；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[-1,1]$ |
| forcing amplitude | 外力幅度；PDE/source parameter | 固定 | $0.1$ |
| forcing wavevector | 外力波数与方向；PDE/source parameter | 固定 | $2\pi(x+y)$ |
| time dependence | 外力时间依赖；PDE/source parameter | 固定为静态 | $f_t=0$ |
| $\nu$ | 黏性/谱稳定化；PDE/numerical coefficient | 固定 | $\simeq4\times10^{-4}$ |

**汇总：** 强迫幅度、波数、方向、相位、时间依赖和黏度都可调；本数据集固定强迫，只随机化速度初值。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`solution: [20000, 21, 2, 128, 128]`
- 原始通道/变量：只存 $[u_x,u_y]$；forcing 在加载时按解析式重建。
- 期望组装文件名：`FNS-KF.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[5,128,128] → [5,128,128]`
- 通道定义：$[1,u_x,u_y,0,f]_{t_i}\to[1,u_x,u_y,0,f]_{t_j}$。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

AZEBAN 流体求解；forcing 由官方加载代码生成。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/FNS-KF --repo-type dataset --local-dir ./FNS-KF
```

进入下载目录并运行仓库自带组装脚本：

```bash
cd ./FNS-KF
python assemble_data.py --input_dir . --output_file FNS-KF.nc
```

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 模型必须把静态 PDE/source 条件与动态速度场区分，同时学习持续能量注入。

## 已知来源差异与复现注意事项

- 论文、官方代码和数据卡在本条目的关键字段上未发现额外冲突。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: FNS-KF](https://huggingface.co/datasets/camlab-ethz/FNS-KF)。
