---
title: "The Well 数据文档"
linkTitle: "The Well"
weight: 5
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
summary: "Polymathic AI 的大规模多物理场 PDE 基准，覆盖声学、流体、MHD、超新星等场景。"
description: "Polymathic AI 的大规模多物理场 PDE 基准，覆盖声学、流体、MHD、超新星等场景。"
dataset_family: "The Well"
---

# The Well：逐方程中英文数据文档

本包包含 **24 份英文数据文档**和 **24 份一一对应的中文文档**。目录按当前官方仓库中的可下载数据目录组织，同时保留论文按 16 个物理场景计数的口径。当前官网列出 23 个专用数据页，仓库另外包含修正后的 `viscoelastic_instability_v2`。

## 每份文档包含什么

每个 Markdown 文件均按照可并入更大规模 PDE/动力学数据集目录的方式组织，包括：

- 所属数据集、目录名、许可证、官网/仓库/Hugging Face 链接；
- 物理概览与控制方程；
- 变量定义、动态通道和静态场；
- 三层参数审计：理论上可调、发布数据实际变化、发布数据固定；
- 初始条件与边界条件；
- 坐标系、空间分辨率、轨迹数、时间长度、字段和数据量；
- HDF5 原始组织与模型输入输出形状；
- 生成软件、数值方法和计算代价说明；
- 下载命令、本地读取和 Hugging Face 流式状态；
- 推荐任务、版本差异和使用注意事项。

## 整理原则

英文文件是**忠实于来源的结构化重写**，不是官网逐字镜像；中文文件是在英文来源基础上的翻译、校勘与补充。方程和参数同时核对官网专用页、当前仓库元数据以及论文附录 C。若不同来源不一致，文档会保留差异，不会静默选取某一个值。

## 目录结构

```text
the_well_markdown_docs/
├── README.md
├── README.zh-CN.md
├── MANIFEST.md
├── SOURCE_NOTES.md
├── TEMPLATE.en.md
├── TEMPLATE.zh-CN.md
├── en/       # 24 份英文文档
└── zh-CN/    # 24 份中文文档
```

## 数据目录索引

| 目录 | 方程族 | 网格 | 帧数 | 轨迹数 | 动态通道 | 体量 | 状态 |
|---|---|---:|---:|---:|---:|---:|---|
| [`acoustic_scattering_discontinuous`](../acoustic_scattering_discontinuous/) | 变系数声学 | $256\times256$ | 101 | 2000 | 3 | 157.7 GB | active |
| [`acoustic_scattering_inclusions`](../acoustic_scattering_inclusions/) | 变系数声学 | $256\times256$ | 101 | 4000 | 3 | 283.8 GB | active |
| [`acoustic_scattering_maze`](../acoustic_scattering_maze/) | 变系数声学 | $256\times256$ | 201 | 2000 | 3 | 311.3 GB | active |
| [`active_matter`](../active_matter/) | 活性流体动理学 | $256\times256$ | 81 | 225 (current parameter product; paper table reports 360) | 11 | 51.3 GB | active |
| [`convective_envelope_rsg`](../convective_envelope_rsg/) | 辐射流体动力学 | $256\times128\times256$ | 100 | 29 temporal cuts | 6 | 570 GB | active |
| [`euler_multi_quadrants_openBC`](../euler_multi_quadrants_openBC/) | 可压缩无黏 Euler 方程 | $512\times512$ | 100 | 5000 | 5 | part of 5.17 TB combined Euler release | active |
| [`euler_multi_quadrants_periodicBC`](../euler_multi_quadrants_periodicBC/) | 可压缩无黏 Euler 方程 | $512\times512$ | 100 | 5000 | 5 | part of 5.17 TB combined Euler release | active |
| [`gray_scott_reaction_diffusion`](../gray_scott_reaction_diffusion/) | 反应扩散 | $128\times128$ | 1001 | 1200 | 2 | 153.8 GB | active |
| [`helmholtz_staircase`](../helmholtz_staircase/) | 波动/Helmholtz 散射 | $1024\times256$ | 50 | 512 | 2 | 52.4 GB | active |
| [`MHD_64`](../MHD_64/) | 理想等温磁流体动力学 | $64^3$ | 100 | 100 | 7 | 71.6 GB | active |
| [`MHD_256`](../MHD_256/) | 理想等温磁流体动力学 | $256^3$ | 100 | 100 | 7 | 4.58 TB | active |
| [`planetswe`](../planetswe/) | 旋转球面浅水方程 | $256\times512$ | 1008 | 120 ML trajectories (from 40 three-year simulations) | 3 | 185.8 GB | active |
| [`post_neutron_star_merger`](../post_neutron_star_merger/) | 广义相对论 MHD + 中微子输运 | $192\times128\times66$ | 181 | 8 | 12 | 110.1 GB | active |
| [`rayleigh_benard`](../rayleigh_benard/) | Boussinesq 热对流 | $512\times128$ | 200 | 1750 | 4 | approximately 342–358 GB across documentation versions | active |
| [`rayleigh_benard_uniform`](../rayleigh_benard_uniform/) | Boussinesq 热对流 | $512\times128$ | 200 | 1750 | 4 | not separately reported; similar order to native-grid data | active |
| [`rayleigh_taylor_instability`](../rayleigh_taylor_instability/) | 变密度可混溶流 | $128^3$ | 119 on current dataset page (paper table: 120) | 45 | 4 | 255.6 GB | active |
| [`shear_flow`](../shear_flow/) | 不可压缩 Navier–Stokes + 示踪剂 | $256\times512$ | 200 | 1120 | 4 | 547 GB | active |
| [`supernova_explosion_64`](../supernova_explosion_64/) | 可压缩 SPH 流体 + 冷却 | $64^3$ | 59 | 740 | 6 | 268.2 GB | active |
| [`supernova_explosion_128`](../supernova_explosion_128/) | 可压缩 SPH 流体 + 冷却 | $128^3$ | 59 | 260 | 6 | 754 GB | active |
| [`turbulence_gravity_cooling`](../turbulence_gravity_cooling/) | 自引力可压缩流体 | $64^3$ | 50 | 2700 | 6 | 829.4 GB | active |
| [`turbulent_radiative_layer_2D`](../turbulent_radiative_layer_2D/) | 可压缩流体 + 辐射冷却 | $128\times384$ | 101 | 90 | 4 | 6.9 GB | active |
| [`turbulent_radiative_layer_3D`](../turbulent_radiative_layer_3D/) | 可压缩流体 + 辐射冷却 | $128\times128\times256$ | 101 | 90 | 5 | 745 GB | active |
| [`viscoelastic_instability`](../viscoelastic_instability/) | FENE-P 黏弹性流 | $512\times512$ | 20 or 60 depending on attractor/segment | 260 | 8 | 66 GB | deprecated |
| [`viscoelastic_instability_v2`](../viscoelastic_instability_v2/) | FENE-P 黏弹性流 | $512\times512$ | 20 or 60 depending on attractor/segment | 260 | 8 | approximately 66 GB; not separately tabulated in the paper | active-corrected |

## 通用下载命令

```bash
pip install the_well
the-well-download --base-path ./the_well_data --dataset active_matter --split train
```

CLI 可以只下载指定数据集和划分。若同时省略两个选择项，会请求约 15 TB 的完整集合。

## 主要来源

- 官方文档：<https://polymathic-ai.org/the_well/>
- 官方仓库：<https://github.com/PolymathicAI/the_well>
- 论文：<https://arxiv.org/abs/2412.00568>
- Hugging Face 集合：<https://huggingface.co/collections/polymathic-ai/the-well>
- 统一数据格式：<https://polymathic-ai.org/the_well/data_format/>

核对日期： **2026-07-21**。
