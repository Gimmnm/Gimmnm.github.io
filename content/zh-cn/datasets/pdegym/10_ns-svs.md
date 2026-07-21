---
title: NS-SVS：正弦涡片初值
parent_dataset: PDEgym
subset: NS-SVS
role: 下游任务：正弦涡片
pde_family: "Incompressible Navier–Stokes / near-inviscid flow"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.incompressible.VortexSheet
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/NS-SVS"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: NS-SVS
weight: 100
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "沿随机正弦曲线分布并经平滑核正则化的涡片初值。"
description: "沿随机正弦曲线分布并经平滑核正则化的涡片初值。"

---

# NS-SVS：正弦涡片初值

> **一句话描述：** 沿随机正弦曲线分布并经平滑核正则化的涡片初值。

## 更长描述

涡片是近奇异、强剪切的经典流体基准。小幅随机扰动会触发复杂卷起，对分辨率和数值耗散非常敏感。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。  
**生成代码或软件：** AZEBAN；$128^2$。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **NS-SVS** |
| 角色 | 下游任务：正弦涡片 |
| PDE 类型 | Incompressible Navier–Stokes / near-inviscid flow |
| 空间维数 | 2D |
| 时间依赖 | 是 |
| 官方代码标识 | `fluids.incompressible.VortexSheet` |
| 官方数据页 | [NS-SVS](https://huggingface.co/datasets/camlab-ethz/NS-SVS) |
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
\omega_0^{\rho_s}=\psi_{\rho_s}*\omega_0,
$$
$$
\Gamma=\left\{(x,y):y=\frac12+0.2\sin(2\pi x)+\sum_{i=1}^{10}\alpha_i\sin(2\pi(x+\beta_i))\right\}.
$$
$\omega_0$ 是集中在 $\Gamma$ 上并减去空间平均的涡片分布，$\psi_{\rho_s}$ 是平滑核。


### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

由平滑涡片恢复初始速度，再映射到 $[u_x,u_y](t)$。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `velocity: [20000, 21, 3, 128, 128]` |
| 可用物理场 | HF 卡列 $[u_x,u_y,\text{passive tracer}]$，但官方 VortexSheet 加载器不支持 tracer。 |
| 轨迹/样本数 | **20000** |
| Train / Val / Test | **19640 / 120 / 240** |
| 官方仓库总文件大小 | **82.6 GB** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=[0,1]^2\simeq\mathbb T^2$ |
| 初始条件/输入 | 正弦涡片及小幅随机扰动。 |
| 边界条件 | 周期边界条件 |
| 保存快照数 | 21 |
| 论文/代码选用快照 | 8 (indices 0,2,…,14) |
| all2all 对数 | 36 pairs per trajectory |
| 总时间范围 | $[0,1]$; benchmark horizon $[0,0.7]$ |
| 保存时间间隔 | $0.05$ raw; selected interval $0.1$ |
| 生成软件/数值方法 | AZEBAN；$128^2$。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $\alpha_i$ | 小尺度涡片扰动幅度；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[0,0.003125]$ |
| $\beta_i$ | 扰动相位；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[0,1]$ |
| $p$ | 随机扰动数；IC / data-distribution parameter | 固定 | $10$ |
| $\rho_s$ | 平滑宽度；IC / data-distribution parameter | 固定 | $5/128$ |
| baseline amplitude | 基准正弦界面振幅；IC / data-distribution parameter | 固定 | $0.2$ |

**汇总：** 平滑宽度、基准振幅、扰动数、黏度和扰动分布均可调整；发布数据只改变小扰动幅度与相位。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`velocity: [20000, 21, 3, 128, 128]`
- 原始通道/变量：HF 卡列 $[u_x,u_y,\text{passive tracer}]$，但官方 VortexSheet 加载器不支持 tracer。
- 期望组装文件名：`NS-SVS.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[4,128,128] → [4,128,128]`
- 通道定义：$[1,u_x,u_y,0]$。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

AZEBAN；$128^2$。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/NS-SVS --repo-type dataset --local-dir ./NS-SVS
```

进入下载目录并运行仓库自带组装脚本：

```bash
cd ./NS-SVS
python assemble_data.py --input_dir . --output_file NS-SVS.nc
```

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 近奇异涡片、极小扰动触发卷起、对数值耗散和分辨率敏感。

## 已知来源差异与复现注意事项

- 论文附录 B.2.4 最后一段误写“generated 20000 NS-SL trajectories”；上下文、表格、图号与仓库均表明应为 NS-SVS。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: NS-SVS](https://huggingface.co/datasets/camlab-ethz/NS-SVS)。
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
