import json, sys, html, datetime
data = json.load(open(sys.argv[1]))
pages = data if isinstance(data, list) else [data]
items = [it for page in pages for it in page['items']]
counts, latest = {}, None
for it in items:
    name = it['repository_url'].rsplit('/', 1)[1]
    counts[name] = counts.get(name, 0) + 1
    if latest is None or it['closed_at'] > latest['closed_at']:
        latest = it
rows = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].lower()))[:6]
total = sum(counts.values())
W, top, rowh = 640, 64, 34
H = top + rowh * len(rows) + 70
lx, bx, bmax = 222, 238, 330
mx = max(c for _, c in rows)
step = 5 if mx > 10 else 2
scale = bmax / (((mx + step - 1) // step) * step)
e = lambda s: html.escape(str(s))
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Merged pull requests by project: ' + ', '.join(f'{e(n)} {c}' for n, c in rows) + '">',
'<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;fill:#1f2328}.m{fill:#59636e}.g{stroke:#d1d9e0}.b{fill:#2da44e}'
'@media (prefers-color-scheme:dark){text{fill:#f0f6fc}.m{fill:#9198a1}.g{stroke:#3d444d}.b{fill:#3fb950}}</style>',
f'<text x="{W/2}" y="30" text-anchor="middle" font-size="15" font-weight="600">Merged pull requests</text>']
t = 0
while t * scale <= bmax + 0.1:
    x = bx + t * scale
    o.append(f'<line class="g" x1="{x:.1f}" y1="{top-12}" x2="{x:.1f}" y2="{top + rowh*len(rows) - 6}" stroke-width="1"/>')
    o.append(f'<text class="m" x="{x:.1f}" y="{top + rowh*len(rows) + 10}" text-anchor="middle" font-size="11">{t}</text>')
    t += step
for i, (n, c) in enumerate(rows):
    y = top + i * rowh
    w = c * scale
    o.append(f'<text x="{lx}" y="{y+13}" text-anchor="end" font-size="14">{e(n)}</text>')
    o.append(f'<rect class="b" x="{bx}" y="{y}" width="{w:.1f}" height="18" rx="3"/>')
    o.append(f'<text class="m" x="{bx + w + 8:.1f}" y="{y+13}" font-size="13">{c}</text>')
d = datetime.datetime.strptime(latest['closed_at'][:10], '%Y-%m-%d')
lname = latest['repository_url'].rsplit('/', 1)[1]
o.append(f'<text class="m" x="{W/2}" y="{H-14}" text-anchor="middle" font-size="12">{total} merged into other people’s projects · latest {e(lname)}#{latest["number"]}, {d:%b} {d.day}, {d:%Y}</text>')
o.append('</svg>')
open(sys.argv[2], 'w').write('\n'.join(o) + '\n')
