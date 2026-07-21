---
title: "FlowBench：二维复杂几何热耦合顶盖驱动方腔（固定 Reynolds 数）"
parent_dataset: FlowBench
subset: LDC_NSHT_2D_constant-Re
equation_family: "incompressible Navier-Stokes + heat transfer, Boussinesq coupling"
spatial_dimension: 2
temporal_regime: steady
task: geometry-and-buoyancy-to-coupled-fields
geometry_families: ""
license: CC-BY-NC-4.0
last_verified: 2026-07-21
linkTitle: "LDC NSHT 2D (const Re)"
weight: 20
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: FlowBench
summary: "固定惯性/黏性流动条件，改变浮力强度与复杂几何，预测稳态速度、压力和温度场。"
description: "固定惯性/黏性流动条件，改变浮力强度与复杂几何，预测稳态速度、压力和温度场。"

---

# 二维热耦合顶盖驱动方腔：固定 Reynolds 数

**一句话描述：** 固定惯性/黏性流动条件，改变浮力强度与复杂几何，预测稳态速度、压力和温度场。

**较长描述：** 该子集在 LDC 流动上加入热输运和 Boussinesq 浮力耦合，同时存在移动顶盖引起的强迫对流和下热上冷引起的自然对流。固定 Reynolds 数后，主要物理扫描量是 Grashof/Richardson 数。

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

FlowBench 将该系统称为 **Navier–Stokes + Heat Transfer (NSHT)**，并说明采用 Boussinesq coupling。与论文的无量纲数和能量方程一致的标准强形式为

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
=\frac{1}{\mathrm{Pe}}\nabla^2\theta.
$$

其中

$$
\mathrm{Ri}=\frac{\mathrm{Gr}}{\mathrm{Re}^2},
\qquad
\mathrm{Pe}=\mathrm{Re}\,\mathrm{Pr},
\qquad
\mathrm{Pe}=0.7\,\mathrm{Re}.
$$

因此数据生成中等效固定 $\mathrm{Pr}=0.7$。论文主要给出 SBM 有限元弱式，并未在数据章节固定浮力项的符号方向；上式的正负号取决于重力向量和参考温度定义。

## 计算域与边界条件

$$
\Omega=[0,2]\times[0,2].
$$

速度边界与纯 NS LDC 相同：

$$
(u,v)=(1,0)\quad\text{on the top wall},
$$

其余外壁和物体表面均为 $(u,v)=(0,0)$。

温度边界条件：

$$
\theta=1,\qquad y=0,
$$

$$
\theta=0,\qquad y=2,
$$

$$
\frac{\partial\theta}{\partial n}=0,
\qquad x=0,\ x=2,
$$

$$
\theta=0,
\qquad \partial\Omega_{\rm object}.
$$

底壁为热壁，顶壁和物体为冷边界，左右壁绝热。因此该问题同时包含：

- 顶盖驱动的强迫对流；
- 浮力驱动的自然对流；
- 复杂物体造成的流动分离和热边界层。


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
| 官方 DataPrep 样本数 | **2990** |
| 论文中的合并 NSHT 样本数 | constant-Re 与 variable-Re 合计 **5990** |
| Reynolds 数 | 固定；论文 fixed-Re 示例使用 $\mathrm{Re}=100$ |
| 浮力参数 | 变化 $\mathrm{Gr}$，等价变化 $\mathrm{Ri}$ |
| 论文总体 Grashof 范围 | $\mathrm{Gr}\in[10,10^7]$ |
| 发布分辨率 | $128^2$、$256^2$、$512^2$ |
| 轨迹长度 | 1 个稳态最终快照 |
| 当前目录体积 | 约 **34.5 GB** |
| 数据目录 | `LDC_NSHT_2D_constant-Re/` |

### 核心张量

官方拆分后的输入示意为

$$
X\in\mathbb R^{2990\times3\times N_x\times N_y},
\qquad
X=[\mathrm{Gr},g,s].
$$

因为 $\mathrm{Re}$ 固定，所以不必再作为信息量不同的输入通道。核心物理场为

$$
Y_{\rm field}\in\mathbb R^{2990\times4\times N_x\times N_y},
\qquad
Y_{\rm field}=[u,v,p,\theta].
$$

DataPrep README 还将输出写成 `[u,v,p,theta,C*]`；`C*` 对应从常数文件读取的 $C_D,C_L,\mathrm{Nu}$ 工程量打包，不是第五个局部 PDE 状态。

## 可调、变化与固定参数

| 项目 | 该子集处理 |
|---|---|
| 几何 | G1/G2/G3 变化 |
| Reynolds 数 | 固定；论文示例为 100 |
| Grashof 数 | 变化 |
| Richardson 数 | 因 $\mathrm{Ri}=\mathrm{Gr}/\mathrm{Re}^2$ 而变化 |
| Péclet 数 | 随固定 Re 固定 |
| Prandtl 数 | 固定为 0.7 |
| 速度边界 | 固定 |
| 温度边界 | 固定 |
| 物体位置 | 固定 |
| 密度、黏度、热扩散率的独立扫描 | 没有 |
| 时间 | 只发布稳态解 |

## 物理区间

$\mathrm{Ri}$ 衡量浮力与惯性之比。论文用约

- $\mathrm{Ri}\approx0.1$：强迫对流占优；
- 中间值：混合对流；
- $\mathrm{Ri}\approx10$：自然/自由对流显著；

来描述覆盖的流动区间。Richardson 数增大通常会增强腔内浮力环流，并改变物体上的升阻力和热传递。


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

- 几何同时控制流动分离和温度边界层；
- 同一几何上可能出现强迫、混合和自然对流三个区间；
- 温度误差不仅影响热场，还会通过浮力反馈到速度和压力；
- $C_D,C_L,\mathrm{Nu}$ 对近壁梯度非常敏感；
- 适合多物理场 operator learning、geometry OOD 和 coupled-PDE residual 研究。

## 版本与文件注意事项

1. 论文把两种 NSHT 合并为 5990 条；当前仓库分为 2990 条 constant-Re 和 3000 条 variable-Re；
2. 论文的统一输入表写 `[Re, Gr, g, s]`，但固定 Re 的 DataPrep 写 `[Gr, g, s]`；
3. 论文图中的 fixed-Re 明确为 100，但目录名本身没有把数值写入文件名，实际加载后仍应检查广播通道或元数据；
4. `C*` 是工程统计量的打包通道，不是温度之外的新 PDE 场；
5. 论文与脚本的 mask/SDF 约定可能不同。


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
    allow_patterns=["LDC_NSHT_2D_constant-Re/128x128/*"],
)
```

把 `LDC_NSHT_2D_constant-Re/128x128/*` 换成上面代码中的实际路径即可。若数据量很大，建议先下载一种几何或一个分辨率，而不是一次下载完整 FlowBench。

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
