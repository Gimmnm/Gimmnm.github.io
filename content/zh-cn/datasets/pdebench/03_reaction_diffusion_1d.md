---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 03_reaction_diffusion_1d
spatial_dimension: 1
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: 1d_reacdiff
last_verified: 2026-07-21
title: 一维扩散—反应方程
linkTitle: "reaction diffusion 1d"
weight: 30
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "扩散与 logistic 源项结合，可产生接近指数的快速演化。"
description: "扩散与 logistic 源项结合，可产生接近指数的快速演化。"

---

# 一维扩散—反应方程

一维扩散—反应方程把扩散过程与依赖 $u$ 的 logistic 型源项结合起来。源项可使解快速增长或饱和，形成强烈的时间尺度分离；扩散则抑制空间高频，因此适合考察快速瞬态与多参数条件化。

![1D Reaction-Diffusion (ν = 0.5, ρ = 1)](./1D-Reaction-Diffusion.png)

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEBench** |
| 数据集论文 | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| 论文 PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| 官方代码库 | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| 数据 DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| 当前下载类别 | `1d_reacdiff` |
| 数据量 | 62 GB |
| 生成代码入口 | [data_gen_NLE/ReactionDiffusionEq](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_gen/data_gen_NLE/ReactionDiffusionEq) |
| 文档核对日期 | 2026-07-21 |

## 控制方程

\[
\partial_tu-\nu\partial_{xx}u-\rho u(1-u)=0,
\qquad x\in(0,1),\quad t\in(0,1],
\]
\[
u(0,x)=u_0(x).
\]

## 变量与坐标

**状态变量**
- $u(t,x)$：标量状态 / 浓度场。

**参数**
- $\nu$：扩散系数。
- $\rho$：反应 / 源项系数（Fisher 型源项 $\rho u(1-u)$）。

**坐标与定义域**
- 空间：一维均匀笛卡尔坐标 $x\in(0,1)$。
- 时间：$t\in(0,1]$。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 1 |
| 含时间 | 是 |
| 网格 | 均匀一维笛卡尔 |
| 空间域 | $x\in(0,1)$ |
| 时间范围 | $t\in[0,1]$ |
| 空间分辨率 | 1024 |
| 时间点数 | 201 |
| 每文件轨迹数 | 10,000 |
| 通道 | 1：$u$ |
| 单样本形状 | $201\times1024\times1$ |
| 数据量 | 62 GB |
| 格式 | HDF5 |

## 初始条件

先使用随机正弦叠加生成初值，再取绝对值并除以最大值归一化，使初值适合 $u(1-u)$ 反应项。随机频谱与 seed 逐轨迹变化。

## 边界条件

周期边界。

## 数值生成方法

扩散部分使用时间与空间二阶中心差分；源项使用 piecewise-exact solution (PES) 方法。

## 参数

| 参数 | 变化方式 | 取值 |
|---|---|---|
| $\nu$（扩散） | 不同 HDF5 文件不同 | $\nu\in\{0.5,1,2,5\}$ |
| $\rho$（反应率） | 不同 HDF5 文件不同 | $\rho\in\{1,2,5,10\}$ → 共 $4\times4=16$ 训练文件 |
| 初值频谱 / 振幅 / 相位 | 每轨迹随机 | 正弦叠加后取绝对值并归一化 |
| 边界、网格、时间、数值格式 | 固定 | 周期；$N_x=1024$；$t\in[0,1]$ |

## 论文配置

16 个论文训练文件形成 $4\times4$ 参数网格，每文件 10,000 条轨迹；当前下载类别还包含额外反应测试文件。

## 数据文件

当前官方下载清单（`pdebench_data_urls.csv`）共 **36** 个文件；相对路径相对于下载根目录。详见 [数据格式](../00_data_format/)。

- `1D/ReactionDiffusion/Train/ReacDiff_Nu0.5_Rho1.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu0.5_Rho2.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu0.5_Rho5.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu0.5_Rho10.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu1.0_Rho1.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu1.0_Rho2.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu1.0_Rho5.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu1.0_Rho10.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu2.0_Rho1.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu2.0_Rho2.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu2.0_Rho5.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu2.0_Rho10.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu5.0_Rho1.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu5.0_Rho2.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu5.0_Rho5.0.hdf5`
- `1D/ReactionDiffusion/Train/ReacDiff_Nu5.0_Rho10.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu0.5_Rho1.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu0.5_Rho2.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu0.5_Rho5.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu0.5_Rho10.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu1.0_Rho1.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu1.0_Rho2.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu1.0_Rho5.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu1.0_Rho10.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu2.0_Rho1.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu2.0_Rho2.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu2.0_Rho5.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu2.0_Rho10.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu5.0_Rho1.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu5.0_Rho2.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu5.0_Rho5.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu5.0_Rho10.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu10.0_Rho1.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu10.0_Rho2.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu10.0_Rho5.0.hdf5`
- `1D/ReactionDiffusion/Test/ReacDiff_react_Nu10.0_Rho10.0.hdf5`

## 数据布局与机器学习输入输出

标量轨迹预测；建议把 $\nu$、$\rho$ 作为两个独立物理条件，而不是只用文件名区分模型。

- **轨迹与训练样本：** 完整 HDF5 轨迹不是固定的模型输入。自回归训练通常从完整轨迹切出 $\ell$ 帧输入与下一帧/未来多帧目标；$\ell$ 由训练配置的 `initial_step` 决定。
- **版本优先级：** 方程与初边值以论文为准；文件数、分辨率、轨迹数与通道以当前可下载 HDF5 / 官方清单为准。

## 下载

官方仓库当前推荐 `download_direct.py`，而不是较慢且可能报错的 EasyDataverse 路径。

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name 1d_reacdiff
```

也可以从 [DaRUS DOI 页面](https://doi.org/10.18419/darus-2986) 手动选择文件。下载后应逐文件检查 HDF5 的实际 `shape`、坐标数组、变量键和 YAML attributes，尤其不要仅凭文件名推断 CFD/不可压 NS 的空间分辨率。

## 从官方代码重新生成

```bash
cd PDEBench/pdebench/data_gen/data_gen_NLE/ReactionDiffusionEq
CUDA_VISIBLE_DEVICES=0 python3 reaction_diffusion_multi_solution_Hydra.py +multi=Rho2e0_Nu5e0.yaml
bash run_trainset.sh
cd ..
python Data_Merge.py
```

生成器参数可通过对应 Hydra YAML 修改。对 NLE 路径生成的 `.npy` 数据，需要执行 `Data_Merge.py` 才能得到官方 dataloader 使用的 HDF5 布局。

## 数据的兴趣点与挑战

反应率大时出现极快瞬态与近饱和解，标准平均误差可能掩盖初期动力学；跨参数尺度差异明显。

## 主要来源

- [PDEBench 论文与补充材料](https://arxiv.org/abs/2210.07182)
- [PDEBench 官方代码库](https://github.com/pdebench/PDEBench)
- [官方下载说明](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench 数据集 DOI](https://doi.org/10.18419/darus-2986)
