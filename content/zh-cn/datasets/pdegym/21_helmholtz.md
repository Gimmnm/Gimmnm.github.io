---
title: Helmholtz：随机介质和边界值到频域波场
parent_dataset: PDEgym
subset: Helmholtz
role: 下游任务：稳态系数算子
pde_family: "Helmholtz equation"
spatial_dimension: 2
time_dependent: false
official_code_identifier: elliptic.Helmholtz(.time)
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/Helmholtz"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: Helmholtz
weight: 210
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "逐样本介质系数场和常 Dirichlet 边界值到 Helmholtz 频域解。"
description: "逐样本介质系数场和常 Dirichlet 边界值到 Helmholtz 频域解。"

---

# Helmholtz：随机介质和边界值到频域波场

**描述：** 逐样本介质系数场和常 Dirichlet 边界值到 Helmholtz 频域解。 该任务同时改变 PDE 系数 $a(x,y)$ 与边界参数 $b$，但频率固定；它是 PDEgym 中典型的稳态波动系数算子。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。
**生成代码或软件：** 类似 DeVITO 的有限差分法；$128^2$。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **Helmholtz** |
| 角色 | 下游任务：稳态系数算子 |
| PDE 类型 | Helmholtz equation |
| 空间维数 | 2D |
| 时间依赖 | 否（稳态） |
| 官方代码标识 | `elliptic.Helmholtz(.time)` |
| 官方数据页 | [Helmholtz](https://huggingface.co/datasets/camlab-ethz/Helmholtz) |
| 官方代码 | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| 论文 | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| 许可 | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## 方程

$$
-\Delta u-\omega^2a(x,y)u=0\quad\text{in }D,
\qquad u=b\quad\text{on }\partial D,
$$
$$
\omega=\frac{5\pi}{2}.
$$
先生成
$$
\bar a(x,y)=-\sum_{i=1}^{n}A_i\exp\!\left[-\frac{(x-x_i)^2+(y-y_i)^2}{2\sigma_i^2}\right],
$$
再做 min–max 归一化 $a=(\bar a-\min\bar a)/(\max\bar a-\min\bar a)$。

### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$(a,b)\mapsto u$。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `HDF5: 19675 groups Sample_i, each with a[128,128], scalar bc, u[128,128]` |
| 可用物理场 | 介质场 $a$、标量边界值 $bc$、解 $u$。 |
| 轨迹/样本数 | **19675** |
| Train / Val / Test | **19035 / 128 / 512** |
| 官方仓库总文件大小 | **5.2 GB** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=(0,1)^2$ |
| 初始条件/输入 | 稳态问题；输入为介质场和边界值。 |
| 边界条件 | 逐样本常值 Dirichlet：$u=b$ |
| 保存快照数 | steady |
| 论文/代码选用快照 | not applicable; `.time` wrapper can assign lead time 1 |
| all2all 对数 | not a physical trajectory pairing |
| 总时间范围 | steady state / frequency domain |
| 保存时间间隔 | not applicable |
| 生成软件/数值方法 | 类似 DeVITO 的有限差分法；$128^2$。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $b$ | 常 Dirichlet 边界值；boundary parameter | 逐样本变化 | $\mathcal U[0.25,0.5]$ |
| $n$ | 介质高斯数；PDE coefficient construction | 逐样本变化 | $\mathcal U\{2,3,4,5,6,7\}$ |
| $A_i$ | 介质高斯幅度；PDE coefficient construction | 逐样本变化 | $\mathcal U[0.5,10]$ |
| $\sigma_i$ | 介质高斯宽度；PDE coefficient construction | 逐样本变化 | $\mathcal U[0.05,0.1]$ |
| $x_i,y_i$ | 介质高斯中心；PDE coefficient construction | 逐样本变化 | $\mathcal U[0.2,0.8]$ |
| $\omega$ | 角频率；PDE coefficient | 固定 | $5\pi/2$ |

**汇总：** 频率、边界空间形状、复数阻尼、域和介质构造均可调；发布数据变化 $a(x,y)$ 与标量 $b$，固定 $\omega$。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`HDF5: 19675 groups Sample_i, each with a[128,128], scalar bc, u[128,128]`
- 原始通道/变量：介质场 $a$、标量边界值 $bc$、解 $u$。
- 期望组装文件名：`Helmholtz.h5`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[2,128,128] → [1,128,128]`
- 通道定义：加载器把 $b$ broadcast 成常值场，与 $a$ 拼成 2 通道输入；输出为 1 通道 $u$。代码还对输入 $a$ 做 `a - 1` 预处理。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

类似 DeVITO 的有限差分法；$128^2$。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/Helmholtz --repo-type dataset --local-dir ./Helmholtz
```

该官方数据卡将文件作为已组装文件直接发布，不要求运行 `assemble_data.py`。

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 介质系数和边界值同时变化，解可具有振荡与共振结构；官方原始格式为逐样本 HDF5 group。

## 已知来源差异与复现注意事项

- 论文、官方代码和数据卡在本条目的关键字段上未发现额外冲突。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: Helmholtz](https://huggingface.co/datasets/camlab-ethz/Helmholtz)。
