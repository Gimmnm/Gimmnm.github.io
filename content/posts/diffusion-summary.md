---
title: "Diffusion Summary"
date: 2026-06-27
draft: false
tags: ["diffusion", "generative-models", "deep-learning"]
categories: ["Machine Learning"]
summary: "A personal summary of diffusion models — forward process, training objective, and sampling."
ShowToc: true
TocOpen: true
---

这是一些不成熟的关于Diffusion Model和相关细节的随笔。

---

## Codelength and likelihood

在信息论里常常将概率取$-log$，称其为codelength；而在机器学习的模型里，如果考虑一个Bayes模型，希望得到极大似然，为了方便以及易于优化，也会取$-log$，得到所谓的likelihood对应的Loss；这两个数学上是一个东西，likelihood越大，当前的模型得到数据更加有确定性，模型越好，同时codelength越小，也就是用更少的bit表现了结果。

我读了DDPM论文里的一些表述习惯，才渐渐习惯理解信息论的视角看概率。比如，作者表示，如果将训练目标改为$L_1$（这实际上是DDIM论文中的写法）后，虽然没有特别好的likelihood，也就是codelength没有压缩到最好，但是观察codelength的分布，发现超过一半的bits都用在最后一步上，从实际效果来看，生成质量反而是更好的，所以启发我们在图片生成的时候likelihood不一定是唯一的目标，codelength的分布可能也有用？

再回看一下信息熵，公式是

{{% mathdisplay %}}
H(X) = -\sum_{x \in X} p(x) \log p(x)
{{% /mathdisplay %}}

也就是对于每个$x$，有$p(x)$的概率用$-\log p(x)$的bits去表示结果，加权求和得到熵。DDPM里公式里用到的KL散度也能一定程度上用信息论角度理解，KL散度就是一个概率分布去近似另一个概率分布时需要多用的bits。

由此DDPM里还类比了压缩算法等等。

## DDIM

DDIM主要是为了解决DDPM采样速度也就是生成图片慢的问题。

- 从数学上，DDPM中优化的目标实际上只和"marginals"有关，所以我们可以用一族新的forward加噪随机过程去达到相同的marginals，但是不是Markovain的，这样保证了$L_1$不会变化。

- 设计一个新的反向过程，充分运用forward的信息。可以证明对应的Loss和$L_1$等价，而$L_1$的形式又没有变化，由此我们直接用DDPM训练好的模型来用新的采样方法。

- 注意到这里实际上还没有什么加速，但是这族forward过程的一个特殊情况，直接变成implicit，也就是给一个特定的采样$x_T$，对应生成全部确定了，由此可以跳步。

DDPM为什么不能跳步？一方面，如果直接把反向的Gaussian过程像正向一样叠加起来，实际上计算不会有什么减少。另一方面，如果写成一个有点像DDIM论文里的对应的DDPM的特殊情况，那么会有随机项，会导致生成不稳定，跳步会导致生成质量下降。

DDIM变成纯隐式后，从Gaussian到$P_Data$变成一个确定的map，由此可以做更多插值等操作。

我需要再咀嚼一下这种概率过程，然后再看看DDIM中关于SDE、ODE的解释。

## 分布

学习了score matching，终于看懂一些DDPM论文中的内容，实际上我们要学的就是一个$P_{\text{data}}$，理解成在比如$\mathbb{R}^{H\times W \times C}$空间中的概率分布，而diffusion、score matching的思路都转化为学习怎么从一个Gaussian分布中的点，走到我们要的这个分布中去。

Diffusion的总体思路是，我设定一个从数据分布到Gaussian分布的路径，然后学习反向过程。DDPM一开始是学习反向的Gaussian的Markov chain过程的均值，重要的突破是改成学习$\varepsilon_{\theta}$，这个总噪音实际上描述了一种方向。在DDPM的反向采样过程中，每一步有随机性，可以说是往数据采样方向一步步走，所以不能跳步太快。看成一个SDE，类比数值方法中的内容，跳步太快肯定会偏。DDIM的好处就在于，整个过程是确定的，Gaussian分布中的点怎么变换到数据分布是确定的，那么采样生成方式就能够找到方式加速。

Score matching直接考虑怎么从一个任意的初始采样点（Maybe Gaussian）走到好的数据分布点上去，虽然也要走多步，但并不是Diffusion那样的latent variable，而是直接根据梯度走。但是真实的数据分布并不知道，更加不知道梯度怎么算，所以要对已有的数据（Training data）去加高斯噪音，得到可以学习以及计算的梯度，成为score，然后沿着score做Langevin sampling。

感觉，score matching里用不同尺度的加噪和diffusion里的forward很像，暂时看到的区别是diffusion有确定的latent variable. 另一个区别是，diffusion是variance preserving的，但是score matching会出现variane explosion. 两种算法用不同的方式加噪音。

## SDE

Wow，在SDE那篇文章中，用连续的SDE来描述离散的diffusion和score matching，真的统一了两者！后续要重点读一下这篇文章！转化为连续的SDE后，forward过程可以写成

{{% mathdisplay %}}
dx = f(x,t)dt + g(t)dW
{{% /mathdisplay %}}

where $dW$ is the Wiener process. $f(x,t)$项是drift part，$g(t)$项是diffusion，反向过程可以用SDE的逆过程来描述，有完整的理论！

从这个出发可以有类似DDPM $\to$ DDIM的故事。通过一些推导，可以从SDE转化为ODE，PF-ODE.

## RL

强化学习训练中和一般的网络比较不同的是，需要有和环境的交互得到对应的reward，一般的Policy Gradient要每次更新model后重新交互收集数据形成reward，因为One man's meat is another man's poison!

- On-Policy
The actor to train and the actor for interacting is the same.

- Off-policy
The actor to train and the actor for interacting are different. Then, the actor to train has to know its difference from the actor to interact.

This lead to Proximal Policy Optimization (PPO) algorithm.

并且，在收集数据的时候，The actor needs to have randomness during data collection. 也就是Exploration.

## Flow matching

穿插一下Flow方法，首先Flow想要的是把原分布变换到目标分布，从采样点角度，single sample满足一个ODE，而从概率分布角度，满足一个概率连续变化，由此确定了变换过程中核心关系，continuity equation:

{{% mathdisplay %}}
\frac{\partial p_t(x_t)}{\partial t} = -\nabla \cdot (p_t u_t(x_t))
{{% /mathdisplay %}}

也就是说，只要找到满足这个方程的$p_t$和$u_t$以及初始条件，就可以得到一个变换。

由此，我们要找容易计算的loss，因为直接考虑maximize likelihood是一个积分过程，每次都要从0积分到1算一次。

有点像PDE中基本解的思路，考虑把initial distribution变换到一个dirac distribution，这种情况下的$u_t$和$p_t$很好算。然后实际的情况，然后从$p_t$角度，是插值叠加，从$u_t$角度，是概率加权的叠加，并且我们转而考虑将$u^{\theta}_t$往这个叠加的$u_t$上学，而不是直接降低likelihood，并且，可以得到的等价的Conditional Loss，更加容易计算!

## References

### Diffusion

- Ho, Jain, Abbeel. *Denoising Diffusion Probabilistic Models.* NeurIPS, 2020. [arXiv:2006.11239](https://arxiv.org/abs/2006.11239)
- Song, Meng, Ermon. *Denoising Diffusion Implicit Models.* ICLR, 2021. [arXiv:2010.02502](https://arxiv.org/abs/2010.02502)
- Nichol, Dhariwal. *Improved Denoising Diffusion Probabilistic Models.* ICML, 2021. [arXiv:2102.09672](https://arxiv.org/abs/2102.09672)
- Kingma et al. *Variational Diffusion Models.* NeurIPS, 2021. [arXiv:2107.00630](https://arxiv.org/abs/2107.00630)
- Lu et al. *DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps.* NeurIPS, 2022. [arXiv:2206.00927](https://arxiv.org/abs/2206.00927)
- Rafailov et al. *Direct Preference Optimization: Your Language Model is Secretly a Reward Model.* NeurIPS, 2023. [arXiv:2305.18290](https://arxiv.org/abs/2305.18290)
- Wallace et al. *Diffusion Model Alignment Using Direct Preference Optimization.* arXiv, 2023. [arXiv:2311.12908](https://arxiv.org/abs/2311.12908)
- Lu et al. *InPO: Inversion Preference Optimization with Reparametrized DDIM for Efficient Diffusion Model Alignment.* arXiv, 2025. [arXiv:2503.18454](https://arxiv.org/abs/2503.18454)
- Lu et al. *Smoothed Preference Optimization via ReNoise Inversion for Aligning Diffusion Models with Varied Human Preferences.* arXiv, 2025. [arXiv:2506.02698](https://arxiv.org/abs/2506.02698)

### Score

- Hyvärinen. *Estimation of Non-Normalized Statistical Models by Score Matching.* JMLR, 2005.
- Vincent. *A Connection Between Score Matching and Denoising Autoencoders.* Neural Computation, 2011.
- Song, Ermon. *Generative Modeling by Estimating Gradients of the Data Distribution.* NeurIPS, 2019. [arXiv:1907.05600](https://arxiv.org/abs/1907.05600)
- Song et al. *Score-Based Generative Modeling through Stochastic Differential Equations.* ICLR, 2021. [arXiv:2011.13456](https://arxiv.org/abs/2011.13456)
- Karras et al. *Elucidating the Design Space of Diffusion-Based Generative Models.* NeurIPS, 2022. [arXiv:2206.00364](https://arxiv.org/abs/2206.00364)

### Flow

- Liu, Gong, Liu. *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow.* ICLR, 2023. [arXiv:2209.03003](https://arxiv.org/abs/2209.03003)
- Lipman et al. *Flow Matching for Generative Modeling.* ICLR, 2023. [arXiv:2210.02747](https://arxiv.org/abs/2210.02747)
- Yin et al. *One-step Diffusion with Distribution Matching Distillation.* CVPR, 2024. [arXiv:2311.18828](https://arxiv.org/abs/2311.18828)
- Lipman et al. *Flow Matching Guide and Code.* arXiv, 2024. [arXiv:2412.06264](https://arxiv.org/abs/2412.06264)
- Lu et al. *Reward Forcing: Efficient Streaming Video Generation with Rewarded Distribution Matching Distillation.* arXiv, 2025. [arXiv:2512.04678](https://arxiv.org/abs/2512.04678)
- Lu et al. *Offline Preference Optimization for Rectified Flow with Noise-Tracked Pairs.* arXiv, 2026. [arXiv:2605.09433](https://arxiv.org/abs/2605.09433)

### SDE

- Anderson. *Reverse-time diffusion equation models.* Stochastic Processes and their Applications, 1982.

### Networks

- Ronneberger, Fischer, Brox. *U-Net: Convolutional Networks for Biomedical Image Segmentation.* MICCAI, 2015. [arXiv:1505.04597](https://arxiv.org/abs/1505.04597)
- Salimans et al. *PixelCNN++: Improving the PixelCNN with Discretized Logistic Mixture Likelihood and Other Modifications.* ICLR, 2017. [arXiv:1701.05517](https://arxiv.org/abs/1701.05517)
- Vaswani et al. *Attention Is All You Need.* NeurIPS, 2017. [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Wu, He. *Group Normalization.* ECCV, 2018. [arXiv:1803.08494](https://arxiv.org/abs/1803.08494)

### Reinforcement Learning

- Sutton et al. *Policy Gradient Methods for Reinforcement Learning with Function Approximation.* NeurIPS, 1999.
- Konda, Tsitsiklis. *Actor-Critic Algorithms.* NeurIPS, 1999.
- Schulman et al. *Proximal Policy Optimization Algorithms.* arXiv, 2017. [arXiv:1707.06347](https://arxiv.org/abs/1707.06347)
