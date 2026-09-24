"""Builds chatbot/index.json from kb/ and sources/. Run locally or via the GitHub Action."""
import csv, datetime, html, json, pathlib, re
from xml.etree import ElementTree as ET
ROOT = pathlib.Path(__file__).resolve().parent.parent

def front(t):
    m, meta = re.match(r'---\n(.*?)\n---\n', t, re.S), {}
    if m:
        for l in m.group(1).splitlines():
            if ':' in l: k, v = l.split(':', 1); meta[k.strip()] = v.strip()
        t = t[m.end():]
    return t, meta

def read(p):
    s = p.suffix.lower()
    if s == '.pdf':
        from pypdf import PdfReader
        r = PdfReader(p); return '\n'.join(pg.extract_text() or '' for pg in r.pages), {'title': (r.metadata.title if r.metadata else '')}
    raw = p.read_text(encoding='utf-8')
    if s == '.md': return front(raw)
    if s == '.html':
        title = re.search(r'<title>(.*?)</title>', raw, re.S)
        raw = re.sub(r'(?s)<(script|style).*?</\1>', '', raw)
        raw = re.sub(r'<h(\d)[^>]*>(.*?)</h\1>', lambda m: '\n\n' + '#' * int(m.group(1)) + ' ' + m.group(2) + '\n\n', raw, flags=re.S)
        raw = re.sub(r'</(p|li|tr)>', '\n\n', raw)
        return html.unescape(re.sub(r'<[^>]+>', ' ', raw)), {'title': title.group(1) if title else ''}
    if s == '.dita':
        r = ET.fromstring(raw); return re.sub(r'\s+', ' ', ' '.join(r.itertext())), {'title': r.findtext('title', '')}
    if s == '.csv': return '\n\n'.join(f"Q: {r['question']} A: {r['answer']}" for r in csv.DictReader(raw.splitlines())), {}
    if s == '.json': return '\n\n'.join('; '.join(f'{k}: {v}' for k, v in d.items()) for d in json.loads(raw)), {}
    m = re.match(r'=\s+(.+)', raw)
    return raw, {'title': m.group(1) if m else ''}  # .adoc, .txt

def chunks(text, limit=90):
    heads, buf, out = {}, [], []
    def flush():
        if buf:
            h = '. '.join(heads[k] for k in sorted(heads))
            out.append((h + '. ' if h else '') + ' '.join(buf).strip())
        buf.clear()
    for para in re.split(r'\n\s*\n|\n(?=[#=])', text):
        first, _, rest = para.strip().partition('\n')
        m = re.match(r'([#=]+) (.*)', first)
        if m:
            flush(); lv = len(m.group(1))
            heads = {k: v for k, v in heads.items() if k < lv}; heads[lv] = m.group(2).strip(); para = rest
        para = re.sub(r'(?m)^\s*[*-]\s+', '', para).strip()
        if not para: continue
        if sum(len(x.split()) for x in buf) + len(para.split()) > limit: flush()
        buf.append(re.sub(r'\s+', ' ', para))
    flush(); return out

items = []
REG = json.loads((ROOT / 'sources' / 'titles.json').read_text()) if (ROOT / 'sources' / 'titles.json').exists() else {}
for folder, cat in (('kb', 'Knowledge base'), ('sources', 'Product documentation')):
    for p in sorted((ROOT / folder).glob('*')):
        if p.suffix.lower() not in {'.md', '.html', '.pdf', '.dita', '.adoc', '.csv', '.json', '.txt'} or p.name in ('manifest.json', 'titles.json'): continue
        text, meta = read(p)
        title = meta.get('title') or REG.get(p.name) or p.stem.replace('-', ' ').title()
        href = f'read.html?a={p.stem}' if folder == 'kb' else f'{folder}/{p.name}'
        for i, c in enumerate(chunks(text)):
            items.append({'id': f'{p.stem}-{i}', 'title': title, 'href': href, 'type': p.suffix[1:].lower(), 'category': cat, 'text': c})
(ROOT / 'chatbot' / 'index.json').write_text(json.dumps({'generated': datetime.date.today().isoformat(), 'chunks': items}, indent=1), encoding='utf-8')
print(f'{len(items)} passages indexed')
