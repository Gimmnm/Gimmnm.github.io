---
title: "FlowBench：二维复杂几何顶盖驱动方腔 Navier–Stokes"
parent_dataset: FlowBench
subset: LDC_NS_2D
equation_family: "incompressible Navier-Stokes"
spatial_dimension: 2
temporal_regime: steady
task: geometry-and-Reynolds-to-field
geometry_families: ""
license: CC-BY-NC-4.0
last_verified: 2026-07-21
linkTitle: "LDC NS 2D"
weight: 10
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: FlowBench
summary: "在带有内部复杂静止物体的二维方腔中，以移动顶盖驱动不可压缩流动，并输出稳态速度和压力场。"
description: "在带有内部复杂静止物体的二维方腔中，以移动顶盖驱动不可压缩流动，并输出稳态速度和压力场。"

---

# 二维复杂几何顶盖驱动方腔（LDC–NS–2D）

**描述：** 在带有内部复杂静止物体的二维方腔中，以移动顶盖驱动不可压缩流动，并输出稳态速度和压力场。 该子集研究同一不可压缩 Navier–Stokes 方程在不同 Reynolds 数和不同复杂物体边界下的稳态解。它是 FlowBench 最标准的 geometry-to-field 子集，也是官方 Geometry Matters 工作主要使用的部分。

**数据集团队：** FlowBench / Baskar Group（Iowa State University 等合作单位）。
**生成软件：** Dendro/Dendro-KT finite-element framework with SBM。

## 所属数据集与链接

| 项目 | 内容 |
|---|---|
| 所属基准 | **FlowBench** |
| 论文 | [arXiv:2409.18032](https://arxiv.org/abs/2409.18032) |
| 论文 PDF | [PDF](https://arxiv.org/pdf/2409.18032) |
| 官方数据 | [BGLab/FlowBench](https://huggingface.co/datasets/BGLab/FlowBench) |
| 官方工具代码 | [baskargroup/flowbench-tools](https://github.com/baskargroup/flowbench-tools) |
| 训练/评测代码 | [baskargroup/GeometryMatters](https://github.com/baskargroup/GeometryMatters) |
| 项目主页 | [FlowBench website](https://baskargroup.bitbucket.io/FlowBench/) |
| 许可证 | **CC-BY-NC-4.0** |
| 数据格式 | NumPy compressed archives (`.npz`) |

## 方程

无量纲不可压缩 Navier–Stokes 方程为

$$
\frac{\partial \mathbf u}{\partial t}
+(\mathbf u\cdot\nabla)\mathbf u
=-\nabla p+\frac{1}{\mathrm{Re}}\nabla^2\mathbf u+\mathbf f,
$$

$$
\nabla\cdot\mathbf u=0,
$$

其中

$$
\mathbf u=(u,v),
\qquad
\mathrm{Re}=\frac{UL}{\nu}.
$$

- $u$：$x$ 方向速度；
- $v$：$y$ 方向速度；
- $p$：无量纲压力；
- $\nu$：运动黏度；
- $\mathrm{Re}$：惯性与黏性作用的相对强度。

数据保存收敛后的**稳态场**，因此每个样本不是一条时间轨迹；机器学习映射通常写成

$$
(\mathrm{Re},g,s)\longmapsto(u,v,p).
$$

## 计算域、坐标与边界条件

空间域：

$$
\Omega=[0,2]\times[0,2].
$$

- $x$：水平方向；
- $y$：竖直方向；
- 内部复杂物体置于方腔中部并保持静止。

速度边界条件：

$$
(u,v)=(1,0),\qquad y=2,
$$

$$
(u,v)=(0,0),\qquad x=0,\ x=2,\ y=0,
$$

$$
(u,v)=(0,0),\qquad \partial\Omega_{\rm object}.
$$

即顶壁以单位速度沿 $x$ 方向移动，其余外壁和物体表面均为无滑移壁面。论文未在数据章节明确给出压力 gauge 的具体实现。

## 几何条件

该子集使用 FlowBench 的三类二维复杂几何。论文总表将二维部分概括为 **300 个形状**，即每类约 100 个。

### G1：NURBS 参数曲线

- 使用均匀 knot vector；
- B-spline 基函数次数固定为二次；
- 控制点数量固定为 8；
- 随机改变 8 个控制点的位置；
- 拒绝不光滑、断裂或自交的曲线；
- 形状归一化到单位正方形 $[0,1]^2$。

一般 NURBS 曲线可写为

$$
\mathbf C(t)=
\frac{\sum_i N_{i,2}(t)w_i\mathbf P_i}
{\sum_i N_{i,2}(t)w_i}.
$$

论文只明确随机改变控制点位置，没有把权重 $w_i$ 列为数据集扫描参数。

### G2：谐波径向曲线

论文将其称作 spherical harmonics；二维实现实际采用 Fourier 型径向函数：

$$
r(t)=0.5+\sum_{n=1}^{N}
\left(a_n\cos nt+b_n\sin nt\right),
\qquad t\in[0,2\pi].
$$

- $N$ 从 $\{8,\ldots,15\}$ 中随机选择；
- $a_n,b_n\in[0,0.2]$；
- 在 $[0,2\pi]$ 上使用 500 个等距采样点；
- 通过
  $$
  \widehat r(t)=0.5\,\frac{r(t)}{r_{\max}}
  $$
  归一化，使边界点到中心的最大距离不超过 $0.5$。

### G3：SkelNetOn 非参数轮廓

- 从 SkelNetOn 灰度形状数据中选择动物、昆虫、鸟类等轮廓；
- 采用固定 Gaussian blur，$\sigma=2$；
- 平滑细小、锯齿和跨分辨率难以解析的结构；
- 再缩放到 $[0,1]^2$。

G3 不是低维连续参数族，通常比 G1/G2 更适合作为几何分布外测试。

### 几何的网格表示

论文定义两种与流场网格同分辨率的输入：

1. **binary geometry mask** $g(\mathbf x)$：论文语义是物体内为 1、物体外为 0；
2. **signed distance field** $s(\mathbf x)$：论文语义是物体内为负、物体外为正、边界为 0。

$$
s(\mathbf x)=
\begin{cases}
<0,&\mathbf x\text{ 在物体内},\\
0,&\mathbf x\text{ 在物体边界},\\
>0,&\mathbf x\text{ 在流体区}.
\end{cases}
$$

**文件级注意事项：** 部分旧版 DataPrep 代码把 mask 写成 `0/255`，并通过 `SDF > 0` 构造 mask；这与论文文字中的符号/数值约定不完全一致。下载后必须画出 mask 与 SDF，确认实际文件的正负号和缩放，而不要只依赖文字定义。

## 关于数据

| 属性 | 内容 |
|---|---|
| 物理问题 | 二维不可压缩 Navier–Stokes，复杂几何 LDC |
| 稳态/瞬态 | 稳态 |
| 论文样本数 | **3000** |
| 几何数 | 300：G1/G2/G3 各约 100 |
| 每几何物理条件 | 由 3000/300 可知设计上约 10 个 Reynolds 条件 |
| Reynolds 范围 | $\mathrm{Re}\in[10,10^3]$ |
| 轨迹长度 | 1 个稳态最终快照 |
| 发布分辨率 | $128\times128$、$256\times256$、$512\times512$ |
| 网格类型 | 发布数据为 uniform Cartesian arrays；原求解使用 tree-based FEM |
| 当前目录体积 | 约 **28.3 GB** |
| 数据目录 | `LDC_NS_2D/` |

### 核心物理场张量：论文定义

$$
X\in\mathbb R^{3000\times3\times N_x\times N_y},
\qquad
X=[\mathrm{Re},g,s],
$$

$$
Y_{\rm field}\in\mathbb R^{3000\times3\times N_x\times N_y},
\qquad
Y_{\rm field}=[u,v,p].
$$

$\mathrm{Re}$ 是标量，但在文件中被广播成与空间网格同尺寸的常数图。

### 官方 DataPrep 的附加通道

官方 DataPrep README 将输出示意写为

```text
Y[3000][u, v, p, C][Nx][Ny]
```

其中 `C` 是由常数文件读取的 $C_D/C_L$ 工程统计量打包，不是局部 PDE 场。论文 Appendix Table 9 的核心输出只列 $[u,v,p]$。因此使用数据时应区分：

- **物理场通道**：$u,v,p$；
- **可能存在的辅助通道**：打包后的 $C_D,C_L$；
- 不要把辅助通道解释成第四个局部状态变量。

## 可调参数、实际变化参数与固定参数

| 项目 | 求解器理论上可调 | 该子集中实际变化 | 该子集中固定 |
|---|---:|---:|---|
| Reynolds 数 | 是 | 是 | — |
| 几何形状 | 是 | 是 | 三种生成机制固定 |
| 几何位置 | 是 | 否 | 方腔中部 |
| 顶盖速度 | 是 | 否 | $(1,0)$ |
| 外壁条件 | 是 | 否 | 三个静止无滑移壁 |
| 物体条件 | 是 | 否 | 静止、无滑移 |
| 密度/黏度单独输入 | 是 | 否 | 由无量纲化和 $\mathrm{Re}$ 概括 |
| Mach 数/可压缩性 | 不属于本子集 | 否 | 不可压缩 |
| 时间 | 是 | 否 | 只发布稳态最终场 |

## 初始条件与模拟时间

论文把该子集定义为稳态问题，没有把初始场或完整收敛过程作为数据发布。训练时不应把它当作 trajectory forecasting 数据；它更接近复杂几何条件下的稳态算子学习。

## 数值生成与后处理

- 求解框架：大规模并行、基于 quadtree/octree 的有限元 CFD/多物理代码；
- 复杂边界：Shifted Boundary Method（SBM），即在固定 Cartesian/tree mesh 上使用代理边界弱施加真实边界条件；
- 高保真目标：二维解析到 Kolmogorov 尺度附近，三维约解析到两倍 Kolmogorov 尺度；
- 后处理：使用 ParaView/VTK 将自适应高分辨率解重采样到规则张量；
- 线性代数：PETSc BCGS solver + ASM preconditioner；
- 相对求解容差：$10^{-8}$；
- 论文报告总计算成本约为 65K node-hours。

发布的低分辨率数据不是独立的低分辨率 CFD 重算，而是从 fully resolved 解后处理得到，因此可用于多分辨率学习与 super-resolution。

## 有趣且具有挑战性的地方

- 同一 PDE 在参数几何和非参数几何上求解，几何分布差异显著；
- 薄、尖和高曲率结构会产生额外的分离、再循环和局部边界层；
- 全域误差可能很小，但物体附近的压力和速度梯度仍可能很差；
- 可直接评测 $C_D$、$C_L$，以及论文定义的 SDF 近壁区域误差；
- 适合研究 mask 与 SDF、跨几何 family OOD、多分辨率泛化和 PDE residual。

## 版本与文件注意事项

1. 论文核心输出为 $[u,v,p]$，旧版 DataPrep 可追加 `C` 辅助通道；
2. mask 在论文中是 0/1，但旧脚本可能使用 0/255；
3. SDF 正负号应从实际样本验证；
4. `.npz` 文件按几何 family 和分辨率分别存放，不一定是一个包含全部 3000 条的单文件；
5. 官方推荐 80/20 随机划分，但若研究几何泛化，应按几何实例或几何 family 划分，避免同一形状的不同 Reynolds 条件泄漏到训练与测试两侧。

## 下载方式

先安装 Hugging Face Hub：

```bash
python -m pip install -U huggingface_hub
```

下载当前子目录：

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="BGLab/FlowBench",
    repo_type="dataset",
    local_dir="./FlowBench",
    allow_patterns=["LDC_NS_2D/128x128/*"],
)
```

把 `LDC_NS_2D/128x128/*` 换成上面代码中的实际路径即可。若数据量很大，建议先下载一种几何或一个分辨率，而不是一次下载完整 FlowBench。

### 检查 `.npz` 内容

```python
from pathlib import Path
import numpy as np

path = Path("PATH_TO_FILE.npz")
with np.load(path, allow_pickle=False) as archive:
    print("keys:", archive.files)
    for key in archive.files:
        array = archive[key]
        print(key, array.shape, array.dtype)
```

论文中的张量公式描述的是**语义轴顺序**。实际使用前仍应检查文件的 key、shape、channel 顺序、mask 数值和 SDF 符号。

## 资料来源与可信度说明

本文档按以下优先级交叉核对：

1. [FlowBench 论文与附录](https://arxiv.org/abs/2409.18032)；
2. [官方 Hugging Face 数据仓库](https://huggingface.co/datasets/BGLab/FlowBench)；
3. [官方数据生成、下采样与张量整理代码](https://github.com/baskargroup/flowbench-tools)；
4. [官方训练与评测代码 Geometry Matters](https://github.com/baskargroup/GeometryMatters)；
5. [FlowBench 项目主页](https://baskargroup.bitbucket.io/FlowBench/)。

论文、代码和当前数据仓库并非完全同一版本。
核对日期： **2026-07-21**。
