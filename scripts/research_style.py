#!/usr/bin/env python3
"""Check or synchronize the embedded research-page assets, site header and footer."""

import argparse
from collections import Counter
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
import tomllib
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'templates/research'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.nodes = []
        self.ids = Counter()
        self.headings = []
        self.outline = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        node = {'tag': tag, 'attrs': attrs, 'text': '', 'outline': any(n['tag'] == 'nav' and 'outline' in n['attrs'].get('class', '').split() for n in self.stack)}
        self.nodes.append(node)
        if attrs.get('id'):
            self.ids[attrs['id']] += 1
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.headings.append(node)
        if tag == 'a' and node['outline']:
            self.outline.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]['tag'] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        for node in self.stack:
            if node['tag'] in ('style', 'script', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                node['text'] += data


SKIP_LINK = '<a class="skip" href="#main">跳到正文</a>'
HEADER_RE = r'<header class="site-header" id="site-header">.*?</header>'
FOOTER_RE = r'<footer class="site-footer" id="site-footer">.*?</footer>'
OLD_THEME_RE = r'\s*<label for="reading-theme">主题</label>\s*<select id="reading-theme">.*?</select>'


def site_chrome():
    """Build the site header and footer from hugo.toml, the same source as the Hugo pages."""
    config = tomllib.loads((ROOT / 'hugo.toml').read_text())
    logo = config['params']['Logo']['logoText']
    items = sorted(config['menu']['main'], key=lambda item: item.get('weight', 0))
    links = []
    for item in items:
        current = ' aria-current="page"' if item['url'] == '/research/' else ''
        links.append(f'<li><a href="{escape(item["url"])}"{current}>{escape(item["name"])}</a></li>')
    header = ('<header class="site-header" id="site-header">\n'
              f'<div class="site-logo-bar"><a href="/"><span class="site-logo"><img class="site-logo__avatar" src="/favicon.png" alt="Luca 的头像" width="24" height="24">{escape(logo)}</span></a></div>\n'
              '<nav class="site-menu" aria-label="站点导航"><ul>\n' + '\n'.join(links) + '\n</ul></nav>\n</header>')
    # No year in the footer, so the pages do not go out of date every January.
    footer = ('<footer class="site-footer" id="site-footer">\n'
              '<span>Powered by <a href="https://gohugo.io">Hugo</a></span>\n'
              '<span>:: <a href="https://github.com/panr/hugo-theme-terminal">Theme</a> made by <a href="https://github.com/panr">panr</a></span>\n'
              '<span>:: <a href="/index.xml">RSS</a></span>\n'
              '<span>:: <button class="theme-toggle" id="theme-toggle" type="button">[dark/light]</button></span>\n'
              '</footer>')
    return header, footer


def normalized(text):
    return ' '.join(text.split())


def check(html, canonical=None):
    page = Page()
    page.feed(html)
    errors = []
    for tag, name, extension in (('style', 'reading-style', 'css'), ('script', 'reading-script', 'js')):
        nodes = [n for n in page.nodes if n['tag'] == tag and n['attrs'].get('id') == name]
        expected = (ASSETS / f'reading.{extension}').read_text().strip()
        if len(nodes) != 1 or nodes[0]['text'].strip() != expected:
            errors.append(f'{name}: shared asset is missing or changed')
        if tag == 'style' and nodes:
            after = page.nodes[page.nodes.index(nodes[0]) + 1:]
            if any(n['tag'] == 'style' or (n['tag'] == 'link' and n['attrs'].get('rel') == 'stylesheet') for n in after):
                errors.append('Place shared styles after all component styles')
    bodies = [n for n in page.nodes if n['tag'] == 'body']
    if len(bodies) != 1 or bodies[0]['attrs'].get('data-reading-version') != '1':
        errors.append('Set data-reading-version="1" on body')
    mains = [n for n in page.nodes if n['tag'] == 'main']
    if len(mains) != 1 or mains[0]['attrs'].get('id') != 'main':
        errors.append('Use one main element with id="main"')
    for node in page.nodes:
        if node['tag'] != 'style' or node['attrs'].get('id') == 'reading-style':
            continue
        css = re.sub(r'/\*.*?\*/', '', node['text'], flags=re.S)
        shared_names = set(re.findall(r'(--[\w-]+)\s*:', (ASSETS / 'reading.css').read_text()))
        for selector, declarations in re.findall(r'(?:^|(?<=[{}]))\s*([^{}]+)\{([^{}]*)\}', css):
            if selector.lstrip().startswith('@'):
                continue
            root_selector = selector.strip().replace("'", '"')
            if all(part.strip() in (':root', ':root[data-theme="dark"]', ':root:not([data-theme="light"])') for part in root_selector.split(',')):
                names = re.findall(r'(?:^|;)\s*([\w-]+)\s*:', declarations)
                if names and all(name.startswith('--') and name not in shared_names for name in names):
                    continue
            if re.search(r'(?<![\w-])(?:html|body|:root|\.layout|\.outline|\.reading-toolbar|\.skip|#main)(?![\w-])', selector):
                errors.append(f'Component CSS changes the shared layout: {selector.strip()}')
    for name, count in page.ids.items():
        if count != 1:
            errors.append(f'Duplicate id: {name}')
    if sum(n['tag'] == 'h1' for n in page.headings) != 1:
        errors.append('Use one h1')
    previous = 1
    expected_outline = []
    for node in page.headings:
        level = int(node['tag'][1])
        if level > previous + 1:
            errors.append(f'Heading level skips: {normalized(node["text"])[:60]}')
        previous = level
        if level in (2, 3):
            name = node['attrs'].get('id')
            if not name:
                errors.append(f'Heading needs its own id: {normalized(node["text"])[:60]}')
            expected_outline.append((name, normalized(node['text'])))
    actual_outline = [(unquote(n['attrs'].get('href', '')[1:]), normalized(n['text'])) for n in page.outline if n['attrs'].get('href', '').startswith('#')]
    if actual_outline != expected_outline:
        errors.append('Outline must match every h2 and h3 in document order')
    if not any(n['tag'] == 'details' and n['outline'] for n in page.nodes):
        errors.append('Use details inside nav.outline')
    for href in ('/research/', '#main'):
        if not any(n['tag'] == 'a' and n['attrs'].get('href') == href for n in page.nodes):
            errors.append(f'Missing navigation link: {href}')
    header, footer = site_chrome()
    if html.count(header) != 1:
        errors.append('Site header is missing or out of date; run research_style.py --sync')
    if html.count(footer) != 1:
        errors.append('Site footer is missing or out of date; run research_style.py --sync')
    if any(n['attrs'].get('id') == 'reading-theme' for n in page.nodes):
        errors.append('Remove the old theme menu; the footer button switches the theme')
    if canonical:
        urls = [n['attrs'].get('href') for n in page.nodes if n['tag'] == 'link' and n['attrs'].get('rel') == 'canonical']
        if urls != [canonical]:
            errors.append(f'Expected canonical: {canonical}')
    meta = {n['attrs'].get('name'): n['attrs'].get('content', '') for n in page.nodes if n['tag'] == 'meta'}
    if not meta.get('description', '').strip():
        errors.append('Missing page description')
    if meta.get('robots') not in ('index,follow', 'noindex,follow'):
        errors.append('Set robots to index,follow or noindex,follow')
    for node in page.nodes:
        if node['tag'] == 'img' and not node['attrs'].get('alt', '').strip():
            errors.append('Image needs nonempty alt text')
    return errors


def sync(html):
    for tag, name, extension in (('style', 'reading-style', 'css'), ('script', 'reading-script', 'js')):
        content = (ASSETS / f'reading.{extension}').read_text().strip()
        block = f'<{tag} id="{name}">\n{content}\n</{tag}>'
        pattern = rf'<{tag}\s+id="{name}"[^>]*>.*?</{tag}>|<!-- {name} -->'
        html, count = re.subn(pattern, lambda match: block, html, flags=re.S)
        if count != 1:
            raise ValueError(f'Expected one {name} block or marker')
    header, footer = site_chrome()
    html = re.sub(OLD_THEME_RE, '', html, flags=re.S)
    html, count = re.subn(HEADER_RE, lambda match: header, html, flags=re.S)
    if count == 0:
        if html.count(SKIP_LINK) != 1:
            raise ValueError('Expected one skip link to place the site header after')
        html = html.replace(SKIP_LINK, SKIP_LINK + '\n' + header)
    html, count = re.subn(FOOTER_RE, lambda match: footer, html, flags=re.S)
    if count == 0:
        marker = '<script id="reading-script">'
        if html.count(marker) != 1:
            raise ValueError('Expected one reading-script block to place the site footer before')
        html = html.replace(marker, footer + '\n' + marker)
    return html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    parser.add_argument('--url-prefix', help='Canonical URL for the input directory')
    parser.add_argument('--sync', action='store_true', help='Update the embedded assets before checking')
    args = parser.parse_args()
    paths = sorted(args.path.rglob('*.html')) if args.path.is_dir() else [args.path]
    if not paths:
        parser.error('No HTML files found')
    failed = 0
    for path in paths:
        html = path.read_text()
        if args.sync:
            try:
                html = sync(html)
            except ValueError as error:
                failed += 1
                print(path)
                print(f'  ERROR: {error}')
                continue
            path.write_text(html)
        canonical = None
        base = args.path if args.path.is_dir() else args.path.parent
        if args.url_prefix:
            relative = path.relative_to(base).as_posix()
            canonical = args.url_prefix.rstrip('/') + '/' + relative.removesuffix('index.html')
        elif path.resolve().is_relative_to(ROOT / 'static/research'):
            canonical = 'https://wulujia.com/research/' + path.resolve().relative_to(ROOT / 'static/research').as_posix().removesuffix('index.html')
        errors = check(html, canonical)
        if errors:
            failed += 1
            print(path)
            for error in errors:
                print(f'  ERROR: {error}')
    print(f'Reading style: {len(paths) - failed}/{len(paths)} pages passed')
    return int(failed > 0)


if __name__ == '__main__':
    raise SystemExit(main())
