---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 09_compressible_ns_2d
spatial_dimension: 2
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: 2d_cfd
last_verified: 2026-07-21
title: "二维可压缩 Navier–Stokes / CFD"
linkTitle: "compressible ns 2d"
weight: 90
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "二维可压缩流；扫描 Mach、黏性与初值族。"
description: "二维可压缩流；扫描 Mach、黏性与初值族。"

---

# 二维可压缩 Navier–Stokes / CFD

二维可压缩 Navier–Stokes 在保留可压缩波与激波的同时引入涡结构与湍流谱。训练配置在周期域上扫描 Mach 数、黏性与 random field / turbulence 初值族。

![2D Compressible Navier–Stokes density evolution (inviscid, M = 0.1)](./2D-CNS.png)

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEBench** |
| 数据集论文 | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| 论文 PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| 官方代码库 | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| 数据 DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| 当前下载类别 | `2d_cfd` |
| 数据量 | 551 GB |
| 生成代码入口 | [data_gen_NLE/CompressibleFluid](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_gen/data_gen_NLE/CompressibleFluid) |
| 文档核对日期 | 2026-07-21 |

## 控制方程

\[
\partial_t\rho+\nabla\cdot(\rho\mathbf v)=0,
\]
\[
\rho(\partial_t\mathbf v+\mathbf v\cdot\nabla\mathbf v)
=-\nabla p+\eta\Delta\mathbf v+\left(\zeta+\frac{\eta}{3}\right)\nabla(\nabla\cdot\mathbf v),
\]
\[
\partial_t\!\left(\epsilon+\frac{\rho|\mathbf v|^2}{2}\right)
+\nabla\cdot\!\left[\left(\epsilon+p+\frac{\rho|\mathbf v|^2}{2}\right)\mathbf v-\mathbf v\cdot\boldsymbol\sigma'\right]=0,
\qquad \epsilon=\frac{p}{\Gamma-1},\quad \Gamma=\frac53.
\]

## 变量与坐标

**状态变量**
- $\rho$：质量密度。
- $p$：气体压力。
- $\mathbf{v}=(v_x,v_y)$：二维速度。
- $\epsilon=p/(\Gamma-1)$：内能（由状态方程导出）。

**参数与辅助量**
- $N_d=2$：空间维数。
- $\Gamma=5/3$：比热比。
- $\eta,\zeta$：剪切黏性与体黏性。
- $\boldsymbol{\sigma}'$：黏性应力张量。
- Mach 数 $M=|\mathbf{v}|/c_s$，声速 $c_s=\sqrt{\Gamma p/\rho}$。

**坐标与定义域**
- 空间：二维均匀笛卡尔周期网格；具体坐标范围从 HDF5 / YAML 读取。
- 时间：通常存 21 个时刻；物理时间读坐标 / attributes。
- 逻辑通道顺序：$[\rho,p,v_x,v_y]$。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 2 |
| 含时间 | 是 |
| 网格 | 均匀二维周期笛卡尔 |
| 空间域 | 读 HDF5 坐标 |
| 时间范围 | 读坐标/attributes |
| 空间分辨率 | 多数训练文件 $512\times512$；部分文件 $128\times128$（以 HDF5 shape 为准） |
| 时间点数 | 21 |
| 每文件轨迹数 | 1,000 |
| 通道 | 4：$\rho$、$p$、$v_x$、$v_y$ |
| 单样本形状 | $21\times512\times512\times4$ |
| 数据量 | 551 GB |
| 格式 | HDF5 |

## 初始条件

PDEBench 对可压缩 NS 使用三类初值族。

### 1. Random field

将一维随机正弦叠加（论文 Eq. 8）推广到二维：对各场分量构造多维正弦随机场。密度与压力由“扰动场 + 均匀背景”得到，即在均匀背景上叠加随机扰动。

### 2. Turbulence

质量密度与压力取均匀场。初速度为（论文 Eq. 17）
\[
\mathbf{v}(\mathbf{x},t=0)=\sum_{i=1}^{n}\mathbf{A}_i\sin(k_i x+\phi_i),
\]
其中 $n=4$，振幅 $A_i=\bar{v}/|k_i|^d$，二维取 $d=1$。平均速度 $\bar{v}$ 由初始 Mach 数确定：$\bar{v}=c_s M$，声速 $c_s=\sqrt{\Gamma p/\rho}$。随后在傅里叶空间做 Helmholtz 分解，从上述速度场中减去可压缩分量，以减弱可压缩性影响。

### 3. Shock tube / Riemann

激波管初值写作
\[
Q(\mathbf{x},t=0)=(Q_L,Q_R),\qquad Q=(\rho,\mathbf{v},p),
\]
其中左右常状态 $Q_L,Q_R$ 与间断位置均随机采样。该 Riemann 问题会生成激波与稀疏波，是对 ML 模型较严格的测试；二维主训练清单以 random / turbulence 为主，shock 等常作为额外测试文件。

## 边界条件

- **Periodic：** 8 个主训练配置均为周期边界。
- **Outgoing：** 将邻近内部单元复制到边界 ghost 区，使波与流体离开计算域（天文流体模拟中亦常用）。当前额外测试文件可采用 outgoing 或其他经典流动设置。

## 数值生成方法

守恒律的无粘部分采用时间与空间二阶 **HLLC** Riemann solver，并结合 **MUSCL** 重构；黏性部分采用中心差分。逻辑状态通道由 $\rho$、$p$ 与各方向速度组成；内能由状态方程 $\epsilon=p/(\Gamma-1)$ 导出。

## 参数

| 参数 | 变化方式 | 取值 |
|---|---|---|
| Mach 数 $M$ | 不同 HDF5 配置文件不同 | $M\in\{0.1,1.0\}$ |
| $(\eta,\zeta)$ | 不同 HDF5 配置文件不同 | $(10^{-8},10^{-8})$、$(10^{-2},10^{-2})$、$(10^{-1},10^{-1})$；$\eta=\zeta$ |
| 初值族 | 不同 HDF5 配置文件不同 | random / turbulence（另有 shock、KH、OTVortex 测试文件） |
| 场 realization | 每轨迹随机 | 随机正弦 / 湍流初值 seed |
| $\Gamma$、周期边界、数值格式 | 固定 | $\Gamma=5/3$；periodic（训练主配置） |

发布主训练八配置：

| # | 初值 | $M$ | $(\eta,\zeta)$ |
|---:|---|---:|---|
| 1 | random | 0.1 | $(10^{-8},10^{-8})$ |
| 2 | random | 0.1 | $(10^{-2},10^{-2})$ |
| 3 | random | 0.1 | $(10^{-1},10^{-1})$ |
| 4 | random | 1.0 | $(10^{-8},10^{-8})$ |
| 5 | random | 1.0 | $(10^{-2},10^{-2})$ |
| 6 | random | 1.0 | $(10^{-1},10^{-1})$ |
| 7 | turbulence | 0.1 | $(10^{-8},10^{-8})$ |
| 8 | turbulence | 1.0 | $(10^{-8},10^{-8})$ |

## 论文配置

8 个主训练配置。当前清单还包含 2D shock、Kelvin–Helmholtz 与 `OTVortex` 等测试文件，这些应单列为 OOD/经典测试。

## 数据文件

当前官方下载清单（`pdebench_data_urls.csv`）共 **17** 个文件；相对路径相对于下载根目录。详见 [数据格式](../00_data_format/)。

- `2D/CFD/2D_Train_Rand/2D_CFD_Rand_M0.1_Eta0.01_Zeta0.01_periodic_128_Train.hdf5`
- `2D/CFD/2D_Train_Rand/2D_CFD_Rand_M0.1_Eta0.1_Zeta0.1_periodic_128_Train.hdf5`
- `2D/CFD/2D_Train_Rand/2D_CFD_Rand_M0.1_Eta1e-08_Zeta1e-08_periodic_512_Train.hdf5`
- `2D/CFD/2D_Train_Rand/2D_CFD_Rand_M1.0_Eta0.01_Zeta0.01_periodic_128_Train.hdf5`
- `2D/CFD/2D_Train_Rand/2D_CFD_Rand_M1.0_Eta0.1_Zeta0.1_periodic_128_Train.hdf5`
- `2D/CFD/2D_Train_Rand/2D_CFD_Rand_M1.0_Eta1e-08_Zeta1e-08_periodic_512_Train.hdf5`
- `2D/CFD/2D_Train_Turb/2D_CFD_Turb_M0.1_Eta1e-08_Zeta1e-08_periodic_512_Train.hdf5`
- `2D/CFD/2D_Train_Turb/2D_CFD_Turb_M1.0_Eta1e-08_Zeta1e-08_periodic_512_Train.hdf5`
- `2D/CFD/Test/2DShock/2D_shock.hdf5`
- `2D/CFD/Test/KH/KH_M01_dk1_Re1e3.hdf5`
- `2D/CFD/Test/KH/KH_M1_dk1_Re1e3.hdf5`
- `2D/CFD/Test/KH/KH_M01_dk2_Re1e3.hdf5`
- `2D/CFD/Test/KH/KH_M01_dk5_Re1e3.hdf5`
- `2D/CFD/Test/KH/KH_M01_dk10_Re1e3.hdf5`
- `2D/CFD/Test/KH/KH_M02_dk1_Re1e3.hdf5`
- `2D/CFD/Test/KH/KH_M04_dk1_Re1e3.hdf5`
- `2D/CFD/Test/TOV/OTVortex.hdf5`

## 数据布局与机器学习输入输出

四通道时序预测；建议条件中显式加入 $M,\eta,\zeta$ 与 `random/turbulence` 标签。

- **轨迹与训练样本：** 完整 HDF5 轨迹不是固定的模型输入。自回归训练通常从完整轨迹切出 $\ell$ 帧输入与下一帧/未来多帧目标；$\ell$ 由训练配置的 `initial_step` 决定。
- **版本优先级：** 方程与初边值以论文为准；文件数、分辨率、轨迹数与通道以当前可下载 HDF5 / 官方清单为准。

## 下载

官方仓库当前推荐 `download_direct.py`，而不是较慢且可能报错的 EasyDataverse 路径。

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name 2d_cfd
```

也可以从 [DaRUS DOI 页面](https://doi.org/10.18419/darus-2986) 手动选择文件。下载后应逐文件检查 HDF5 的实际 `shape`、坐标数组、变量键和 YAML attributes，尤其不要仅凭文件名推断 CFD/不可压 NS 的空间分辨率。

## 从官方代码重新生成

```bash
cd PDEBench/pdebench/data_gen/data_gen_NLE/CompressibleFluid
bash run_trainset_2D.sh
bash run_trainset_2DTurb.sh
# optional test sets
bash run_testset.sh
bash run_testset_KHI.sh
cd ..
python Data_Merge.py
```

生成器参数可通过对应 Hydra YAML 修改。对 NLE 路径生成的 `.npy` 数据，需要执行 `Data_Merge.py` 才能得到官方 dataloader 使用的 HDF5 布局。

## 数据的兴趣点与挑战

高分辨率单轨迹极大、激波与涡并存、Mach/黏性跨配置变化；部分文件为 $128^2$ 而非 $512^2$，加载前应核对 shape。

## 主要来源

- [PDEBench 论文与补充材料](https://arxiv.org/abs/2210.07182)
- [PDEBench 官方代码库](https://github.com/pdebench/PDEBench)
- [官方下载说明](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench 数据集 DOI](https://doi.org/10.18419/darus-2986)
