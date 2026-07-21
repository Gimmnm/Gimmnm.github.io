---
title: "CE-KH：Kelvin–Helmholtz 剪切层不稳定性"
parent_dataset: PDEgym
subset: CE-KH
role: 预训练算子
pde_family: "Compressible Euler"
spatial_dimension: 2
time_dependent: true
official_code_identifier: fluids.compressible.KelvinHelmholtz
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/CE-KH"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: CE-KH
weight: 50
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "随机扰动双界面的可压缩 Kelvin–Helmholtz 剪切层。"
description: "随机扰动双界面的可压缩 Kelvin–Helmholtz 剪切层。"

---

# CE-KH：Kelvin–Helmholtz 剪切层不稳定性

**描述：** 随机扰动双界面的可压缩 Kelvin–Helmholtz 剪切层。 两层流体具有不同密度和相反的水平速度，小幅随机界面扰动触发卷起与混合。该算子向预训练集提供典型的剪切不稳定性。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。
**生成代码或软件：** ALSVINN；$512^2\to128^2$。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **CE-KH** |
| 角色 | 预训练算子 |
| PDE 类型 | Compressible Euler |
| 空间维数 | 2D |
| 时间依赖 | 是 |
| 官方代码标识 | `fluids.compressible.KelvinHelmholtz` |
| 官方数据页 | [CE-KH](https://huggingface.co/datasets/camlab-ethz/CE-KH) |
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

初值为
$$
(\rho,v_x,v_y,p)|_{t=0}=\begin{cases}
(1,0.5,0,2.5),&y<0.25+\sigma_0(x)\ \text{或}\ y>0.75+\sigma_1(x),\\
(2,-0.5,0,2.5),&\text{否则},
\end{cases}
$$
$$
\sigma_i(x)=\varepsilon\frac{\sum_{j=1}^{p}\alpha_{ij}\cos(2\pi j(x+\beta_{ij}))}{\sum_{j=1}^{p}\alpha_{ij}},\qquad \varepsilon=0.05.
$$

### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

随机界面形状的剪切层初值 $\mapsto [\rho,v_x,v_y,p](t)$。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `data: [10000, 21, 5, 128, 128]` |
| 可用物理场 | $[\rho,v_x,v_y,p,E]$。 |
| 轨迹/样本数 | **10000** |
| Train / Val / Test | **9640 / 120 / 240** |
| 官方仓库总文件大小 | **68.8 GB** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=[0,1]^2$ |
| 初始条件/输入 | 双剪切层，界面由随机 Fourier 形状扰动。 |
| 边界条件 | 周期边界条件 |
| 保存快照数 | 21 |
| 论文/代码选用快照 | 11 (indices 0,2,…,20) |
| all2all 对数 | 66 pairs per trajectory |
| 总时间范围 | $[0,1]$ |
| 保存时间间隔 | $0.05$ |
| 生成软件/数值方法 | ALSVINN；$512^2\to128^2$。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $\alpha_{ij}$ | 界面模态权重；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[0,1]$ |
| $\beta_{ij}$ | 界面模态相位；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[0,1]$ |
| $\varepsilon$ | 界面扰动总幅度；IC / data-distribution parameter | 固定 | $0.05$ |
| $p$ | 扰动模态数；IC / data-distribution parameter | 附录未明确发布数值 | not specified |
| $\rho_1,\rho_2$ | 两层密度；IC / data-distribution parameter | 固定 | $1,2$ |
| $v_{x,1},v_{x,2}$ | 两层水平速度；IC / data-distribution parameter | 固定 | $0.5,-0.5$ |
| $\gamma$ | 比热比；PDE coefficient | 固定 | $1.4$ |

**汇总：** 密度比、速度差、压力、界面厚度/幅度、模态数和 $\gamma$ 均可调；发布数据只随机化界面模态权重与相位。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`data: [10000, 21, 5, 128, 128]`
- 原始通道/变量：$[\rho,v_x,v_y,p,E]$。
- 期望组装文件名：`CE-KH.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[4,128,128] → [4,128,128]`
- 通道定义：$[\rho,v_x,v_y,p]$。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

ALSVINN；$512^2\to128^2$。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/CE-KH --repo-type dataset --local-dir ./CE-KH
```

进入下载目录并运行仓库自带组装脚本：

```bash
cd ./CE-KH
python assemble_data.py --input_dir . --output_file CE-KH.nc
```

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 强非线性卷起、混合层增长以及多尺度涡旋形成。

## 已知来源差异与复现注意事项

- 附录公式含模态数 $p$，但该小节未明确给出发布值。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: CE-KH](https://huggingface.co/datasets/camlab-ethz/CE-KH)。
