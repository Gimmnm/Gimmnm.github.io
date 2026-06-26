# Gzh' Blog

Personal learning notes on machine learning, mathematics, and related topics.

- **Site:** https://gimmnm.github.io/
- **Stack:** [Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod) + [KaTeX](https://katex.org/)

Posts may be written in **English** or **中文** — no paired translations required.

## Local preview

```bash
make serve
```

Open http://localhost:1313

## Write a new post

```bash
hugo new content posts/my-topic.md
```

**Math:** inline `$E=mc^2$`; multi-line display formulas use `{{% mathdisplay %}}` … `{{% /mathdisplay %}}`.

## Deploy

Push to `main` on `Gimmnm/Gimmnm.github.io`. GitHub Actions publishes automatically.

Ensure **Settings → Pages → Source** is **GitHub Actions**.
