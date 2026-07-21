---
title: "CFDBench — 圆管水-空气两相流"
dataset: CFDBench
problem_id: tube_flow
equation_family: "2D incompressible Navier-Stokes"
time_dependent: true
data_origin: "ANSYS Fluent numerical simulation"
interpolated_grid: "64 x 64"
license: "Apache-2.0 (Hugging Face dataset card)"
paper: "https://arxiv.org/abs/2310.05963"
code: "https://github.com/luo-yining/CFDBench"
interpolated_data: "https://huggingface.co/datasets/chen-yingfa/CFDBench"
raw_data: "https://huggingface.co/datasets/chen-yingfa/CFDBench-raw"
last_verified: 2026-07-21
subsets: ["bc", "prop", "geo"]
multiphase: true
linkTitle: "Tube Flow"
weight: 20
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: CFDBench
summary: "水从左侧进入初始充满空气的二维圆管轴向截面，形成近壁面黏性边界层和移动两相界面；数据分别改变入口速度、工作流体物性和管道几何。"
description: "水从左侧进入初始充满空气的二维圆管轴向截面，形成近壁面黏性边界层和移动两相界面；数据分别改变入口速度、工作流体物性和管道几何。"

---

# CFDBench — 圆管水--空气两相流（Tube Flow）

**一句话描述：** 水从左侧进入初始充满空气的二维圆管轴向截面，形成近壁面黏性边界层和移动两相界面；数据分别改变入口速度、工作流体物性和管道几何。

**较长描述：** 该问题用于检验模型能否同时表达入口发展流、无滑移壁面导致的速度剖面、压力出口和水--空气界面。论文把它称为 circular tube flow，但发布给二维模型的是管道轴向截面上的二维场。Fluent 使用 VOF 两相模型，官方插值压缩包则统一提供 $u,v$，没有把体积分数作为标准学习通道发布。

- 所属数据集： **CFDBench**
- 数据集作者：Yining Luo、Yingfa Chen、Zhen Zhang
- 生成软件：ANSYS Fluent 2021R1，VOF 两相模型
- 官方 loader：[`src/dataset/tube.py`](https://github.com/luo-yining/CFDBench/blob/main/src/dataset/tube.py)


## 控制方程

论文为四类问题统一写出二维不可压缩牛顿流体 Navier--Stokes 方程。守恒形式为

$$
\nabla\cdot(\rho\mathbf u)=0,
$$

$$
\frac{\partial(\rho\mathbf u)}{\partial t}
+\nabla\cdot(\rho\mathbf u\otimes\mathbf u)
=-\nabla p
+\nabla\cdot\left\{\mu\left[\nabla\mathbf u+(\nabla\mathbf u)^{\mathsf T}\right]\right\}
+\rho\mathbf g,
$$

其中 $\mathbf u=(u,v)^{\mathsf T}$，$u$、$v$ 分别是 $x$、$y$ 方向速度，$p$ 是压力，$\rho$ 是密度，$\mu$ 是动力黏度。除 dam 问题外，可取 $\mathbf g=\mathbf 0$。在 $\rho$、$\mu$ 为常数时，二维分量形式为

$$
\frac{\partial u}{\partial x}+\frac{\partial v}{\partial y}=0,
$$

$$
\frac{\partial u}{\partial t}
+u\frac{\partial u}{\partial x}
+v\frac{\partial u}{\partial y}
=-\frac{1}{\rho}\frac{\partial p}{\partial x}
+\frac{\mu}{\rho}\left(
\frac{\partial^2u}{\partial x^2}+\frac{\partial^2u}{\partial y^2}
\right)+g_x,
$$

$$
\frac{\partial v}{\partial t}
+u\frac{\partial v}{\partial x}
+v\frac{\partial v}{\partial y}
=-\frac{1}{\rho}\frac{\partial p}{\partial y}
+\frac{\mu}{\rho}\left(
\frac{\partial^2v}{\partial x^2}+\frac{\partial^2v}{\partial y^2}
\right)+g_y.
$$

> **方程范围说明。** 论文正文逐式写出的数学系统是上述不可压缩 Navier--Stokes 方程。Tube 和 Dam 的 Fluent 配置还使用 VOF 两相模型；Cylinder 的部分工况使用 SST $k$--$\omega$ 湍流闭合。论文没有完整列出 VOF 或 SST 的附加输运方程及模型常数，因此本文档不会把这些未明示的方程伪装成数据集论文的原始公式。


### 两相辅助变量

Fluent 配置使用水相体积分数 $\alpha$。在忽略相间质量传递时，标准 VOF 输运关系通常写为

$$
\frac{\partial\alpha}{\partial t}+\nabla\cdot(\alpha\mathbf u)=0.
$$

这是对官方 VOF 配置的标准解释，不是论文正文额外逐式列出的目标标签方程。官方插值档案未统一提供 $\alpha$。

## 物理区域、坐标和边界条件

$x$ 沿管轴由左向右，$y$ 为管径方向。理想化区域可写为

$$
D=[0,l]\times[0,d].
$$

边界条件为

$$
\mathbf u(0,y,t)=(u_\mathrm{{in}},0),
$$

$$
\mathbf u(x,0,t)=\mathbf u(x,d,t)=\mathbf 0,
$$

$$
p(l,y,t)=p_\mathrm{{out}}.
$$

生成 Scheme 把混合物速度和压力初始化为静止，并将域初始为空气相，然后从左侧入口注入水相。

## 关于数据

| 项目 | 数值或说明 |
|---|---|
| 空间维数 | 2D 轴向截面 |
| 相态 | 水--空气两相，VOF |
| 原始插值尺寸 | `u.npy`, `v.npy`: $(T_i,64,64)$ |
| 当前 loader 特征 | 左边补入口列、上下补壁面行后约为 $(T_i,3,66,65)$；通道 $(u,v,\mathrm{{mask}})$ |
| 论文附录示例 | 只明确举出上下补线后的 $66\times64$；与当前 loader 的额外左列不同 |
| 物理输出 | $u,v$；原始导出可含水相体积分数和压力 |
| 轨迹/case | 175 = 50 BC + 100 PROP + 25 GEO |
| 总帧数 | 39,553 |
| 平均帧数 | 226.02，仅为平均值 |
| 时间间隔 | 论文：$0.01\,\mathrm s$；当前 loader 中存在 `data_delta_time=0.1`，见注意事项 |
| 统一 $t_\max$ | 未给出；从每条轨迹和采用的时间元数据计算 |
| 论文每帧原始量 | 约 4.8 MB |
| 论文生成时间 | 约 1.08 s/帧 |
| 当前压缩包 | `tube.zip`，约 213 MB（2026-07-21） |

## 基准工况

$$
\rho=100\,\mathrm{{kg\,m^{{-3}}}},\qquad
\mu=0.1\,\mathrm{{Pa\,s}},
$$

$$
u_\mathrm{{in}}=1\,\mathrm{{m/s}},\qquad
d=0.1\,\mathrm m,\qquad l=1\,\mathrm m.
$$

代码工况参数顺序：

```text
[vel_in, density, viscosity, height, width]
```

其中 `height/width` 对应插值域的物理高、宽；与论文的 $d,l$ 命名需通过 `case.json` 核对。

## 参数扫描：改变了什么，固定了什么

| 子集 | case 数 | 实际扫描参数 | 固定条件 |
|---|---:|---|---|
| BC | 50 | $u_\mathrm{{in}}=0.1,0.2,\ldots,5.0\,\mathrm{{m/s}}$ | $\rho=100$，$\mu=0.1$，$d=0.1$，$l=1$；相模型、初始空气填充和边界类型固定 |
| PROP | 100 | $\rho=\{{10,120,230,340,450,560,670,780,890,1000\}}\,\mathrm{{kg/m^3}}$；$\mu=\{{0.01,0.12,0.23,0.34,0.45,0.56,0.67,0.78,0.89,1.00\}}\,\mathrm{{Pa\,s}}$；$10\times10$ 组合 | $u_\mathrm{{in}}=1$，$d=0.1$，$l=1$；边界和初始相分布固定 |
| GEO | 25 | 正文称从 $\{{0.01,0.05,0.1,0.3,0.5\}}\,\mathrm m$ 取五个管径，并为每个管径选五种径长关系，使 $0.1\le l\le10$ | $u_\mathrm{{in}}=1$，$\rho=100$，$\mu=0.1$；入口、出口、壁面和两相设置固定 |

> **Tube GEO 原文歧义。** 正文说最终有 25 个几何；表 3 同时列出五个尺寸值和十个 $d/l$ 候选，如果做全组合会得到 50 个。论文没有给出完整的 25 对 $(d,l)$ case 表。不要自行构造组合，应以下载后的逐 case `case.json` 为准。

**可调但未扫描：** 出口压力、空气相物性、接触角/表面张力、初始相界面、重力等在更一般的两相问题中可调，但 CFDBench 的公开参数扫描主要是入口速度、给定流体 $\rho/\mu$ 和有限几何集合。


## 数值生成设置

- 生成软件：ANSYS Fluent 2021R1；网格生成与批处理脚本位于仓库 `generation-code/`，其中包括 ICEM RPL 和 Fluent Scheme 文件。
- 层流/湍流：层流工况采用 laminar model；需要湍流闭合时采用 SST $k$--$\omega$。
- 压力--速度耦合：单相流采用 Coupled Scheme；两相流采用 SIMPLE。
- 空间离散：压力方程二阶插值；VOF 使用 PRESTO!；动量方程二阶迎风。
- 时间离散：一阶隐式。
- 插值：最小二乘；最终发布数据映射到 $64\times64$ 笛卡尔网格。
- 近壁面网格：第一层网格尺度加密至约 $10^{-5}\,\mathrm m$。
- 收敛：论文给出的全局残差收敛阈值为 $10^{-9}$；最终速度残差至少达到约 $10^{-6}$ 量级。
- 生成硬件：AMD Ryzen Threadripper 3990X，30 个 solver processes。
- 数值精度：论文未明确说明单精度或双精度；不要仅根据 NumPy 文件 dtype 反推 Fluent 求解精度。



## 学习任务、输入与输出

CFDBench 同时支持两种问题定义。

### 非自回归坐标查询

$$
\widehat{q}(x,y,t)=f_\theta\big((x,y,t),\Omega\big),
$$

其中 $\Omega$ 是边界、物性和几何条件。论文中的 FFN/DeepONet 实验通常在查询点预测一个标量速度分量；磁盘上仍保存两个速度分量 $u,v$。

### 自回归场推进

$$
\widehat{\mathbf u}^{\,n+1}
=f_\theta\big(\mathbf u^n,\Omega,\mathrm{mask}\big).
$$

典型输入是当前帧的二维速度场、工况向量和几何/边界 mask，标签是下一时刻的 $u,v$。官方代码把 `u`、`v`、`mask` 堆叠为 `(T,3,H,W)` 的特征，但 mask 是静态条件而不是守恒物理量，不应与速度通道采用同一归一化策略。

### 数据划分

论文对每个基础子集按 case 进行 8:1:1 的训练/验证/测试划分。同一条轨迹的帧不会跨 split，从而保证测试工况在训练时不可见。若要严格复现，需固定代码版本、随机种子以及最终生成的 case 列表。



## 下载与目录组织

### 官方链接

- 论文：[https://arxiv.org/abs/2310.05963](https://arxiv.org/abs/2310.05963)
- 官方代码：[https://github.com/luo-yining/CFDBench](https://github.com/luo-yining/CFDBench)
- 插值数据：[https://huggingface.co/datasets/chen-yingfa/CFDBench](https://huggingface.co/datasets/chen-yingfa/CFDBench)
- 原始 Fluent 数据：[https://huggingface.co/datasets/chen-yingfa/CFDBench-raw](https://huggingface.co/datasets/chen-yingfa/CFDBench-raw)
- 百度网盘原始数据：[https://pan.baidu.com/s/1p0q60cv2hFZ7UcIf3XKSaw?pwd=cfd4](https://pan.baidu.com/s/1p0q60cv2hFZ7UcIf3XKSaw?pwd=cfd4)，提取码 `cfd4`
- 文档版式参考：[https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/](https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/)

官方仓库把插值数据描述为约 13.4 GB；Hugging Face 页面在 **2026-07-21** 显示总文件大小为约 14.4 GB。原始库在仓库 README 中被描述为约 460 GB，而 Hugging Face 原始页当前显示约 205 GB，并注明 Cylinder 部分仍在上传。对可复现工作，应记录具体下载日期和仓库 revision。

### 命令行下载

先安装当前 Hugging Face CLI：

```bash
python -m pip install -U huggingface_hub
```

完整下载插值库：

```bash
hf download chen-yingfa/CFDBench \
  --repo-type dataset \
  --local-dir ./downloads/CFDBench
```

完整下载原始库会占用数百 GB，执行前建议先检查：

```bash
hf download chen-yingfa/CFDBench-raw \
  --repo-type dataset \
  --local-dir ./downloads/CFDBench-raw \
  --dry-run
```

### 代码仓库

```bash
git clone https://github.com/luo-yining/CFDBench.git
cd CFDBench
python -m pip install -r requirements.txt
```

解压后的推荐目录结构为

```text
data/
├── cavity/
│   ├── bc/caseXXXX/{case.json,u.npy,v.npy}
│   ├── geo/caseXXXX/{case.json,u.npy,v.npy}
│   └── prop/caseXXXX/{case.json,u.npy,v.npy}
├── tube/
├── dam/
└── cylinder/
```


### 只下载本问题

```bash
hf download chen-yingfa/CFDBench tube.zip \\
  --repo-type dataset \\
  --local-dir ./downloads/CFDBench
unzip ./downloads/CFDBench/tube.zip -d ./data
```

## 有趣且具有挑战性的方面

- 需要同时捕捉两相界面和近壁面速度梯度。
- 压力出口、速度入口和无滑移壁面是非周期边界，区别于许多规则 PDE benchmark。
- 几何变化改变物理网格间距和流动发展长度。
- 统一只提供 $u,v$ 会丢失直接的相界面标签；模型只能从速度场间接推断界面，或从原始数据自行加入 VOF。

## 已知注意事项

- **时间间隔冲突：** 论文为 $0.01\,\mathrm s$，当前 `tube.py` 中存在 $0.1\,\mathrm s$ 的 loader 元数据。训练前应检查 `case.json`、生成 Scheme 和实际帧时间，不应只相信类常量。
- **padding 冲突：** 论文附录举例得到 $66\times64$，当前 loader 还增加左侧入口列，可能得到 $66\times65$。务必打印实际 tensor shape。
- **GEO 组合不完备：** 只能从真实 case 元数据恢复 25 个几何。
- 压力和水相 VOF 不是插值压缩包的统一标签通道。

## 引用

```bibtex
@article{CFDBench,
  title  = {CFDBench: A Large-Scale Benchmark for Machine Learning Methods in Fluid Dynamics},
  author = {Luo, Yining and Chen, Yingfa and Zhang, Zhen},
  year   = {2023},
  url    = {https://arxiv.org/abs/2310.05963}
}
```

## 原始出处定位

- 论文：第 3.1、3.3 节，表 3、表 6，第 3.6 节，附录 E.1。
- 代码：`src/dataset/tube.py`，Tube 对应 Fluent Scheme。
