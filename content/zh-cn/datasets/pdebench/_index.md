---
title: "PDEBench"
linkTitle: PDEBench
weight: 10
draft: false
ShowToc: true
hidemeta: true
ShowPostNavLinks: false
hiddenInHomeList: true
math: true
summary: "广泛使用的科学机器学习基准，覆盖 1D–3D 平流、扩散、浅水与可压缩/不可压流体等 11 类任务。"
description: "广泛使用的科学机器学习基准，覆盖 1D–3D 平流、扩散、浅水与可压缩/不可压流体等 11 类任务。"
dataset_family: PDEBench
---

# PDEBench

## 问题定义

PDE 的解是一个向量值函数 $\mathbf{v} : \mathcal{T} \times \mathcal{S} \times \Theta \rightarrow \mathbb{R}^{d}$，定义在某个空间域 $\mathcal{S}$ 上，带有时间索引 $\mathcal{T}$，以及某个可能为函数值的参数空间 $\Theta$。例如在热扩散方程中，$\mathbf{v}$ 可以表示某处介质在给定点 $\mathbf{s} \in \mathcal{S}$、给定时刻 $t \in \mathcal{T}$ 的局部温度 $\tau \in \mathbb{R}^{1}$，并条件于刻画非均匀介质的空间变化标量电导率场 $\theta : \mathcal{S} \rightarrow \mathbb{R}^{+}$。将某一时间步的解状态映射到下一时间步解的算子 $\mathfrak{F}_{\theta} : \mathbf{v}_{\theta}(t,\cdot) \rightarrow \mathbf{v}_{\theta}(t+1,\cdot)$ 称为*前向传播算子*（forward propagator）。

科学机器学习（Scientific ML）的目标，是通过学习近似 $\widehat{\mathfrak{F}}_{\theta} \simeq \mathfrak{F}_{\theta}$，为该前向传播算子寻找某种基于机器学习的代理模型（surrogate），有时也称为仿真器（emulator）。PDE 的前向传播算子不仅依赖于当前状态，还依赖于状态场的空间与时间导数。实践中，单一时间步的系统状态往往无法方便地编码解的时间导数。因此，前向传播算子还可能依赖于解的多个先前时间步，以便对时间导数做有限差分近似。于是，离散化的前向传播算子 $\mathring{\mathfrak{F}}_{\theta}$ 作用于 $\ell \geq 1$ 个连续时间步，使得 $\mathring{\mathfrak{F}}_{\theta} : \mathbf{v}_{\theta}(t-\ell,\cdot),\dots,\mathbf{v}_{\theta}(t-1,\cdot) \mapsto \mathbf{v}_{\theta}(t,\cdot)$，并简记为 $\mathbf{v}_{\theta}([t-\ell:t-1],\cdot) := \mathbf{v}_{\theta}(t-\ell,\cdot),\dots,\mathbf{v}_{\theta}(t-1,\cdot)$。

我们寻求用仿真器 $\widehat{\mathfrak{F}}_{\theta} \simeq \mathring{\mathfrak{F}}_{\theta}$ 近似该离散算子，即在相同输入下，仿真器预测相对于某种代价度量应接近地面真值模拟。我们固定一类参数化模型 $\{\mathfrak{F}_{\theta,\phi}\}_{\phi}$。从该类中，我们由数据学习代理模型 $\widehat{\mathfrak{F}}_{\theta,\phi}$。学习时，取数据集 $\mathcal{D}$，其中包含以选定参数值 $(\theta_k)$ 为条件的离散化 PDE 解，$\mathcal{D} := \{\mathbf{v}_{\theta_k}^{(k)}([0:t_{\mathrm{max}}],\cdot) \mid k=1,\dots,K\}$。固定损失泛函 $L$ 后，目标是找到某个 $\phi$，使其在训练数据集上达到最小总损失：

\[
\hat{\phi} = \operatorname{argmin}_{\phi} \sum_{t=1}^{t_{\mathrm{max}}} \sum_{k=1}^{K} L\Bigl(\mathfrak{F}_{\theta_k,\phi}\{\mathbf{v}_{\theta_k}^{(k)}([t-\ell:t-1],\cdot)\},\mathbf{v}_{\theta_k}^{(k)}(t,\cdot)\Bigr).
\]

由于使用随机梯度下降等迭代优化算法，以及上述优化问题的非凸性，我们通常得到的是局部最优。数据集 $\mathcal{D}$ 由旨在高精度模拟目标动力学的地面真值求解器生成。在这些数据中，我们可以改变初始条件（即改变 $\mathbf{v}_{\theta}(0,\cdot)$）、改变 $\theta$，或两者同时改变。

除前向问题外，我们还考虑用学到的代理模型近似求解*反问题*，其中未知初始条件 $\mathbf{v}_{\theta}(0,\cdot)$ 或未知参数 $\theta$ 被选成与某些观测输出 $\mathbf{v}_{\theta}([t:t+\ell],\cdot)$ 相一致。我们采用近似代理方法，将前向代理作为模型的均值预测器。我们假设 $\mathbf{v}_{\theta}(t,\cdot) = \mathfrak{F}_{\theta,\phi}\{\mathbf{v}_{\theta}([t-\ell:t-1],\cdot)\} + \epsilon$，其中 $\epsilon$ 为零均值观测噪声，并对感兴趣的未知量假定先验分布。该领域亦可使用其他反演方法，例如生成对抗模型或变分自编码器。

## 方程目录

![Paper Table1](./Table1.png)

先读 [数据格式](./00_data_format/)（HDF5 约定）；各方程页另列该类下载文件。

| # | 方程文档 | 下载键 | 当前标称体积 |
|---:|---|---|---:|
| — | [数据格式](./00_data_format/) | — | — |
| 1 | [一维线性平流方程](./01_advection_1d/) | `advection` | 47 GB |
| 2 | [一维 Burgers 方程](./02_burgers_1d/) | `burgers` | 93 GB |
| 3 | [一维扩散—反应方程](./03_reaction_diffusion_1d/) | `1d_reacdiff` | 62 GB |
| 4 | [一维扩散—吸附方程](./04_diffusion_sorption_1d/) | `diff_sorp` | 4 GB |
| 5 | [二维 FitzHugh–Nagumo 扩散—反应系统](./05_reaction_diffusion_2d/) | `2d_reacdiff` | 13 GB |
| 6 | [二维 Darcy Flow](./06_darcy_flow_2d/) | `darcy` | 6.2 GB |
| 7 | [二维浅水方程：径向溃坝](./07_shallow_water_2d/) | `swe` | 6.2 GB |
| 8 | [一维可压缩 Navier–Stokes / CFD](./08_compressible_ns_1d/) | `1d_cfd` | 88 GB |
| 9 | [二维可压缩 Navier–Stokes / CFD](./09_compressible_ns_2d/) | `2d_cfd` | 551 GB |
| 10 | [三维可压缩 Navier–Stokes / CFD](./10_compressible_ns_3d/) | `3d_cfd` | 285 GB |
| 11 | [二维非均匀强迫不可压 Navier–Stokes](./11_incompressible_ns_2d/) | `ns_incom` | 2.3 TB |

## 统一口径

- PDEBench 论文称 11 个 PDE/任务、不同参数化形成 35 个基线配置；这不等于当前下载清单中的 HDF5 文件数。
- 各方程页「参数」分两块：**发布文件配置**（按 `pdebench_data_urls.csv` 逐文件）与 **生成器可调范围**（YAML 能改什么/范围，即使下载未扫全）。文件名与论文摘要冲突时以实际文件为准。
- HDF5 通用数组约定为 $(b,t,x_1,\ldots,x_d,v)$；compressible NS 的物理变量可能分别存为独立 datasets。细节见 [数据格式](./00_data_format/)。
- Darcy Flow 是静态 $a\mapsto u$ 算子任务；其余主要为时序任务。
- 当前 11 类一键下载标称体积合计约 **3.46 TB**（按十进制 GB/TB 直接相加，未考虑文件系统单位差异）。
