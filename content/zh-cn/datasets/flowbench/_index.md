---
title: "FlowBench"
parent_dataset: FlowBench
last_verified: 2026-07-21
linkTitle: FlowBench
weight: 60
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
summary: "复杂几何上流场模拟大规模基准，覆盖二维/三维顶盖驱动与瞬态 FPO 等配置。"
description: "复杂几何上流场模拟大规模基准，覆盖二维/三维顶盖驱动与瞬态 FPO 等配置。"
dataset_family: FlowBench
---

# FlowBench

![FlowBench 三类几何示例：G1（NURBS）、G2（球谐/谐波）、G3（骨架轮廓）](./G1G2G3examples.png)

![各配置输入 / 输出张量的公式化描述](./inputoutputtensor.png)

## 配置列表

| 配置 | PDE/说明 | 维数 | 状态 | 名义/当前样本数 | 当前体积 |
|---|---|---:|---|---:|---:|
| [LDC NS 2D](./01_ldc_ns_2d/) | LDC，不可压缩 NS | 2D | 稳态 | 3000 | 28.3 GB |
| [LDC NSHT 2D（固定 Re）](./02_ldc_nsht_2d_constant_re/) | LDC，NS + Heat，固定 Re | 2D | 稳态 | 2990 | 34.5 GB |
| [LDC NSHT 2D（变化 Re）](./03_ldc_nsht_2d_variable_re/) | LDC，NS + Heat，变化 Re | 2D | 稳态 | 3000 | 34.6 GB |
| [FPO NS 2D](./04_fpo_ns_2d/) | FPO，不可压缩 NS | 2D | 瞬态 | 名义 1150；当前删除过损坏样本 | 1.59 TB |
| [LDC NS 3D](./05_ldc_ns_3d/) | LDC，不可压缩 NS | 3D | 稳态 | 论文 500；当前 1000 | 33.4 GB |

## FlowBench 总体

- 当前官方仓库总规模约 **1.72 TB**；
- 许可证： **CC-BY-NC-4.0**；
- 论文：[FlowBench: A Large Scale Benchmark for Flow Simulation over Complex Geometries](https://arxiv.org/abs/2409.18032)；
- 数据：[BGLab/FlowBench](https://huggingface.co/datasets/BGLab/FlowBench)；
- 工具代码：[flowbench-tools](https://github.com/baskargroup/flowbench-tools)；
- 训练/评测：[GeometryMatters](https://github.com/baskargroup/GeometryMatters)。

## 最重要的跨版本差异

1. FPO：论文写 240 帧；当前数据卡/代码为 242 原始帧，通常忽略前两帧；
2. FPO：$512\times128$ 已被删除，当前保留 $1024\times256$；
3. 3D LDC：论文 500 条，当前 1000 条；
4. 3D 输出：论文表格遗漏 $w$，官方代码读取 $u,v,w,p$；
5. DataPrep 可把 $C_D,C_L,\mathrm{Nu}$ 打包为辅助 channel，不能当作局部 PDE 场；
6. mask/SDF 在论文语义和部分旧脚本中存在符号或 0/1 与 0/255 的差异。
