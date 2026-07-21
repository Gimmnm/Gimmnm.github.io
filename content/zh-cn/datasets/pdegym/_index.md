---
title: "PDEgym docs"
linkTitle: PDEgym
weight: 50
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
summary: "ETH CAMLab 的预训练与下游算子学习任务集合，覆盖不可压/可压缩流体、波动与椭圆方程等。"
description: "ETH CAMLab 的预训练与下游算子学习任务集合，覆盖不可压/可压缩流体、波动与椭圆方程等。"
dataset_family: PDEgym
---

# PDEgym 子数据集 Markdown 技术文档（中文）

本目录按照 [The Well 单数据集页面](https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/) 的信息组织方式，为 PDEgym 的每个**逻辑任务/算子**建立一份独立 Markdown 文档，并补充所属数据集、官方链接、下载/组装命令、原始张量、模型接口、可调/变化/固定参数、代码标识和来源冲突说明。

## 文档范围

- **21 个逻辑任务**：6 个预训练算子 + 15 个下游任务。
- **20 个物理数据仓库**：NS-PwC 与 NS-Tracer-PwC 共用同一个 `NS-PwC` 仓库与 NetCDF 文件。Hugging Face 的 PDEgym collection 显示 21 个条目，是因为其中还包含论文条目。
- 中文文档位于 `zh-CN/`，英文文档位于 `en/`。
- 20 个不重复物理仓库共包含 **299,088**条轨迹/稳态样本；按 21 个逻辑任务重复计入 tracer 视图时为 **319,088**。
- 按 20 个官方 Hugging Face 数据仓库当前显示的总文件大小相加，发布量约为 **992.07 GB**（十进制 GB，约 0.992 TB）；这不等同于解压后磁盘占用或训练时缓存占用。

## 统一口径

1. **原始文件尺寸**与**模型单个训练样本尺寸**分开写。原始轨迹通常是 `[N,T,C,H,W]`；官方 all2all 加载器返回 `[C,H,W] → [C,H,W]` 和 lead time，批处理后才有 batch 维。
2. **数学上可调参数**、**生成代码可改参数**与**发布数据实际扫描参数**分开写。
3. 对来源冲突不擅自猜测：例如 Wave-Layer 的 21/15 帧冲突、Wave 数据时间标定冲突、ACE 的 $\epsilon$ 与 $\epsilon^2$ 记法，以及多个 raw tracer 通道未被论文任务使用。
4. 稳态任务的 `.time` 只是官方代码的长时间极限包装，不代表 raw 文件存在时间轨迹。

## 索引

| # | 子数据集 | 角色 | PDE | 数量 | 原始形状 | 官方容量/说明 |
|---:|---|---|---|---:|---|---|
| 01 | [NS-Sines](../01_ns-sines/) | 预训练算子 | Incompressible Navier–Stokes / near-inviscid flow | 20000 | velocity: [20000, 21, 3, 128, 128] | 82.6 GB |
| 02 | [NS-Gauss](../02_ns-gauss/) | 预训练算子 | Incompressible Navier–Stokes / near-inviscid flow | 20000 | velocity: [20000, 21, 3, 128, 128] | 82.6 GB |
| 03 | [CE-RP](../03_ce-rp/) | 预训练算子 | Compressible Euler | 10000 | data: [10000, 21, 5, 128, 128] | 68.8 GB |
| 04 | [CE-CRP](../04_ce-crp/) | 预训练算子 | Compressible Euler | 10000 | data: [10000, 21, 5, 128, 128] | 68.8 GB |
| 05 | [CE-KH](../05_ce-kh/) | 预训练算子 | Compressible Euler | 10000 | data: [10000, 21, 5, 128, 128] | 68.8 GB |
| 06 | [CE-Gauss](../06_ce-gauss/) | 预训练算子 | Compressible Euler | 10000 | data: [10000, 21, 5, 128, 128] | 68.8 GB |
| 07 | [NS-PwC](../07_ns-pwc/) | 下游任务：新初值分布 | Incompressible Navier–Stokes / near-inviscid flow | 20000 | velocity: [20000, 21, 3, 128, 128] | 82.6 GB (shared with NS-Tracer-PwC) |
| 08 | [NS-BB](../08_ns-bb/) | 下游任务：粗糙随机初值 | Incompressible Navier–Stokes / near-inviscid flow | 20000 | velocity: [20000, 21, 3, 128, 128] | 82.6 GB |
| 09 | [NS-SL](../09_ns-sl/) | 下游任务：剪切层 | Incompressible Navier–Stokes / near-inviscid flow | 40000 | velocity: [40000, 21, 2, 128, 128] | 110 GB |
| 10 | [NS-SVS](../10_ns-svs/) | 下游任务：正弦涡片 | Incompressible Navier–Stokes / near-inviscid flow | 20000 | velocity: [20000, 21, 3, 128, 128] | 82.6 GB |
| 11 | [NS-Tracer-PwC](../11_ns-tracer-pwc/) | 下游任务：新增被动标量物理 | Incompressible Navier–Stokes + advection–diffusion | 20000 | velocity: [20000, 21, 3, 128, 128] (shared NS-PwC file) | No additional storage; shares the 82.6 GB NS-PwC repository |
| 12 | [FNS-KF](../12_fns-kf/) | 下游任务：新增外部强迫 | Forced incompressible Navier–Stokes | 20000 | solution: [20000, 21, 2, 128, 128] | 55.1 GB |
| 13 | [CE-RPUI](../13_ce-rpui/) | 下游任务：新界面分布 | Compressible Euler | 10000 | data: [10000, 21, 5, 128, 128] | 68.8 GB |
| 14 | [CE-RM](../14_ce-rm/) | 下游任务：激波–界面不稳定性 | Compressible Euler | 1260 | solution: [1260, 21, 5, 128, 128] | 8.67 GB |
| 15 | [GCE-RT](../15_gce-rt/) | 下游任务：新增重力源项与物理参数 | Compressible Euler with gravity | 1260 | solution: [1260, 11, 6, 128, 128] | 5.45 GB |
| 16 | [Wave-Gauss](../16_wave-gauss/) | 下游任务：逐样本 PDE 系数 | Variable-coefficient wave equation | 10512 | solution: [10512, 15, 128, 128]; c: [10512, 128, 128] | 11.7 GB |
| 17 | [Wave-Layer](../17_wave-layer/) | 下游任务：分层不连续 PDE 系数 | Variable-coefficient wave equation | 10512 | solution: [10512, 15, 128, 128]; c: [10512, 128, 128] | 15.2 GB |
| 18 | [ACE](../18_ace/) | 下游任务：新 PDE/相变物理 | Allen–Cahn reaction–diffusion | 15000 | solution: [15000, 20, 128, 128] | 19.7 GB |
| 19 | [SE-AF](../19_se-af/) | 下游任务：稳态几何条件算子 | Steady compressible Euler | 10869 | solution: [10869, 2, 128, 128] | 1.43 GB |
| 20 | [Poisson-Gauss](../20_poisson-gauss/) | 下游任务：稳态椭圆算子 | Poisson equation | 20000 | source: [20000,128,128]; solution: [20000,128,128] | 2.62 GB |
| 21 | [Helmholtz](../21_helmholtz/) | 下游任务：稳态系数算子 | Helmholtz equation | 19675 | HDF5: 19675 groups Sample_i, each with a[128,128], scalar bc, u[128,128] | 5.2 GB |

## 其他文件

- [`manifest.json`](manifest.json)：机器可读索引。
- [`manifest.csv`](manifest.csv)：表格索引。
- [`TEMPLATE_zh-CN.md`](TEMPLATE_zh-CN.md)：以后整理其他数据集可复用的中文模板。
- [`TEMPLATE_en.md`](TEMPLATE_en.md)：英文模板。
- [`SOURCES.md`](SOURCES.md)：统一来源与版本说明。
