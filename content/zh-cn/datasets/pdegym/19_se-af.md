---
title: "SE-AF：翼型几何到稳态 Euler 密度场"
parent_dataset: PDEgym
subset: SE-AF
role: 下游任务：稳态几何条件算子
pde_family: "Steady compressible Euler"
spatial_dimension: 2
time_dependent: false
official_code_identifier: fluids.compressible.steady.Airfoil(.time)
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/SE-AF"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: SE-AF
weight: 190
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "输入随机 Hicks–Henne 扰动翼型的形状掩码，输出稳态可压缩 Euler 密度场。"
description: "输入随机 Hicks–Henne 扰动翼型的形状掩码，输出稳态可压缩 Euler 密度场。"

---

# SE-AF：翼型几何到稳态 Euler 密度场

> **一句话描述：** 输入随机 Hicks–Henne 扰动翼型的形状掩码，输出稳态可压缩 Euler 密度场。

## 更长描述

该任务不是轨迹预测，而是几何到场的稳态算子。原始求解使用贴体椭圆网格，再插值到 Cartesian 网格。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。  
**生成代码或软件：** NEWTUN/NUWTUN 稳态 Euler 求解器；$243\times43$ 贴体网格后插值到 $128^2$。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **SE-AF** |
| 角色 | 下游任务：稳态几何条件算子 |
| PDE 类型 | Steady compressible Euler |
| 空间维数 | 2D |
| 时间依赖 | 否（稳态） |
| 官方代码标识 | `fluids.compressible.steady.Airfoil(.time)` |
| 官方数据页 | [SE-AF](https://huggingface.co/datasets/camlab-ethz/SE-AF) |
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

稳态情况下 $\partial_t\mathbf U=0$。RAE2822 参考翼型的上下表面分别叠加 15 个 Hicks–Henne bump：
$$
y^{L/U}(\xi)=y_{ref}^{L/U}(\xi)+\sum_{i=1}^{15}a_i^{L/U}B_i(\xi),\qquad B_i(\xi)=\sin^3(\pi\xi^{q_i}).
$$
输入为翼型区域特征函数 $f=\chi_S$，输出为稳态密度 $\rho$。


### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$f(x,y)=\chi_S(x,y)\mapsto\rho_{steady}(x,y)$。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `solution: [10869, 2, 128, 128]` |
| 可用物理场 | 第 1 通道为 airfoil shape mask，第 2 通道为 density。 |
| 轨迹/样本数 | **10869** |
| Train / Val / Test | **10509 / 120 / 240** |
| 官方仓库总文件大小 | **1.43 GB** |
| 网格类型 | 原始 $243\times43$ 椭圆贴体网格；发布为 $128^2$ Cartesian 网格 |
| 空间区域 | $D=[-0.75,1.75]^2$ after interpolation |
| 初始条件/输入 | 稳态问题，无时间初值；输入是几何形状函数。 |
| 边界条件 | 固定自由来流边界；翼型为固体几何边界 |
| 保存快照数 | steady (2 fields, no time axis) |
| 论文/代码选用快照 | not applicable; `.time` wrapper assigns normalized lead time 1 |
| all2all 对数 | not a physical trajectory pairing |
| 总时间范围 | steady state |
| 保存时间间隔 | not applicable |
| 生成软件/数值方法 | NEWTUN/NUWTUN 稳态 Euler 求解器；$243\times43$ 贴体网格后插值到 $128^2$。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $\psi\in[0,1]^{30}$ | 30 个 Hicks–Henne bump 参数；geometry parameter | 逐样本变化 | uniform on $[0,1]^{30}$ |
| $M_\infty$ | 自由来流 Mach 数；physical parameter | 固定 | $0.729$ |
| $\alpha$ | 攻角；physical parameter | 固定 | $2.31^\circ$ |
| $T_\infty$ | 自由来流温度；physical parameter | 固定 | $1$ |
| $p_\infty$ | 自由来流压力；physical parameter | 固定 | $1$ |
| reference airfoil | 参考翼型；geometry parameter | 固定 | RAE2822 |

**汇总：** Mach 数、攻角、来流状态、翼型族和 bump 范围都可调；发布集仅扫描 30 维翼型几何。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`solution: [10869, 2, 128, 128]`
- 原始通道/变量：第 1 通道为 airfoil shape mask，第 2 通道为 density。
- 期望组装文件名：`SE-AF.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[1,128,128] → [1,128,128]`
- 通道定义：shape mask $\to$ density；官方 pixel mask 忽略翼型内部，内部密度被设为 1。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

NEWTUN/NUWTUN 稳态 Euler 求解器；$243\times43$ 贴体网格后插值到 $128^2$。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/SE-AF --repo-type dataset --local-dir ./SE-AF
```

该官方数据卡将文件作为已组装文件直接发布，不要求运行 `assemble_data.py`。

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 非 Cartesian 原始几何、贴体到规则网格插值、几何条件与跨激波稳态流。

## 已知来源差异与复现注意事项

- 论文称 30 个 bump 参数；公式排版中上下表面参数索引存在容易混淆之处，精确几何生成应以官方数据/代码为准。
- 训练与评估误差只在翼型外部计算。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: SE-AF](https://huggingface.co/datasets/camlab-ethz/SE-AF)。
5. 文档结构参考 [The Well dataset documentation](https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/)，但字段内容来自 PDEgym 原始论文、代码和数据卡。

## 引用

```bibtex
@misc{herde2024poseidon,
  title        = {POSEIDON: Efficient Foundation Models for PDEs},
  author       = {Maximilian Herde and Bogdan Raoni\'{c} and Tobias Rohner and
                  Roger K\"appeli and Roberto Molinaro and Emmanuel de B\'{e}zenac
                  and Siddhartha Mishra},
  year         = {2024},
  eprint       = {2405.19101},
  archivePrefix= {arXiv},
  primaryClass = {cs.LG}
}
```
