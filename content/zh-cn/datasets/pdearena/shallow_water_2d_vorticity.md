---
title: 二维球面浅水方程（涡度形式任务视图）
dataset_family: PDEArena
dataset_release: ShallowWater-2D
equation: "Rotating shallow-water equations in vorticity task representation"
spatial_dimension: 2
coordinate_system: "global longitude-latitude / spherical spectral grid"
task_variant: "vorticity-form 2-day task"
official_status: "official benchmark task view over the ShallowWater-2D release"
license: MIT
last_verified: 2026-07-21
linkTitle: "Shallow Water (vorticity)"
weight: 40
draft: false
ShowToc: true
TocOpen: true
hidemeta: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
math: true
hiddenInHomeList: true
summary: "从同一批球面浅水轨迹中使用压力/自由表面标量和垂直涡度两个标量通道，构造 2-day 预测任务。"
description: "从同一批球面浅水轨迹中使用压力/自由表面标量和垂直涡度两个标量通道，构造 2-day 预测任务。"

---

# 二维球面浅水方程（涡度形式任务视图）

> **一句话说明：** 从同一批球面浅水轨迹中使用压力/自由表面标量和垂直涡度两个标量通道，构造 2-day 预测任务。

[English version](../en/shallow_water_2d_vorticity.md)

## 较长说明

该页面描述的是 PDEArena 论文中的 **vorticity--stream-function task representation**。它不是另一个 124 GB 的独立数据发布，而是对 `ShallowWater-2D` 速度轨迹进行字段变换后得到的 benchmark 视图。风场 $(u,v)$ 被转换为球面法向涡度 $\zeta$，模型只接收两个标量场。

## 所属数据集与来源

- **所属数据集：** PDEArena
- **底层官方发布：** `pdearena/ShallowWater-2D`
- **论文任务：** shallow-water vorticity-stream formulation, 2-day prediction
- **数值软件：** 修改后的 SpeedyWeather.jl
- **许可证：** MIT

## 方程与涡度表示

底层动力学仍是旋转浅水方程：

$$
\frac{\partial h}{\partial t}+\nabla_s\cdot(h\mathbf v)=0,
$$

$$
\frac{\partial\mathbf v}{\partial t}
+(\mathbf v\cdot\nabla_s)\mathbf v
+f_c\hat{\mathbf r}\times\mathbf v
+g\nabla_s h=\mathcal D.
$$

球面垂直涡度定义为

$$
\zeta=(\nabla_s\times\mathbf v)\cdot\hat{\mathbf r}.
$$

在局部笛卡尔近似下，可直观写成

$$
\zeta\approx\frac{\partial v}{\partial x}-\frac{\partial u}{\partial y}.
$$

该数据任务使用 $[p,\zeta]$，不是潜在涡度 $(\zeta+f_c)/h$，也不保存流函数作为独立输出通道。

## 数据说明

### 离散维度

| 项目 | 规格 |
|---|---|
| 空间 | 全球球面，经纬度规则输出网格 |
| 论文分辨率 | 经度 $192$ × 纬度 $96$ |
| 常见数组形状 | $[96,192]$ |
| 任务时间窗 | 2 days / 48 h |
| 轨迹长 | $T=11$ |
| 历史/未来 | 2 帧输入、1 帧输出 |
| 单帧字段 | pressure/free-surface scalar、vertical vorticity |
| 单帧通道 | 2 |

$$
X\in\mathbb R^{2\times2\times96\times192},\qquad
Y\in\mathbb R^{1\times2\times96\times192}.
$$

展平时间维后：

$$
[4,96,192]\longrightarrow[2,96,192].
$$

### 轨迹数和容量

该视图共享 `ShallowWater-2D` 的切分：

| split | 底层轨迹数 |
|---|---:|
| train | 5,600 |
| validation | 1,400 |
| test | 1,400 |
| **总计**| **8,400** |

**共享仓库大小：124 GB。** 不应把速度文档的 124 GB 和本页再次相加。

### 初始条件、边界与生成器

初始条件、球面拓扑、随机 `random2` 风场、20-day 模拟、谱截断和步长配置与[速度形式文档](../shallow_water_2d_velocity/)完全相同。涡度是在同一动力学轨迹上由风场导出。

论文附录明确说明 pressure 和 vorticity 字段在训练前进行归一化。

## 参数：可调、实际变化与固定

| 类型 | 内容 |
|---|---|
| 实际变化 | 初始风场随机系数、逐格随机量、随机谱扰动、随机种子 |
| 由任务变换得到 | $\zeta$，由 $(u,v)$ 计算，不是独立随机参数 |
| 固定 | 网格、球面拓扑、20-day 模拟设置、谱截断、波扰动结构、求解器物理常数/defaults |
| 时间任务 | 论文明确给出 2-day 涡度任务；没有证据支持一个独立发布的 1-day 涡度数据仓库 |

## 下载

```bash
git lfs install
git clone https://huggingface.co/datasets/pdearena/ShallowWater-2D
```

下载后需要按 PDEArena 数据管道计算/读取涡度视图；Hugging Face 上没有第二个名为 “ShallowWater-Vorticity” 的独立官方仓库。

## 有趣与困难之处

- 涡度直接突出旋转、剪切和小尺度涡结构；
- 将二维向量场压缩为一个标量会改变学习难度和对称性要求；
- 从涡度恢复速度需要解全局椭圆问题，因此局部误差可能产生非局部影响；
- 与速度形式共享轨迹，适合公平比较场表示对模型性能的影响。

## 已知限制

本任务不是对不同浅水物理参数的扫描；它主要改变状态表示。把它称为独立数据集时必须注明其底层轨迹与速度形式共享。


## 引用

PDEArena 的 Navier--Stokes 与浅水方程数据应引用：

```bibtex
@article{gupta2022towards,
  title={Towards Multi-spatiotemporal-scale Generalized PDE Modeling},
  author={Gupta, Jayesh K. and Brandstetter, Johannes},
  journal={arXiv preprint arXiv:2209.15616},
  year={2022}
}
```

## 资料链接

- [原论文](https://arxiv.org/abs/2209.15616)
- [速度形式配套文档](../shallow_water_2d_velocity/)
- [Hugging Face 底层数据页](https://huggingface.co/datasets/pdearena/ShallowWater-2D)
- [官方代码库](https://github.com/pdearena/pdearena)
