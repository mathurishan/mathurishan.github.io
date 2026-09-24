"""Site checks. Run from the site root:  python tools/check_site.py

Fails (exit code 1) on broken internal links or anchors, missing images, duplicate ids,
pages without exactly one <h1>, images without alt text, and wording that must never
appear on the public site. GitHub Actions runs this on every push (.github/workflows/check.yml).
"""
import glob
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REDIRECTS = {"powerbi.html", "sql.html", "python.html"}

# Wording the manuscript rules out, library systems that stay private, and personal details.
BANNED = [
    (r"\bcurrently pursuing\b|\bexpected (june )?2026\b", "study described as unfinished"),
    (r"\bpostgresql\b|\bscikit", "tool the manuscript does not support"),
    (r"\bcase stud(y|ies)\b", "use 'project' wording, not 'case study'"),
    (r"\bjanuary\b|fixed[- ]term|[removed]", "availability month or contract end date"),
    (r"[removed]|[removed]|[removed]|[removed]|[removed]|[removed]|[removed]|[removed]|[removed]|[removed]|[removed]",
     "library system name"),
    (r"[removed]|\bpassport\b|date of birth", "personal detail"),
    (r"[removed]|[removed]|[removed]", "referee name"),
    (r"15[‑–-]25\s?%|100% efficiency", "unsupported metric"),
]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs, self.h1, self.imgs_no_alt = [], [], 0, []
        self.text, self._skip = [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])
        if tag == "h1":
            self.h1 += 1
        if tag == "img" and "alt" not in a:
            self.imgs_no_alt.append(a.get("src"))
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def main():
    os.chdir(ROOT)
    pages = {}
    for path in sorted(glob.glob("*.html")):
        p = Page()
        p.feed(open(path, encoding="utf-8").read())
        pages[path] = p

    problems = []
    for path, p in pages.items():
        dupes = {i for i in p.ids if p.ids.count(i) > 1}
        if dupes:
            problems.append(f"{path}: duplicate ids {sorted(dupes)}")
        if path not in REDIRECTS and p.h1 != 1:
            problems.append(f"{path}: {p.h1} <h1> elements (expected 1)")
        for src in p.imgs_no_alt:
            problems.append(f"{path}: image without alt text: {src}")
        for ref in p.refs:
            if ref.startswith(("http:", "https:", "mailto:", "tel:", "//", "data:")):
                continue
            raw, _, frag = ref.partition("#")
            raw = raw.split("?")[0]
            if raw == "":
                target = path                      # same-page anchor
            elif raw in ("./", "/"):
                target = "index.html"
            else:
                target = raw.lstrip("/")
            if not os.path.exists(target):
                problems.append(f"{path}: missing file {ref}")
            elif frag and target in pages and frag not in pages[target].ids:
                problems.append(f"{path}: missing anchor {ref}")
        text = " ".join(p.text).lower()
        for pattern, why in BANNED:
            m = re.search(pattern, text)
            if m:
                problems.append(f"{path}: {why}: '{m.group(0)}'")

    sitemap = open("sitemap.xml", encoding="utf-8").read()
    for loc in re.findall(r"<loc>https://mathurishan\.github\.io/([^<]*)</loc>", sitemap):
        if not os.path.exists(loc or "index.html"):
            problems.append(f"sitemap.xml lists a missing page: {loc}")

    if problems:
        print(f"{len(problems)} problem(s):")
        for line in problems:
            print("  -", line)
        sys.exit(1)
    print(f"All checks passed ({len(pages)} pages).")


if __name__ == "__main__":
    main()
