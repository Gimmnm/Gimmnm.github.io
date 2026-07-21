---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 10_compressible_ns_3d
spatial_dimension: 3
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: 3d_cfd
last_verified: 2026-07-21
title: "三维可压缩 Navier–Stokes / CFD"
linkTitle: "compressible ns 3d"
weight: 100
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "三维可压缩流；高维、大体积、少样本。"
description: "三维可压缩流；高维、大体积、少样本。"

---

# 三维可压缩 Navier–Stokes / CFD

三维可压缩 Navier–Stokes 把同一守恒律系统推到高维网格，单条轨迹体积大、样本相对稀少，用于评估高维内存占用与少样本条件下的建模能力。

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEBench** |
| 数据集论文 | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| 论文 PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| 官方代码库 | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| 数据 DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| 当前下载类别 | `3d_cfd` |
| 数据量 | 285 GB |
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
- $\mathbf{v}=(v_x,v_y,v_z)$：三维速度。
- $\epsilon=p/(\Gamma-1)$：内能（由状态方程导出）。

**参数与辅助量**
- $N_d=3$：空间维数。
- $\Gamma=5/3$：比热比。
- $\eta,\zeta$：剪切黏性与体黏性。
- $\boldsymbol{\sigma}'$：黏性应力张量。
- Mach 数 $M=|\mathbf{v}|/c_s$，声速 $c_s=\sqrt{\Gamma p/\rho}$。

**坐标与定义域**
- 空间：三维均匀笛卡尔周期网格；具体坐标从 HDF5 / YAML 读取。
- 时间：通常存 21 个时刻。
- 逻辑通道顺序：$[\rho,p,v_x,v_y,v_z]$。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 3 |
| 含时间 | 是 |
| 网格 | 均匀三维周期笛卡尔 |
| 空间域 | 读 HDF5 坐标 |
| 时间范围 | 21 个存储时刻 |
| 空间分辨率 | $128\times128\times128$ |
| 时间点数 | 21 |
| 每文件轨迹数 | 100 |
| 通道 | 5：$\rho$、$p$、$v_x$、$v_y$、$v_z$ |
| 单样本形状 | $21\times128^3\times5$ |
| 数据量 | 285 GB |
| 格式 | HDF5 |

## 初始条件

PDEBench 对可压缩 NS 使用三类初值族。

### 1. Random field

将一维随机正弦叠加（论文 Eq. 8）推广到三维：对各场分量构造多维正弦随机场。密度与压力由“扰动场 + 均匀背景”得到，即在均匀背景上叠加随机扰动。

### 2. Turbulence

质量密度与压力取均匀场。初速度为（论文 Eq. 17）
\[
\mathbf{v}(\mathbf{x},t=0)=\sum_{i=1}^{n}\mathbf{A}_i\sin(k_i x+\phi_i),
\]
其中 $n=4$，振幅 $A_i=\bar{v}/|k_i|^d$，三维取 $d=2$。平均速度 $\bar{v}$ 由初始 Mach 数确定：$\bar{v}=c_s M$，声速 $c_s=\sqrt{\Gamma p/\rho}$。随后在傅里叶空间做 Helmholtz 分解，从上述速度场中减去可压缩分量，以减弱可压缩性影响。

### 3. Shock tube / Riemann

激波管初值写作
\[
Q(\mathbf{x},t=0)=(Q_L,Q_R),\qquad Q=(\rho,\mathbf{v},p),
\]
其中左右常状态 $Q_L,Q_R$ 与间断位置均随机采样。该 Riemann 问题会生成激波与稀疏波；三维主训练口径以 random / turbulence 为主，BlastWave 等常作为额外测试文件。

## 边界条件

- **Periodic：** 主训练配置为周期边界。
- **Outgoing：** 将邻近内部单元复制到边界 ghost 区，使波与流体离开计算域；额外测试文件可能采用其他边界设置。

## 数值生成方法

守恒律的无粘部分采用时间与空间二阶 **HLLC** Riemann solver，并结合 **MUSCL** 重构；黏性部分采用中心差分。逻辑状态通道由 $\rho$、$p$ 与各方向速度组成；内能由状态方程 $\epsilon=p/(\Gamma-1)$ 导出。

## 参数

对照公式：

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

### 发布文件配置

**与论文差异：** 论文参数表还有三维 $(\eta,\zeta)=(10^{-2},10^{-2})$ 等行，当前可下载训练文件仅近无粘 $(10^{-8},10^{-8})$。  
`BlastWave` / `Turb_M*` 为**额外测试集**，参数来自文件名与 YAML（例如 `M0`）。

| 数据文件 | initial field | boundary | $(\eta,\zeta,M)$ | 每轨迹随机 | 备注 |
|---|---|---|---|---|---|
| `3D_CFD_Rand_M1.0_Eta1e-08_Zeta1e-08_periodic_Train.hdf5` | random field | periodic | $(10^{-8},10^{-8},1.0)$ | 随机场 | 主训练 |
| `3D_CFD_Turb_M1.0_Eta1e-08_Zeta1e-08_periodic_Train.hdf5` | turbulence | periodic | $(10^{-8},10^{-8},1.0)$ | 湍流 seed | 主训练 |
| `BlastWave.hdf5` | blast wave | outgoing (`trans`) | $(10^{-8},10^{-8},1.0)$；$256^3$ | 否 | 额外测试集（YAML） |
| `Turb_M01.hdf5` | turbulence | periodic | $(10^{-8},10^{-8},0.1)$；$256^3$ | 否（`numbers=4`） | 额外测试集（YAML） |
| `Turb_M05.hdf5` | turbulence | periodic | $(10^{-8},10^{-8},0.5)$；$256^3$ | 否（少样本） | 额外测试集 |
| `Turb_M1.hdf5` | turbulence | periodic | $(10^{-8},10^{-8},1.0)$；$256^3$ | 否（少样本） | 额外测试集 |
| `Turb_M2.hdf5` | turbulence | periodic | $(10^{-8},10^{-8},2.0)$；$256^3$ | 否（少样本） | 额外测试集 |
| `Turb_M4.hdf5` | turbulence | periodic | $(10^{-8},10^{-8},4.0)$；$256^3$ | 否（少样本） | 额外测试集 |

### 生成器可调范围

| 参数 | 可调范围 / 选项 | 发布数据是否覆盖 |
|---|---|---|
| $\eta,\zeta$ | 任意非负；论文亦列 $10^{-2}$ | 训练发布仅 $10^{-8}$；可用生成器补扫 |
| $M$ | 任意正实数 | 训练发布 $M=1$；测试另有 $0.1,0.5,2,4$ |
| 初值族 | random / turbulence / blast … | 是 |
| 网格（YAML 测试可为 $256^3$ 等） | 可改 | 主训练发布标称 $128^3$ |

## 数据文件

当前官方下载清单（`pdebench_data_urls.csv`）共 **8** 个文件；相对路径相对于下载根目录。详见 [数据格式](../00_data_format/)。

- `3D/Train/3D_CFD_Rand_M1.0_Eta1e-08_Zeta1e-08_periodic_Train.hdf5`
- `3D/Train/3D_CFD_Turb_M1.0_Eta1e-08_Zeta1e-08_periodic_Train.hdf5`
- `3D/Test/BlastWave/BlastWave.hdf5`
- `3D/Test/Turbulence/Turb_M01.hdf5`
- `3D/Test/Turbulence/Turb_M1.hdf5`
- `3D/Test/Turbulence/Turb_M2.hdf5`
- `3D/Test/Turbulence/Turb_M4.hdf5`
- `3D/Test/Turbulence/Turb_M05.hdf5`

## 数据布局与机器学习输入输出

五通道三维时序预测。由于单轨迹约含 $2.20\times10^8$ 个标量，通常需要空间/时间下采样、patching、分片 I/O 或并行训练。

- **轨迹与训练样本：** 完整 HDF5 轨迹不是固定的模型输入。自回归训练通常从完整轨迹切出 $\ell$ 帧输入与下一帧/未来多帧目标；$\ell$ 由训练配置的 `initial_step` 决定。
- **版本优先级：** 方程与初边值以论文为准；文件数、分辨率、轨迹数与通道以当前可下载 HDF5 / 官方清单为准。

## 下载

官方仓库当前推荐 `download_direct.py`，而不是较慢且可能报错的 EasyDataverse 路径。

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name 3d_cfd
```

也可以从 [DaRUS DOI 页面](https://doi.org/10.18419/darus-2986) 手动选择文件。下载后应逐文件检查 HDF5 的实际 `shape`、坐标数组、变量键和 YAML attributes，尤其不要仅凭文件名推断 CFD/不可压 NS 的空间分辨率。

## 从官方代码重新生成

```bash
cd PDEBench/pdebench/data_gen/data_gen_NLE/CompressibleFluid
bash run_trainset_3D.sh
bash run_trainset_3DTurb.sh
# optional 3D turbulence tests
bash run_testset_3DTurb.sh
cd ..
python Data_Merge.py
```

生成器参数可通过对应 Hydra YAML 修改。对 NLE 路径生成的 `.npy` 数据，需要执行 `Data_Merge.py` 才能得到官方 dataloader 使用的 HDF5 布局。

## 数据的兴趣点与挑战

极端内存和 I/O、仅 100 级样本、三维多尺度结构、长 rollout 稳定性，以及论文配置表内部不一致。

## 主要来源

- [PDEBench 论文与补充材料](https://arxiv.org/abs/2210.07182)
- [PDEBench 官方代码库](https://github.com/pdebench/PDEBench)
- [官方下载说明](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench 数据集 DOI](https://doi.org/10.18419/darus-2986)
