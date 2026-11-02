#!/usr/bin/env python3
"""Check or synchronize the embedded reading-page assets."""

import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'templates/reading'
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
    for href in ('/reading/', '#main'):
        if not any(n['tag'] == 'a' and n['attrs'].get('href') == href for n in page.nodes):
            errors.append(f'Missing navigation link: {href}')
    themes = [n for n in page.nodes if n['tag'] == 'select' and n['attrs'].get('id') == 'reading-theme']
    if len(themes) != 1:
        errors.append('Missing shared theme control')
    if not any(n['tag'] == 'label' and n['attrs'].get('for') == 'reading-theme' for n in page.nodes):
        errors.append('Missing theme control label')
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
            html = sync(html)
            path.write_text(html)
        canonical = None
        base = args.path if args.path.is_dir() else args.path.parent
        if args.url_prefix:
            relative = path.relative_to(base).as_posix()
            canonical = args.url_prefix.rstrip('/') + '/' + relative.removesuffix('index.html')
        elif path.resolve().is_relative_to(ROOT / 'static/reading'):
            canonical = 'https://wlj.me/reading/' + path.resolve().relative_to(ROOT / 'static/reading').as_posix().removesuffix('index.html')
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
