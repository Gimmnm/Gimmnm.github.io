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

我读了DDPM论文里的一些表述习惯，才渐渐习惯理解信息论的视角看概率。比如，作者在表示，如果将训练目标改为$L_1$（这实际上是DDIM论文中的写法）后，虽然没有特别好的likelihood，也就是codelength没有压缩到最好，但是观察codelength的分布，发现超过一半的bits都用在最后一步上，从实际效果来看，生成质量反而是最好的，所以启发我们在图片生成的时候likelihood不一定是唯一的目标，codelength的分布可能也有用？

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

## References

- Author. *Paper title.* Venue, year. [link]()
- Add papers as you read them

