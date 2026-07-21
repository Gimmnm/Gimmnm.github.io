---
title: NS-PwC：分片常数涡量初值
parent_dataset: PDEgym
subset: NS-PwC
role: 下游任务：新初值分布
pde_family: "Incompressible Navier–Stokes / near-inviscid flow"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.incompressible.PiecewiseConstants
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/NS-PwC"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: NS-PwC
weight: 70
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: '初始涡量在 $10\times10$ 方格上分片常数，随后恢复速度并演化。'
description: '初始涡量在 $10\times10$ 方格上分片常数，随后恢复速度并演化。'

---

# NS-PwC：分片常数涡量初值

> **一句话描述：** 初始涡量在 $10\times10$ 方格上分片常数，随后恢复速度并演化。

## 更长描述

该任务类似在涡量场上同时放置许多 Riemann 间断，用来检验对粗糙、非训练分布初值的迁移。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。  
**生成代码或软件：** AZEBAN；$128^2$。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **NS-PwC** |
| 角色 | 下游任务：新初值分布 |
| PDE 类型 | Incompressible Navier–Stokes / near-inviscid flow |
| 空间维数 | 2D |
| 时间依赖 | 是 |
| 官方代码标识 | `fluids.incompressible.PiecewiseConstants` |
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

$$
\omega_0(x,y)=c_{ij},\qquad (x,y)\in[x_{i-1},x_i]\times[y_{j-1},y_j],\qquad x_i=y_i=i/10.
$$
由涡量和不可压条件恢复 $(u_x^0,u_y^0)$。

### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$[u_x,u_y](0)\mapsto[u_x,u_y](t)$；此逻辑任务不读取 tracer。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `velocity: [20000, 21, 3, 128, 128]` |
| 可用物理场 | $[u_x,u_y,c_{tr}]$；同一物理文件也服务于 NS-Tracer-PwC。 |
| 轨迹/样本数 | **20000** |
| Train / Val / Test | **19640 / 120 / 240** |
| 官方仓库总文件大小 | **82.6 GB (shared with NS-Tracer-PwC)** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=[0,1]^2$ |
| 初始条件/输入 | $10\times10$ 分片常数涡量。 |
| 边界条件 | 周期边界条件 |
| 保存快照数 | 21 |
| 论文/代码选用快照 | 8 (indices 0,2,…,14) |
| all2all 对数 | 36 pairs per trajectory |
| 总时间范围 | $[0,1]$; paper benchmark horizon $[0,0.7]$ |
| 保存时间间隔 | $0.05$ raw; selected interval $0.1$ |
| 生成软件/数值方法 | AZEBAN；$128^2$。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $c_{ij}$ | 每个网格块的初始涡量；IC / data-distribution parameter | 逐格、逐轨迹变化 | $\mathcal U[-1,1]$ |
| $p$ | 每方向分块数；IC / data-distribution parameter | 固定 | $10$ |
| $\nu$ | 有效谱黏性；PDE/numerical coefficient | 固定 | $\simeq4\times10^{-4}$ |

**汇总：** 可以改变分块数、涡量范围、黏度、边界；发布数据只随机化 $c_{ij}$。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`velocity: [20000, 21, 3, 128, 128]`
- 原始通道/变量：$[u_x,u_y,c_{tr}]$；同一物理文件也服务于 NS-Tracer-PwC。
- 期望组装文件名：`NS-PwC.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[4,128,128] → [4,128,128]`
- 通道定义：$[1,u_x,u_y,0]_{t_i}\to[1,u_x,u_y,0]_{t_j}$。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

AZEBAN；$128^2$。

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

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 粗糙分片常数涡量产生大量小尺度界面和复杂涡相互作用。

## 已知来源差异与复现注意事项

- NS-PwC 与 NS-Tracer-PwC 共用同一仓库和 NetCDF 文件，汇总物理存储容量时不可重复相加。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: NS-PwC](https://huggingface.co/datasets/camlab-ethz/NS-PwC)。
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
