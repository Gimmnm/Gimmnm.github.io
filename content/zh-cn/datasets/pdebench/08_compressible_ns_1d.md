---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 08_compressible_ns_1d
spatial_dimension: 1
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: 1d_cfd
last_verified: 2026-07-21
title: "一维可压缩 Navier–Stokes / CFD"
linkTitle: "compressible ns 1d"
weight: 80
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "一维可压缩守恒律；含随机场与激波管等配置。"
description: "一维可压缩守恒律；含随机场与激波管等配置。"

---

# 一维可压缩 Navier–Stokes / CFD

可压缩 Navier–Stokes 描述密度、速度与压力耦合的守恒律系统，可产生声波、接触间断、激波与稀疏波等结构。一维配置通过黏性、初值族与边界类型覆盖从光滑随机场到 Riemann 激波管的难度谱。

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEBench** |
| 数据集论文 | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| 论文 PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| 官方代码库 | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| 数据 DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| 当前下载类别 | `1d_cfd` |
| 数据量 | 88 GB |
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
- $\mathbf{v}$（一维为 $v_x$）：速度。
- $\epsilon=p/(\Gamma-1)$：内能（由状态方程导出，一般不单独作为独立论文通道）。

**参数与辅助量**
- $N_d=1$：空间维数。
- $\Gamma=5/3$：比热比。
- $\eta,\zeta$：剪切黏性与体黏性。
- $\boldsymbol{\sigma}'$：黏性应力张量。
- Mach 数 $M=|\mathbf{v}|/c_s$，声速 $c_s=\sqrt{\Gamma p/\rho}$（一维训练配置通常不扫 $M$）。

**坐标与定义域**
- 空间：一维均匀笛卡尔网格；具体域长与坐标数组从 HDF5 / 生成 YAML 读取（论文未给全部 CFD 文件统一域）。
- 时间：通常存 100 个时刻；物理时间读坐标 / attributes。
- 逻辑通道顺序：$[\rho,p,v_x]$（HDF5 中常分 dataset 存储）。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 1 |
| 含时间 | 是 |
| 网格 | 均匀一维笛卡尔 |
| 空间域 | 读 HDF5 坐标 |
| 时间范围 | 读坐标数组 |
| 空间分辨率 | 1024 |
| 时间点数 | 100 |
| 每文件轨迹数 | 10,000 |
| 通道 | 3：$\rho$、$p$、$v_x$ |
| 单样本形状 | $100\times1024\times3$ |
| 数据量 | 88 GB |
| 格式 | HDF5 |

## 初始条件

PDEBench 对可压缩 NS 使用三类初值族。

### 1. Random field

采用论文 Eq. 8 的随机正弦叠加，并扩展到本维设置。密度与压力由“扰动场 + 均匀背景”得到，即在均匀背景上叠加随机扰动。

### 2. Turbulence

质量密度与压力取均匀场。初速度为（论文 Eq. 17）
\[
\mathbf{v}(x,t=0)=\sum_{i=1}^{n}\mathbf{A}_i\sin(k_i x+\phi_i),
\]
其中 $n=4$，振幅 $A_i=\bar{v}/|k_i|^d$。平均速度 $\bar{v}$ 由初始 Mach 数确定：$\bar{v}=c_s M$，声速 $c_s=\sqrt{\Gamma p/\rho}$。随后在傅里叶空间做 Helmholtz 分解，从上述速度场中减去可压缩分量，以减弱可压缩性影响。一维主训练清单以 random / shock tube 为主；turbulence 族在更高维配置中更常见。

### 3. Shock tube / Riemann

激波管初值写作
\[
Q(x,t=0)=(Q_L,Q_R),\qquad Q=(\rho,v,p),
\]
其中左右常状态 $Q_L,Q_R$ 与间断位置均随机采样。该 Riemann 问题会生成激波与稀疏波，是对 ML 模型较严格的测试。

## 边界条件

训练配置使用 **periodic** 或 **outgoing**（文件/脚本中常记为 `trans`）。

- **Periodic：** 周期边界，用于多数 random 训练配置。
- **Outgoing：** 将邻近内部单元复制到边界 ghost 区，使波与流体离开计算域（天文流体模拟中亦常用）；shock tube 配置使用 outgoing。

## 数值生成方法

守恒律的无粘部分采用时间与空间二阶 **HLLC** Riemann solver，并结合 **MUSCL** 重构；黏性部分采用中心差分。逻辑状态通道由 $\rho$、$p$ 与速度组成；内能由状态方程 $\epsilon=p/(\Gamma-1)$ 导出。

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

前 5 行为主训练扫描；`Sod*` 是**额外测试/经典激波管**（不在主训练的初值随机扫描里），但**同样有参数**：YAML 中 `init_mode=shocktube1…7`，`bc=trans`，$(\eta,\zeta)=(10^{-8},10^{-8})$，$\Gamma=5/3$。一维主训练不扫 Mach，故 $M$ 记为 —。

> **“额外测试集”是什么：** 相对主训练分布（随机场 / 随机 Riemann）的**固定经典算例**，用来做泛化评测；英文文献常称 OOD（out-of-distribution）测试。不是“没有参数”。

| 数据文件 | initial field | boundary | $(\eta,\zeta,M)$ | 每轨迹随机 | 备注 |
|---|---|---|---|---|---|
| `1D_CFD_Rand_Eta1.e-8_Zeta1.e-8_periodic_Train.hdf5` | random field | periodic | $(10^{-8},10^{-8},\text{—})$ | 随机场 realization | 主训练 |
| `1D_CFD_Rand_Eta0.01_Zeta0.01_periodic_Train.hdf5` | random field | periodic | $(10^{-2},10^{-2},\text{—})$ | 同上 | 主训练 |
| `1D_CFD_Rand_Eta0.1_Zeta0.1_periodic_Train.hdf5` | random field | periodic | $(10^{-1},10^{-1},\text{—})$ | 同上 | 主训练 |
| `1D_CFD_Rand_Eta1.e-8_Zeta1.e-8_trans_Train.hdf5` | random field | outgoing (`trans`) | $(10^{-8},10^{-8},\text{—})$ | 同上 | 主训练 |
| `1D_CFD_Shock_Eta1.e-8_Zeta1.e-8_trans_Train.hdf5` | shock-tube（随机 Riemann） | outgoing (`trans`) | $(10^{-8},10^{-8},\text{—})$ | 左右态与间断位置随机 | 主训练 |
| `Sod1.hdf5` | `shocktube1`（固定经典） | outgoing | $(10^{-8},10^{-8},\text{—})$ | 否（初值固定） | 额外测试集 |
| `Sod2.hdf5` | `shocktube2` | outgoing | $(10^{-8},10^{-8},\text{—})$ | 否 | 额外测试集 |
| `Sod3.hdf5` | `shocktube3` | outgoing | $(10^{-8},10^{-8},\text{—})$ | 否 | 额外测试集 |
| `Sod4.hdf5` | `shocktube4` | outgoing | $(10^{-8},10^{-8},\text{—})$ | 否 | 额外测试集 |
| `Sod5.hdf5` | `shocktube5` | outgoing | $(10^{-8},10^{-8},\text{—})$ | 否 | 额外测试集 |
| `Sod6.hdf5` | `shocktube6` | outgoing | $(10^{-8},10^{-8},\text{—})$ | 否 | 额外测试集（清单在 Train/ShockTube） |
| `Sod7.hdf5` | `shocktube7` | outgoing | $(10^{-8},10^{-8},\text{—})$ | 否 | 额外测试集 |

各 `Sod*` 的左右常状态数值以对应 YAML / HDF5 attributes 为准（`fin_time` 等也可能不同）。

### 生成器可调范围

| 参数 | 可调范围 / 选项 | 发布数据是否覆盖 |
|---|---|---|
| $\eta,\zeta$（常取 $\eta=\zeta$） | 任意非负；常用 $\{10^{-8},10^{-2},10^{-1}\}$ | 主训练覆盖这三档 |
| 边界 | `periodic` / `trans`（outgoing）等 | 是 |
| 初值族 | random / shock-tube（随机）/ `shocktube1…7`（固定）等 | 是（含随机与经典） |
| Mach $M$ | YAML 有 `M0`；一维主训练通常不扫 | 一维发布主训练未扫 $M$ |
| $\Gamma$、网格、CFL、时间窗 | 可改 | 发布主训练大致固定 |

## 数据文件

当前官方下载清单（`pdebench_data_urls.csv`）共 **12** 个文件；相对路径相对于下载根目录。详见 [数据格式](../00_data_format/)。

- `1D/CFD/Train/1D_CFD_Rand_Eta0.01_Zeta0.01_periodic_Train.hdf5`
- `1D/CFD/Train/1D_CFD_Rand_Eta0.1_Zeta0.1_periodic_Train.hdf5`
- `1D/CFD/Train/1D_CFD_Rand_Eta1.e-8_Zeta1.e-8_periodic_Train.hdf5`
- `1D/CFD/Train/1D_CFD_Rand_Eta1.e-8_Zeta1.e-8_trans_Train.hdf5`
- `1D/CFD/Train/1D_CFD_Shock_Eta1.e-8_Zeta1.e-8_trans_Train.hdf5`
- `1D/CFD/Train/ShockTube/Sod6.hdf5`
- `1D/CFD/Test/ShockTube/Sod1.hdf5`
- `1D/CFD/Test/ShockTube/Sod2.hdf5`
- `1D/CFD/Test/ShockTube/Sod3.hdf5`
- `1D/CFD/Test/ShockTube/Sod4.hdf5`
- `1D/CFD/Test/ShockTube/Sod5.hdf5`
- `1D/CFD/Test/ShockTube/Sod7.hdf5`

## 数据布局与机器学习输入输出

多物理量轨迹预测。加载时将独立 HDF5 arrays 对齐为 $[\rho,p,v_x]$，并可附加 $(\eta,\zeta)$、边界类型和初值类型条件。

- **轨迹与训练样本：** 完整 HDF5 轨迹不是固定的模型输入。自回归训练通常从完整轨迹切出 $\ell$ 帧输入与下一帧/未来多帧目标；$\ell$ 由训练配置的 `initial_step` 决定。
- **版本优先级：** 方程与初边值以论文为准；文件数、分辨率、轨迹数与通道以当前可下载 HDF5 / 官方清单为准。

## 下载

官方仓库当前推荐 `download_direct.py`，而不是较慢且可能报错的 EasyDataverse 路径。

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name 1d_cfd
```

也可以从 [DaRUS DOI 页面](https://doi.org/10.18419/darus-2986) 手动选择文件。下载后应逐文件检查 HDF5 的实际 `shape`、坐标数组、变量键和 YAML attributes，尤其不要仅凭文件名推断 CFD/不可压 NS 的空间分辨率。

## 从官方代码重新生成

```bash
cd PDEBench/pdebench/data_gen/data_gen_NLE/CompressibleFluid
# main random-field configurations
bash run_trainset_1D.sh
# outgoing and shock-tube variants
bash run_trainset_1D_trans.sh
bash run_trainset_1DShock.sh
cd ..
python Data_Merge.py
```

生成器参数可通过对应 Hydra YAML 修改。对 NLE 路径生成的 `.npy` 数据，需要执行 `Data_Merge.py` 才能得到官方 dataloader 使用的 HDF5 布局。

## 数据的兴趣点与挑战

守恒耦合、强间断、边界类型变化、黏性跨数量级和各通道量纲尺度差异。

## 主要来源

- [PDEBench 论文与补充材料](https://arxiv.org/abs/2210.07182)
- [PDEBench 官方代码库](https://github.com/pdebench/PDEBench)
- [官方下载说明](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench 数据集 DOI](https://doi.org/10.18419/darus-2986)
