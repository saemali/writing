"""Check that every form control has a matching <label for> and every
aria-describedby id exists. Usage: python3 checkform.py page.html"""
import sys
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.label_for, self.controls, self.described = set(), set(), [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "label" and "for" in a:
            self.label_for.add(a["for"])
        if tag in ("input", "textarea", "select") and a.get("type") not in ("hidden", "submit"):
            self.controls.append(a.get("id") or a.get("name"))
        for ref in (a.get("aria-describedby") or "").split():
            self.described.append(ref)

p = P()
p.feed(open(sys.argv[1], encoding="utf-8").read())
problems = [f"no label for control '{c}'" for c in p.controls if c not in p.label_for]
problems += [f"aria-describedby points to missing id '{r}'" for r in p.described if r not in p.ids]
for x in problems:
    print("FAIL:", x)
print(f"{len(p.controls)} controls checked, {len(problems)} problems")
sys.exit(1 if problems else 0)
