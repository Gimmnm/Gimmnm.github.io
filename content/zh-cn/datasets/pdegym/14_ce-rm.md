---
title: "CE-RM：Richtmyer–Meshkov 不稳定性"
parent_dataset: PDEgym
subset: CE-RM
role: 下游任务：激波–界面不稳定性
pde_family: "Compressible Euler"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.compressible.RichtmyerMeshkov
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/CE-RM"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: CE-RM
weight: 140
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "冲击波撞击随机扰动密度界面的 Richtmyer–Meshkov 轨迹。"
description: "冲击波撞击随机扰动密度界面的 Richtmyer–Meshkov 轨迹。"

---

# CE-RM：Richtmyer–Meshkov 不稳定性

**描述：** 冲击波撞击随机扰动密度界面的 Richtmyer–Meshkov 轨迹。 该经典不稳定性产生界面增长、混合和多尺度结构。与预训练 Euler 数据相比，它使用不同的生成代码、时间尺度和数据规模。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。
**生成代码或软件：** FISH 高分辨率有限体积流体代码；发布分辨率 $128^2$。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **CE-RM** |
| 角色 | 下游任务：激波–界面不稳定性 |
| PDE 类型 | Compressible Euler |
| 空间维数 | 2D |
| 时间依赖 | 是 |
| 官方代码标识 | `fluids.compressible.RichtmyerMeshkov` |
| 官方数据页 | [CE-RM](https://huggingface.co/datasets/camlab-ethz/CE-RM) |
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

附录给出
$$
p_0(x,y)=\begin{cases}20,&\sqrt{x^2+y^2}<0.1,\\1,&\text{否则},\end{cases}\qquad
\rho_0(x,y)=\begin{cases}2,&|x|<I(x,y,\omega),\\1,&\text{否则},\end{cases}
$$
$$
v_x^0=v_y^0=0,\qquad I=0.25+\epsilon\sum_{j=1}^{10}a_j\sin\bigl(2\pi((x,y)+b_j)\bigr).
$$

### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$[\rho,v_x,v_y,p](0)\mapsto[\rho,v_x,v_y,p](t)$。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `solution: [1260, 21, 5, 128, 128]` |
| 可用物理场 | HF 卡：$[\rho,v_x,v_y,p,\text{passive tracer}]$；论文与官方加载器只使用前 4 通道。 |
| 轨迹/样本数 | **1260** |
| Train / Val / Test | **1030 / 100 / 130** |
| 官方仓库总文件大小 | **8.67 GB** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=[0,1]^2$ |
| 初始条件/输入 | 局部高压冲击与随机扰动密度界面，初速度为零。 |
| 边界条件 | 论文指定周期边界 |
| 保存快照数 | 21 |
| 论文/代码选用快照 | paper evaluation at raw index 14; standard downstream pairing uses selected snapshots through index 14 |
| all2all 对数 | up to 36 pairs under the standard 8-snapshot setup |
| 总时间范围 | $[0,2]$; evaluated at $t=1.4$ |
| 保存时间间隔 | $0.1$ |
| 生成软件/数值方法 | FISH 高分辨率有限体积流体代码；发布分辨率 $128^2$。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $a_j$ | 界面扰动权重；IC / data-distribution parameter | 逐轨迹变化并归一化 | $\mathcal U[0,1]$, $\sum_j a_j=1$ |
| $b_j$ | 界面扰动相位/偏移；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[0,1]$ |
| $K$ | 扰动模态数；IC / data-distribution parameter | 固定 | $10$ |
| $\epsilon$ | 界面扰动幅度；IC / data-distribution parameter | 仅说明 $>0$，未给数值 | not specified |
| density ratio | 两侧密度；IC / data-distribution parameter | 固定 | $2/1$ |
| pressure levels | 冲击/背景压力；IC / data-distribution parameter | 固定 | $20/1$ |

**汇总：** 冲击强度、密度比、$\epsilon$、$K$、$\gamma$ 与边界均可调；发布数据主要改变界面扰动谱。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`solution: [1260, 21, 5, 128, 128]`
- 原始通道/变量：HF 卡：$[\rho,v_x,v_y,p,\text{passive tracer}]$；论文与官方加载器只使用前 4 通道。
- 期望组装文件名：`CE-RM.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[4,128,128] → [4,128,128]`
- 通道定义：$[\rho,v_x,v_y,p]$。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

FISH 高分辨率有限体积流体代码；发布分辨率 $128^2$。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/CE-RM --repo-type dataset --local-dir ./CE-RM
```

进入下载目录并运行仓库自带组装脚本：

```bash
cd ./CE-RM
python assemble_data.py --input_dir . --output_file CE-RM.nc
```

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 激波驱动的界面不稳定性、混合与复杂小尺度结构；轨迹数远少于多数 PDEgym 子集。

## 已知来源差异与复现注意事项

- 附录对 $I(x,y,\omega)$ 的向量正弦记法与坐标原点较简略，精确复现应以生成代码为准。
- 附录没有给出 $\epsilon$ 的数值。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: CE-RM](https://huggingface.co/datasets/camlab-ethz/CE-RM)。
