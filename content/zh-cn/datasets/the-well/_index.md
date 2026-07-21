---
title: "The Well"
linkTitle: "The Well"
weight: 20
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
math: true
summary: "Polymathic AI 的大规模多物理场 PDE 基准：约 15TB、覆盖 16 个物理场景。"
description: "Polymathic AI 的大规模多物理场 PDE 基准：约 15TB、覆盖 16 个物理场景。"
dataset_family: "The Well"
---

# The Well：15TB 物理仿真数据

![The Well](/the-well/the_well_color.svg)

The Well 是一套面向机器学习的大规模时空物理仿真数据集，由领域科学家与数值软件开发者共同贡献，总计约 **15TB**、覆盖 **16** 个物理场景（生物活性物质、流体、声学散射、磁流体、超新星爆炸等）。各数据集可单独使用，也可作为 surrogate 模型基准套件。

官网：[polymathic-ai.org/the_well](https://polymathic-ai.org/the_well/)。下文与官方数据集页面对齐；当同一物理场景拆成多个可下载目录时（如声学 / Euler / MHD / 超新星变体，以及 `rayleigh_benard_uniform`、`viscoelastic_instability_v2`），每个目录各有一页。

## 数据集目录

每个可下载目录一行。数值在总览表与专用页不一致时，优先采用官方专用页。

| 目录 | 分辨率 | 帧数 | 轨迹数 | 体量 | 状态 |
|---|---|---:|---:|---:|---|
| [`acoustic_scattering_discontinuous`](./acoustic_scattering_discontinuous/) | 256×256 | 101 | 2000 | 157.7 GB | active |
| [`acoustic_scattering_inclusions`](./acoustic_scattering_inclusions/) | 256×256 | 101 | 4000 | 283.8 GB | active |
| [`acoustic_scattering_maze`](./acoustic_scattering_maze/) | 256×256 | 201 | 2000 | 311.3 GB | active |
| [`active_matter`](./active_matter/) | 256×256 | 81 | 225 | 51.3 GB | active |
| [`convective_envelope_rsg`](./convective_envelope_rsg/) | 256×128×256 | 100 | 29 | 570 GB | active |
| [`euler_multi_quadrants_openBC`](./euler_multi_quadrants_openBC/) | 512×512 | 100 | 5000 | 合计 5.17 TB 之一 | active |
| [`euler_multi_quadrants_periodicBC`](./euler_multi_quadrants_periodicBC/) | 512×512 | 100 | 5000 | 合计 5.17 TB 之一 | active |
| [`gray_scott_reaction_diffusion`](./gray_scott_reaction_diffusion/) | 128×128 | 1001 | 1200 | 153.8 GB | active |
| [`helmholtz_staircase`](./helmholtz_staircase/) | 1024×256 | 50 | 512 | 52.4 GB | active |
| [`MHD_64`](./MHD_64/) | 64³ | 100 | 100 | 71.6 GB | active |
| [`MHD_256`](./MHD_256/) | 256³ | 100 | 100 | 4.58 TB | active |
| [`planetswe`](./planetswe/) | 256×512 | 1008 | 120 | 185.8 GB | active |
| [`post_neutron_star_merger`](./post_neutron_star_merger/) | 192×128×66 | 181 | 8 | 110.1 GB | active |
| [`rayleigh_benard`](./rayleigh_benard/) | 512×128 | 200 | 1750 | 约 342–358 GB | active |
| [`rayleigh_benard_uniform`](./rayleigh_benard_uniform/) | 512×128 | 200 | 1750 | 同量级 | active |
| [`rayleigh_taylor_instability`](./rayleigh_taylor_instability/) | 128³ | 119 | 45 | 255.6 GB | active |
| [`shear_flow`](./shear_flow/) | 256×512 | 200 | 1120 | 547 GB | active |
| [`supernova_explosion_64`](./supernova_explosion_64/) | 64³ | 59 | 740 | 268.2 GB | active |
| [`supernova_explosion_128`](./supernova_explosion_128/) | 128³ | 59 | 260 | 754 GB | active |
| [`turbulence_gravity_cooling`](./turbulence_gravity_cooling/) | 64³ | 50 | 2700 | 829.4 GB | active |
| [`turbulent_radiative_layer_2D`](./turbulent_radiative_layer_2D/) | 128×384 | 101 | 90 | 6.9 GB | active |
| [`turbulent_radiative_layer_3D`](./turbulent_radiative_layer_3D/) | 128×128×256 | 101 | 90 | 745 GB | active |
| [`viscoelastic_instability`](./viscoelastic_instability/) | 512×512 | 可变 | 260 | 66 GB | deprecated |
| [`viscoelastic_instability_v2`](./viscoelastic_instability_v2/) | 512×512 | 可变 | 260 | 约 66 GB | active |

## 统一格式

数据在均匀网格、等时间间隔采样，存为自描述 HDF5，并附带 `dataset_name.yaml`。数组为 `fp32`，概念形状 `(n_traj, n_steps, coord1, coord2[, coord3])`。按张量阶划分：标量 `t0_fields`、矢量 `t1_fields`、张量 `t2_fields`。默认按轨迹 0.8 / 0.1 / 0.1 划分训练 / 验证 / 测试。

详见官方 [data format](https://polymathic-ai.org/the_well/data_format/)。

## 下载与读取

```bash
pip install the_well
the-well-download --base-path ./the_well_data --dataset active_matter --split train
```

同时省略 `--dataset` / `--split` 会请求约 15TB 的完整集合。

```python
from the_well.data import WellDataset
from torch.utils.data import DataLoader

trainset = WellDataset(
    well_base_path="path/to/base",
    well_dataset_name="active_matter",
    well_split_name="train",
)
train_loader = DataLoader(trainset)
for batch in train_loader:
    ...
```

多数数据集也可通过 `well_base_path="hf://datasets/polymathic-ai/"` 从 Hugging Face 流式读取。

## 生成代价（官方总览）

| 数据集 | 体量 (GB) | 运行时间 (h) | 硬件 | 软件 |
|---|---:|---:|---|---|
| `acoustic_discontinuous` | 157 | 0.25 | 64 C | Clawpack |
| `acoustic_inclusions` | 283 | 0.25 | 64 C | Clawpack |
| `acoustic_maze` | 311 | 0.33 | 64 C | Clawpack |
| `active_matter` | 51.3 | 0.33 | A100 GPU | Python |
| `convective_envelope_rsg` | 570 | 1460 | 80 C | Athena++ |
| `euler` | 5170 | 80* | 160 C* | ClawPack |
| `helmholtz_staircase` | 52 | 0.11 | 64 C | Python |
| `MHD_256` | 4580 | 48 | 64 C | Fortran MPI |
| `MHD_64` | 72 | — | — | — |
| `gray_scott_reaction_diffusion` | 154 | 33* | 40 C | Matlab |
| `planetswe` | 186 | 0.75 | 64 C | Dedalus |
| `post_neutron_star_merger` | 110 | 505* | 300 C* | νbhlight |
| `rayleigh_benard` | 358 | 60* | 768 C* | Dedalus |
| `rayleigh_taylor_instability` | 256 | 65* | 128 C* | TurMix3D |
| `shear_flow` | 115† | 5* | 448 C* | Dedalus |
| `supernova_explosion_128` | 754 | 4* | 1040 C* | ASURA-FDPS |
| `supernova_explosion_64` | 268 | 4* | 1040 C* | ASURA-FDPS |
| `turbulence_gravity_cooling` | 829 | 577* | 1040 C* | ASURA-FDPS |
| `turbulent_radiative_layer_2D` | 6.9 | 2* | 48 C | Athena++ |
| `turbulent_radiative_layer_3D` | 745 | 271* | 128 C | Athena++ |
| `viscoelastic_instability` | 66 | 34* | 64 C | Dedalus |

\* 为全部运行合计；C 为 CPU 核数。† 总览表数值；[shear_flow](./shear_flow/) 专用页报告 **547 GB**。

## 主要来源

- 官方文档：<https://polymathic-ai.org/the_well/>
- 数据集总览：<https://polymathic-ai.org/the_well/datasets_overview/>
- 官方仓库：<https://github.com/PolymathicAI/the_well>
- 论文：<https://arxiv.org/abs/2412.00568>
- Hugging Face：<https://huggingface.co/collections/polymathic-ai/the-well>
- 统一数据格式：<https://polymathic-ai.org/the_well/data_format/>

核对日期：**2026-07-21**。
