#!/usr/bin/env python3
"""Generate a GitHub Pages-ready static portfolio from src/*.json.

Usage: python build.py
No external Python / JavaScript packages required.
"""
from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from urllib.parse import quote

BASE = Path(__file__).resolve().parent
DEST = BASE / 'docs'
site = json.loads((BASE / 'src' / 'site.json').read_text(encoding='utf-8'))
projects = json.loads((BASE / 'src' / 'projects.json').read_text(encoding='utf-8'))
by_slug = {p['slug']: p for p in projects}


def e(value):
    return html.escape(str(value), quote=True)


def tags(items):
    return '<div class="tags">' + ''.join(f'<span class="tag">{e(t)}</span>' for t in items) + '</div>'


def logo():
    return f'<span class="brand-icon" aria-hidden="true">{e(site["initials"][:2])}</span><span>{e(site["name"])}</span>'


def head(title: str, description: str, root: str, path: str):
    url = site.get('site_url', '').rstrip('/')
    canonical = f'<link rel="canonical" href="{e(url + path)}" />' if url else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="theme-color" content="#f7f7f1" />
<meta name="color-scheme" content="light" />
<meta name="description" content="{e(description)}" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{e(title)}" />
<meta property="og:description" content="{e(description)}" />
{canonical}
<title>{e(title)}</title>
<link rel="icon" type="image/svg+xml" href="{root}assets/img/favicon.svg" />
<link rel="stylesheet" href="{root}assets/css/style.css" />
<script defer src="{root}assets/js/main.js"></script>
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>'''


def header(root: str, current=''):
    nav = [('Work', f'{root}#work', 'work'), ('Expertise', f'{root}#expertise', 'expertise'),
           ('About', f'{root}#about', 'about'), ('Resume', f'{root}resume/', 'resume')]
    links = ''.join(f'<a href="{h}"'+(' aria-current="page"' if current==key else '')+f'>{label}</a>' for label,h,key in nav)
    return f'''
<header class="site-header">
  <div class="scroll-progress" aria-hidden="true"></div>
  <div class="container">
    <a class="brand" href="{root}" aria-label="{e(site['name'])} — home">{logo()}</a>
    <nav class="header-nav" aria-label="Primary navigation">{links}</nav>
    <a class="header-cta" href="{root}#contact">LET'S CONNECT <span aria-hidden="true">↗</span></a>
    <button class="menu-toggle" data-menu-toggle aria-expanded="false" aria-controls="mobile-navigation" aria-label="Open navigation menu"><i></i><i></i><i></i></button>
  </div>
  <nav id="mobile-navigation" class="mobile-nav" data-mobile-nav aria-label="Mobile navigation">{links}<a href="{root}#contact">CONTACT ↗</a><small>ENGINEERING / RESEARCH / COMPUTATION</small></nav>
</header>'''


def footer(root):
    return f'''
<footer class="site-footer">
<div class="container">
 <div class="footer-main">
   <div><div class="footer-monogram">{e(site['initials'])}</div><p>COMPUTATIONAL MECHANICS<br/>MODEL / SIMULATE / UNDERSTAND</p></div>
   <div><div class="footer-heading">NAVIGATE</div><a href="{root}#work">Selected work ↗</a><a href="{root}#expertise">Expertise ↗</a><a href="{root}#about">About ↗</a><a href="{root}resume/">Resume ↗</a></div>
   <div><div class="footer-heading">CONNECT</div><a target="_blank" rel="noopener noreferrer" href="{e(site['github'])}">GitHub ↗</a><a target="_blank" rel="noopener noreferrer" href="{e(site['linkedin'])}">LinkedIn ↗</a><a href="mailto:{e(site['email'])}">Email ↗</a></div>
 </div>
 <div class="footer-bottom"><span>© {e(site['copyright'])} {e(site['name'])}. ALL RIGHTS RESERVED.</span><span>MONOLUME-INSPIRED · ORIGINAL ADAPTATION</span><span>BUILD WITH CURIOSITY. ✳</span></div>
</div></footer></body></html>'''


def topbar(left, right):
    return f'<div class="section-topline"><span>{e(left)}</span><span>{e(right)}</span></div>'


def work_block(p):
    art = e(f"assets/img/{p['image']}")
    link = f"projects/{e(p['slug'])}/"
    return f'''
<article class="work-item reveal">
  <a class="project-art" href="{link}" aria-label="Explore {e(p['short_title'])}">
    <img src="{art}" alt="{e(p['image_alt'])}" width="1200" height="760" loading="lazy" />
    <span class="project-art-index">{e(p['number'])} / SELECTED WORK</span>
  </a>
  <div class="work-content">
    <div class="work-meta"><span>{e(p['category'])}</span><span>/{e(p['number'])}</span></div>
    <h3 class="work-heading"><a href="{link}">{e(p['short_title'])}</a></h3>
    <p class="work-copy">{e(p['subtitle'])}</p>
    {tags(p['tags'])}
    <a class="work-link" href="{link}">Explore the case <span aria-hidden="true">↗</span></a>
  </div>
</article>'''


def homepage():
    focus = ''.join(f'''<div class="focus-card reveal"><span class="num">{e(f['number'])} /</span><div><h3>{e(f['label'])}</h3><p>{e(f['detail'])}</p></div></div>''' for f in site['focus'])
    return head(f"{site['name']} — {site['title']}", site['tagline'], './', '/') + header('./') + f'''
<main id="main">
<section class="container hero" id="top">
 <div class="hero-copy">
  <div class="hero-eyebrow eyebrow"><span class="status-dot" aria-hidden="true"></span>{e(site['eyebrow'])}</div>
  <h1 class="display hero-title"><span class="line">ENGINEER</span><span class="line outlined">THE</span><span class="line">UNSEEN<span class="period">.</span></span></h1>
  <div class="hero-bottom">
   <p class="hero-desc">{e(site['tagline'])}</p>
   <div class="hero-actions"><a class="btn btn-primary" href="#work">EXPLORE PROJECTS <span class="arr" aria-hidden="true">↗</span></a><a class="btn btn-secondary" href="resume/">VIEW RESUME <span class="arr" aria-hidden="true">↗</span></a></div>
  </div>
  <div class="hero-footnote"><span>FINITE ELEMENTS / FRACTURE / MULTIPHYSICS</span><span>SCROLL TO EXPLORE ↓</span></div>
 </div>
 <div class="hero-visual">
  <div class="floating-stamp" aria-hidden="true"><div class="stamp-inside">✳<small>RESEARCH<br>DRIVEN</small></div></div>
  <div class="frame"><img src="assets/img/hero-mesh.svg" width="870" height="1040" alt="Original schematic visualization of stress localization and distorted numerical mesh" /></div>
  <div class="corner-caption">A WINDOW INTO COMPLEX<br>PHYSICAL SYSTEMS / 001</div>
 </div>
</section>
<div class="ticker" aria-label="Research themes"><div class="track" aria-hidden="true"><span>FINITE ELEMENT METHOD</span><b>✳</b><span>FRACTURE & DAMAGE</span><b>✳</b><span>MULTIPHYSICS MODELING</span><b>✳</b><span>SCIENTIFIC COMPUTING</span><b>✳</b><span>FINITE ELEMENT METHOD</span><b>✳</b><span>FRACTURE & DAMAGE</span><b>✳</b><span>MULTIPHYSICS MODELING</span><b>✳</b><span>SCIENTIFIC COMPUTING</span><b>✳</b></div></div>
<section class="container work-section" id="work">
 {topbar('01 / RESEARCH & ENGINEERING', 'SELECTED STUDIES — 03')}
 <div class="section-intro reveal"><h2 class="display section-title">SELECTED<br>WORK<span style="color:#99d639">.</span></h2><p>Problems at the intersection of continuum mechanics, materials, and computation. Detailed case studies are ready for your own validated results.</p></div>
 {''.join(work_block(p) for p in projects)}
 <div class="view-all">↳ THREE FEATURED RESEARCH AREAS · MORE CAN BE ADDED IN src/projects.json</div>
</section>
<section class="focus-section" id="expertise">
 <div class="container">
 {topbar('02 / TOOLKIT & THINKING', 'WHAT I WORK ON')}
 <h2 class="display section-title reveal">FROM<br>EQUATIONS<br>TO <em>INSIGHT.</em></h2>
 <div class="focus-grid">{focus}</div>
 </div>
</section>
<section class="about-section container" id="about">
 {topbar('03 / THE PERSON BEHIND THE MODELS', 'INTRODUCTION')}
 <div class="about-grid">
  <div class="reveal"><h2 class="display section-title">MORE<br>THAN<br>PRETTY<br>CONTOURS<span class="small-dot">.</span></h2></div>
  <div class="about-text reveal">
    <p>{e(site['about_p1'])}</p>
    <p>{e(site['about_p2'])}</p>
    <ul class="info-list"><li><b>ROLE</b><span>{e(site['title'])}</span></li><li><b>FOCUS</b><span>Mechanics · Materials · Computation</span></li><li><b>STATUS</b><span>{e(site['location'])}</span></li></ul>
    <a class="btn btn-dark" href="resume/">MORE ABOUT ME <span class="arr" aria-hidden="true">↗</span></a>
  </div>
 </div>
</section>
<section class="contact-section" id="contact">
 <div class="container">
 {topbar('04 / OPEN A CONVERSATION','CONTACT')}
 <h2 class="display section-title reveal">LET'S<br>CONNECT<span style="color:var(--ink)">.</span></h2>
 <div class="contact-bottom"><p>Interested in simulation, advanced materials, or a challenging engineering problem? I'd love to talk.</p><a class="contact-link" href="mailto:{e(site['email'])}">{e(site['email'])} <span aria-hidden="true">↗</span></a></div>
 </div>
</section>
</main>''' + footer('./')


def case_page(p):
    root='../../'
    related=by_slug[p['related']]
    description=p['subtitle']
    approach=''.join(f'<li>{e(t)}</li>' for t in p['approach'])
    return head(f"{p['short_title']} | {site['name']}",description,root,f"/projects/{p['slug']}/") + header(root,'work') + f'''
<main id="main">
<section class="page-hero container">
  <div class="breadcrumbs"><a href="{root}">HOME</a><span>/</span><a href="{root}#work">WORK</a><span>/</span><span>STUDY {e(p['number'])}</span></div>
  <h1 class="display page-title">{e(p.get('hero_title',p['short_title']))}<span style="color:#99d639">.</span></h1>
  <p class="page-subtitle">{e(description)}</p>
  <div class="page-meta"><span>STUDY {e(p['number'])} / {e(p['category'])}</span><span>COMPUTATIONAL ENGINEERING</span><span>2026 / PROJECT OVERVIEW</span></div>
</section>
<div class="container"><div class="project-cover"><img src="{root}assets/img/{e(p['image'])}" width="1200" height="760" alt="{e(p['image_alt'])}" /></div><p class="caption">FIGURE 01 — ORIGINAL SCHEMATIC ILLUSTRATION FOR WEBSITE DESIGN. NOT A VALIDATED SIMULATION OR RESEARCH RESULT.</p></div>
<section class="container case-body">
 <aside class="case-side"><span class="mono">{e(p['category'])} / CASE {e(p['number'])}</span><h2>{e(p['short_title'])}</h2><p class="caption">PROJECT THEMES / METHODS</p>{tags(p['methods'])}</aside>
 <div class="case-main">
  <div class="case-block reveal"><h3>THE CONTEXT</h3><p>{e(p['summary'])}</p></div>
  <div class="case-block reveal"><h3>THE QUESTION</h3><p>{e(p['question'])}</p></div>
  <div class="case-block reveal"><h3>THE APPROACH</h3><ul>{approach}</ul></div>
  <div class="case-block reveal"><h3>RESULTS & NEXT STEPS</h3><p>{e(p['deliverables'])}</p></div>
  <div class="notice">This is a portfolio draft built around your research areas. Add your own data, numerical parameters, validated figures, and repository links before presenting it as a completed case study.</div>
 </div>
</section>
<div class="container case-back"><a href="{root}#work">← ALL SELECTED WORK</a><a href="{root}projects/{e(related['slug'])}/">NEXT: {e(related['short_title']).upper()} ↗</a></div>
</main>''' + footer(root)


def resume_page():
    root='../'
    pdf=site.get('resume_pdf', '').strip()
    pdfbtn=f'<a class="btn btn-primary" href="{root}{e(pdf)}" download>DOWNLOAD CV (PDF) <span class="arr">↗</span></a>' if pdf else ''
    focus=''.join(f'<span class="tag">{e(x["label"])}</span>' for x in site['focus'])
    return head(f"Resume | {site['name']}",site['intro'],root,'/resume/') + header(root,'resume') + f'''
<main id="main">
<section class="page-hero container">
<div class="breadcrumbs"><a href="{root}">HOME</a><span>/</span><span>RESUME</span></div>
<h1 class="display page-title">THE PERSON<br>BEHIND THE<br>MODELS<span style="color:#99d639">.</span></h1>
<p class="page-subtitle">{e(site['title'])}</p>
<div class="page-meta"><span>CURRICULUM VITAE / OVERVIEW</span><span>{e(site['name'])}</span></div>
</section>
<section class="container">
 <p class="resume-intro">{e(site['intro'])}</p>
 <div class="resume-cta">{pdfbtn}<a class="btn btn-secondary" href="{root}#work">EXPLORE PROJECTS <span class="arr">↗</span></a><a class="btn btn-secondary" href="mailto:{e(site['email'])}">EMAIL ME <span class="arr">↗</span></a></div>
 <div class="resume-grid">
  <div class="resume-col"><h2>01 / PROFILE</h2><h3>Computational mechanics</h3><p>{e(site['about_p1'])}</p><p>{e(site['about_p2'])}</p></div>
  <div class="resume-col"><h2>02 / CORE CAPABILITIES</h2><h3>Methods over buzzwords</h3><p>Numerical modeling, validation, and physical interpretation across solid mechanics and multiphysics engineering.</p><div class="resume-tags">{focus}</div></div>
  <div class="resume-col"><h2>03 / SELECTED PROJECTS</h2>{''.join(f'<h3><a href="{root}projects/{e(p["slug"])}/">{e(p["short_title"])} ↗</a></h3><p>{e(p["subtitle"])}</p>' for p in projects)}</div>
  <div class="resume-col"><h2>04 / WHAT TO ADD</h2><h3>Your verified CV details</h3><p>Add your education, publications, professional experience, and awards when you are ready. A downloadable PDF button appears automatically after setting <strong>resume_pdf</strong> in <strong>src/site.json</strong>.</p><h3>Get in touch</h3><p><a href="mailto:{e(site['email'])}">{e(site['email'])}</a></p></div>
 </div>
</section>
</main>''' + footer(root)


def write_page(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data,encoding='utf-8')


def build():
    if len(by_slug) != len(projects):
        raise ValueError('Duplicate project slugs in src/projects.json')
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()
    shutil.copytree(BASE/'assets',DEST/'assets')
    write_page(DEST/'index.html', homepage())
    for p in projects:
        write_page(DEST/'projects'/p['slug']/'index.html',case_page(p))
    write_page(DEST/'resume'/'index.html',resume_page())
    write_page(DEST/'.nojekyll','')
    write_page(DEST/'robots.txt','User-agent: *\nAllow: /\n')
    write_page(DEST/'404.html',head('Page not found', 'Page not found.', './', '/404.html')+header('./')+'''
      <main id="main" class="container page-hero" style="min-height:75svh"><div class="eyebrow">HTTP 404 / PAGE NOT FOUND</div><h1 class="display page-title">NOT IN<br>THE MODEL<span style="color:#99d639">.</span></h1><p class="page-subtitle">This page doesn't exist. Try heading back to the work.</p><a class="btn btn-primary" href="./">BACK TO HOME ↗</a></main>'''+footer('./'))
    print(f'Generated {len(projects)+3} HTML pages and all local assets in {DEST}/')

if __name__=='__main__':
    build()
