"""Use article tag names for reading metadata."""
import ast
from collections import Counter
import json
from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def vocabulary(root=ROOT):
    counts = Counter()
    for path in (root / 'content/posts').glob('*.md'):
        text = path.read_text().split('---', 2)
        if len(text) < 3:
            continue
        match = re.search(r'^tags:\s*(\[.*\])\s*$', text[1], re.M)
        if match:
            try:
                values = ast.literal_eval(match[1])
            except (ValueError, SyntaxError):
                continue
            counts.update(t for t in values if isinstance(t, str) and re.fullmatch(r'[A-Za-z][A-Za-z0-9 -]*', t))
    names = {}
    for name, _ in counts.most_common():
        names.setdefault(name.casefold(), name)
    return names


def normalize(values, names):
    if not isinstance(values, list) or not 1 <= len(values) <= 5:
        raise ValueError('每页需要 1–5 个文章主题标签。')
    result = []
    for value in values:
        if not isinstance(value, str) or value.casefold() not in names:
            raise ValueError(f'标签不在文章标签体系中：{value}')
        name = names[value.casefold()]
        if name not in result:
            result.append(name)
    return result


def replace_tags(text, mapping):
    blocks = text.split('[[materials]]')
    for i, block in enumerate(blocks):
        match = re.search(r'^slug = "([^"]+)"$', block, re.M)
        if not match or match[1] not in mapping:
            continue
        line = 'tags = ' + json.dumps(mapping[match[1]], ensure_ascii=False)
        if re.search(r'^tags = .*$', block, re.M):
            block = re.sub(r'^tags = .*$', lambda _: line, block, flags=re.M)
        else:
            block = re.sub(r'^(category = .*?)$', lambda m: m[0] + '\n' + line, block, flags=re.M)
        blocks[i] = block
    return '[[materials]]'.join(blocks)


def main():
    path = ROOT / 'data/reading-materials.toml'
    materials = tomllib.loads(path.read_text()).get('materials', [])
    existing = {m['slug']: m for m in materials}
    names = vocabulary()
    mode = sys.argv[1]
    if mode == 'resolve':
        slug, raw = sys.argv[2:4]
        values = raw.split(',') if raw else existing.get(slug, {}).get('tags', [])
        print(json.dumps(normalize([v.strip() for v in values], names)))
    elif mode == 'check':
        for material in materials:
            tags = material.get('tags', [])
            if normalize(tags, names) != tags:
                raise ValueError(f'标签大小写或重复项错误：{material["slug"]}')
        print(f'Reading tags: {len(materials)}/{len(materials)} entries passed')
    elif mode == 'batch':
        mapping = json.loads(Path(sys.argv[2]).read_text())
        if not isinstance(mapping, dict) or not mapping:
            raise ValueError('标签清单必须是非空对象。')
        for slug, values in mapping.items():
            if slug not in existing:
                raise ValueError(f'整理页不存在：{slug}')
            mapping[slug] = normalize(values, names)
        text = replace_tags(path.read_text(), mapping)
        if '--write' in sys.argv[3:]:
            path.write_text(text)
        print(f'Reading tags: {len(mapping)} entries validated')
    else:
        raise ValueError('未知标签命令。')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError) as error:
        sys.exit(str(error))
