---
title: "CFDBench 数据文档索引"
dataset: CFDBench
problem_id: cfdbench
equation_family: "2D incompressible Navier-Stokes"
time_dependent: true
data_origin: "ANSYS Fluent numerical simulation"
interpolated_grid: "64 x 64"
license: "Apache-2.0 (Hugging Face dataset card)"
paper: "https://arxiv.org/abs/2310.05963"
code: "https://github.com/luo-yining/CFDBench"
interpolated_data: "https://huggingface.co/datasets/chen-yingfa/CFDBench"
raw_data: "https://huggingface.co/datasets/chen-yingfa/CFDBench-raw"
last_verified: 2026-07-21
linkTitle: CFDBench
weight: 10
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
summary: "二维不可压缩 Navier–Stokes 的四种典型 CFD 工况：方腔、圆管、溃坝越障与圆柱绕流。"
description: "二维不可压缩 Navier–Stokes 的四种典型 CFD 工况：方腔、圆管、溃坝越障与圆柱绕流。"
dataset_family: CFDBench
---

# CFDBench 数据文档索引

CFDBench 不是包含四套完全不同控制方程的 PDE 集合，而是把同一类二维不可压缩 Navier--Stokes 系统放入四种典型 CFD 工况中：顶盖驱动方腔、圆管两相流、带障碍物的重力越障流和圆柱绕流。为了与 The Well 的“一种数据配置一页”方式一致，本目录按 **四个问题配置** 各写一份 Markdown；每份文档内部再完整区分 BC、PROP、GEO 三个基础子集。

## 文档列表

| 问题配置 | 中文文档 | 物理特征 | 轨迹数 | 总帧数 |
|---|---|---|---:|---:|
| Cavity Flow | [cavity_flow.md](../cavity_flow/) | 单相、封闭腔、移动壁面 | 159 | 34,582 |
| Tube Flow | [tube_flow.md](../tube_flow/) | 水--空气两相、入口边界层 | 175 | 39,553 |
| Dam Flow | [dam_flow.md](../dam_flow/) | 两相、重力、障碍物和射流 | 220 | 21,916 |
| Cylinder Flow | [cylinder_flow.md](../cylinder_flow/) | 单相绕流、涡脱落、周期尾迹 | 185 | 205,620 |
| **合计**| — | — | **739**| **301,671** |

## 统一数据事实

- 每个问题有 `bc`、`prop`、`geo` 三个互斥生成子集；它们不是所有参数的全笛卡尔积。
- 论文报告 739 条 case/轨迹和 301,671 帧。
- 官方插值文件以 `u.npy`、`v.npy` 保存二维速度分量；每条 case 的时间长度 $T_i$ 可能不同。
- 论文统一将结果插值到 $64\times64$；当前 loader 还会生成 mask，并在 Tube/Dam 中补边界网格线。
- 论文摘要提到速度和压力场，但当前官方插值压缩包及基线 loader 统一使用的是 `u.npy`、`v.npy`。压力存在于原始 Fluent 导出中，需要自行解析和插值。
- 数据页许可证标记为 Apache-2.0；论文/代码的引用要求仍应遵守。

## 信息优先级

遇到论文、附录、代码和下载文件不一致时，建议按以下顺序决定实际训练配置：

1. 下载后的 `case.json` 和 `u.npy/v.npy.shape`；
2. 固定 commit 的实际 loader；
3. 论文正文；
4. 论文表格或代码注释。

这样可以避免把已知的 Tube GEO、Dam PROP/GEO、Cylinder `d`/`radius` 和时间间隔冲突带入数据预处理。


## 下载与目录组织

### 官方链接

- 论文：[https://arxiv.org/abs/2310.05963](https://arxiv.org/abs/2310.05963)
- 官方代码：[https://github.com/luo-yining/CFDBench](https://github.com/luo-yining/CFDBench)
- 插值数据：[https://huggingface.co/datasets/chen-yingfa/CFDBench](https://huggingface.co/datasets/chen-yingfa/CFDBench)
- 原始 Fluent 数据：[https://huggingface.co/datasets/chen-yingfa/CFDBench-raw](https://huggingface.co/datasets/chen-yingfa/CFDBench-raw)
- 百度网盘原始数据：[https://pan.baidu.com/s/1p0q60cv2hFZ7UcIf3XKSaw?pwd=cfd4](https://pan.baidu.com/s/1p0q60cv2hFZ7UcIf3XKSaw?pwd=cfd4)，提取码 `cfd4`
- 文档版式参考：[https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/](https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/)

官方仓库把插值数据描述为约 13.4 GB；Hugging Face 页面在 **2026-07-21** 显示总文件大小为约 14.4 GB。原始库在仓库 README 中被描述为约 460 GB，而 Hugging Face 原始页当前显示约 205 GB，并注明 Cylinder 部分仍在上传。对可复现工作，应记录具体下载日期和仓库 revision。

### 命令行下载

先安装当前 Hugging Face CLI：

```bash
python -m pip install -U huggingface_hub
```

完整下载插值库：

```bash
hf download chen-yingfa/CFDBench \
  --repo-type dataset \
  --local-dir ./downloads/CFDBench
```

完整下载原始库会占用数百 GB，执行前建议先检查：

```bash
hf download chen-yingfa/CFDBench-raw \
  --repo-type dataset \
  --local-dir ./downloads/CFDBench-raw \
  --dry-run
```

### 代码仓库

```bash
git clone https://github.com/luo-yining/CFDBench.git
cd CFDBench
python -m pip install -r requirements.txt
```

解压后的推荐目录结构为

```text
data/
├── cavity/
│   ├── bc/caseXXXX/{case.json,u.npy,v.npy}
│   ├── geo/caseXXXX/{case.json,u.npy,v.npy}
│   └── prop/caseXXXX/{case.json,u.npy,v.npy}
├── tube/
├── dam/
└── cylinder/
```


## 引用

```bibtex
@article{CFDBench,
  title  = {CFDBench: A Large-Scale Benchmark for Machine Learning Methods in Fluid Dynamics},
  author = {Luo, Yining and Chen, Yingfa and Zhang, Zhen},
  year   = {2023},
  url    = {https://arxiv.org/abs/2310.05963}
}
```

## 资料来源

- 论文 v2：第 3 节、表 2--6、附录 E.1。
- 官方仓库 README、`src/dataset/*.py`、`generation-code/`。
- 官方 Hugging Face 插值与原始数据页。
- 页面结构参考 The Well 的 `acoustic_scattering_discontinuous` 数据说明。
