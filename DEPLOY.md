# 部署说明（必读）

## 为什么首页像 README？

如果打开 https://gimmnm.github.io/ 看到的是 README 文字，说明 **GitHub Pages 还在用仓库根目录的 Markdown**，没有跑 Hugo 构建。

## 正确设置（只需做一次）

1. 打开：https://github.com/Gimmnm/Gimmnm.github.io/settings/pages

2. **Build and deployment → Source** 选 **GitHub Actions**  
   （不要选 "Deploy from a branch"）

3. 打开：https://github.com/Gimmnm/Gimmnm.github.io/actions

4. 左侧点 **Deploy Hugo site to GitHub Pages** → 右上角 **Run workflow** → **Run workflow**

5. 等 1～2 分钟，工作流出现绿色 ✓ 后，再访问：
   - 首页：https://gimmnm.github.io/
   - 文章：https://gimmnm.github.io/posts/basic-diffusion-model/

## 以后更新博客

```bash
git add .
git commit -m "update post"
git push
```

每次 push 到 `main` 会自动重新部署。

## 本地预览（不依赖 GitHub）

```bash
cd ~/Documents/Gimmnm.github.io
make serve
```

浏览器打开 http://localhost:1313
