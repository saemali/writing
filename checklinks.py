import sys, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.found = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src"):
            if a.get(key): self.found.append(a[key])

start = sys.argv[1]
host = urlparse(start).netloc
todo, seen, broken = [start], set(), []
while todo:
    url = todo.pop()
    if url in seen: continue
    seen.add(url)
    try:
        with urllib.request.urlopen(url) as r:
            ctype = r.headers.get("Content-Type", "")
            body = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        broken.append((url, e.code)); continue
    if "text/html" in ctype:
        p = Links(); p.feed(body)
        for link in p.found:
            full = urljoin(url, link).split("#")[0]
            if urlparse(full).netloc == host: todo.append(full)
print(f"Checked {len(seen)} URLs")
for url, code in broken: print(f"BROKEN {code} {url}")
sys.exit(1 if broken else 0)
