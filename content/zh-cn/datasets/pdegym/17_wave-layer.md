---
title: Wave-Layer：随机分层介质中的波动方程
parent_dataset: PDEgym
subset: Wave-Layer
role: "下游任务：分层不连续 PDE 系数"
pde_family: "Variable-coefficient wave equation"
spatial_dimension: 2
time_dependent: true
official_code_identifier: wave.Layer
official_data_repository: "https://huggingface.co/datasets/camlab-ethz/Wave-Layer"
paper: "https://arxiv.org/abs/2405.19101"
license: "CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories)"
linkTitle: Wave-Layer
weight: 170
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEgym
summary: "高斯初始波源在随机弯曲、分片常波速的垂向分层介质中传播。"
description: "高斯初始波源在随机弯曲、分片常波速的垂向分层介质中传播。"

---

# Wave-Layer：随机分层介质中的波动方程

**描述：** 高斯初始波源在随机弯曲、分片常波速的垂向分层介质中传播。 与 Wave-Gauss 的光滑波速场相比，本任务含系数间断和随机层界面，更接近分层地下介质。

**数据集作者/维护者：** POSEIDON 作者团队，ETH Zurich Computational and Applied Mathematics Laboratory。
**生成代码或软件：** 有限差分法；$128^2$。

## 基本信息

| 项目 | 内容 |
|---|---|
| 所属数据集 | [PDEgym](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651) |
| 子数据集/逻辑任务 | **Wave-Layer** |
| 角色 | 下游任务：分层不连续 PDE 系数 |
| PDE 类型 | Variable-coefficient wave equation |
| 空间维数 | 2D |
| 时间依赖 | 是 |
| 官方代码标识 | `wave.Layer` |
| 官方数据页 | [Wave-Layer](https://huggingface.co/datasets/camlab-ethz/Wave-Layer) |
| 官方代码 | [camlab-ethz/poseidon](https://github.com/camlab-ethz/poseidon) |
| 论文 | [POSEIDON: Efficient Foundation Models for PDEs](https://arxiv.org/abs/2405.19101) |
| 许可 | CC BY-NC 4.0 (as stated on the official Hugging Face dataset repositories) |

## 方程

$$
\partial_{tt}u-c(x,y)^2\Delta u=0.
$$

为了写成一阶解算子，可以扩充为
$$
u_t=v,\qquad v_t=c^2\Delta u,\qquad c_t=0,$$
但 Wave-Gauss 与 Wave-Layer 的实际发布文件只显式保存位移轨迹 $u$ 和静态系数场 $c$，并不保存 $v=u_t$ 通道。

初始位移的高斯源规则与 Wave-Gauss 相同。波速 $c(x,y)$ 在每个随机弯曲层内为常数；层界面由 10 个正弦模态构造并缩放以避免相交。

### 物理量

- 坐标采用二维 Cartesian 坐标 $(x,y)$；除特别说明外，坐标由数组索引隐式给定，并不作为额外通道。
- 原始发布场、论文算子场和官方模型接口可能不同，具体见“数据格式与通道”。

## 算子任务

$[u(t_i),c]\mapsto[u(t_j),c]$，评价 $u$。

## About the data / 数据说明

| 字段 | 内容 |
|---|---|
| 离散数据维度 | `solution: [10512, 15, 128, 128]; c: [10512, 128, 128]` |
| 可用物理场 | `solution` 为 $u$，`c` 为静态分层波速。 |
| 轨迹/样本数 | **10512** |
| Train / Val / Test | **10212 / 60 / 240** |
| 官方仓库总文件大小 | **15.2 GB** |
| 网格类型 | 均匀 Cartesian Eulerian 网格 |
| 空间区域 | $D=(0,1)^2$ |
| 初始条件/输入 | 同 Wave-Gauss 的随机高斯位移源。 |
| 边界条件 | 吸收边界条件 |
| 保存快照数 | 15 |
| 论文/代码选用快照 | 8 (indices 0,2,…,14) |
| all2all 对数 | 36 pairs per trajectory |
| 总时间范围 | HF card: $[0,1]$; paper benchmark uses index 14 as $t=0.7$ |
| 保存时间间隔 | source conflict; follow code/indexing for reproduction |
| 生成软件/数值方法 | 有限差分法；$128^2$。 |
| 近似生成时间 | 论文与官方数据卡未逐条报告单轨迹生成时间。 |
| 生成硬件与精度 | 数据生成硬件与精度未按子数据集完整列出；论文附录仅给出求解器与生成/发布分辨率。 |

## 可调参数、实际变化参数与固定参数

| 参数 | 含义/类型 | 数据集中的状态 | 取值或分布 |
|---|---|---|---|
| $n_{layer}$ | 介质层数；PDE coefficient geometry | 逐轨迹变化 | $\mathcal U\{3,4,5,6\}$ |
| interface modes | 每条层界面的正弦模态数；IC / data-distribution parameter | 固定构造 | $10$ |
| interface coefficients | 层界面随机系数/偏置；PDE coefficient geometry | 逐轨迹变化后缩放 | sampled in $(0,1)$ |
| $c_i$ | 每层常波速；PDE coefficient | 逐层、逐轨迹变化 | $\mathcal U[2000,5000]$ |
| $n$ | 初始高斯源数；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U\{2,3,4,5,6\}$ |
| $s_i$ | 源宽度；IC / data-distribution parameter | 逐轨迹变化 | $\mathcal U[0.039,0.156]$ |

**汇总：** 层数、层波速、界面形状和源几何在数据中变化；各向异性、初速度、吸收层和界面物理未扫描。

> 参数表中的“可调”要分清三层：方程在数学上允许改变；生成器可通过改代码改变；官方发布数据是否真的对其进行了采样扫描。没有显式标注的随机初值参数通常只编码在场实现中，而不是单独的 metadata 向量。

## 数据格式、输入输出尺寸与通道

### 原始发布文件

- 原始形状：`solution: [10512, 15, 128, 128]; c: [10512, 128, 128]`
- 原始通道/变量：`solution` 为 $u$，`c` 为静态分层波速。
- 期望组装文件名：`Wave-Layer.nc`

### 官方 POSEIDON 模型接口

- 单个输入输出对：`[2,128,128] → [2,128,128]`
- 通道定义：$[u(t_i),c]\to[u(t_j),c]$。
- 批处理后一般为 `[B,C,H,W]`；轨迹原始文件通常为 `[N,T,C,H,W]`，二者不可混淆。
- 对时间依赖任务，官方 `BaseTimeDataset` 返回两个快照以及标量 lead time；all2all 枚举选定时间点中所有 $t_i\le t_j$ 的快照对。

## 数值生成

有限差分法；$128^2$。

标准化只属于训练实现：官方加载器使用预计算均值/标准差，不会增加物理通道，也不表示 PDE 参数发生变化。

## 下载与组装

```bash
pip install -U huggingface_hub
huggingface-cli download camlab-ethz/Wave-Layer --repo-type dataset --local-dir ./Wave-Layer
```

进入下载目录并运行仓库自带组装脚本：

```bash
cd ./Wave-Layer
python assemble_data.py --input_dir . --output_file Wave-Layer.nc
```

下载后，可把组装文件路径传给官方训练/推理脚本的 `--data_path`。稳态数据可在代码标识后添加 `.time`，把稳态映射包装成归一化 lead time 为 1 的长时间极限任务；这不意味着原始文件中存在物理时间轨迹。

## 有趣与困难之处

- 波速系数跨层间断、界面随机弯曲，导致反射、透射和复杂波前。

## 已知来源差异与复现注意事项

- 论文附录 B.2.11 写保存 21 帧，但官方 HF 发布卡给出 15 帧；原始尺寸以实际发布数据为准。
- 论文的一阶辅助通道 $v=u_t$ 未在发布文件中保存。

## 来源

1. [POSEIDON paper and Supplementary Material](https://arxiv.org/abs/2405.19101)，重点参见附录 B。
2. [Official POSEIDON code](https://github.com/camlab-ethz/poseidon)，数据标识与加载器位于 [`scOT/problems`](https://github.com/camlab-ethz/poseidon/tree/main/scOT/problems)。
3. [Official PDEgym collection](https://huggingface.co/collections/camlab-ethz/pdegym-665472c2b1181f7d10b40651)。
4. [Official dataset repository: Wave-Layer](https://huggingface.co/datasets/camlab-ethz/Wave-Layer)。
