---
title: "FlowBench：二维复杂几何绕流 Navier–Stokes 瞬态轨迹"
parent_dataset: FlowBench
subset: FPO_NS_2D_1024x256
equation_family: "time-dependent incompressible Navier-Stokes"
spatial_dimension: 2
temporal_regime: transient
task: "sequence-to-sequence or geometry-conditioned trajectory"
geometry_families: ""
license: CC-BY-NC-4.0
last_verified: 2026-07-21
linkTitle: "FPO NS 2D"
weight: 40
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: FlowBench
summary: "不可压缩流体流过静止复杂钝体，数据保存高分辨率长时序速度和压力场，用于涡脱落预测。"
description: "不可压缩流体流过静止复杂钝体，数据保存高分辨率长时序速度和压力场，用于涡脱落预测。"

---

# 二维复杂几何绕流（FPO–NS–2D）

**一句话描述：** 不可压缩流体流过静止复杂钝体，数据保存高分辨率长时序速度和压力场，用于涡脱落预测。

**较长描述：** FPO 是 FlowBench 唯一公开的瞬态 family。物体位于长通道上游，尾迹中出现周期或非周期涡脱落。它既可构造成过去场到未来场的 sequence-to-sequence 任务，也可进一步加入 Reynolds 数、mask 和 SDF，形成 geometry-conditioned trajectory prediction。

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
=-\nabla p+\frac{1}{\mathrm{Re}}\nabla^2\mathbf u+\mathbf f,
$$

$$
\nabla\cdot\mathbf u=0,
\qquad
\mathbf u=(u,v).
$$

该子集保留时间导数，基本状态向量为

$$
\mathbf q(t,x,y)=(u,v,p).
$$

常见机器学习任务为

$$
\mathbf q_{t_0:t_k}
\longmapsto
\mathbf q_{t_{k+1}:t_{k+m}}.
$$

## 计算域、位置与边界条件

完整 CFD 域：

$$
\Omega=[0,64]\times[0,16].
$$

复杂物体中心固定为

$$
(x_c,y_c)=(6,8).
$$

- 左边界：抛物线速度入口；
- 上、下边界：无滑移 Dirichlet 条件；
- 右边界：零压力出口；
- 物体表面：静止、无滑移。

论文称发布时截取了物理尺寸约为 $[0,16]\times[0,4]$ 的尾迹区域，以平衡文件大小和保留的物理信息。这里的写法描述 cropped span；实际数组坐标原点和方向应从文件或下采样脚本验证。


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
| 物理问题 | 2D 瞬态不可压缩 Navier–Stokes 外流 |
| 论文/代码名义样本数 | **1150 simulations** |
| 当前实际数量 | 官方仓库删除过损坏样本；应枚举当前 `Re_*.npz` 文件 |
| Reynolds 范围 | $\mathrm{Re}\in[10^2,10^3]$ |
| 原始时间帧 | 当前数据卡与代码： **242** |
| 推荐可用帧 | 代码说明忽略前 2 帧，因此通常为 **240** |
| 每帧通道 | $[u,v,p]$ |
| 当前分辨率 | $1024\times256$ |
| 旧论文分辨率 | 还曾列出 $512\times128$ |
| 当前目录体积 | 约 **1.59 TB** |
| 数据目录 | `FPO_NS_2D_1024x256/` |
| 存储组织 | 几何 family / 几何编号 / `Re_<value>.npz` |

### 时间设置

论文附录给出：

- 数值积分步长：$\Delta t_{\rm solve}=0.01$；
- 从无量纲时间约 $t=392$ 开始输出；
- 输出间隔：$\Delta t_{\rm out}=0.05$；
- 保存到约 $t=404$；
- 每条样本至少覆盖两个完整涡脱落周期；
- 选择输出频率时，目标是每个涡脱落周期至少约 100 个快照。

### 张量形式

论文 Appendix Table 9 给出的语义形式为

$$
Y\in\mathbb R^{1150\times240\times3\times N_x\times N_y},
\qquad
Y=[u,v,p].
$$

当前数据仓库直接发布每次模拟的完整 242 帧，而不预先固定训练的输入/输出时间窗。官方 `fpo2d.py` 可根据

```text
t_start_in, t_end_in, t_start_out, t_end_out
```

构造

$$
X\in\mathbb R^{N\times T_{in}\times3\times N_x\times N_y},
$$

$$
Y\in\mathbb R^{N\times T_{out}\times3\times N_x\times N_y}.
$$

脚本先用 `[N,T,C,N_y,N_x]` 初始化，再 transpose 为 `[N,T,C,N_x,N_y]`。旧 README 曾出现不同轴顺序，因此必须检查实际 shape。

### 几何条件是否在输入中？

存在两种合理任务定义：

1. **官方示例 Seq2Seq：** 只输入过去的 $u,v,p$ 帧；官方脚本注释称此时“不使用几何信息”；
2. **条件轨迹模型：** 额外输入 $\mathrm{Re},g,s$，从几何和物理条件预测完整轨迹或未来轨迹。

后者在物理上合理，但不是官方 `fpo2d.py` 的默认打包方式。

## 可调、变化与固定参数

| 项目 | 该子集中处理 |
|---|---|
| 几何 | 变化 |
| Reynolds 数 | 变化 |
| 时间状态 | 变化，完整轨迹 |
| 物体位置 | 固定 $(6,8)$ |
| 主来流方向 | 固定沿 $x$ |
| 入口形式 | 固定为抛物线 |
| 上下壁 | 固定无滑移 |
| 出口 | 固定零压力 |
| 时间步 | 固定 0.01 |
| 输出间隔 | 固定 0.05 |
| 温度 | 不存在 |
| 可压缩性 | 不可压缩 |

## 涡量派生量

论文常用二维涡量展示尾迹：

$$
\omega_z=\frac{\partial v}{\partial x}
-\frac{\partial u}{\partial y}.
$$

涡量是由速度派生的可视化/评测量，不是 Appendix Table 9 列出的基本文件通道。

## 自适应网格

物体和尾迹区域使用多层加密。论文给出物体中心周围半径 0.71、0.8、1、2.5、3 的五个圆形区域，refinement level 分别为 13、12、11、10、9；紧邻物体达到 level 14。尾迹方向还有两个矩形加密区。

- 自适应网格约 117,978 个节点；
- 速度和压力合计约 353,934 个自由度；
- 若用最细尺度的全域均匀网格，论文估算约 201M 自由度。


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

- 同一数据同时包含几何变化、Reynolds 变化和长时序动力学；
- 低 Re 可出现较规则的周期涡脱落，高 Re 更复杂、更不规则；
- 长期 rollout 会累积相位、频率和幅值误差；
- 物体附近和尾迹远场对空间分辨率的要求不同；
- 数据量约 1.59 TB，对 I/O、时间裁剪、分块训练和缓存提出挑战；
- 适合 sequence modeling、autoregressive rollout、latent dynamics 和 geometry-conditioned video/field prediction。

## 版本与文件注意事项

1. 论文表格写 240 帧，当前数据卡写 242 帧，代码明确“模拟 242 帧、建模时忽略前两帧”；
2. 若按 $392$ 到 $404$ 每 $0.05$ 且包含两端计算，会得到 241 个点，因此精确时间坐标应以文件为准；
3. 2025-02-02 官方删除 $512\times128$ 版本，因为几何解析不足；当前只发布 $1024\times256$；
4. Hugging Face 历史记录显示删除过损坏的 harmonics/nurbs 样本，因此当前文件数可能低于名义 1150；
5. 数据卡文字曾称每个几何有 3 个流动条件，但当前示例目录可有 5 个 `Re_*.npz`；不要假定固定个数，应枚举文件；
6. FPO 目录中的 SkelNetOn 拼写在不同版本中出现 `skelneton`、`skelenton` 等差异，下载 pattern 应以当前文件树为准。

## 下载方式

先只下载一个几何实例，避免直接拉取 1.59 TB：

```bash
python -m pip install -U huggingface_hub
```

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="BGLab/FlowBench",
    repo_type="dataset",
    local_dir="./FlowBench",
    allow_patterns=["FPO_NS_2D_1024x256/nurbs/36/*"],
)
```

完整 family 可使用：

```python
allow_patterns=["FPO_NS_2D_1024x256/nurbs/*"]
```

但该目录非常大。下载后应逐个检查 `Re_*.npz` 的 key 和 shape，不要预先假定每个几何有相同数量的 Reynolds 条件。


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
