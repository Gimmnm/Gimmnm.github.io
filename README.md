# Gzh' Blog

Personal learning notes on machine learning, mathematics, and related topics.

- **Site:** https://gimmnm.github.io/
- **Stack:** [Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod) + [KaTeX](https://katex.org/)
- **Languages:** English & 中文

## Local preview

```bash
make serve
# or: hugo server -D
```

Open http://localhost:1313

## Build

```bash
make build
make deploy-check   # verify KaTeX is in output
```

## Write a new post

```bash
# English (default)
hugo new content posts/my-topic.md

# Chinese
hugo new content zh/posts/my-topic.md
```

Use the same `translationKey` in both files to link translations.

**Math:** inline `$E=mc^2$`, display:

```markdown
$$
\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\,\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\,\boldsymbol{\epsilon}
$$
```

## Deploy

Push to `main` on `Gimmnm/Gimmnm.github.io`. GitHub Actions publishes automatically.

```bash
git add .
git commit -m "your message"
git push
```

Ensure **Settings → Pages → Source** is **GitHub Actions**.

## Style notes

- **Lil'Log-inspired:** clean post cards, welcome banner, tags/archive/search
- **Terence Tao-inspired:** serif body text, generous line height, understated meta
