---
parent_dataset: PDEBench
dataset_id: pdebench
equation_id: 11_incompressible_ns_2d
spatial_dimension: 2
time_dependent: true
data_format: HDF5
paper: "arXiv:2210.07182v7"
dataset_doi: 10.18419/darus-2986
download_key: ns_incom
last_verified: 2026-07-21
title: "二维非均匀强迫不可压 Navier–Stokes"
linkTitle: "incompressible ns 2d"
weight: 110
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEBench
summary: "带空间非均匀外力的不可压流；非周期 Dirichlet 边界。"
description: "带空间非均匀外力的不可压流；非周期 Dirichlet 边界。"

---

# 二维非均匀强迫不可压 Navier–Stokes

不可压 Navier–Stokes 适用于波速远高于流动速度的情形。PDEBench 采用带空间非均匀外力的增广形式，并使用非周期 Dirichlet 边界，以挑战习惯周期卷积的模型；外力场也可作为反演目标。

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEBench** |
| 数据集论文 | [PDEBench: An Extensive Benchmark for Scientific Machine Learning](https://arxiv.org/abs/2210.07182) |
| 论文 PDF | [arXiv PDF](https://arxiv.org/pdf/2210.07182) |
| 官方代码库 | [pdebench/PDEBench](https://github.com/pdebench/PDEBench) |
| 数据 DOI / DaRUS | [10.18419/darus-2986](https://doi.org/10.18419/darus-2986) |
| 当前下载类别 | `ns_incom` |
| 数据量 | 2.3 TB |
| 生成代码入口 | [gen_ns_incomp.py + configs/ns_incomp.yaml](https://github.com/pdebench/PDEBench/blob/main/pdebench/data_gen/gen_ns_incomp.py) |
| 文档核对日期 | 2026-07-21 |

## 控制方程

\[
\nabla\cdot\mathbf v=0,
\]
\[
\rho(\partial_t\mathbf v+\mathbf v\cdot\nabla\mathbf v)
=-\nabla p+\eta\Delta\mathbf v+\mathbf f(\mathbf x).
\]

## 变量与坐标

**状态变量**
- $\mathbf{v}=(v_x,v_y)$：不可压缩速度场（动态预测目标）。
- $p$：约束压力（由不可压条件决定）。

**条件场与参数**
- $\mathbf{f}=(f_x,f_y)$：空间变化、时间固定的外力场（静态条件输入）。
- 论文增广方程中外力记为 $\mathbf{u}$；本文用 $\mathbf{f}$，以免与速度混淆。
- $\rho$：密度（均匀介质假设）。
- $\eta$（论文中常写作黏性 $\nu=0.01$）：黏性系数。

**坐标与定义域**
- 空间：二维均匀笛卡尔，$\Omega=[0,1]^2$；PhiFlow staggered / scalar grid 细节由生成器处理。
- 时间：当前配置总时长约 $5$（$10^5$ 步 $\times 5\cdot10^{-5}$），按间隔存帧。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 2 |
| 含时间 | 是 |
| 网格 | 均匀二维笛卡尔 |
| 空间域 | $[0,1]^2$ |
| 时间范围 | 物理时间约 5 |
| 空间分辨率 | $256\times256$ |
| 时间点数 | 1,000 |
| 每文件轨迹数 | 1,000（分片下载） |
| 通道 | 动态 2：$v_x$、$v_y$；条件 2：$f_x$、$f_y$ |
| 单样本形状 | 速度 $1000\times256\times256\times2$（外力另存） |
| 数据量 | 2.3 TB |
| 格式 | HDF5 分片 |

## 初始条件

初速度与外力分别从各向同性 Gaussian random field 采样。论文给 $\tau_{v_0}=-3,\sigma_{v_0}=0.15$，$\tau_f=-1,\sigma_f=0.4$；样本差异主要来自随机 seed。当前 YAML 中参数键为 `smoothness=1.0, scale=0.4, force_smoothness=3.0, force_scale=0.15`，命名与论文符号对应关系应按生成器解释。

## 边界条件

Dirichlet no-slip：边界速度固定为零。当前配置 `velocity_extrapolation: ZERO`、`force_extrapolation: ZERO`。

## 数值生成方法

论文使用 PhiFlow。当前 `ns_incomp.yaml`：`domain_size=[1,1]`, `grid_size=[256,256]`, `NU=0.01`, `n_steps=100000`, `DT=5e-5`, `frame_int=100`, backend JAX, GPU, JIT。

## 参数

对照公式：

\[
\nabla\cdot\mathbf v=0,
\]
\[
\rho(\partial_t\mathbf v+\mathbf v\cdot\nabla\mathbf v)
=-\nabla p+\eta\Delta\mathbf v+\mathbf f(\mathbf x).
\]

### 发布文件配置

274 个分片为**同一物理配置**。文件名含 `512`，实际网格以论文 / YAML 为准为 **$256\times256$**。

| 数据文件（模式） | $\nu$ | 边界 | 每轨迹随机 | 固定 |
|---|---:|---|---|---|
| `ns_incom_inhom_2d_512-{0…274\setminus49}.h5` | $0.01$ | no-slip Dirichlet | 初速度 GRF、外力 GRF | 域 $[0,1]^2$，$256^2$，$N_t=1000$ |

### 生成器可调范围

| 参数 | 可调范围 / 选项 | 发布数据是否覆盖 |
|---|---|---|
| $\nu$（`NU`） | 任意正实数 | 否（固定 $0.01$） |
| GRF：`smoothness, scale, force_smoothness, force_scale` | 可改 | 否（发布用 YAML 默认） |
| `grid_size`, `DT`, `n_steps`, `frame_int` | 可改 | 否（发布对应 $256^2$、$N_t=1000$） |
| 边界外推方式 | 可改 | 否（`ZERO` no-slip） |

## 数据文件

当前官方下载清单（`pdebench_data_urls.csv`）共 **274** 个文件；相对路径相对于下载根目录。详见 [数据格式](../00_data_format/)。

分片模式：`2D/NS_incom/ns_incom_inhom_2d_512-{i}.h5`，索引 $0$–$274$，缺索引 `49`，合计 274 个。文件名中的 `512` 不代表网格分辨率。

完整文件名：

```
ns_incom_inhom_2d_512-0.h5
ns_incom_inhom_2d_512-1.h5
ns_incom_inhom_2d_512-2.h5
ns_incom_inhom_2d_512-3.h5
ns_incom_inhom_2d_512-4.h5
ns_incom_inhom_2d_512-5.h5
ns_incom_inhom_2d_512-6.h5
ns_incom_inhom_2d_512-7.h5
ns_incom_inhom_2d_512-8.h5
ns_incom_inhom_2d_512-9.h5
ns_incom_inhom_2d_512-10.h5
ns_incom_inhom_2d_512-11.h5
ns_incom_inhom_2d_512-12.h5
ns_incom_inhom_2d_512-13.h5
ns_incom_inhom_2d_512-14.h5
ns_incom_inhom_2d_512-15.h5
ns_incom_inhom_2d_512-16.h5
ns_incom_inhom_2d_512-17.h5
ns_incom_inhom_2d_512-18.h5
ns_incom_inhom_2d_512-19.h5
ns_incom_inhom_2d_512-20.h5
ns_incom_inhom_2d_512-21.h5
ns_incom_inhom_2d_512-22.h5
ns_incom_inhom_2d_512-23.h5
ns_incom_inhom_2d_512-24.h5
ns_incom_inhom_2d_512-25.h5
ns_incom_inhom_2d_512-26.h5
ns_incom_inhom_2d_512-27.h5
ns_incom_inhom_2d_512-28.h5
ns_incom_inhom_2d_512-29.h5
ns_incom_inhom_2d_512-30.h5
ns_incom_inhom_2d_512-31.h5
ns_incom_inhom_2d_512-32.h5
ns_incom_inhom_2d_512-33.h5
ns_incom_inhom_2d_512-34.h5
ns_incom_inhom_2d_512-35.h5
ns_incom_inhom_2d_512-36.h5
ns_incom_inhom_2d_512-37.h5
ns_incom_inhom_2d_512-38.h5
ns_incom_inhom_2d_512-39.h5
ns_incom_inhom_2d_512-40.h5
ns_incom_inhom_2d_512-41.h5
ns_incom_inhom_2d_512-42.h5
ns_incom_inhom_2d_512-43.h5
ns_incom_inhom_2d_512-44.h5
ns_incom_inhom_2d_512-45.h5
ns_incom_inhom_2d_512-46.h5
ns_incom_inhom_2d_512-47.h5
ns_incom_inhom_2d_512-48.h5
ns_incom_inhom_2d_512-50.h5
ns_incom_inhom_2d_512-51.h5
ns_incom_inhom_2d_512-52.h5
ns_incom_inhom_2d_512-53.h5
ns_incom_inhom_2d_512-54.h5
ns_incom_inhom_2d_512-55.h5
ns_incom_inhom_2d_512-56.h5
ns_incom_inhom_2d_512-57.h5
ns_incom_inhom_2d_512-58.h5
ns_incom_inhom_2d_512-59.h5
ns_incom_inhom_2d_512-60.h5
ns_incom_inhom_2d_512-61.h5
ns_incom_inhom_2d_512-62.h5
ns_incom_inhom_2d_512-63.h5
ns_incom_inhom_2d_512-64.h5
ns_incom_inhom_2d_512-65.h5
ns_incom_inhom_2d_512-66.h5
ns_incom_inhom_2d_512-67.h5
ns_incom_inhom_2d_512-68.h5
ns_incom_inhom_2d_512-69.h5
ns_incom_inhom_2d_512-70.h5
ns_incom_inhom_2d_512-71.h5
ns_incom_inhom_2d_512-72.h5
ns_incom_inhom_2d_512-73.h5
ns_incom_inhom_2d_512-74.h5
ns_incom_inhom_2d_512-75.h5
ns_incom_inhom_2d_512-76.h5
ns_incom_inhom_2d_512-77.h5
ns_incom_inhom_2d_512-78.h5
ns_incom_inhom_2d_512-79.h5
ns_incom_inhom_2d_512-80.h5
ns_incom_inhom_2d_512-81.h5
ns_incom_inhom_2d_512-82.h5
ns_incom_inhom_2d_512-83.h5
ns_incom_inhom_2d_512-84.h5
ns_incom_inhom_2d_512-85.h5
ns_incom_inhom_2d_512-86.h5
ns_incom_inhom_2d_512-87.h5
ns_incom_inhom_2d_512-88.h5
ns_incom_inhom_2d_512-89.h5
ns_incom_inhom_2d_512-90.h5
ns_incom_inhom_2d_512-91.h5
ns_incom_inhom_2d_512-92.h5
ns_incom_inhom_2d_512-93.h5
ns_incom_inhom_2d_512-94.h5
ns_incom_inhom_2d_512-95.h5
ns_incom_inhom_2d_512-96.h5
ns_incom_inhom_2d_512-97.h5
ns_incom_inhom_2d_512-98.h5
ns_incom_inhom_2d_512-99.h5
ns_incom_inhom_2d_512-100.h5
ns_incom_inhom_2d_512-101.h5
ns_incom_inhom_2d_512-102.h5
ns_incom_inhom_2d_512-103.h5
ns_incom_inhom_2d_512-104.h5
ns_incom_inhom_2d_512-105.h5
ns_incom_inhom_2d_512-106.h5
ns_incom_inhom_2d_512-107.h5
ns_incom_inhom_2d_512-108.h5
ns_incom_inhom_2d_512-109.h5
ns_incom_inhom_2d_512-110.h5
ns_incom_inhom_2d_512-111.h5
ns_incom_inhom_2d_512-112.h5
ns_incom_inhom_2d_512-113.h5
ns_incom_inhom_2d_512-114.h5
ns_incom_inhom_2d_512-115.h5
ns_incom_inhom_2d_512-116.h5
ns_incom_inhom_2d_512-117.h5
ns_incom_inhom_2d_512-118.h5
ns_incom_inhom_2d_512-119.h5
ns_incom_inhom_2d_512-120.h5
ns_incom_inhom_2d_512-121.h5
ns_incom_inhom_2d_512-122.h5
ns_incom_inhom_2d_512-123.h5
ns_incom_inhom_2d_512-124.h5
ns_incom_inhom_2d_512-125.h5
ns_incom_inhom_2d_512-126.h5
ns_incom_inhom_2d_512-127.h5
ns_incom_inhom_2d_512-128.h5
ns_incom_inhom_2d_512-129.h5
ns_incom_inhom_2d_512-130.h5
ns_incom_inhom_2d_512-131.h5
ns_incom_inhom_2d_512-132.h5
ns_incom_inhom_2d_512-133.h5
ns_incom_inhom_2d_512-134.h5
ns_incom_inhom_2d_512-135.h5
ns_incom_inhom_2d_512-136.h5
ns_incom_inhom_2d_512-137.h5
ns_incom_inhom_2d_512-138.h5
ns_incom_inhom_2d_512-139.h5
ns_incom_inhom_2d_512-140.h5
ns_incom_inhom_2d_512-141.h5
ns_incom_inhom_2d_512-142.h5
ns_incom_inhom_2d_512-143.h5
ns_incom_inhom_2d_512-144.h5
ns_incom_inhom_2d_512-145.h5
ns_incom_inhom_2d_512-146.h5
ns_incom_inhom_2d_512-147.h5
ns_incom_inhom_2d_512-148.h5
ns_incom_inhom_2d_512-149.h5
ns_incom_inhom_2d_512-150.h5
ns_incom_inhom_2d_512-151.h5
ns_incom_inhom_2d_512-152.h5
ns_incom_inhom_2d_512-153.h5
ns_incom_inhom_2d_512-154.h5
ns_incom_inhom_2d_512-155.h5
ns_incom_inhom_2d_512-156.h5
ns_incom_inhom_2d_512-157.h5
ns_incom_inhom_2d_512-158.h5
ns_incom_inhom_2d_512-159.h5
ns_incom_inhom_2d_512-160.h5
ns_incom_inhom_2d_512-161.h5
ns_incom_inhom_2d_512-162.h5
ns_incom_inhom_2d_512-163.h5
ns_incom_inhom_2d_512-164.h5
ns_incom_inhom_2d_512-165.h5
ns_incom_inhom_2d_512-166.h5
ns_incom_inhom_2d_512-167.h5
ns_incom_inhom_2d_512-168.h5
ns_incom_inhom_2d_512-169.h5
ns_incom_inhom_2d_512-170.h5
ns_incom_inhom_2d_512-171.h5
ns_incom_inhom_2d_512-172.h5
ns_incom_inhom_2d_512-173.h5
ns_incom_inhom_2d_512-174.h5
ns_incom_inhom_2d_512-175.h5
ns_incom_inhom_2d_512-176.h5
ns_incom_inhom_2d_512-177.h5
ns_incom_inhom_2d_512-178.h5
ns_incom_inhom_2d_512-179.h5
ns_incom_inhom_2d_512-180.h5
ns_incom_inhom_2d_512-181.h5
ns_incom_inhom_2d_512-182.h5
ns_incom_inhom_2d_512-183.h5
ns_incom_inhom_2d_512-184.h5
ns_incom_inhom_2d_512-185.h5
ns_incom_inhom_2d_512-186.h5
ns_incom_inhom_2d_512-187.h5
ns_incom_inhom_2d_512-188.h5
ns_incom_inhom_2d_512-189.h5
ns_incom_inhom_2d_512-190.h5
ns_incom_inhom_2d_512-191.h5
ns_incom_inhom_2d_512-192.h5
ns_incom_inhom_2d_512-193.h5
ns_incom_inhom_2d_512-194.h5
ns_incom_inhom_2d_512-195.h5
ns_incom_inhom_2d_512-196.h5
ns_incom_inhom_2d_512-197.h5
ns_incom_inhom_2d_512-198.h5
ns_incom_inhom_2d_512-199.h5
ns_incom_inhom_2d_512-200.h5
ns_incom_inhom_2d_512-201.h5
ns_incom_inhom_2d_512-202.h5
ns_incom_inhom_2d_512-203.h5
ns_incom_inhom_2d_512-204.h5
ns_incom_inhom_2d_512-205.h5
ns_incom_inhom_2d_512-206.h5
ns_incom_inhom_2d_512-207.h5
ns_incom_inhom_2d_512-208.h5
ns_incom_inhom_2d_512-209.h5
ns_incom_inhom_2d_512-210.h5
ns_incom_inhom_2d_512-211.h5
ns_incom_inhom_2d_512-212.h5
ns_incom_inhom_2d_512-213.h5
ns_incom_inhom_2d_512-214.h5
ns_incom_inhom_2d_512-215.h5
ns_incom_inhom_2d_512-216.h5
ns_incom_inhom_2d_512-217.h5
ns_incom_inhom_2d_512-218.h5
ns_incom_inhom_2d_512-219.h5
ns_incom_inhom_2d_512-220.h5
ns_incom_inhom_2d_512-221.h5
ns_incom_inhom_2d_512-222.h5
ns_incom_inhom_2d_512-223.h5
ns_incom_inhom_2d_512-224.h5
ns_incom_inhom_2d_512-225.h5
ns_incom_inhom_2d_512-226.h5
ns_incom_inhom_2d_512-227.h5
ns_incom_inhom_2d_512-228.h5
ns_incom_inhom_2d_512-229.h5
ns_incom_inhom_2d_512-230.h5
ns_incom_inhom_2d_512-231.h5
ns_incom_inhom_2d_512-232.h5
ns_incom_inhom_2d_512-233.h5
ns_incom_inhom_2d_512-234.h5
ns_incom_inhom_2d_512-235.h5
ns_incom_inhom_2d_512-236.h5
ns_incom_inhom_2d_512-237.h5
ns_incom_inhom_2d_512-238.h5
ns_incom_inhom_2d_512-239.h5
ns_incom_inhom_2d_512-240.h5
ns_incom_inhom_2d_512-241.h5
ns_incom_inhom_2d_512-242.h5
ns_incom_inhom_2d_512-243.h5
ns_incom_inhom_2d_512-244.h5
ns_incom_inhom_2d_512-245.h5
ns_incom_inhom_2d_512-246.h5
ns_incom_inhom_2d_512-247.h5
ns_incom_inhom_2d_512-248.h5
ns_incom_inhom_2d_512-249.h5
ns_incom_inhom_2d_512-250.h5
ns_incom_inhom_2d_512-251.h5
ns_incom_inhom_2d_512-252.h5
ns_incom_inhom_2d_512-253.h5
ns_incom_inhom_2d_512-254.h5
ns_incom_inhom_2d_512-255.h5
ns_incom_inhom_2d_512-256.h5
ns_incom_inhom_2d_512-257.h5
ns_incom_inhom_2d_512-258.h5
ns_incom_inhom_2d_512-259.h5
ns_incom_inhom_2d_512-260.h5
ns_incom_inhom_2d_512-261.h5
ns_incom_inhom_2d_512-262.h5
ns_incom_inhom_2d_512-263.h5
ns_incom_inhom_2d_512-264.h5
ns_incom_inhom_2d_512-265.h5
ns_incom_inhom_2d_512-266.h5
ns_incom_inhom_2d_512-267.h5
ns_incom_inhom_2d_512-268.h5
ns_incom_inhom_2d_512-269.h5
ns_incom_inhom_2d_512-270.h5
ns_incom_inhom_2d_512-271.h5
ns_incom_inhom_2d_512-272.h5
ns_incom_inhom_2d_512-273.h5
ns_incom_inhom_2d_512-274.h5
```

## 数据布局与机器学习输入输出

更准确的条件动力学任务是 $(\mathbf v_{0:\ell-1},\mathbf f,\text{boundary/coordinates})\mapsto\mathbf v_{\ell:T-1}$，而不是只把速度当作无条件视频。

- **轨迹与训练样本：** 完整 HDF5 轨迹不是固定的模型输入。自回归训练通常从完整轨迹切出 $\ell$ 帧输入与下一帧/未来多帧目标；$\ell$ 由训练配置的 `initial_step` 决定。
- **版本优先级：** 方程与初边值以论文为准；文件数、分辨率、轨迹数与通道以当前可下载 HDF5 / 官方清单为准。

## 下载

官方仓库当前推荐 `download_direct.py`，而不是较慢且可能报错的 EasyDataverse 路径。

```bash
git clone https://github.com/pdebench/PDEBench.git
cd PDEBench/pdebench/data_download
python download_direct.py --root_folder /path/to/pdebench_data --pde_name ns_incom
```

也可以从 [DaRUS DOI 页面](https://doi.org/10.18419/darus-2986) 手动选择文件。下载后应逐文件检查 HDF5 的实际 `shape`、坐标数组、变量键和 YAML attributes，尤其不要仅凭文件名推断 CFD/不可压 NS 的空间分辨率。

## 从官方代码重新生成

```bash
cd PDEBench
python -m pdebench.data_gen.gen_ns_incomp
# Hydra configuration: pdebench/data_gen/configs/ns_incomp.yaml
```

生成器参数可通过对应 Hydra YAML 修改；该路径直接写出 HDF5，无需执行 `Data_Merge.py`。

## 数据的兴趣点与挑战

超大数据量、长时间轨迹、不可压约束、非周期 no-slip 边界、动态速度与静态外力的异构张量布局。

## 主要来源

- [PDEBench 论文与补充材料](https://arxiv.org/abs/2210.07182)
- [PDEBench 官方代码库](https://github.com/pdebench/PDEBench)
- [官方下载说明](https://github.com/pdebench/PDEBench/tree/main/pdebench/data_download)
- [PDEBench 数据集 DOI](https://doi.org/10.18419/darus-2986)
