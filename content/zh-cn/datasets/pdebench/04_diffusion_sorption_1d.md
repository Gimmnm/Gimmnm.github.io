---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 04_diffusion_sorption_1d
spatial_dimension: 1
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: diff_sorp
last_verified: 2026-07-21
title: 一维扩散—吸附方程
linkTitle: "diffusion sorption 1d"
weight: 40
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "被 Freundlich 延滞的扩散；适用于地下水污染物输运。"
description: "被 Freundlich 延滞的扩散；适用于地下水污染物输运。"

---

# 一维扩散—吸附方程

扩散—吸附方程描述被吸附过程延滞的扩散，典型应用是地下水污染物输运。有效扩散被浓度依赖的 Freundlich 延滞因子除去，并在 $u\to 0$ 附近出现奇异性；边界也包含非常规的导数关系，而不仅是周期或齐次条件。

![1D Diffusion–Sorption time evolution](./1D-diffusion-sorption.png)

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEBench** |
| 数据集论文 | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| 论文 PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| 官方代码库 | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| 数据 DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| 当前下载类别 | `diff_sorp` |
| 数据量 | 4 GB |
| 生成代码入口 | [gen_diff_sorp.py + configs/diff-sorp.yaml](https://github.com/pdebench/PDEBench/blob/main/pdebench/data_gen/gen_diff_sorp.py) |
| 文档核对日期 | 2026-07-21 |

## 控制方程

\[
\partial_tu(t,x)=\frac{D}{R(u)}\,\partial_{xx}u(t,x),\qquad x\in(0,1),\quad t\in(0,500],
\]
\[
R(u)=1+\frac{1-\phi}{\phi}\rho_s k n_f u^{n_f-1}.
\]

## 变量与坐标

**状态变量**
- $u(t,x)$：溶质浓度。

**参数与介质量**
- $D$：有效扩散系数（论文取 $D=5\times10^{-4}$）。
- $R(u)$：吸附导致的延滞因子，随浓度变化。
- $\phi$：孔隙率（$0.29$）。
- $\rho_s$：bulk density（$2880$）。
- $k$：Freundlich 参数（$3.5\times10^{-4}$）。
- $n_f$：Freundlich 指数（$0.874$）。

**坐标与定义域**
- 空间：一维均匀有限体积网格，$x\in(0,1)$。
- 时间：$t\in(0,500]$。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 1 |
| 含时间 | 是 |
| 网格 | 均匀一维有限体积 |
| 空间域 | $x\in(0,1)$ |
| 时间范围 | $t\in[0,500]$ |
| 空间分辨率 | 1024 |
| 时间点数 | 原始 501；训练常用 101 |
| 每文件轨迹数 | 10,000 |
| 通道 | 1：$u$（浓度） |
| 单样本形状 | 训练 $101\times1024\times1$；原始 $501\times1024\times1$ |
| 数据量 | 4 GB |
| 格式 | HDF5 |

## 初始条件

论文写 $u(0,x)\sim\mathcal U(0,0.2)$；论文示例显示每条轨迹的初值为空间常值、其数值随机抽样。

## 边界条件

论文给出的边界为
\[
u(t,0)=1.0,\qquad u(t,1)=D\,\partial_xu(t,1).
\]
正文将其概括为 Cauchy 类型边界。第二个条件含空间导数，对卷积模型的 padding 处理更具挑战。

## 数值生成方法

空间采用有限体积法。论文文字称 SciPy 内置四阶 Runge–Kutta；当前 YAML metadata 标记为 RK45（5(4) 阶自适应格式），应按所用代码版本记录。当前配置为 `D=5e-4, por=0.29, rho_s=2880, k_f=3.5e-4, n_f=0.874, t=500, tdim=501, xdim=1024`。

## 参数

| 参数 | 变化方式 | 取值 |
|---|---|---|
| $D,\phi,\rho_s,k,n_f$ | 固定 | $D=5\times10^{-4}$，$\phi=0.29$，$\rho_s=2880$，$k=3.5\times10^{-4}$，$n_f=0.874$；文件名 `NA_NA` |
| 初始浓度 | 每轨迹随机 | $u(0,x)\sim\mathcal U(0,0.2)$（示例为空间常值抽样） |
| 边界、域、网格、时间 | 固定 | Cauchy 边界；$x\in(0,1)$；$N_x=1024$ |

## 论文配置

一个主要论文文件 `1D_diff-sorp_NA_NA.h5`，含 10,000 条轨迹；`NA_NA` 表明论文集没有参数扫描。

## 数据文件

当前官方下载清单（`pdebench_data_urls.csv`）共 **1** 个文件；相对路径相对于下载根目录。详见 [数据格式](../00_data_format/)。

- `1D/diffusion-sorption/1D_diff-sorp_NA_NA.h5`

## 数据布局与机器学习输入输出

单通道浓度轨迹预测；也可做由后期浓度反演初值/材料参数的逆问题，但论文文件本身不提供材料参数多样性。

- **轨迹与训练样本：** 完整 HDF5 轨迹不是固定的模型输入。自回归训练通常从完整轨迹切出 $\ell$ 帧输入与下一帧/未来多帧目标；$\ell$ 由训练配置的 `initial_step` 决定。
- **版本优先级：** 方程与初边值以论文为准；文件数、分辨率、轨迹数与通道以当前可下载 HDF5 / 官方清单为准。

## 下载

官方仓库当前推荐 `download_direct.py`，而不是较慢且可能报错的 EasyDataverse 路径。

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name diff_sorp
```

也可以从 [DaRUS DOI 页面](https://doi.org/10.18419/darus-2986) 手动选择文件。下载后应逐文件检查 HDF5 的实际 `shape`、坐标数组、变量键和 YAML attributes，尤其不要仅凭文件名推断 CFD/不可压 NS 的空间分辨率。

## 从官方代码重新生成

```bash
cd PDEBench
python -m pdebench.data_gen.gen_diff_sorp
# Hydra configuration: pdebench/data_gen/configs/diff-sorp.yaml
```

生成器参数可通过对应 Hydra YAML 修改；该路径直接写出 HDF5，无需执行 `Data_Merge.py`。

## 数据的兴趣点与挑战

$u\to0$ 的奇异延滞、超长时间尺度、非标准导数边界以及浓度前沿的局部误差。

## 主要来源

- [PDEBench 论文与补充材料](https://arxiv.org/abs/2210.07182)
- [PDEBench 官方代码库](https://github.com/pdebench/PDEBench)
- [官方下载说明](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench 数据集 DOI](https://doi.org/10.18419/darus-2986)
