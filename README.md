# Simulation Engineer Portfolio — Monolume-inspired

A ready-to-deploy engineering portfolio site with big Monolume-style typography, pale-lime accents, illustrative scientific visuals, and detailed research project pages.

**Live source inspiration:** [Monolume by Mahesh Odedara](https://github.com/heshify/monolume) — MIT-licensed. This deliverable is an original, simplified static adaptation, **not a copy of the original Astro repository**. MIT notice is preserved in `LICENSE-MONOLUME`.

## What is inside

- `docs/index.html` — homepage: hero, selected work, expertise, about, contact
- `docs/projects/*/index.html` — 3 case-study pages
- `docs/resume/index.html` — editable CV overview and optional PDF link
- `docs/assets/img/*` — original schematic SVG illustrations (not real simulation results)
- `src/site.json` — your name, email, GitHub, LinkedIn, about text, etc.
- `src/projects.json` — featured projects, titles, methods, and captions
- `build.py` — regenerate the complete site with the Python standard library
- `assets/css/style.css` — color, typography, spacing, and mobile layout
- `assets/js/main.js` — mobile navigation and small interactive effects
- `.github/workflows/site-check.yml` — basic checks on GitHub pushes

**No Node.js, Astro installation, npm packages, back-end, database, or hosting plan are required.** Everything in `docs/` is fully static.

## Quick start (中文)

### 1. 修改个人资料

编辑 `src/site.json`，至少替换：

| 字段 | 填写内容 |
| --- | --- |
| `name` | 你的英文姓名 |
| `initials` | 左上角的缩写，例如 `LL.` |
| `email` | 你的真实邮箱 |
| `github` | 你的 GitHub Profile 地址 |
| `linkedin` | 你的 LinkedIn Profile 地址 |
| `site_url` | 上线后的网站地址，例如 `https://YOUR_USERNAME.github.io` |
| `resume_pdf` | 可选：`assets/files/resume.pdf`（将 PDF 放到项目的 `assets/files/`） |

`src/projects.json` 可以修改 3 个示例项目的文字、研究方法和内容。建议将图片换成经过验证的实际模拟结果。**目前的 SVG 均是艺术化示意图，不是真实计算结果。**

### 2. 重新生成网页

在项目根目录运行：

```bash
python build.py
```

如果你使用 Windows，也可能需要运行：

```powershell
py build.py
```

生成后的文件位于 `docs/`，浏览器打开 `docs/index.html` 就能本地预览。

### 3. 创建 GitHub Pages 网站

1. 登录 GitHub，点击 **New repository**。
2. 新建公开仓库，名字必须为 **`YOUR_USERNAME.github.io`**（把 `YOUR_USERNAME` 换成你自己的 GitHub 用户名）。
3. 将这个项目的所有文件上传或 Git push 到仓库 `main` 分支。
4. 进入 **Settings → Pages → Build and deployment**。
5. **Source** 选择 `Deploy from a branch`；**Branch** 选择 `main`；**Folder** 选择 `/docs`，点击 **Save**。
6. 等待 Pages 部署完成，然后打开 `https://YOUR_USERNAME.github.io/`。

注意：GitHub Pages 在**仓库根目录**寻找 `docs`，所以不要只上传 `docs` 内的文件却同时把 Pages Folder 设为 `/docs`。

### 4. 命令行上传（可选）

先在 GitHub 创建好空仓库，并在本机安装 Git，然后在本项目文件夹运行：

```bash
git init
git add .
git commit -m "Add engineering portfolio"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_USERNAME.github.io.git
git push -u origin main
```

以后更新内容：编辑 JSON → `python build.py` → `git add .` → `git commit` → `git push`。

## CV PDF

目前 Resume 页面是**文字版占位介绍**，并不冒充你的正式简历。如果你想展示 PDF：

1. 在源文件的 `assets/` 下创建 `files/` 文件夹，把真实 CV 命名为 `resume.pdf` 放到 `assets/files/resume.pdf`。
2. 在 `src/site.json` 将 `resume_pdf` 改成 `assets/files/resume.pdf`。
3. 执行 `python build.py`，生成器会自动把 PDF 复制到 `docs/assets/files/resume.pdf`。下载按钮会同时出现。

## Optional styling

Open `assets/css/style.css` and edit these CSS variables near the top:

```css
--bg: #f7f7f1;
--ink: #151a18;
--lime: #c8f777;
--dark: #111b19;
```

Regenerate with `python build.py`. The SVG illustrations have their own local colors; modify `generate_art.py`, run `python generate_art.py`, then `python build.py` to regenerate them.

## Quality & scope

- Responsive desktop, tablet and mobile layouts
- Accessible mobile menu with Escape support and reduced-motion settings
- Local assets only; no dependence on Google Fonts or remote image hosts
- No contact form back-end: the contact action intentionally uses `mailto:`
- Projects are research **drafts**; replace methods/descriptions with your own verified information
- No fake publications, employers, awards, numeric research results, or code repositories
- All example personal links remain placeholders until updated

## Credit

Original visual inspiration: [Monolume](https://github.com/heshify/monolume), © 2025 Mahesh Odedara, MIT License (see `LICENSE-MONOLUME`). This project is an independently written static site, keeping the recognizable oversized typography and bright accent while adding original scientific artwork and engineering-focused case pages.
