from argparse import ArgumentParser, ArgumentTypeError
from dataclasses import dataclass
from html import escape as h
from json import dumps, loads
from pathlib import Path
from re import fullmatch
from urllib.parse import urlsplit
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
LINKEDIN = 'https://www.linkedin.com/in/zhuoran-wang-151437325/'
LAB = 'https://zhuoran-frontdesk-lab.jackandwzr.chatgpt.site'
# Google Search Console ownership token for the GitHub Pages property. Keep it, or verification is lost.
GOOGLE_SITE_VERIFICATION = '85ujjiV8bpENyZ2mHrsleQaIXhjzl0w-IllRL5oOpG0'
LANGS = loads((ROOT / 'portfolio.json').read_text(encoding='utf-8'))
LANG_NAV = ('中文', 'English', 'Bahasa Melayu')
FIGURES = ('inventory-price', 'seasonality', 'energy-spread', 'china-imports')
NAME_EN = 'Zhuoran Wang'
NAME_ZH = '汪卓燃'
SITE_NAME = f'{NAME_ZH} · {NAME_EN}'


@dataclass(frozen=True)
class SiteUrls:
    origin: str
    prefix: str

    def href(self, path):
        return self.prefix + path

    def absolute(self, path):
        return self.origin + self.href(path)


def parse_site_url(value):
    parts = urlsplit(value.strip().rstrip('/'))
    if (
        parts.scheme != 'https'
        or not fullmatch(r'[a-zA-Z0-9.-]+', parts.netloc)
        or not fullmatch(r'(?:/[a-zA-Z0-9_.~-]+)*', parts.path)
        or any(segment in {'.', '..'} for segment in parts.path.split('/'))
        or parts.query
        or parts.fragment
    ):
        raise ArgumentTypeError('Use an HTTPS site URL, such as https://example.com.')
    return SiteUrls(f'https://{parts.netloc.lower()}', parts.path)


def url(lang, case=None):
    if case:
        suffix = ('', '-en', '-ms')[LANGS.index(lang)]
        return f'/work/{case}{suffix}.html'
    return '/' if lang['file'] == 'index.html' else '/' + lang['file']


def image(site, lang, index, lazy=True):
    src = site.href(f'/assets/palm-{FIGURES[index]}.webp')
    return (f'<img src="{src}" width="800" height="497"'
            f' alt="{h(lang["labels"][index])}"' + (' loading="lazy"' if lazy else '') + '>')


def figure(site, lang, index, lazy=True, extra_class=''):
    """Numbered report figure. The image links to the full file, so it works without JavaScript;
    zoom.js upgrades the link to an in-page viewer."""
    ui = lang['ui']
    label = lang['labels'][index]
    src = site.href(f'/assets/palm-{FIGURES[index]}.webp')
    cls = f' class="{extra_class}"' if extra_class else ''
    return (f'<figure{cls}><a class="zoom" href="{src}" data-zoom aria-label="{h(ui["zoomOf"] + label)}">'
            f'{image(site, lang, index, lazy)}<span class="zoom-hint" aria-hidden="true">⤢ {h(ui["zoom"])}</span></a>'
            f'<figcaption>{h(label)}</figcaption></figure>')


def is_internship(lang, slug):
    return any(job[3] == slug for job in lang['jobs'])


def case_kind(lang, case):
    return f"{case[1]} · {lang['intern'] if is_internship(lang, case[0]) else lang['research']}"


def structured_data(site, lang, canonical, headline, description, case):
    home = site.absolute('/')
    person_id = home + '#zhuoran-wang'
    person = {
        '@type': 'Person',
        '@id': person_id,
        'name': lang['name'],
        'alternateName': NAME_EN if lang['lang'] == 'zh-CN' else NAME_ZH,
        'url': home,
        'sameAs': [LINKEDIN],
    }
    entry = {'url': canonical, 'inLanguage': lang['lang'], 'description': description}
    if case:
        entry.update({
            '@type': 'Article',
            'headline': headline,
            'mainEntityOfPage': canonical,
            'author': {'@id': person_id},
        })
        if case == 'palm-oil':
            entry['image'] = [site.absolute(f'/assets/palm-{name}.webp') for name in FIGURES]
    else:
        entry.update({'@type': 'ProfilePage', 'mainEntity': {'@id': person_id}})

    graph = [person, entry]
    if canonical == home and not site.prefix:
        graph.append({
            '@type': 'WebSite',
            'name': SITE_NAME,
            'alternateName': [NAME_EN, NAME_ZH],
            'url': home,
        })
    return dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('<', '\\u003c')


def page(site, lang, body, headline, description, case=None, script=False):
    ui = lang['ui']
    canonical = site.absolute(url(lang, case))
    home = site.href(url(lang))
    if case:
        title = f"{headline} | {lang['name']}"
    else:
        alternate_name = NAME_EN if lang['lang'] == 'zh-CN' else NAME_ZH
        title = f"{lang['name']} ({alternate_name}) | {headline}"

    links = '\n'.join(
        f'<link rel="alternate" hreflang="{x["lang"]}" href="{site.absolute(url(x, case))}">'
        for x in LANGS
    )
    switch = ''.join(
        f'<a href="{site.href(url(x, case))}" hreflang="{x["lang"]}" lang="{x["lang"]}"'
        + (' aria-current="page"' if lang is x else '')
        + f'><span class="lang-full">{label}</span><span class="lang-code" aria-hidden="true">{x["ui"]["langCode"]}</span></a>'
        for label, x in zip(LANG_NAV, LANGS)
    )
    schema = structured_data(site, lang, canonical, headline, description, case)
    zoom = f'\n<script src="{site.href("/zoom.js")}" defer></script>' if script else ''
    verification = (f'\n<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">'
                    if GOOGLE_SITE_VERIFICATION and not case else '')
    return f"""<!doctype html>
<html lang="{lang['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h(title)}</title>
<meta name="description" content="{h(description)}">
<meta name="robots" content="index,follow">{verification}
<link rel="canonical" href="{canonical}">
{links}
<link rel="alternate" hreflang="x-default" href="{site.absolute(url(LANGS[0], case))}">
<meta property="og:title" content="{h(title)}">
<meta property="og:description" content="{h(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:type" content="{'article' if case else 'website'}">
<script type="application/ld+json">{schema}</script>
<link rel="stylesheet" href="{site.href('/style.css')}">{zoom}
</head>
<body>
<a class="skip" href="#main">{h(ui['skip'])}</a>
<header class="header">
  <div class="frame header-inner">
    <a class="wordmark" href="{home}">Zhuoran Wang</a>
    <nav class="site-nav" aria-label="{h(ui['mainNav'])}">
      <a href="{home}#work">{h(lang['work'])}</a>
      <a href="{home}#experience">{h(lang['exp'])}</a>
    </nav>
    <nav class="languages" aria-label="{h(ui['langNav'])}">{switch}</nav>
  </div>
</header>
{body}
<footer class="frame footer">
  <span>{h(lang['name'])} · {h(lang['location'])}</span>
  <div><a href="{LAB}">{h(lang['practice'])} ↗</a><a href="{LINKEDIN}">LinkedIn ↗</a></div>
</footer>
</body>
</html>
"""


def metrics(rows):
    items = ''.join(
        f'<div><dt>{h(label)}</dt><dd>{h(value)}</dd></div>' for value, label in rows
    )
    return f'<dl class="metrics">{items}</dl>'


def homepage(site, lang):
    ui = lang['ui']
    palm, *other = lang['cases']
    featured = site.href(url(lang, palm[0]))
    rows = ''.join(
        f'<article class="project-row"><p class="meta">{h(case_kind(lang, c))}</p>'
        f'<div><h3><a class="row-link" href="{site.href(url(lang, c[0]))}">{h(c[2])}</a></h3><p>{h(c[3])}</p></div>'
        f'<span class="jump" aria-hidden="true">↗</span></article>'
        for c in other
    )
    jobs = ''.join(
        f'<div class="job"><div><h3>{h(job)}</h3><p class="meta">{h(role)}</p></div>'
        f'<div><p>{h(desc)}</p>'
        + (f'<a class="text-link" href="{site.href(url(lang, slug))}">{h(lang["read"])} ↗</a>' if slug else '')
        + '</div></div>'
        for job, role, desc, slug in lang['jobs']
    )
    body = f"""<main id="main" class="frame">
<section class="hero">
  <div class="hero-id">
    <p class="meta">{h(lang['degree'])}</p>
    <h1>{h(lang['name'])}</h1>
    <p class="hero-role">{h(lang['title'])}</p>
  </div>
  <div class="hero-intro">
    <p>{h(lang['intro'])}</p>
    <p class="actions"><a class="text-link" href="{LINKEDIN}">LinkedIn ↗</a></p>
  </div>
</section>
<section id="work" class="work" aria-labelledby="work-title">
  <div class="section-title"><h2 id="work-title">{h(lang['work'])}</h2></div>
  <article class="featured">
    <div class="featured-copy">
      <p class="tag">{h(ui['lead'])}</p>
      <p class="meta">{h(case_kind(lang, palm))}</p>
      <h3><a class="row-link" href="{featured}">{h(palm[2])}</a></h3>
      <p>{h(palm[3])}</p>
      <span class="text-link" aria-hidden="true">{h(lang['read'])} ↗</span>
    </div>
    <figure class="featured-chart">
      {image(site, lang, 0, lazy=False)}
      <figcaption>{h(lang['labels'][0])} · {h(palm[4])}</figcaption>
    </figure>
  </article>
  {rows}
</section>
<section id="experience" class="experience" aria-labelledby="experience-title">
  <div class="section-title"><h2 id="experience-title">{h(lang['exp'])}</h2></div>
  {jobs}
</section>
</main>"""
    return page(site, lang, body, lang['title'], lang['intro'])


def workflow(lang):
    title, *steps, note = lang['demo']
    items = ''.join(
        f'<li><details><summary><span class="step-no">{n}</span>{h(step)}</summary>'
        f'<div><strong>{h(status)}</strong><p>{h(description)}</p></div></details></li>'
        for n, (step, (status, description)) in enumerate(zip(steps, lang['demoSteps']), 1)
    )
    return f"""<section class="highlight workflow" aria-labelledby="workflow-title">
  <h2 id="workflow-title" class="highlight-title">{h(title)}</h2><p class="highlight-note">{h(note)}</p>
  <ol class="steps">{items}</ol>
</section>"""


def sop_panel(hl):
    chips = ''.join(f'<li>{h(item)}</li>' for item in hl['items'])
    return f"""<section class="highlight sop" aria-labelledby="sop-title">
  <h2 id="sop-title" class="highlight-title">{h(hl['title'])}</h2>
  <p class="big-number"><strong>{h(hl['count'])}</strong> {h(hl['countLabel'])}</p>
  <ul class="chips">{chips}</ul>
  <p class="highlight-note">{h(hl['note'])}</p>
</section>"""


def formula_panel(hl):
    parts = []
    for i, (term, gloss) in enumerate(hl['terms']):
        if i:
            parts.append('<span class="op" aria-hidden="true">−</span><span class="sr-only">−</span>')
        sub = f'<small>{h(gloss)}</small>' if gloss else ''
        parts.append(f'<span class="term"><b>{h(term)}</b>{sub}</span>')
    return f"""<section class="highlight formula-panel" aria-labelledby="formula-title">
  <h2 id="formula-title" class="highlight-title">{h(hl['title'])}</h2>
  <p class="formula">{''.join(parts)}</p>
  <p class="highlight-note">{h(hl['note'])}</p>
</section>"""


def deck_panel(hl):
    decks = ''.join(
        f'<li class="deck"><span class="deck-pages">{h(pages)}</span><span class="deck-name">QFI · {h(name)}</span></li>'
        for name, pages in hl['decks']
    )
    items = ''.join(f'<li>{h(item)}</li>' for item in hl['items'])
    return f"""<section class="highlight deck-panel" aria-labelledby="deck-title">
  <h2 id="deck-title" class="highlight-title">{h(hl['title'])}</h2>
  <ul class="decks">{decks}</ul>
  <ol class="toc">{items}</ol>
  <p class="highlight-note">{h(hl['note'])}</p>
</section>"""


def casepage(site, lang, case):
    ui = lang['ui']
    slug, kind, title, desc, scope, sections, numbers = case
    hl = lang.get('highlights', {}).get(slug)
    report = slug == 'palm-oil'
    gallery = ''
    if report:
        figures = ''.join(figure(site, lang, i) for i in (1, 2, 3))
        gallery = (f'<div class="gallery">{figures}</div>'
                   f'<p class="caption source">{h(lang["source"])} {h(lang["note"])}</p>')

    reading = ''.join(f'<section><h3>{h(heading)}</h3><p>{h(text)}</p></section>'
                      for heading, text in sections)
    additional = figure(site, lang, 0, lazy=False, extra_class='lead-chart') if report else ''
    if slug == 'tusstar-membership':
        additional = workflow(lang) + (sop_panel(hl) if hl else '')
    if slug == 'ferrous' and hl:
        additional = formula_panel(hl)
    if slug == 'citic-futures' and hl:
        additional = deck_panel(hl)
    related = ''.join(
        f'<li><a href="{site.href(url(lang, c[0]))}"><span class="meta">{h(case_kind(lang, c))}</span>'
        f'<span class="related-title">{h(c[2])} ↗</span></a></li>'
        for c in lang['cases'] if c[0] != slug)
    body = f"""<main id="main" class="frame article">
<a class="text-link back" href="{site.href(url(lang))}#work">← {h(lang['home'])}</a>
<header class="article-title">
  <p class="meta">{h(case_kind(lang, case))}</p>
  <h1>{h(title)}</h1>
  <p class="dek">{h(desc)}</p>
  <p class="byline"><span>{h(ui['by'])} <a rel="author" href="{site.href(url(lang))}">{h(lang['name'])}</a></span><span>{h(scope)}</span></p>
</header>
{metrics(numbers)}
{additional}
<div class="article-body"><h2>{h(lang['evidence'])}</h2>{reading}</div>
{gallery}
<aside class="related" aria-labelledby="related-title">
  <h2 id="related-title">{h(ui['related'])}</h2>
  <ul>{related}</ul>
</aside>
</main>"""
    if report:
        body += f"""
<dialog class="viewer" aria-label="{h(ui['zoom'])}" data-fit="{h(ui['zoomFit'])}" data-native="{h(ui['zoomNative'])}" data-double="{h(ui['zoomDouble'])}" data-close="{h(ui['close'])}"></dialog>"""
    return page(site, lang, body, title, desc, slug, script=report)


def main():
    parser = ArgumentParser(description='Build the static portfolio for its published address.')
    parser.add_argument('--site-url', required=True, type=parse_site_url)
    site = parser.parse_args().site_url

    (DIST / 'work').mkdir(parents=True, exist_ok=True)
    paths = []
    for lang in LANGS:
        (DIST / lang['file']).write_text(homepage(site, lang), encoding='utf-8')
        paths.append(url(lang))
        for case in lang['cases']:
            p = url(lang, case[0])
            (DIST / p.lstrip('/')).write_text(casepage(site, lang, case), encoding='utf-8')
            paths.append(p)
    urls = '\n'.join(f'  <url><loc>{xml_escape(site.absolute(p))}</loc></url>' for p in paths)
    (DIST / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '\n</urlset>\n',
        encoding='utf-8'
    )
    sitemap = site.absolute('/sitemap.xml')
    (DIST / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {sitemap}\n', encoding='utf-8')


if __name__ == '__main__':
    main()
