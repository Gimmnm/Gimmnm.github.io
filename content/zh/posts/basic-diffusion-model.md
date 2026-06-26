---
title: "推导最基本的 Diffusion Model"
date: 2026-06-26
draft: false
tags: ["diffusion", "generative-models", "deep-learning"]
categories: ["机器学习"]
translationKey: "basic-diffusion"
summary: "从 Gaussian 前向加噪过程出发，推导 DDPM 风格的 epsilon 预测训练目标。"
ShowToc: true
TocOpen: true
---

Diffusion model 通过**逆转**一个逐步加噪的过程来学习生成数据。本文一步步推导 **DDPM 风格**的最简目标：前向过程、反向 Markov 链、变分下界，以及常见的「预测噪声」损失。

## 问题设定

设 $\mathbf{x}_0 \sim q(\mathbf{x}_0)$ 为数据（例如图像）。定义 **前向过程**，在 $T$ 步内逐步加入 Gaussian 噪声：

$$
q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = \mathcal{N}\big(\mathbf{x}_t;\ \sqrt{1-\beta_t}\,\mathbf{x}_{t-1},\ \beta_t \mathbf{I}\big),
\quad t = 1,\ldots,T,
$$

其中 $\{\beta_t\}_{t=1}^T$ 为方差 schedule，$\beta_t > 0$ 且通常很小。

记 $\alpha_t = 1 - \beta_t$，$\bar{\alpha}_t = \prod_{s=1}^{t} \alpha_s$。一个重要结论是（重参数化）：

$$
q(\mathbf{x}_t \mid \mathbf{x}_0) = \mathcal{N}\big(\mathbf{x}_t;\ \sqrt{\bar{\alpha}_t}\,\mathbf{x}_0,\ (1-\bar{\alpha}_t)\mathbf{I}\big).
$$

等价地，

$$
\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\,\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\,\boldsymbol{\epsilon},
\quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I}).
\tag{1}
$$

当 $t$ 很大时，$\mathbf{x}_t$ 近似纯噪声。

## 反向过程

生成阶段学习反向 Markov 链 $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$。为可 tractable，设 Gaussian 转移、方差固定：

$$
p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}\big(\mathbf{x}_{t-1};\ \boldsymbol{\mu}_\theta(\mathbf{x}_t, t),\ \sigma_t^2 \mathbf{I}\big).
$$

训练目标是最大化 $\log p_\theta(\mathbf{x}_0)$，但精确似然不可 tractable，因此优化 **变分下界（ELBO）**。

## ELBO 分解

令 $q(\mathbf{x}_{1:T} \mid \mathbf{x}_0) = \prod_{t=1}^T q(\mathbf{x}_t \mid \mathbf{x}_{t-1})$，ELBO 可写为：

$$
\log p_\theta(\mathbf{x}_0)
\;\ge\;
\mathbb{E}_{q}\Big[
\underbrace{D_{\mathrm{KL}}\big(q(\mathbf{x}_T \mid \mathbf{x}_0)\,\|\,p(\mathbf{x}_T)\big)}_{\text{LT}}
+
\sum_{t=2}^{T}
\underbrace{D_{\mathrm{KL}}\big(q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)\,\|\,p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)\big)}_{\mathcal{L}_t}
-
\underbrace{\log p_\theta(\mathbf{x}_0 \mid \mathbf{x}_1)}_{\mathcal{L}_0}
\Big].
$$

- **$\mathcal{L}_T$**：与先验匹配；若 $q(\mathbf{x}_T \mid \mathbf{x}_0) \approx \mathcal{N}(\mathbf{0}, \mathbf{I})$ 则影响很小。
- **$\mathcal{L}_0$**：$t=1$ 处的重建项。
- **$\mathcal{L}_t$（$t \ge 2$）**：去噪项 —— 主要训练信号。

## 真实后验 $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)$

前向两步都是 Gaussian，后验也是 Gaussian：

$$
q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)
= \mathcal{N}\big(\mathbf{x}_{t-1};\ \tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0),\ \tilde{\beta}_t \mathbf{I}\big),
$$

其中

$$
\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0)
= \frac{\sqrt{\bar{\alpha}_{t-1}}\,\beta_t}{1-\bar{\alpha}_t}\,\mathbf{x}_0
+ \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}\,\mathbf{x}_t,
$$

$$
\tilde{\beta}_t = \frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\,\beta_t.
$$

用式 (1) 把 $\mathbf{x}_0$ 换成噪声 $\boldsymbol{\epsilon}$：

$$
\tilde{\boldsymbol{\mu}}_t
= \frac{1}{\sqrt{\alpha_t}}\Big(
\mathbf{x}_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\,\boldsymbol{\epsilon}
\Big).
\tag{2}
$$

## 用「预测噪声」参数化 $p_\theta$

设 $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_\theta(\mathbf{x}_t, t), \sigma_t^2 \mathbf{I})$，并取

$$
\boldsymbol{\mu}_\theta(\mathbf{x}_t, t)
= \frac{1}{\sqrt{\alpha_t}}\Big(
\mathbf{x}_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\,\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)
\Big),
$$

即网络 $\boldsymbol{\epsilon}_\theta$ 预测前向过程中使用的 **同一噪声** $\boldsymbol{\epsilon}$。取 $\sigma_t^2 = \tilde{\beta}_t$（或固定 schedule）时，KL 项 $\mathcal{L}_t$ 化为对 $\boldsymbol{\epsilon}$ 的加权 MSE。

Ho 等人 (2020) 还发现对 $t$ **均匀加权**在实践中效果很好。标准训练目标为：

$$
\mathcal{L}_{\mathrm{simple}}
= \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}}
\Big[
\big\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\big\|^2
\Big],
\quad
\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\,\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\,\boldsymbol{\epsilon}.
\tag{3}
$$

**训练流程：**

1. 从数据采样 $\mathbf{x}_0$，$t \sim \mathrm{Uniform}\{1,\ldots,T\}$，$\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$。
2. 用式 (1) 构造带噪 $\mathbf{x}_t$。
3. 最小化 $\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\|^2$。

## 采样（反向扩散）

推理时从 $\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 出发，令 $t = T, T-1, \ldots, 1$ 迭代：

$$
\mathbf{x}_{t-1}
= \frac{1}{\sqrt{\alpha_t}}\Big(
\mathbf{x}_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\,\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)
\Big)
+ \sigma_t \mathbf{z},
\quad \mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})\ \text{（} t > 1 \text{ 时）}.
$$

这就是 **DDPM** 的核心采样器：从噪声逐步去噪到数据。

## 本文未展开的内容

- Score matching / SDE 视角（Song 等）
- 更高效的采样器（DDIM、DPM-Solver）
- Latent diffusion（Stable Diffusion）
- 可学习方差与 noise schedule 设计

这些都建立在式 (1) 的前向加噪恒等式，以及式 (2)–(3) 的 epsilon 参数化之上。

## 参考文献

- Ho, Jain, Abbeel. *Denoising Diffusion Probabilistic Models.* NeurIPS 2020.
- Sohl-Dickstein et al. *Deep Unsupervised Learning using Nonequilibrium Thermodynamics.* ICML 2015.
