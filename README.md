# Siyuan Liu — Academic Research Portfolio (Soft Scientific · C)

A simple, light-weight academic homepage with a **Soft Scientific (C)** color palette (pale blue, mint and soft yellow), organized in the style of **[Yalin Yang's website](https://gisyaliny.github.io/)**: one-page research profile + separate documentation-style Projects and Notes.

**This is a new site.** No Monolume files, CSS, scripts, imagery, or design components are included. The implementation is original HTML/CSS/JavaScript; no Yalin website code or image assets are copied.

## Pages

- `docs/index.html`: Home, About, Research & Knowledge Base, Selected Research, Publications, Contact
- `docs/projects/index.html`: project index
- `docs/projects/*/index.html`: four research/project detail pages
- `docs/notes/index.html`: technical note index
- `docs/notes/*/index.html`: four short technical notes
- `docs/404.html`: fallback
- `docs/.nojekyll`: disables Jekyll transformations for static files

## How to edit

All profile text is in `content/site.json`.

- `name`, `role`, `hero_title`, `hero_subtitle`, `about`: homepage profile
- `research_background`: points shown under About Me
- `github`, `linkedin`, `email`: personal links (empty values hide the link)
- `cv_pdf`: path to an actual PDF, e.g. `files/CV.pdf` (PDF must exist under the source directory; then run `build.py`)
- `publications`: list of verified articles; each entry can have `authors`, `year`, `title`, `venue`, `url`

Project entries and links: `content/projects.json`.
Technical notes: `content/notes.json`.
CSS: `source/assets/css/style.css` (Viridis A palette overrides are at the end; edit them for further color tuning).

**IMPORTANT:** The scientific images in `source/assets/img/` are original **schematic illustrations**, not numerical solutions or experimental evidence. Replace with your own real plots, results, and/or photos as appropriate.

## Rebuild

Python 3 is sufficient; no external packages or web connection are required.

```sh
python build.py
```

The builder removes and recreates `docs/` every time. It does not carry forward previous webpage versions.

Open `docs/index.html` in a web browser to preview locally. The final static site can be hosted from the `/docs` directory using GitHub Pages.

## Note about CV, publications and affiliations

Only topics consistent with the known research profile are prefilled. **No institution, degree completion, teaching appointment, paper title or DOI has been invented.** A placeholder is used instead of an unprovided portrait. The formal publication list is intentionally empty until you provide it. If you provide your own CV, images and paper list, they can be inserted directly.

## Hosting

For username `liusiyuan588`, use the repo `liusiyuan588/liusiyuan588.github.io` and Pages setting `Deploy from a branch → main → /docs`. The URL is `https://liusiyuan588.github.io/` after deployment.
