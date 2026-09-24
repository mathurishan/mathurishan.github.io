"""Site checks. Run from the site root:  python tools/check_site.py

Fails (exit code 1) on broken internal links or anchors, missing images, duplicate ids,
pages without exactly one <h1>, images without alt text, and wording that must never
appear on the public site. GitHub Actions runs this on every push (.github/workflows/check.yml).
"""
import glob
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REDIRECTS = {"powerbi.html", "sql.html", "python.html"}

# Wording the manuscript rules out. Private terms (library system names, personal details,
# referee names) are deliberately NOT listed here, because this repository is public: they are
# read from the PRIVATE_TERMS environment variable (a GitHub Actions secret) or from
# tools/private_terms.txt, which is git-ignored. One regular expression per line.
BANNED = [
    (r"currently pursuing|expected (june )?2026", "study described as unfinished"),
    (r"postgresql|scikit", "tool the manuscript does not support"),
    (r"case stud(y|ies)", "use 'project' wording, not 'case study'"),
    (r"january|fixed[- ]term", "availability month or contract wording"),
    (r"passport|date of birth", "personal detail"),
    (r"15[‑–-]25\s?%|100% efficiency", "unsupported metric"),
]


def private_terms():
    """Private patterns from the environment or the local git-ignored file; empty if neither."""
    raw = os.environ.get("PRIVATE_TERMS", "").strip()
    local = os.path.join(ROOT, "tools", "private_terms.txt")
    if not raw and os.path.exists(local):
        raw = open(local, encoding="utf-8").read()
    lines = (line.strip() for line in raw.splitlines())
    return [line for line in lines if line and not line.startswith("#")]


def served_text_files():
    """Every tracked text file GitHub Pages serves (it serves the whole repository)."""
    try:
        out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
        files = out.splitlines()
    except (OSError, subprocess.CalledProcessError):
        files = glob.glob("**/*", recursive=True)
    text_ext = (".html", ".js", ".css", ".xml", ".webmanifest", ".txt", ".py", ".json", ".csv",
                ".sql", ".md", ".svg", ".yml")
    return sorted(f for f in files if f.lower().endswith(text_ext) and os.path.isfile(f)
                  and not f.startswith(".git/"))


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

    private = private_terms()
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
        # Private terms are checked against the whole file (text, attributes, scripts, JSON-LD),
        # and a match is reported without echoing it, so CI logs stay clean too.

    sitemap = open("sitemap.xml", encoding="utf-8").read()
    for loc in re.findall(r"<loc>https://mathurishan\.github\.io/([^<]*)</loc>", sitemap):
        if not os.path.exists(loc or "index.html"):
            problems.append(f"sitemap.xml lists a missing page: {loc}")

    # Private terms are checked against every served text file (pages, scripts, data, the
    # build tools), and a match is reported without echoing it, so CI logs stay clean too.
    for path in served_text_files():
        text = open(path, encoding="utf-8", errors="replace").read()
        if any(re.search(t, text, re.I) for t in private):
            problems.append(f"{path}: contains a private term (see tools/private_terms.txt)")

    # In CI the check must not silently pass because the secret is missing. Pull requests
    # from forks get no secrets, so they are the one exception.
    in_ci = os.environ.get("GITHUB_ACTIONS") == "true"
    from_fork = os.environ.get("GITHUB_EVENT_NAME") == "pull_request" and os.environ.get("IS_FORK") == "true"
    if not private and in_ci and not from_fork:
        problems.append("PRIVATE_TERMS secret is missing or empty, so the private-term check could not run")

    if problems:
        print(f"{len(problems)} problem(s):")
        for line in problems:
            print("  -", line)
        sys.exit(1)
    note = "" if private else " Private-term check skipped: no PRIVATE_TERMS or tools/private_terms.txt."
    print(f"All checks passed ({len(pages)} pages).{note}")


if __name__ == "__main__":
    main()
