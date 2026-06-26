# Gzh' Blog

Personal learning notes on machine learning, mathematics, and related topics.

- **Site:** https://gimnnm.github.io/
- **Stack:** [Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod)
- **Languages:** English & 中文

## Local preview

```bash
hugo server -D
```

Open http://localhost:1313

## Write a new post

```bash
# English
hugo new content en/posts/my-post.md

# Chinese
hugo new content zh/posts/my-post.md
```

Link translations with the same `translationKey` in front matter.

## Deploy

Push to `main` on the `Gimnnm/Gimnnm.github.io` repository. GitHub Actions builds and publishes automatically.

### First-time GitHub setup

1. Create a new repository named **`Gimnnm.github.io`** on GitHub (must match your username).
2. Push this folder:

```bash
git remote add origin git@github.com:Gimnnm/Gimnnm.github.io.git
git add .
git commit -m "Initial blog setup with Hugo and PaperMod"
git push -u origin main
```

3. In repo **Settings → Pages**, set Source to **GitHub Actions**.

## Theme

PaperMod lives in `themes/PaperMod`. To update:

```bash
cd themes/PaperMod && git pull
```
