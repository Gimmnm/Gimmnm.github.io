---
title: "ACE：Allen–Cahn 反应–扩散相场"
parent_dataset: PDEgym
subset: ACE
role: "下游任务：新 PDE/相变物理"
pde_family: "Allen–Cahn reaction–diffusion"
spatial_dimension: 2
time_dependent: true
official_code_identifier: reaction_diffusion.AllenCahn
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/ACE"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: ACE
weight: 180
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "二维周期区域上的非线性 Allen–Cahn 相变轨迹。"
description: "二维周期区域上的非线性 Allen–Cahn 相变轨迹。"

---

# ACE：Allen–Cahn 反应–扩散相场

> **一句话描述：** 二维周期区域上的非线性 Allen–Cahn 相变轨迹。

## 更长描述

该任务与预训练中的对流主导流体方程差异很大：动力学由扩散、双稳态反应和界面运动主导。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。  
**生成代码或软件：** 有限差分法；$128^2$。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **ACE** |
| 角色 | 下游任务：新 PDE/相变物理 |
| PDE 类型 | Allen–Cahn reaction–diffusion |
| 空间维数 | 2D |
| 时间依赖 | 是 |
| 官方代码标识 | `reaction_diffusion.AllenCahn` |
| 官方数据页 | [ACE](https://huggingface.co/datasets/camlab-ethz/ACE) |
| 官方代码 | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| 论文 | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| 许可 | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## 方程


$$
\partial_tu=\Delta u-\epsilon^2u(u^2-1).
$$
初值
$$
u_0(x,y)=\frac1{K^2}\sum_{i,j=1}^{K}a_{ij}(i^2+j^2)^{-r}\sin(\pi ix)\sin(\pi jy).
$$


### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$u_0\mapsto u(t)$。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `solution: [15000, 20, 128, 128]` |
| 可用物理场 | 单通道相场/浓度 $u$。 |
| 轨迹/样本数 | **15000** |
| Train / Val / Test | **14700 / 60 / 240** |
| 官方仓库总文件大小 | **19.7 GB** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=(0,1)^2$ |
| 初始条件/输入 | 随机衰减 Fourier 正弦级数。 |
| 边界条件 | 周期边界条件 |
| 保存快照数 | 20 |
| 论文/代码选用快照 | 8 (indices 0,2,…,14) |
| all2all 对数 | 36 pairs per trajectory |
| 总时间范围 | $[0,0.0002]$ |
| 保存时间间隔 | nominal endpoint-inclusive interval $0.0002/19$ |
| 生成软件/数值方法 | 有限差分法；$128^2$。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $K$ | 初值频谱截断；IC / data-distribution parameter | 逐轨迹变化 | uniform integer in $[16,32]$ |
| $r$ | 频谱衰减指数；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[0.7,1.0]$ |
| $a_{ij}$ | 随机初值系数；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[-1,1]$ |
| $\epsilon$ | 反应参数；PDE coefficient | 固定 | $220$ in the paper text |
| diffusion coefficient | 扩散系数；PDE coefficient | 固定 | $1$ |

**汇总：** 扩散系数、反应率/界面宽度、势函数和边界均可调；发布数据只改变初值频谱。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`solution: [15000, 20, 128, 128]`
- 原始通道/变量：单通道相场/浓度 $u$。
- 期望组装文件名：`ACE.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[1,128,128] → [1,128,128]`
- 通道定义：$u(t_i)\to u(t_j)$。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

有限差分法；$128^2$。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/ACE --repo-type dataset --local-dir ./ACE
```

进入下载目录并运行仓库自带组装脚本：

```bash
cd ./ACE
python assemble_data.py --input_dir . --output_file ACE.nc
```

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 薄界面运动、非线性双稳态反应和极短物理时间尺度。

## 已知来源差异与复现注意事项

- 论文文字称 reaction rate $\epsilon=220$，公式写 $\epsilon^2$；精确复现时应直接核对生成器对参数的实现，避免二次平方。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: ACE](https://huggingface.co/datasets/camlab-ethz/ACE)。
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
