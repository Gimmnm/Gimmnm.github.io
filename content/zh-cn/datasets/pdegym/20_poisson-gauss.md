---
title: "Poisson-Gauss：高斯源到 Poisson 稳态解"
parent_dataset: PDEgym
subset: Poisson-Gauss
role: 下游任务：稳态椭圆算子
pde_family: "Poisson equation"
spatial_dimension: 2
time_dependent: false
official_code_identifier: elliptic.poisson.Gaussians(.time)
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/Poisson-Gauss"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: Poisson-Gauss
weight: 200
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "随机数目高斯源项到齐次 Dirichlet Poisson 解的稳态映射。"
description: "随机数目高斯源项到齐次 Dirichlet Poisson 解的稳态映射。"

---

# Poisson-Gauss：高斯源到 Poisson 稳态解

**描述：** 随机数目高斯源项到齐次 Dirichlet Poisson 解的稳态映射。 这是与流体预训练物理差异很大的椭圆扩散/平滑算子，用来测试从源项到稳态场的迁移。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。
**生成代码或软件：** FEniCS 有限元法；发布为 $128^2$ 场。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **Poisson-Gauss** |
| 角色 | 下游任务：稳态椭圆算子 |
| PDE 类型 | Poisson equation |
| 空间维数 | 2D |
| 时间依赖 | 否（稳态） |
| 官方代码标识 | `elliptic.poisson.Gaussians(.time)` |
| 官方数据页 | [Poisson-Gauss](https://huggingface.co/datasets/camlab-ethz/Poisson-Gauss) |
| 官方代码 | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| 论文 | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| 许可 | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## 方程

$$
-\Delta u=f\quad\text{in }(0,1)^2,\qquad u=0\quad\text{on }\partial D,
$$
$$
f(x,y)=\sum_{i=1}^{N_g}\exp\!\left[-\frac{(x-\mu_{x,i})^2+(y-\mu_{y,i})^2}{2\sigma_i^2}\right].
$$

### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$f\mapsto u$。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `source: [20000,128,128]; solution: [20000,128,128]` |
| 可用物理场 | 1 通道 source，1 通道 solution。 |
| 轨迹/样本数 | **20000** |
| Train / Val / Test | **19640 / 120 / 240** |
| 官方仓库总文件大小 | **2.62 GB** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=(0,1)^2$ |
| 初始条件/输入 | 稳态问题；输入为高斯源场。 |
| 边界条件 | 齐次 Dirichlet：$u=0$ |
| 保存快照数 | steady |
| 论文/代码选用快照 | not applicable |
| all2all 对数 | not a physical trajectory pairing |
| 总时间范围 | steady state |
| 保存时间间隔 | not applicable |
| 生成软件/数值方法 | FEniCS 有限元法；发布为 $128^2$ 场。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $N_g$ | 高斯源数；source parameter | 逐样本变化 | $\mathrm{Geom}(0.4)$ |
| $\mu_{x,i},\mu_{y,i}$ | 源中心；source parameter | 逐样本变化 | $\mathcal U[0,1]$ |
| $\sigma_i$ | 源宽度；source parameter | 逐样本变化 | $\mathcal U[0.025,0.1]$ |
| Gaussian amplitude | 每个高斯幅值；source parameter | 固定 | $1$ |
| elliptic coefficient | Laplace 算子系数；PDE coefficient | 固定 | $1$ |
| boundary value | 边界值；boundary parameter | 固定 | $0$ |

**汇总：** 空间变扩散系数、非齐次边界、域形状和反应项都可调；发布数据只变化源项。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`source: [20000,128,128]; solution: [20000,128,128]`
- 原始通道/变量：1 通道 source，1 通道 solution。
- 期望组装文件名：`Poisson-Gauss.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[1,128,128] → [1,128,128]`
- 通道定义：$f\to u$；`.time` 包装时 lead time 固定为 1。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

FEniCS 有限元法；发布为 $128^2$ 场。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/Poisson-Gauss --repo-type dataset --local-dir ./Poisson-Gauss
```

该官方数据卡将文件作为已组装文件直接发布，不要求运行 `assemble_data.py`。

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 从局部源到全局平滑解；稳态、椭圆和 Dirichlet 边界均与预训练设置不同。

## 已知来源差异与复现注意事项

- 论文、官方代码和数据卡在本条目的关键字段上未发现额外冲突。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: Poisson-Gauss](https://huggingface.co/datasets/camlab-ethz/Poisson-Gauss)。
