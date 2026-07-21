# PDE Dataset Docs

Bilingual (中文 / English) documentation for scientific ML / CFD benchmarks, structured like [The Well](https://polymathic-ai.org/the_well/datasets/acoustic_scattering_discontinuous/).

**Datasets:** The Well · CFDBench · FlowBench · PDEArena · PDEBench · PDEgym

- **Site:** https://gimmnm.github.io/
- **Stack:** [Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod) + [KaTeX](https://katex.org/)

## Local preview

```bash
make serve
```

Open http://localhost:1313 (Chinese) or http://localhost:1313/en/ (English).  
Use the language switch next to the theme toggle to jump to the matching translation.

## Re-import source Markdown

```bash
python3 scripts/import_dataset_docs.py
```

Source packages at repo root (`*_markdown_docs*`, `the_well_markdown_docs/`) are copied into `content/zh-cn/datasets/` and `content/en/datasets/`.

## Deploy

Push to `main`. GitHub Actions publishes automatically.
