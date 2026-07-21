---
parent_dataset: PDEArena
dataset_id: pdearena
equation_id: 03_shallow_water_2d_velocity
spatial_dimension: 2
time_dependent: true
data_format: Zarr
paper: "arXiv:2209.15616v2"
download_key: ShallowWater-2D
last_verified: 2026-07-21
title: 二维球面浅水方程（速度形式）
linkTitle: "SWE velocity"
weight: 30
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
dataset_family: PDEArena
summary: "全球经纬网格上的旋转浅水；压力/自由表面 + 纬向/经向风；1-day 与 2-day 任务视图。"
description: "全球经纬网格上的旋转浅水；压力/自由表面 + 纬向/经向风；1-day 与 2-day 任务视图。"
---

# 二维球面浅水方程（速度形式）

在全球球面上用修改后的 SpeedyWeather.jl 模拟旋转浅水方程，保存压力/自由表面标量与纬向、经向风速。`ShallowWater2DVel-1Day` 与 `ShallowWater2DVel-2Day` 是同一批轨迹的不同时间抽样视图，不是两套独立模拟。

## 所属数据集与访问方式

| 字段 | 内容 |
|---|---|
| 所属数据集 | **PDEArena** |
| 数据集论文 | [Towards Multi-spatiotemporal-scale Generalized PDE Modeling](https://arxiv.org/abs/2209.15616) |
| 论文 PDF | [arXiv PDF](https://arxiv.org/pdf/2209.15616) |
| 官方代码库 | [pdearena/pdearena](https://github.com/pdearena/pdearena) |
| Hugging Face | [pdearena/ShallowWater-2D](https://huggingface.co/datasets/pdearena/ShallowWater-2D) |
| 数据量 | 124 GB（与涡度视图共享） |
| 数值软件 | [SpeedyWeather.jl](https://github.com/SpeedyWeather/SpeedyWeather.jl) |
| 许可证 | MIT |
| 文档核对日期 | 2026-07-21 |

## 控制方程

论文说明了浅水模型与字段，未在正文打印完整球面方程。目录用标准向量形式：

\[
\frac{\partial h}{\partial t}+\nabla_s\cdot(h\mathbf{v})=0,
\]
\[
\frac{\partial\mathbf{v}}{\partial t}+(\mathbf{v}\cdot\nabla_s)\mathbf{v}+f_c\,\hat{\mathbf{r}}\times\mathbf{v}+g\nabla_s h=\mathcal{D}.
\]

其中 $\nabla_s$ 为球面微分算子，$f_c$ 为科氏参数，$\mathcal{D}$ 为耗散/数值闭合。

## 变量与坐标

- $h$ 或 $p$：自由表面位移 / 位势高度 / 论文所称 pressure；
- $u$：纬向（zonal）风；$v$：经向（meridional）风；
- $(\lambda,\phi)$：经度、纬度；输出网格 $192\times96$（$\Delta x=1.875^\circ$，$\Delta y=3.75^\circ$），常见数组尾维 $[N_{\mathrm{lat}},N_{\mathrm{lon}}]=[96,192]$。

## 关于数据

| 属性 | 内容 |
|---|---|
| 空间维数 | 2（球面） |
| 含时间 | 是 |
| 网格 | 规则经纬输出；球面谱方法求解 |
| 空间分辨率 | $192\times96$ |
| 2-day 轨迹长 | $T=11$（配置注释 $n_t=88$，`sample_rate=8`） |
| 1-day 轨迹长 | $T=21$（$n_t=84$，`sample_rate=4`） |
| 轨迹数 | train 5,600 / valid 1,400 / test 1,400（合计 8,400） |
| 通道 | 3：$p$（或 $h$）、$u$、$v$ |
| 数据量 | 124 GB |
| 格式 | NetCDF 生成 → 发布 Zarr；附 `normstats.pt` |

## 初始条件

`random2` 初值：$\mathrm{offset}\sim\mathrm{Unif}\{80,\ldots,120\}$，$a_1\sim\mathrm{Unif}\{-20,\ldots,30\}$，$a_2,a_3\sim\mathrm{Unif}\{-20,\ldots,40\}$；近似初始纬向风含逐格随机量 $r$，并加固定结构波扰动（$A=10^{-4}$，$m=6$，$\theta_0=45^\circ$，$\theta_w=10^\circ$）与幅度 $5\times10^{-6}$ 的随机谱微扰。

## 边界条件

经度方向周期；极点由球面谱表示处理。论文概括为 regular grid with periodic boundary conditions，不宜把球面当成平面四边完全等价卷绕。

## 数值生成方法

修改后的 SpeedyWeather.jl；核心设置含 `n_days=20`，`trunc=62`，`Δt_at_T85=40`，`initial_conditions=:random2`。生成后可 `convertnc2zarr.py` 转 Zarr，并用 `compute_normalization.py` 计算归一化统计。

## 参数

| 参数 | 变化方式 | 取值 |
|---|---|---|
| 随机种子 / `offset,$a_i,r$ | 每轨迹随机 | 见初值区间 |
| 谱微扰 realization | 每轨迹随机 | 幅度固定 $5\times10^{-6}$ |
| 波扰动 $A,m,\theta_0,\theta_w$ | 固定 | 见上 |
| 模拟时长 / 谱截断 / 网格 | 固定 | 20 days；`trunc=62`；$192\times96$ |
| 1-day / 2-day 抽样 | 任务视图不同 | `sample_rate` 4 vs 8 |
| 重力、行星半径、科氏、耗散 | 固定（求解器默认） | 发布未扫描 |

## 发布配置

- 任务视图：`shallowwater2d_2day.yaml` / `shallowwater2d_1day.yaml`（2 帧历史 → 1 帧未来）。
- 完整发布：train 5,600 / valid 1,400 / test 1,400；1-day 与 2-day、速度与涡度共用同一仓库。
- pressure / vorticity 训练前使用发布附带的归一化统计（`normstats.pt`）。

## 数据文件

发布布局：

```
train/seed=*/
valid/seed=*/
test/seed=*/
normstats.pt
```

约 56 个 seed 目录/切分（生成脚本 56 seeds × 100/25/25）。速度与涡度、1-day/2-day 共用，勿重复计量体积。详见 [数据格式](../00_data_format/)。

## 数据布局与机器学习输入输出

2-day 典型样本：

\[
X\in\mathbb{R}^{2\times3\times96\times192}\to Y\in\mathbb{R}^{1\times3\times96\times192}.
\]

1-day 空间与通道相同，时间抽样更细。

## 下载

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/ShallowWater-2D
```

## 从官方代码重新生成

```bash
# 见 docs/data.md 浅水循环脚本
python scripts/generate_data.py base=pdedatagen/configs/shallowwater.yaml \
  experiment=shallowwater mode=train samples=100 seed=$SEED \
  dirname=pdearena_data/shallowwater
# 转换与归一化
python scripts/convertnc2zarr.py "pdearena_data/shallowwater/$mode"
python scripts/compute_normalization.py --dataset shallowwater pdearena_data/shallowwater
```

## 数据的兴趣点与挑战

球面上局部结构与大尺度环流并存；经度周期与极区几何使平面卷积假设不完全成立；1-day/2-day 可隔离时间尺度影响。

## 主要来源

- [PDEArena 论文](https://arxiv.org/abs/2209.15616)
- [浅水生成目录](https://github.com/pdearena/pdearena/tree/main/pdedatagen/shallowwater)
- [Hugging Face 数据页](https://huggingface.co/datasets/pdearena/ShallowWater-2D)
