#!/usr/bin/env python3
"""Import bilingual dataset Markdown into Hugo contentDirs.

Produces:
  content/zh-cn/datasets/...
  content/en/datasets/...

Sources:
  CFDBench, FlowBench, PDEArena, PDEBench, PDEgym, The Well
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_raw, body = parts[1], parts[2]
    fm: dict = {}
    for line in fm_raw.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            fm[k] = [] if not inner else [x.strip().strip("\"'") for x in inner.split(",")]
        elif v.lower() in ("true", "false"):
            fm[k] = v.lower() == "true"
        elif (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            fm[k] = v[1:-1]
        else:
            try:
                fm[k] = int(v)
            except ValueError:
                try:
                    fm[k] = float(v)
                except ValueError:
                    fm[k] = v
    return fm, body.lstrip("\n")


def fmt_value(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(f'"{x}"' for x in v) + "]"
    s = str(v)
    if any(c in s for c in ":#[]{}'\"\n") or s == "" or " " in s:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def normalize_bold(text: str) -> str:
    text = re.sub(r"\*\*[ \t]+([^*\n]+?)\*\*", r"**\1**", text)
    text = re.sub(r"([：:])\*\*(?=\S)", r"\1 **", text)
    text = re.sub(r"\*\*([^*]*?[：:。．])\*\*(?=\S)", r"**\1** ", text)
    return text


def dump_page(path: Path, fm: dict, body: str, link_fix=None) -> None:
    body2 = body
    if link_fix:
        for pat, repl in link_fix:
            body2 = re.sub(pat, repl, body2)
    body2 = re.sub(r" \\n  ", " \\\n  ", body2)
    body2 = normalize_bold(body2)
    # Drop source language key to avoid confusing Hugo
    fm = {k: v for k, v in fm.items() if k not in {"language", "slug"} and v is not None}
    lines = ["---"] + [f"{k}: {fmt_value(v)}" for k, v in fm.items()] + ["---"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n\n" + body2.lstrip("\n"), encoding="utf-8")


def sibling_link_fix(files: list[str]) -> list[tuple[str, str]]:
    fixes = []
    for other in files:
        stem = Path(other).stem
        fixes.append((rf"\]\({re.escape(other)}\)", f"](../{stem}/)"))
        fixes.append((rf"\]\(\./{re.escape(other)}\)", f"](../{stem}/)"))
        fixes.append((rf"\]\({re.escape(stem)}\)", f"](../{stem}/)"))
    return fixes


def family_defs() -> list[dict]:
    pdegym_files = [
        "01_ns-sines.md", "02_ns-gauss.md", "03_ce-rp.md", "04_ce-crp.md", "05_ce-kh.md",
        "06_ce-gauss.md", "07_ns-pwc.md", "08_ns-bb.md", "09_ns-sl.md", "10_ns-svs.md",
        "11_ns-tracer-pwc.md", "12_fns-kf.md", "13_ce-rpui.md", "14_ce-rm.md", "15_gce-rt.md",
        "16_wave-gauss.md", "17_wave-layer.md", "18_ace.md", "19_se-af.md", "20_poisson-gauss.md",
        "21_helmholtz.md",
    ]
    well_files = sorted(p.name for p in (ROOT / "the_well_markdown_docs" / "en").glob("*.md"))

    return [
        {
            "slug": "the-well",
            "title": {"zh-cn": "The Well", "en": "The Well"},
            "weight": 5,
            "summary": {
                "zh-cn": "Polymathic AI 的大规模多物理场 PDE 基准，覆盖声学、流体、MHD、超新星等场景。",
                "en": "Polymathic AI's large-scale multi-physics PDE benchmark spanning acoustics, fluids, MHD, supernovae, and more.",
            },
            "src": {"zh-cn": ROOT / "the_well_markdown_docs" / "zh-CN", "en": ROOT / "the_well_markdown_docs" / "en"},
            "index": {"zh-cn": ROOT / "the_well_markdown_docs" / "README.zh-CN.md", "en": ROOT / "the_well_markdown_docs" / "README.md"},
            "files": well_files,
            "extra_link_fix": {
                "zh-cn": [(rf"\]\({re.escape(f)}\)", f"](../{Path(f).stem}/)") for f in well_files]
                + [(rf"\]\(zh-CN/{re.escape(f)}\)", f"](../{Path(f).stem}/)") for f in well_files],
                "en": [(rf"\]\({re.escape(f)}\)", f"](../{Path(f).stem}/)") for f in well_files]
                + [(rf"\]\(en/{re.escape(f)}\)", f"](../{Path(f).stem}/)") for f in well_files],
            },
        },
        {
            "slug": "cfdbench",
            "title": {"zh-cn": "CFDBench", "en": "CFDBench"},
            "weight": 10,
            "summary": {
                "zh-cn": "二维不可压缩 Navier–Stokes 的四种典型 CFD 工况：方腔、圆管、溃坝越障与圆柱绕流。",
                "en": "Four classic 2D incompressible Navier–Stokes CFD setups: cavity, tube, dam, and cylinder flow.",
            },
            "src": {"zh-cn": ROOT / "CFDBench_markdown_docs" / "zh-CN", "en": ROOT / "CFDBench_markdown_docs" / "en"},
            "index": {
                "zh-cn": ROOT / "CFDBench_markdown_docs" / "zh-CN" / "README.md",
                "en": ROOT / "CFDBench_markdown_docs" / "en" / "README.md",
            },
            "files": ["cavity_flow.md", "tube_flow.md", "dam_flow.md", "cylinder_flow.md"],
        },
        {
            "slug": "flowbench",
            "title": {"zh-cn": "FlowBench", "en": "FlowBench"},
            "weight": 20,
            "summary": {
                "zh-cn": "复杂几何上流场模拟大规模基准，覆盖二维/三维顶盖驱动与瞬态 FPO 等配置。",
                "en": "Large-scale flow-over-complex-geometry benchmark with 2D/3D lid-driven cavity and transient FPO setups.",
            },
            "src": {"zh-cn": ROOT / "FlowBench_markdown_docs" / "zh", "en": ROOT / "FlowBench_markdown_docs" / "en"},
            "index": {
                "zh-cn": ROOT / "FlowBench_markdown_docs" / "zh" / "README.md",
                "en": ROOT / "FlowBench_markdown_docs" / "en" / "README.md",
            },
            "files": [
                "01_ldc_ns_2d.md", "02_ldc_nsht_2d_constant_re.md", "03_ldc_nsht_2d_variable_re.md",
                "04_fpo_ns_2d.md", "05_ldc_ns_3d.md",
            ],
        },
        {
            "slug": "pdearena",
            "title": {"zh-cn": "PDEArena", "en": "PDEArena"},
            "weight": 30,
            "summary": {
                "zh-cn": "面向算子学习的 PDE 基准：Navier–Stokes、浅水方程、Maxwell-3D 与 KS 等。",
                "en": "Operator-learning PDE benchmark covering Navier–Stokes, shallow water, Maxwell-3D, and KS.",
            },
            "src": {
                "zh-cn": ROOT / "PDEArena_markdown_docs_bilingual" / "zh",
                "en": ROOT / "PDEArena_markdown_docs_bilingual" / "en",
            },
            "index": {
                "zh-cn": ROOT / "PDEArena_markdown_docs_bilingual" / "zh" / "README.md",
                "en": ROOT / "PDEArena_markdown_docs_bilingual" / "en" / "README.md",
            },
            "files": [
                "navier_stokes_2d_standard.md", "navier_stokes_2d_conditioned.md",
                "shallow_water_2d_velocity.md", "shallow_water_2d_vorticity.md",
                "maxwell_3d.md", "kuramoto_sivashinsky_1d.md",
            ],
        },
        {
            "slug": "pdebench",
            "title": {"zh-cn": "PDEBench", "en": "PDEBench"},
            "weight": 40,
            "summary": {
                "zh-cn": "广泛使用的科学机器学习基准，覆盖 1D–3D 平流、扩散、浅水与可压缩/不可压流体等 11 类任务。",
                "en": "Widely used scientific ML benchmark with 11 1D–3D tasks spanning advection, diffusion, shallow water, and fluids.",
            },
            "src": {
                "zh-cn": ROOT / "PDEBench_markdown_docs_bilingual" / "zh",
                "en": ROOT / "PDEBench_markdown_docs_bilingual" / "en",
            },
            "index": {
                "zh-cn": ROOT / "PDEBench_markdown_docs_bilingual" / "zh" / "README.md",
                "en": ROOT / "PDEBench_markdown_docs_bilingual" / "en" / "README.md",
            },
            "files": [
                "01_advection_1d.md", "02_burgers_1d.md", "03_reaction_diffusion_1d.md",
                "04_diffusion_sorption_1d.md", "05_reaction_diffusion_2d.md", "06_darcy_flow_2d.md",
                "07_shallow_water_2d.md", "08_compressible_ns_1d.md", "09_compressible_ns_2d.md",
                "10_compressible_ns_3d.md", "11_incompressible_ns_2d.md",
            ],
        },
        {
            "slug": "pdegym",
            "title": {"zh-cn": "PDEgym", "en": "PDEgym"},
            "weight": 50,
            "summary": {
                "zh-cn": "ETH CAMLab 的预训练与下游算子学习任务集合，覆盖不可压/可压缩流体、波动与椭圆方程等。",
                "en": "ETH CAMLab pretraining and downstream operator-learning tasks across fluids, waves, and elliptic PDEs.",
            },
            "src": {"zh-cn": ROOT / "PDEgym_markdown_docs" / "zh-CN", "en": ROOT / "PDEgym_markdown_docs" / "en"},
            "index": {
                "zh-cn": ROOT / "PDEgym_markdown_docs" / "README_zh-CN.md",
                "en": ROOT / "PDEgym_markdown_docs" / "README_en.md",
            },
            "files": pdegym_files,
            "extra_link_fix": {
                "zh-cn": [(rf"\]\(zh-CN/{re.escape(f)}\)", f"](../{Path(f).stem}/)") for f in pdegym_files],
                "en": [(rf"\]\(en/{re.escape(f)}\)", f"](../{Path(f).stem}/)") for f in pdegym_files],
            },
        },
    ]


OVERVIEW = {
    "zh-cn": """# 数据集总览

本站整理科学机器学习 / CFD 基准数据介绍。每个 benchmark 下按方程或问题配置分页。

| 数据集 | 简介 |
|---|---|
| [The Well](the-well/) | Polymathic AI 多物理场 PDE 基准 |
| [CFDBench](cfdbench/) | 二维不可压缩 NS 的四种典型 CFD 工况 |
| [FlowBench](flowbench/) | 复杂几何上流场模拟大规模基准 |
| [PDEArena](pdearena/) | 算子学习 PDE 基准 |
| [PDEBench](pdebench/) | 广泛使用的 1D–3D PDE 科学 ML 基准 |
| [PDEgym](pdegym/) | 预训练与下游算子学习任务集合 |

字段包括一句话描述、控制方程、About the data、初边值、参数扫描、下载等。
""",
    "en": """# Datasets overview

Documentation for scientific ML / CFD benchmarks.

| Dataset | Summary |
|---|---|
| [The Well](the-well/) | Polymathic AI multi-physics PDE benchmark |
| [CFDBench](cfdbench/) | Four classic 2D incompressible NS CFD setups |
| [FlowBench](flowbench/) | Large-scale flow over complex geometries |
| [PDEArena](pdearena/) | Operator-learning PDE benchmark |
| [PDEBench](pdebench/) | Widely used 1D–3D scientific ML PDE benchmark |
| [PDEgym](pdegym/) | Pretraining and downstream operator-learning tasks |

Each page covers a one-line description, governing equations, about-the-data fields, ICs/BCs, parameter sweeps, and download.
""",
}


def short_link_title(lang: str, fam_title: str, fname: str, title: str) -> str:
    stem = Path(fname).stem
    # Prefer compact labels in sidebar
    if fam_title == "The Well":
        return stem
    if fam_title == "CFDBench":
        return {
            "cavity_flow": "Cavity Flow",
            "tube_flow": "Tube Flow",
            "dam_flow": "Dam Flow",
            "cylinder_flow": "Cylinder Flow",
        }.get(stem, title)
    if fam_title == "FlowBench":
        return {
            "01_ldc_ns_2d": "LDC NS 2D",
            "02_ldc_nsht_2d_constant_re": "LDC NSHT 2D (const Re)",
            "03_ldc_nsht_2d_variable_re": "LDC NSHT 2D (var Re)",
            "04_fpo_ns_2d": "FPO NS 2D",
            "05_ldc_ns_3d": "LDC NS 3D",
        }.get(stem, title)
    if fam_title == "PDEArena":
        return {
            "navier_stokes_2d_standard": "NS-2D Standard",
            "navier_stokes_2d_conditioned": "NS-2D Conditioned",
            "shallow_water_2d_velocity": "Shallow Water (velocity)",
            "shallow_water_2d_vorticity": "Shallow Water (vorticity)",
            "maxwell_3d": "Maxwell-3D",
            "kuramoto_sivashinsky_1d": "KS-1D",
        }.get(stem, title)
    if fam_title == "PDEBench":
        return re.sub(r"^\d+_", "", stem).replace("_", " ")
    if fam_title == "PDEgym":
        short = title.split("：")[0].split(":")[0].strip()
        return short or stem
    return title


def write_home_and_hidden_posts(lang: str) -> None:
    out = ROOT / "content" / lang
    out.mkdir(parents=True, exist_ok=True)
    (out / "posts").mkdir(parents=True, exist_ok=True)
    if lang == "zh-cn":
        dump_page(out / "_index.md", {"title": "首页"}, "")
        (out / "posts" / "_index.md").write_text(
            """---
title: Posts
draft: true
build:
  list: never
  render: never
cascade:
  draft: true
  build:
    list: never
    render: never
---

博客文章暂时隐藏。
""",
            encoding="utf-8",
        )
    else:
        dump_page(out / "_index.md", {"title": "Home"}, "")
        (out / "posts" / "_index.md").write_text(
            """---
title: Posts
draft: true
build:
  list: never
  render: never
cascade:
  draft: true
  build:
    list: never
    render: never
---

Blog posts are temporarily hidden.
""",
            encoding="utf-8",
        )


def import_lang(lang: str) -> int:
    out = ROOT / "content" / lang / "datasets"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    n = 0
    families = family_defs()

    for fam in families:
        dest = out / fam["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        idx_path = fam["index"][lang]
        fm, body = parse_frontmatter(idx_path.read_text(encoding="utf-8"))
        fm.update(
            {
                "title": fm.get("title") or (
                    f"{fam['title'][lang]} 数据文档" if lang == "zh-cn" else f"{fam['title'][lang]} documentation"
                ),
                "linkTitle": fam["title"][lang],
                "weight": fam["weight"],
                "draft": False,
                "ShowToc": True,
                "hidemeta": True,
                "ShowPostNavLinks": False,
                "hiddenInHomeList": True,
                "summary": fam["summary"][lang],
                "dataset_family": fam["title"][lang],
            }
        )
        link_fix = sibling_link_fix(fam["files"]) + list((fam.get("extra_link_fix") or {}).get(lang, []))
        dump_page(dest / "_index.md", fm, body, link_fix)
        n += 1

        for i, fname in enumerate(fam["files"], start=1):
            src = fam["src"][lang] / fname
            if not src.exists():
                print(f"WARN missing {src}")
                continue
            fm, body = parse_frontmatter(src.read_text(encoding="utf-8"))
            title = fm.get("title") or Path(fname).stem
            fm.update(
                {
                    "title": title,
                    "linkTitle": short_link_title(lang, fam["title"][lang], fname, str(title)),
                    "weight": i * 10,
                    "draft": False,
                    "ShowToc": True,
                    "TocOpen": True,
                    "hidemeta": True,
                    "ShowBreadCrumbs": True,
                    "ShowPostNavLinks": True,
                    "math": True,
                    "hiddenInHomeList": True,
                    "dataset_family": fam["title"][lang],
                }
            )
            dump_page(dest / fname, fm, body, sibling_link_fix(fam["files"]))
            n += 1

    # overview
    overview_path = out / "_index.md"
    dump_page(
        overview_path,
        {
            "title": "Datasets" if lang == "en" else "数据集",
            "weight": 1,
            "draft": False,
            "ShowToc": False,
            "hidemeta": True,
            "ShowPostNavLinks": False,
            "summary": "Dataset documentation overview." if lang == "en" else "科学机器学习基准数据集文档总览。",
        },
        OVERVIEW[lang],
    )
    text = overview_path.read_text(encoding="utf-8")
    text = text.replace(
        "---\n\n#",
        "cascade:\n  type: datasets\n  hiddenInHomeList: true\n---\n\n#",
        1,
    )
    overview_path.write_text(text, encoding="utf-8")
    n += 1
    return n


def main() -> None:
    # Remove legacy single-lang datasets tree
    legacy = ROOT / "content" / "datasets"
    if legacy.exists():
        shutil.rmtree(legacy)

    # Clean language content dirs (keep nothing stale)
    for lang in ("zh-cn", "en"):
        d = ROOT / "content" / lang
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)

    # Hide root-level blog leftovers if present
    for name in ("about.md", "faq.md", "search.md", "_index.md"):
        p = ROOT / "content" / name
        if p.exists():
            p.unlink()
    posts = ROOT / "content" / "posts"
    if posts.exists():
        shutil.rmtree(posts)
    for empty in ("content/zh",):
        p = ROOT / empty
        # leave if needed; zh was old empty

    total = 0
    for lang in ("zh-cn", "en"):
        write_home_and_hidden_posts(lang)
        total += import_lang(lang)
        print(f"{lang}: imported")

    print(f"done, {total} dataset pages/indexes written")


if __name__ == "__main__":
    main()
