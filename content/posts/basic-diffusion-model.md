---
title: "Deriving the Basic Diffusion Model"
date: 2026-06-26
draft: false
tags: ["diffusion", "generative-models", "deep-learning"]
categories: ["Machine Learning"]
summary: "From a Gaussian forward noising process to the simplified epsilon-prediction training objective used in DDPM."
ShowToc: true
TocOpen: true
---

Diffusion models learn to generate data by reversing a gradual noising process. This post derives the **simplest DDPM-style objective** step by step: forward process, reverse Markov chain, variational bound, and the familiar "predict the noise" loss.

## Setup

Let $\mathbf{x}_0 \sim q(\mathbf{x}_0)$ be a data point (e.g. an image). We define a **forward process** that adds Gaussian noise over $T$ steps:

{{% mathdisplay %}}
q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = \mathcal{N}\big(\mathbf{x}_t;\ \sqrt{1-\beta_t}\,\mathbf{x}_{t-1},\ \beta_t \mathbf{I}\big),
\quad t = 1,\ldots,T,
{{% /mathdisplay %}}

where $\{\beta_t\}_{t=1}^T$ is a variance schedule with small $\beta_t > 0$.

Define $\alpha_t = 1 - \beta_t$ and $\bar{\alpha}_t = \prod_{s=1}^{t} \alpha_s$. A key identity (reparameterization) is:

{{% mathdisplay %}}
q(\mathbf{x}_t \mid \mathbf{x}_0) = \mathcal{N}\big(\mathbf{x}_t;\ \sqrt{\bar{\alpha}_t}\,\mathbf{x}_0,\ (1-\bar{\alpha}_t)\mathbf{I}\big).
{{% /mathdisplay %}}

Equivalently,

{{% mathdisplay %}}
\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\,\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\,\boldsymbol{\epsilon},
\quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I}).
\tag{1}
{{% /mathdisplay %}}

So at large $t$, $\mathbf{x}_t$ is almost pure noise.

## Reverse process

Generation learns a reverse Markov chain $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)$. For tractability, assume Gaussian transitions with fixed variance:

{{% mathdisplay %}}
p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}\big(\mathbf{x}_{t-1};\ \boldsymbol{\mu}_\theta(\mathbf{x}_t, t),\ \sigma_t^2 \mathbf{I}\big).
{{% /mathdisplay %}}

Training maximizes $\log p_\theta(\mathbf{x}_0)$, but the exact likelihood is intractable. Instead, optimize a **variational lower bound (ELBO)**.

## ELBO decomposition

Let $q(\mathbf{x}_{1:T} \mid \mathbf{x}_0) = \prod_{t=1}^T q(\mathbf{x}_t \mid \mathbf{x}_{t-1})$. The ELBO can be written as:

{{% mathdisplay %}}
\log p_\theta(\mathbf{x}_0)
\;\ge\;
\mathbb{E}_{q}\Big[
\underbrace{D_{\mathrm{KL}}\big(q(\mathbf{x}_T \mid \mathbf{x}_0)\,\|\,p(\mathbf{x}_T)\big)}_{\text{LT}}
+ \sum_{t=2}^{T}
\underbrace{D_{\mathrm{KL}}\big(q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)\,\|\,p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t)\big)}_{\mathcal{L}_t}
- \underbrace{\log p_\theta(\mathbf{x}_0 \mid \mathbf{x}_1)}_{\mathcal{L}_0}
\Big].
{{% /mathdisplay %}}

- **$\mathcal{L}_T$**: prior match; negligible if $q(\mathbf{x}_T \mid \mathbf{x}_0) \approx \mathcal{N}(\mathbf{0}, \mathbf{I})$.
- **$\mathcal{L}_0$**: reconstruction at $t=1$ (often NLL under a decoder).
- **$\mathcal{L}_t$ ($t \ge 2$)**: denoising steps — the main training signal.

## True posterior $q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)$

Because both forward steps are Gaussian, the posterior is also Gaussian:

{{% mathdisplay %}}
q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{x}_0)
= \mathcal{N}\big(\mathbf{x}_{t-1};\ \tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0),\ \tilde{\beta}_t \mathbf{I}\big),
{{% /mathdisplay %}}

with

{{% mathdisplay %}}
\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0)
= \frac{\sqrt{\bar{\alpha}_{t-1}}\,\beta_t}{1-\bar{\alpha}_t}\,\mathbf{x}_0
+ \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}\,\mathbf{x}_t,
{{% /mathdisplay %}}

{{% mathdisplay %}}
\tilde{\beta}_t = \frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\,\beta_t.
{{% /mathdisplay %}}

Substitute $\mathbf{x}_0$ from Eq. (1) using noise $\boldsymbol{\epsilon}$:

{{% mathdisplay %}}
\tilde{\boldsymbol{\mu}}_t
= \frac{1}{\sqrt{\alpha_t}}\Big(
\mathbf{x}_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\,\boldsymbol{\epsilon}
\Big).
\tag{2}
{{% /mathdisplay %}}

## Parameterize $p_\theta$ by predicting noise

Set $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_\theta(\mathbf{x}_t, t), \sigma_t^2 \mathbf{I})$ and choose

{{% mathdisplay %}}
\boldsymbol{\mu}_\theta(\mathbf{x}_t, t)
= \frac{1}{\sqrt{\alpha_t}}\Big(
\mathbf{x}_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\,\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)
\Big),
{{% /mathdisplay %}}

i.e. the network $\boldsymbol{\epsilon}_\theta$ predicts the **same noise** $\boldsymbol{\epsilon}$ used in the forward step. With $\sigma_t^2 = \tilde{\beta}_t$ (or a fixed schedule), the KL term $\mathcal{L}_t$ simplifies to a weighted MSE on $\boldsymbol{\epsilon}$.

Ho et al. (2020) further found that **uniform weighting** over $t$ works well in practice. The standard training objective becomes:

{{% mathdisplay %}}
\mathcal{L}_{\mathrm{simple}}
= \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}}
\Big[
\big\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\big\|^2
\Big],
\quad
\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\,\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\,\boldsymbol{\epsilon}.
\tag{3}
{{% /mathdisplay %}}

**Training loop:**

1. Sample $\mathbf{x}_0$ from data, $t \sim \mathrm{Uniform}\{1,\ldots,T\}$, $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$.
2. Form noisy $\mathbf{x}_t$ via Eq. (1).
3. Minimize $\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\|^2$.

## Sampling (reverse diffusion)

At inference, start from $\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ and iterate $t = T, T-1, \ldots, 1$:

{{% mathdisplay %}}
\mathbf{x}_{t-1}
= \frac{1}{\sqrt{\alpha_t}}\Big(
\mathbf{x}_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}\,\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)
\Big)
+ \sigma_t \mathbf{z},
\quad \mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})\ \text{for } t > 1.
{{% /mathdisplay %}}

This is the core **DDPM** sampler: denoise step-by-step from noise to data.

## What we skipped (for brevity)

- Score matching / SDE viewpoint (Song et al.)
- Better samplers (DDIM, DPM-Solver)
- Latent diffusion (Stable Diffusion)
- Learned variance and noise schedules

Those build on the same forward noising identity in Eq. (1) and the epsilon parameterization in Eq. (2)–(3).

## References

- Ho, Jain, Abbeel. *Denoising Diffusion Probabilistic Models.* NeurIPS 2020.
- Sohl-Dickstein et al. *Deep Unsupervised Learning using Nonequilibrium Thermodynamics.* ICML 2015.
