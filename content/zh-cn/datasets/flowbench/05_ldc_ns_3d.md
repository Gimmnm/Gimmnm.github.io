---
title: "FlowBench：三维复杂几何顶盖驱动立方腔 Navier–Stokes"
parent_dataset: FlowBench
subset: LDC_NS_3D
equation_family: "3-D incompressible Navier-Stokes"
spatial_dimension: 3
temporal_regime: steady
task: "3-D geometry-and-Reynolds-to-field"
geometry_families: ""
license: CC-BY-NC-4.0
last_verified: 2026-07-21
linkTitle: "LDC NS 3D"
weight: 50
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: FlowBench
summary: "在含三维静止物体的立方腔中，以移动顶面驱动不可压缩流动，并发布规则 $128^3$ 稳态张量。"
description: "在含三维静止物体的立方腔中，以移动顶面驱动不可压缩流动，并发布规则 $128^3$ 稳态张量。"

---

# 三维复杂几何顶盖驱动立方腔（LDC–NS–3D）

**描述：** 在含三维静止物体的立方腔中，以移动顶面驱动不可压缩流动，并发布规则 $128^3$ 稳态张量。 该子集把二维 LDC 扩展到三维，几何附近采用自适应 octree 加密。论文原始版本为 500 条 ellipsoid/torus 数据；当前官方仓库已更新为 1000 条，并列出 ellipsoid、toroid、box 和 cylinder。

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
$$

$$
\mathbf u=(u,v,w).
$$

三维连续性条件为

$$
\frac{\partial u}{\partial x}
+\frac{\partial v}{\partial y}
+\frac{\partial w}{\partial z}=0.
$$

数据为稳态解：

$$
(\mathrm{Re},g,s)\longmapsto(u,v,w,p).
$$

## 计算域与边界条件

$$
\Omega=[0,2]\times[0,2]\times[0,2].
$$

顶面沿 $x$ 方向运动：

$$
(u,v,w)=(1,0,0)\quad\text{on the top face}.
$$

其余五个外壁和物体表面：

$$
(u,v,w)=(0,0,0).
$$

内部物体置于立方腔中部并保持静止。

## 三维几何

### 论文与早期代码版本

- 论文报告 500 条；
- 主要几何为 ellipsoids 和 tori/rings；
- 椭球改变主轴/次轴比例；
- 环面改变内外半径比例；
- 论文正文还说明考虑不同 aspect ratios 和 orientations；
- CaseGenerator README 说明早期提供 50 个 3D 形状，每个形状配多个 Reynolds 条件。

论文没有公布半轴比、内外半径比和旋转角的完整采样区间。

### 当前官方数据版本

当前 Hugging Face 数据卡列出：

- ellipsoids；
- toroids；
- boxes；
- cylinders；

并将数据更新为 **1000 samples at $128^3$**。因此当前仓库不是论文原始 500 条版本的完全冻结副本。

### 几何输入

语义上仍使用

- Reynolds 常数场；
- binary mask $g(x,y,z)$；
- signed distance field $s(x,y,z)$。

论文规定 SDF 内负外正、mask 内 1 外 0；旧 3D DataPrep 代码却使用 `SDF > 0` 生成 0/255 mask，因此实际文件必须可视化验证。

## 关于数据

| 属性 | 内容 |
|---|---|
| 物理问题 | 3D 稳态不可压缩 Navier–Stokes LDC |
| 论文样本数 | 500 |
| 当前样本数 | **1000** |
| Reynolds 范围 | 论文总体 $[10,10^3]$ |
| 当前分辨率 | $128\times128\times128$ |
| 轨迹长度 | 1 个稳态最终快照 |
| 当前目录体积 | 约 **33.4 GB** |
| 输入文件 | `LDC_3d_X.npz`，约 7.25 GB |
| 输出文件 | `LDC_3d_Y.npz`，约 26.2 GB |
| 数据目录 | `LDC_NS_3D/` |

### 论文的简写张量

论文 Appendix Table 9 写作

$$
X\in\mathbb R^{500\times3\times N_x\times N_y\times N_z},
\qquad
X=[\mathrm{Re},g,s],
$$

$$
Y\in\mathbb R^{500\times3\times N_x\times N_y\times N_z},
\qquad
Y=[u,v,p].
$$

这里的输出明显遗漏了三维速度分量 $w$。

### 官方 DataPrep 代码的实际物理通道

3D 脚本明确读取源数据列

```text
x, y, z, u, v, w, p
```

并把四个场写入输出：

$$
[u,v,w,p].
$$

脚本还创建第五个辅助通道，把 $C_D$ 和 $C_L$ 分别广播到该通道的两个空间半区。因此旧脚本的完整输出可理解为

$$
Y_{\rm script}=[u,v,w,p,C],
$$

其中 $C$ 不是局部 PDE 场。当前托管文件应通过实际 shape 验证是否沿用了这一打包方式。

## 可调、变化与固定参数

| 项目 | 该子集中处理 |
|---|---|
| Reynolds 数 | 变化 |
| 三维几何类型 | 变化 |
| 长宽比/半径比 | 变化 |
| 方向 | 论文称变化，精确范围未公开 |
| 物体位置 | 固定在腔体中部 |
| 顶盖速度 | 固定 $(1,0,0)$ |
| 其他外壁和物体 | 固定无滑移 |
| 域大小 | 固定 $[0,2]^3$ |
| 时间 | 只发布稳态解 |
| 温度 | 不存在 |
| 可压缩性 | 不可压缩 |

## 网格与自由度

- 物体表面附近 refinement level 9，标称尺度 $2/2^9$；
- 远离物体逐步粗化到 level 7，标称尺度 $2/2^7$；
- 原始问题约 2.5M degrees of freedom；
- 三维求解目标约为两倍 Kolmogorov 尺度；
- 最终全部重采样到 uniform $128^3$。

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

- 三维输入输出张量体积大，单个高 batch 训练成本高；
- 需要同时恢复三分量速度和压力；
- 不同 orientation/aspect ratio 会产生真正的三维再循环结构；
- 当前版本包含论文外新增几何类型，适合评测版本迁移和 geometry OOD；
- SDF、mask 与复杂表面附近的速度/压力梯度对模型分辨率非常敏感。

## 版本与文件注意事项

1. 论文与旧 DataPrep 为 500 条，当前仓库为 1000 条；
2. 论文/旧几何说明主要是 ellipsoid 和 torus，当前数据卡还列 box 和 cylinder；
3. 论文表格漏写 $w$，官方代码明确读取并输出 $w$；
4. 旧代码还打包第五个 $C_D/C_L$ 辅助通道；
5. 旧脚本默认设置中曾出现 `num_geometry=25`、`num_Reynolds=10` 等未完成/旧配置，不应据此推断当前 1000 条的准确组成；
6. 当前文件约 33.4 GB，下载前应预留额外解压和训练缓存空间。

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
    allow_patterns=["LDC_NS_3D/*"],
)
```

把 `LDC_NS_3D/*` 换成上面代码中的实际路径即可。若数据量很大，建议先下载一种几何或一个分辨率，而不是一次下载完整 FlowBench。

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
