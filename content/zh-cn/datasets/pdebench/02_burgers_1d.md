---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 02_burgers_1d
spatial_dimension: 1
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: burgers
last_verified: 2026-07-21
title: "一维 Burgers 方程"
linkTitle: "burgers 1d"
weight: 20
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "非线性对流与扩散共存；ν 控制冲击形成与扩散主导。"
description: "非线性对流与扩散共存；ν 控制冲击形成与扩散主导。"

---

# 一维 Burgers 方程

Burgers 方程同时包含非线性对流与扩散，是冲击形成与黏性平滑的经典模型。扩散系数 $\nu$ 决定非线性与扩散的相对强弱：等效 Reynolds 数较大时易形成陡峭波前，较小时扩散主导。

![1D Burgers (ν = 0.01)](./1D-Burgers.png)

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEBench** |
| 数据集论文 | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| 论文 PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| 官方代码库 | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| 数据 DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| 当前下载类别 | `burgers` |
| 数据量 | 93 GB |
| 生成代码入口 | [data_gen_NLE/BurgersEq](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_gen/data_gen_NLE/BurgersEq) |
| 文档核对日期 | 2026-07-21 |

## 控制方程

\[
\partial_tu+\partial_x\!\left(\frac{u^2}{2}\right)=\frac{\nu}{\pi}\partial_{xx}u,
\qquad x\in(0,1),\quad t\in(0,2],
\]
\[
u(0,x)=u_0(x).
\]

## 变量与坐标

**状态变量**
- $u(t,x)$：标量速度 / 守恒变量。

**参数**
- $\nu$：论文所称 diffusion coefficient；方程中扩散项系数为 $\nu/\pi$。
- 雷诺数类比：$R\equiv\pi u L/\nu$（$R>1$ 偏非线性激波，$R<1$ 偏扩散）。

**坐标与定义域**
- 空间：一维均匀笛卡尔坐标；控制方程写作 $x\in(0,1)$。
- 时间：$t\in(0,2]$。
- 说明：附图与部分生成配置会出现 $[-1,1]$，以 HDF5 坐标 / YAML 为准。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 1 |
| 含时间 | 是 |
| 网格 | 均匀一维笛卡尔 |
| 空间域 | 公式 $x\in(0,1)$；配置常见 $[-1,1]$ |
| 时间范围 | $t\in[0,2]$ |
| 空间分辨率 | $N_x=1024$ |
| 时间点数 | 201 |
| 每文件轨迹数 | 10,000 |
| 通道 | 1：$u$ |
| 单样本形状 | $201\times1024\times1$ |
| 数据量 | 93 GB |
| 格式 | HDF5 |

## 初始条件

与一维平流相同的随机正弦叠加初值族；波数、振幅、相位和 seed 变化。

## 边界条件

周期边界。

## 数值生成方法

非线性对流项采用时间与空间二阶迎风差分；扩散项采用中心差分。

## 参数

| 参数 | 变化方式 | 取值 |
|---|---|---|
| $\nu$（黏性） | 不同 HDF5 文件不同 | $\{0.001,0.002,0.004,0.01,0.02,0.04,0.1,0.2,0.4,1,2,4\}$（12 文件） |
| 初值 $n_i,A_i,\phi_i$ | 每轨迹随机 | 与 1D-advection 同族随机正弦叠加 |
| 边界、时间、分辨率、离散格式 | 固定 | 周期；$N_x=1024$；$t\in[0,2]$ |

## 论文配置

12 个训练参数文件，每个固定一个 $\nu$ 并含 10,000 条轨迹。

## 数据文件

当前官方下载清单（`pdebench_data_urls.csv`）共 **12** 个文件；相对路径相对于下载根目录。详见 [数据格式](../00_data_format/)。

- `1D/Burgers/Train/1D_Burgers_Sols_Nu0.001.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu0.01.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu0.1.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu0.002.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu0.02.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu0.2.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu0.004.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu0.04.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu0.4.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu1.0.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu2.0.hdf5`
- `1D/Burgers/Train/1D_Burgers_Sols_Nu4.0.hdf5`

## 数据布局与机器学习输入输出

标量轨迹预测；适合分别训练单参数模型，也适合把 $\nu$ 作为条件统一训练。

- **轨迹与训练样本：** 完整 HDF5 轨迹不是固定的模型输入。自回归训练通常从完整轨迹切出 $\ell$ 帧输入与下一帧/未来多帧目标；$\ell$ 由训练配置的 `initial_step` 决定。
- **版本优先级：** 方程与初边值以论文为准；文件数、分辨率、轨迹数与通道以当前可下载 HDF5 / 官方清单为准。

## 下载

官方仓库当前推荐 `download_direct.py`，而不是较慢且可能报错的 EasyDataverse 路径。

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name burgers
```

也可以从 [DaRUS DOI 页面](https://doi.org/10.18419/darus-2986) 手动选择文件。下载后应逐文件检查 HDF5 的实际 `shape`、坐标数组、变量键和 YAML attributes，尤其不要仅凭文件名推断 CFD/不可压 NS 的空间分辨率。

## 从官方代码重新生成

```bash
cd PDEBench/pdebench/data_gen/data_gen_NLE/BurgersEq
CUDA_VISIBLE_DEVICES=0 python3 burgers_multi_solution_Hydra.py +multi=1e-1.yaml
bash run_trainset.sh
cd ..
python Data_Merge.py
```

生成器参数可通过对应 Hydra YAML 修改。对 NLE 路径生成的 `.npy` 数据，需要执行 `Data_Merge.py` 才能得到官方 dataloader 使用的 HDF5 布局。

## 数据的兴趣点与挑战

低黏性下形成窄激波与高频结构；同一模型需覆盖扩散主导与非线性主导两个极端。

## 主要来源

- [PDEBench 论文与补充材料](https://arxiv.org/abs/2210.07182)
- [PDEBench 官方代码库](https://github.com/pdebench/PDEBench)
- [官方下载说明](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench 数据集 DOI](https://doi.org/10.18419/darus-2986)
