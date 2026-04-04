#!/usr/bin/env python3
"""
Batch fetch all 69 blog posts from Wayback Machine for hi.baidu.com/wulujia
and convert to Hugo markdown format.
"""

import subprocess
import re
import time
import os
import json
import html as html_module
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "content" / "posts"
CACHE_DIR = Path("/tmp/baidu_hi_cache")
CACHE_DIR.mkdir(exist_ok=True)

# Step 1: Get all unique blog post URLs with their best timestamps
def get_post_list():
    """Fetch CDX data and return dict of item_id -> list of timestamps"""
    r = subprocess.run(
        ['curl', '-s',
         'https://web.archive.org/cdx/search/cdx?url=hi.baidu.com/wulujia/blog/item/*&output=text&fl=timestamp,original,statuscode&filter=statuscode:200&limit=300'],
        capture_output=True, text=True, timeout=30
    )
    items = {}
    for line in r.stdout.strip().split('\n'):
        parts = line.split()
        if len(parts) < 3 or '/cmtid/' in parts[1] or '.html' not in parts[1]:
            continue
        url = parts[1].replace('http://hi.baidu.com:80/', 'http://hi.baidu.com/')
        item_id = url.split('/item/')[-1].replace('.html', '')
        if item_id not in items:
            items[item_id] = []
        items[item_id].append(parts[0])
    return items


def fetch_page(timestamp, item_id):
    """Fetch a page from Wayback Machine, with caching."""
    cache_file = CACHE_DIR / f"{item_id}_{timestamp}.html"
    if cache_file.exists():
        return cache_file.read_bytes()

    url = f"http://hi.baidu.com/wulujia/blog/item/{item_id}.html"
    wayback_url = f"https://web.archive.org/web/{timestamp}/{url}"

    r = subprocess.run(
        ['curl', '-sL', '--max-time', '20',
         '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
         wayback_url],
        capture_output=True, timeout=25
    )
    cache_file.write_bytes(r.stdout)
    return r.stdout


def decode_html(raw_bytes):
    """Decode HTML bytes trying multiple encodings."""
    for enc in ['gbk', 'gb2312', 'gb18030', 'utf-8']:
        try:
            return raw_bytes.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw_bytes.decode('utf-8', errors='replace')


def extract_article(html_text):
    """Extract title, date, category, and body from Baidu Space blog HTML."""
    result = {
        'title': '',
        'date': '',
        'category': '',
        'body_html': '',
    }

    # Title from <title> tag
    m = re.search(r'<title[^>]*>(.*?)</title>', html_text, re.DOTALL | re.IGNORECASE)
    if m:
        title = m.group(1).strip()
        title = re.sub(r'<[^>]+>', '', title)
        for suffix in ['_野路子_百度空间', '_野路子']:
            title = title.replace(suffix, '')
        title = html_module.unescape(title).strip()
        if title and title != '百度空间' and '百度' not in title:
            result['title'] = title

    # Date
    date_match = re.search(r'(20\d\d-\d\d-\d\d)\s+(\d\d:\d\d)', html_text)
    if date_match:
        result['date'] = f"{date_match.group(1)}T{date_match.group(2)}:00+08:00"
    else:
        date_match2 = re.search(r'(20\d\d-\d\d-\d\d)', html_text)
        if date_match2:
            result['date'] = f"{date_match2.group(1)}T00:00:00+08:00"

    # Category
    cat_match = re.search(r'类别[：:]?\s*(?:<[^>]+>)*\s*([\u4e00-\u9fff\w]+)', html_text)
    if cat_match:
        result['category'] = cat_match.group(1).strip()

    # Body: try to find the blog content div
    body = ''

    # Pattern 1: div id="blog_text" or class="blog_text"
    m = re.search(r'<div[^>]*(?:id|class)=["\']?blog[_-]?text["\']?[^>]*>(.*?)</div>', html_text, re.DOTALL | re.IGNORECASE)
    if m:
        body = m.group(1)

    # Pattern 2: div class="content" or id="content"
    if not body:
        m = re.search(r'<div[^>]*(?:id|class)=["\']?content["\']?[^>]*>(.*?)</div>\s*<div', html_text, re.DOTALL | re.IGNORECASE)
        if m:
            body = m.group(1)

    # Pattern 3: td class="blog_text"
    if not body:
        m = re.search(r'<td[^>]*class=["\']?blog_text["\']?[^>]*>(.*?)</td>', html_text, re.DOTALL | re.IGNORECASE)
        if m:
            body = m.group(1)

    # Pattern 4: Look for the main text between known markers
    if not body:
        # Find text between the title area and the comment/footer area
        m = re.search(r'(?:阅读全文|类别|评论\(\d+\))', html_text)
        if not m:
            # Fallback: grab everything between <body> and </body>, strip nav
            m = re.search(r'<body[^>]*>(.*?)</body>', html_text, re.DOTALL | re.IGNORECASE)
            if m:
                body = m.group(1)

    if not body:
        body = html_text

    result['body_html'] = body
    return result


def html_to_markdown(html_text):
    """Convert HTML to simple markdown."""
    text = html_text

    # Remove Wayback Machine toolbar/injections
    text = re.sub(r'<!--\s*BEGIN WAYBACK.*?END WAYBACK.*?-->', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<div id="wm-ipp-base".*?</div>\s*</div>\s*</div>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Images: convert to markdown
    def img_replace(m):
        src = ''
        src_match = re.search(r'src=["\']([^"\']+)["\']', m.group(0))
        if src_match:
            src = src_match.group(1)
            # Clean wayback URL prefix
            src = re.sub(r'https?://web\.archive\.org/web/\d+(?:im_)?/', '', src)
        alt = ''
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', m.group(0))
        if alt_match:
            alt = alt_match.group(1)
        return f'![{alt}]({src})' if src else ''

    text = re.sub(r'<img[^>]+/?>', img_replace, text, flags=re.IGNORECASE)

    # Links
    def link_replace(m):
        href = ''
        href_match = re.search(r'href=["\']([^"\']+)["\']', m.group(1))
        if href_match:
            href = href_match.group(1)
            href = re.sub(r'https?://web\.archive\.org/web/\d+/', '', href)
        link_text = re.sub(r'<[^>]+>', '', m.group(2))
        if href and link_text.strip():
            return f'[{link_text.strip()}]({href})'
        elif href:
            return href
        return link_text

    text = re.sub(r'<a\s([^>]+)>(.*?)</a>', link_replace, text, flags=re.DOTALL | re.IGNORECASE)

    # Block elements
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?p[^>]*>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?div[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<h(\d)[^>]*>(.*?)</h\1>', lambda m: f"\n{'#' * int(m.group(1))} {re.sub(r'<[^>]+>', '', m.group(2)).strip()}\n", text, flags=re.DOTALL | re.IGNORECASE)

    # Lists
    text = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: f"- {re.sub(r'<[^>]+>', '', m.group(1)).strip()}", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'</?[ou]l[^>]*>', '\n', text, flags=re.IGNORECASE)

    # Bold/italic
    text = re.sub(r'<(?:b|strong)[^>]*>(.*?)</(?:b|strong)>', r'**\1**', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<(?:i|em)[^>]*>(.*?)</(?:i|em)>', r'*\1*', text, flags=re.DOTALL | re.IGNORECASE)

    # Blockquote
    text = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>',
                  lambda m: '\n'.join('> ' + l for l in re.sub(r'<[^>]+>', '', m.group(1)).strip().split('\n')),
                  text, flags=re.DOTALL | re.IGNORECASE)

    # Code/pre
    text = re.sub(r'<pre[^>]*>(.*?)</pre>',
                  lambda m: f"\n```\n{re.sub(r'<[^>]+>', '', html_module.unescape(m.group(1))).strip()}\n```\n",
                  text, flags=re.DOTALL | re.IGNORECASE)

    # Strip remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Decode HTML entities
    text = html_module.unescape(text)

    # Clean up whitespace
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+\n', '\n', text)

    # Remove Wayback Machine artifacts
    lines = text.split('\n')
    clean_lines = []
    skip_patterns = [
        'The Wayback Machine', 'web.archive.org', 'Got an HTTP',
        'Wayback Machine', 'wayback', 'archive.org',
        '野路子', '百度首页', '百度空间', '个人档案', '好友',
        '文章列表', '主页 博客 相册', '阅读全文', '上一篇',
        '下一篇', '类别：', '评论(', '浏览(', '发表评论',
        '系统提示', '登录', '注册', '百度Hi', '把百度空间',
        '检举', '吴鲁加的网络日志',
    ]
    for line in lines:
        stripped = line.strip()
        if not stripped:
            clean_lines.append('')
            continue
        if any(p in stripped for p in skip_patterns):
            continue
        if len(stripped) < 3 and not re.search(r'[\u4e00-\u9fff]', stripped):
            continue
        clean_lines.append(line)

    text = '\n'.join(clean_lines).strip()
    # Final cleanup
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def category_to_tag(category):
    """Map Baidu Space category to a tag."""
    mapping = {
        '默认分类': 'Life',
        '商业经营': 'Business',
        '读书看片': 'Reading',
        '防泄密': 'Security',
    }
    return mapping.get(category, 'Life')


def generate_slug(item_id):
    """Generate a slug from item_id."""
    return f"blog-baiduhi-{item_id[:8]}"


def main():
    print("Step 1: Getting post list from Wayback Machine CDX API...")
    items = get_post_list()
    print(f"  Found {len(items)} unique blog posts")

    posts = []
    total = len(items)

    print(f"\nStep 2: Fetching {total} articles...")
    for idx, (item_id, timestamps) in enumerate(sorted(items.items())):
        # Try earliest timestamp first (original content), fallback to others
        sorted_ts = sorted(timestamps)
        success = False

        for ts in sorted_ts:
            try:
                raw = fetch_page(ts, item_id)
                if len(raw) < 500:
                    continue
                text = decode_html(raw)
                article = extract_article(text)
                if article['date']:
                    md_body = html_to_markdown(article['body_html'])
                    if len(md_body) > 20:
                        posts.append({
                            'item_id': item_id,
                            'title': article['title'],
                            'date': article['date'],
                            'category': article['category'],
                            'body': md_body,
                            'timestamp': ts,
                        })
                        status = '✓' if article['title'] else '? (no title)'
                        print(f"  [{idx+1}/{total}] {status} {article['title'] or item_id[:12]} ({article['date'][:10]})")
                        success = True
                        break
            except Exception as e:
                continue

        if not success:
            print(f"  [{idx+1}/{total}] ✗ FAILED {item_id[:12]}")

        if idx % 5 == 4:
            time.sleep(2)

    print(f"\nStep 3: Processing {len(posts)} articles...")

    # Save intermediate results
    with open(CACHE_DIR / 'posts.json', 'w') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    # Write markdown files
    written = 0
    needs_title = []
    for post in posts:
        slug = generate_slug(post['item_id'])
        tag = category_to_tag(post['category'])
        title = post['title']

        if not title:
            needs_title.append(post)
            continue

        # Escape quotes in title
        title_escaped = title.replace('"', '\\"')

        frontmatter = f'''---
title: "{title_escaped}"
date: {post['date']}
tags: ["{tag}"]
draft: false
slug: "{slug}"
---

'''
        content = frontmatter + post['body'] + '\n'
        filepath = OUTPUT_DIR / f"{slug}.md"
        filepath.write_text(content, encoding='utf-8')
        written += 1

    print(f"  Written {written} posts with titles")
    print(f"  {len(needs_title)} posts need title generation")

    # Save needs-title list for LLM processing
    if needs_title:
        title_tasks = []
        for post in needs_title:
            # Get first 300 chars of body for title generation
            preview = post['body'][:500].strip()
            title_tasks.append({
                'item_id': post['item_id'],
                'date': post['date'],
                'category': post['category'],
                'preview': preview,
                'body': post['body'],
                'slug': generate_slug(post['item_id']),
                'tag': category_to_tag(post['category']),
            })
        with open(CACHE_DIR / 'needs_title.json', 'w') as f:
            json.dump(title_tasks, f, ensure_ascii=False, indent=2)
        print(f"\n  Title generation data saved to {CACHE_DIR}/needs_title.json")

    print(f"\nDone! Total: {len(posts)} fetched, {written} written, {len(needs_title)} pending titles")


if __name__ == '__main__':
    main()
