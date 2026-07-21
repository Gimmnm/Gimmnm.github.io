---
title: "FlowBench 方程级数据文档索引"
parent_dataset: FlowBench
last_verified: 2026-07-21
linkTitle: FlowBench
weight: 20
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
summary: "复杂几何上流场模拟大规模基准，覆盖二维/三维顶盖驱动与瞬态 FPO 等配置。"
description: "复杂几何上流场模拟大规模基准，覆盖二维/三维顶盖驱动与瞬态 FPO 等配置。"
dataset_family: FlowBench
---

# FlowBench 方程级数据文档（中文）

本目录把 FlowBench 按**实际公开的 PDE/物理配置子集**拆成独立 Markdown 文档。结构参考 The Well 的单数据集页面：一句话描述、长描述、生成软件、方程、About the data、参数、边界条件、挑战、下载和引用；同时补充所属数据集、官方链接、几何、张量格式和版本差异。

## 文档列表

| 文件 | PDE/配置 | 维数 | 状态 | 名义/当前样本数 | 当前体积 |
|---|---|---:|---|---:|---:|
| [01_ldc_ns_2d.md](../01_ldc_ns_2d/) | LDC，不可压缩 NS | 2D | 稳态 | 3000 | 28.3 GB |
| [02_ldc_nsht_2d_constant_re.md](../02_ldc_nsht_2d_constant_re/) | LDC，NS + Heat，固定 Re | 2D | 稳态 | 2990 | 34.5 GB |
| [03_ldc_nsht_2d_variable_re.md](../03_ldc_nsht_2d_variable_re/) | LDC，NS + Heat，变化 Re | 2D | 稳态 | 3000 | 34.6 GB |
| [04_fpo_ns_2d.md](../04_fpo_ns_2d/) | FPO，不可压缩 NS | 2D | 瞬态 | 名义 1150；当前删除过损坏样本 | 1.59 TB |
| [05_ldc_ns_3d.md](../05_ldc_ns_3d/) | LDC，不可压缩 NS | 3D | 稳态 | 论文 500；当前 1000 | 33.4 GB |

## FlowBench 总体

- 当前官方仓库总规模约 **1.72 TB**；
- 许可证： **CC-BY-NC-4.0**；
- 论文：[FlowBench: A Large Scale Benchmark for Flow Simulation over Complex Geometries](https://arxiv.org/abs/2409.18032)；
- 数据：[BGLab/FlowBench](https://huggingface.co/datasets/BGLab/FlowBench)；
- 工具代码：[flowbench-tools](https://github.com/baskargroup/flowbench-tools)；
- 训练/评测：[GeometryMatters](https://github.com/baskargroup/GeometryMatters)。

## 统一字段约定

每个文档的 YAML front matter 都包含：

- `parent_dataset`
- `subset`
- `equation_family`
- `spatial_dimension`
- `temporal_regime`
- `task`
- `geometry_families`
- `license`
- `last_verified`

因此这些文件可以直接用于 MkDocs、静态网站或后续多数据集索引脚本。

## 最重要的跨版本差异

1. FPO：论文写 240 帧；当前数据卡/代码为 242 原始帧，通常忽略前两帧；
2. FPO：$512\times128$ 已被删除，当前保留 $1024\times256$；
3. 3D LDC：论文 500 条，当前 1000 条；
4. 3D 输出：论文表格遗漏 $w$，官方代码读取 $u,v,w,p$；
5. DataPrep 可把 $C_D,C_L,\mathrm{Nu}$ 打包为辅助 channel，不能当作局部 PDE 场；
6. mask/SDF 在论文语义和部分旧脚本中存在符号或 0/1 与 0/255 的差异。
