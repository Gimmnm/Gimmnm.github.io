---
title: "FlowBench：二维复杂几何热耦合顶盖驱动方腔（变化 Reynolds 数）"
parent_dataset: FlowBench
subset: LDC_NSHT_2D_variable-Re
equation_family: "incompressible Navier-Stokes + heat transfer, Boussinesq coupling"
spatial_dimension: 2
temporal_regime: steady
task: geometry-Reynolds-Richardson-to-coupled-fields
geometry_families: ""
license: CC-BY-NC-4.0
last_verified: 2026-07-21
linkTitle: "LDC NSHT 2D (var Re)"
weight: 30
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: FlowBench
summary: "同时改变复杂几何、Reynolds 数和浮力/惯性比例，预测稳态速度、压力与温度。"
description: "同时改变复杂几何、Reynolds 数和浮力/惯性比例，预测稳态速度、压力与温度。"

---

# 二维热耦合顶盖驱动方腔：变化 Reynolds 数

**一句话描述：** 同时改变复杂几何、Reynolds 数和浮力/惯性比例，预测稳态速度、压力与温度。

**较长描述：** 该子集与 constant-Re NSHT 使用相同的耦合 PDE 和边界条件，但同时扫描惯性/黏性比例与浮力强度，因此更适合训练跨物理区间的多参数算子。

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

$$
\frac{\partial \mathbf u}{\partial t}
+(\mathbf u\cdot\nabla)\mathbf u
=-\nabla p
+\frac{1}{\mathrm{Re}}\nabla^2\mathbf u
+\mathrm{Ri}\,\theta\,\mathbf e_g
+\mathbf f,
$$

$$
\nabla\cdot\mathbf u=0,
$$

$$
\frac{\partial\theta}{\partial t}
+\mathbf u\cdot\nabla\theta
=\frac{1}{\mathrm{Pe}}\nabla^2\theta,
$$

以及

$$
\mathrm{Ri}=\frac{\mathrm{Gr}}{\mathrm{Re}^2},
\qquad
\mathrm{Gr}=\mathrm{Ri}\,\mathrm{Re}^2,
\qquad
\mathrm{Pe}=0.7\,\mathrm{Re}.
$$

这意味着输入 $\mathrm{Ri}$ 和 $\mathrm{Re}$ 已足以恢复 $\mathrm{Gr}$，无需把三者都作为独立通道。

## 计算域与边界条件

$$
\Omega=[0,2]\times[0,2].
$$

速度边界：

- 顶壁 $(u,v)=(1,0)$；
- 其余三个外壁和物体表面 $(u,v)=(0,0)$。

温度边界：

- 底壁 $\theta=1$；
- 顶壁 $\theta=0$；
- 左、右壁 $\partial_n\theta=0$；
- 物体表面 $\theta=0$。


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
| 物理问题 | 2D 不可压缩 NS + 热传递，Boussinesq 耦合 |
| 稳态/瞬态 | 稳态 |
| 样本数 | **3000** |
| 几何数 | 约 300 |
| 每几何条件数 | 约 10 |
| Reynolds 范围 | 论文总体 $[10,10^3]$ |
| Grashof 范围 | 论文总体 $[10,10^7]$ |
| 发布分辨率 | $128^2$、$256^2$、$512^2$ |
| 轨迹长度 | 1 个稳态最终快照 |
| 当前目录体积 | 约 **34.6 GB** |
| 数据目录 | `LDC_NSHT_2D_variable-Re/` |

### 张量

官方 DataPrep 对该拆分写为

$$
X\in\mathbb R^{3000\times4\times N_x\times N_y},
\qquad
X=[\mathrm{Ri},\mathrm{Re},g,s],
$$

$$
Y_{\rm field}\in\mathbb R^{3000\times4\times N_x\times N_y},
\qquad
Y_{\rm field}=[u,v,p,\theta].
$$

旧版 README 可在 $Y$ 中追加 `C*` 辅助通道，编码 $C_D,C_L,\mathrm{Nu}$。

## 参数变化设计

| 参数 | 是否变化 | 关系/范围 |
|---|---:|---|
| 几何 | 是 | G1/G2/G3 |
| $\mathrm{Re}$ | 是 | 论文总体 $10$–$10^3$ |
| $\mathrm{Ri}$ | 是 | 浮力/惯性比 |
| $\mathrm{Gr}$ | 随前两者变化 | $\mathrm{Gr}=\mathrm{Ri}\mathrm{Re}^2$ |
| $\mathrm{Pe}$ | 随 Re 联动 | $0.7\mathrm{Re}$ |
| $\mathrm{Pr}$ | 否 | 0.7 |
| 域和物体位置 | 否 | 固定 |
| 速度/温度 BC | 否 | 固定 |
| 时间 | 否 | 稳态 |

论文示例给出过 $(\mathrm{Ri},\mathrm{Re})$ 组合
$(0.321,16)$、$(1.76,640)$、$(2.847,720)$、$(9.452,952)$，展示了惯性和浮力共同变化时的流场与温度场差异。这些只是可视化示例，不应被误解为完整参数集合。


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

- 同时存在 geometry shift、Reynolds shift 和 convection-regime shift；
- 相同 Richardson 数在不同 Reynolds 数下仍可能有不同边界层厚度和涡结构；
- $\mathrm{Re}$ 增大降低相对黏性作用，$\mathrm{Ri}$ 增大强化浮力环流，两者可能产生竞争；
- 模型需要同时预测四个耦合场并保持不可压缩性和能量方程一致性；
- 非常适合研究参数编码、无量纲条件 token 和多物理 foundation model。

## 版本与文件注意事项

1. 论文合并表把输入写为 `[Re, Gr, g, s]`，实际 DataPrep 使用 `[Ri, Re, g, s]`；
2. 两种写法信息等价，但模型预处理必须保持一致；
3. `C*` 可能作为辅助打包通道出现，不是局部状态；
4. mask/SDF 的符号和数值范围需从文件验证；
5. 若随机切分样本，同一几何可能同时出现在训练集和测试集；几何泛化实验应按几何编号切分。


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
    allow_patterns=["LDC_NSHT_2D_variable-Re/128x128/*"],
)
```

把 `LDC_NSHT_2D_variable-Re/128x128/*` 换成上面代码中的实际路径即可。若数据量很大，建议先下载一种几何或一个分辨率，而不是一次下载完整 FlowBench。

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



## 引用

使用该数据时应引用 FlowBench 论文：

```bibtex
@article{tali2024flowbench,
  title   = {FlowBench: A Large Scale Benchmark for Flow Simulation over Complex Geometries},
  author  = {Tali, Ronak and Rabeh, Ali and Yang, Cheng-Hau and Shadkhah, Mehdi
             and Karki, Samundra and Upadhyaya, Abhisek and Dhakshinamoorthy, Suriya
             and Saadati, Marjan and Sarkar, Soumik and Krishnamurthy, Adarsh
             and Hegde, Chinmay and Balu, Aditya and Ganapathysubramanian, Baskar},
  journal = {arXiv preprint arXiv:2409.18032},
  year    = {2024}
}
```

数据和官方工具代码标注为 **CC-BY-NC-4.0**；商业使用前应核对许可证原文。



## 资料来源与可信度说明

本文档按以下优先级交叉核对：

1. [FlowBench 论文与附录](https://arxiv.org/abs/2409.18032)；
2. [官方 Hugging Face 数据仓库](https://huggingface.co/datasets/BGLab/FlowBench)；
3. [官方数据生成、下采样与张量整理代码](https://github.com/baskargroup/flowbench-tools)；
4. [官方训练与评测代码 Geometry Matters](https://github.com/baskargroup/GeometryMatters)；
5. [FlowBench 项目主页](https://baskargroup.bitbucket.io/FlowBench/)。

论文、代码和当前数据仓库并非完全同一版本。本文档会把“论文定义”“旧版数据整理脚本”和“当前仓库状态”分开写明。  
核对日期： **2026-07-21**。
