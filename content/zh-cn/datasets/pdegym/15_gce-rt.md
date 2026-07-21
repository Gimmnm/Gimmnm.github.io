---
title: "GCE-RT：重力 Euler 的 Rayleigh–Taylor 不稳定性"
parent_dataset: PDEgym
subset: GCE-RT
role: 下游任务：新增重力源项与物理参数
pde_family: "Compressible Euler with gravity"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.compressible.gravity.RayleighTaylor
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/GCE-RT"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: GCE-RT
weight: 150
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "带重力势源项的可压缩 Euler，多方中子星模型上的随机 Rayleigh–Taylor 不稳定性。"
description: "带重力势源项的可压缩 Euler，多方中子星模型上的随机 Rayleigh–Taylor 不稳定性。"

---

# GCE-RT：重力 Euler 的 Rayleigh–Taylor 不稳定性

> **一句话描述：** 带重力势源项的可压缩 Euler，多方中子星模型上的随机 Rayleigh–Taylor 不稳定性。

## 更长描述

这是少数真正逐样本改变物理参数的 PDEgym 任务之一：中心密度、中心压力和 Atwood 数均变化，并把重力势作为静态场输入。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。  
**生成代码或软件：** 二阶 well-balanced 有限体积法；$256^2$ 生成后下采样至 $128^2$。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **GCE-RT** |
| 角色 | 下游任务：新增重力源项与物理参数 |
| PDE 类型 | Compressible Euler with gravity |
| 空间维数 | 2D |
| 时间依赖 | 是 |
| 官方代码标识 | `fluids.compressible.gravity.RayleighTaylor` |
| 官方数据页 | [GCE-RT](https://huggingface.co/datasets/camlab-ethz/GCE-RT) |
| 官方代码 | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| 论文 | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| 许可 | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## 方程


$$
\partial_t\mathbf U+\nabla\cdot\mathbf F(\mathbf U)=\mathbf S(\rho,\mathbf v,\nabla\phi),
$$
其中 $\mathbf U=(\rho,\rho\mathbf v,E)^\top$，$\phi$ 为重力势，数据采用 $\gamma=2$ 多方模型。径向平衡态为
$$
p(r)=K_0\left(\rho_0\frac{\sin(\alpha r)}{\alpha r}\right)^2,\qquad
\phi(r)=-2K_0\rho_0\frac{\sin(\alpha r)}{\alpha r},
$$
$$
K_0=p_0/\rho_0^2,\qquad \alpha=\sqrt{\frac{4\pi G}{2K_0}}.
$$

重力源项按守恒变量 $\mathbf U=(\rho,\rho v_x,\rho v_y,E)^\top$ 写为
$$
\mathbf S=
\begin{bmatrix}0\\-\rho\\0\\-\rho v_x\end{bmatrix}\partial_x\phi+
\begin{bmatrix}0\\0\\-\rho\\-\rho v_y\end{bmatrix}\partial_y\phi.
$$
初速度固定为零。密度剖面和轻/重流体界面为
$$
\rho(r)=\sqrt{\frac{K_0}{\widetilde K(r)}}\,\rho_0\frac{\sin(\alpha r)}{\alpha r},
\qquad
\widetilde K(r)=
\begin{cases}
K_0,&r<r_{RT},\\
\left(\dfrac{1-A}{1+A}\right)^2K_0,&r\ge r_{RT},
\end{cases}
$$
$$
r_{RT}=0.25\left[1+a\cos\!\left(\operatorname{atan2}(y,x)+b\right)\right],
$$
$$
\rho_0=1+0.2c,\qquad p_0=1+0.2d,\qquad A=0.05(1+0.2e),
\qquad c,d,e\sim\mathcal U[-1,1].
$$


### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$[\rho,v_x,v_y,p,\phi](0)\mapsto[\rho,v_x,v_y,p,\phi](t)$；$\phi$ 静态。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `solution: [1260, 11, 6, 128, 128]` |
| 可用物理场 | $[\rho,v_x,v_y,p,c_{tr},\phi]$。 |
| 轨迹/样本数 | **1260** |
| Train / Val / Test | **1030 / 100 / 130** |
| 官方仓库总文件大小 | **5.45 GB** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=[-1/2,1/2]^2$ |
| 初始条件/输入 | 多方重力平衡态、零初速度、随机扰动重/轻流体界面。 |
| 边界条件 | 周期边界条件 |
| 保存快照数 | 11 |
| 论文/代码选用快照 | 8 (indices 0,1,…,7) |
| all2all 对数 | 36 pairs per trajectory |
| 总时间范围 | $[0,5]$ |
| 保存时间间隔 | $0.5$ |
| 生成软件/数值方法 | 二阶 well-balanced 有限体积法；$256^2$ 生成后下采样至 $128^2$。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $a$ | RT 界面扰动幅度；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[-1,1]$ |
| $b$ | RT 界面相位；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[-\pi,\pi]$ |
| $\rho_0$ | 中心密度；physical parameter | 逐轨迹变化 | $1+0.2c,\ c\sim\mathcal U[-1,1]$ |
| $p_0$ | 中心压力；physical parameter | 逐轨迹变化 | $1+0.2d,\ d\sim\mathcal U[-1,1]$ |
| $A$ | Atwood 数/密度跳跃；physical parameter | 逐轨迹变化 | $0.05(1+0.2e),\ e\sim\mathcal U[-1,1]$ |
| $\gamma$ | 多方/比热参数；PDE coefficient | 固定 | $2$ |
| $G$ | 重力常数；PDE coefficient | 固定 | $1$ |
| $r_{RT,0}$ | 基准界面半径；IC / data-distribution parameter | 固定 | $0.25$ |

**汇总：** 发布数据实际改变 $\rho_0,p_0,A$ 和界面几何；$G,\gamma$ 与初速度固定。理论上还可改变势场、边界和多方常数。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`solution: [1260, 11, 6, 128, 128]`
- 原始通道/变量：$[\rho,v_x,v_y,p,c_{tr},\phi]$。
- 期望组装文件名：`GCE-RT.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[5,128,128] → [5,128,128]`
- 通道定义：官方加载器丢弃第 5 个 raw passive-tracer 通道，使用 $[\rho,v_x,v_y,p,\phi]$。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

二阶 well-balanced 有限体积法；$256^2$ 生成后下采样至 $128^2$。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/GCE-RT --repo-type dataset --local-dir ./GCE-RT
```

进入下载目录并运行仓库自带组装脚本：

```bash
cd ./GCE-RT
python assemble_data.py --input_dir . --output_file GCE-RT.nc
```

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 重力平衡保持、RT 不稳定性和多个逐样本物理参数同时出现。

## 已知来源差异与复现注意事项

- HF 卡将空间文字描述为 unit square，但论文明确写 $[-1/2,1/2]^2$；本文采用论文坐标范围。
- 官方 Hugging Face 文件树当前显示仓库总大小为 5.45 GB；该数值与按 raw shape 估算的 float32 有效载荷量级一致。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: GCE-RT](https://huggingface.co/datasets/camlab-ethz/GCE-RT)。
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
