"""Rebuild the generated pages.

Run from the site root:  python tools/build.py

Importing build_site writes the five project pages and the three redirect pages;
this file then writes resume.html and 404.html. index.html and economics-game.html
are edited by hand.
"""
import sys, os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # every path below is site-relative
from build_site import head, header, footer, JS_V  # noqa: E402  (also rebuilds project pages)


def role(title, org, when, bullets):
    lis = "\n              ".join(f"<li>{b}</li>" for b in bullets)
    slug = "role-" + "-".join("".join(ch if ch.isalnum() else " " for ch in title.replace("&amp;", "")).lower().split())
    return f'''<div class="role" id="{slug}">
            <h3>{title}</h3>
            <p class="when">{org} · {when}</p>
            <ul>
              {lis}
            </ul>
          </div>
          '''


ROLES = [
    role("Technology Services &amp; Collections Analyst", "University of Waikato Library, Hamilton", "Jul 2026 – present", [
        "Built a privacy-conscious API reporting workflow, now in production with monthly runs and fortnightly reporting, that turns booking and questionnaire data into reusable analytical tables and excludes personal student contact details",
        "Cut recurring reporting work that previously took days to a matter of hours by automating data preparation and standardising templates",
        "Cleaned, joined and validated data from multiple Library systems in SQL into analysis-ready datasets and Power BI reporting models",
        "Consolidated three Library registers (Services, Technical Solutions and Integrations) into one searchable HTML dashboard giving leadership a single view of systems, ownership and integrations",
        "Used Google Analytics 4 across two Library web properties to show where users came from and what they used, informing resource-spend decisions",
        "Published every dashboard and report through SharePoint, each to the site of the team or stakeholder group it serves"]),
    role("Student Assistant, Library (Collections Strategy &amp; Access)", "University of Waikato, Hamilton", "Jul 2025 – Jun 2026 · part-time", [
        "Built operational Power BI dashboards tracking throughput, backlog, ageing and exceptions for reading-list processing of about 80–150 items a week at peak",
        "Applied DAX measures and Power Query transformations to standardise fields across multiple source systems and make them reporting-ready",
        "Designed QA controls catching incorrect editions, duplicate entries, invalid URLs and access errors earlier in the process"]),
    role("Sessional Assistant, Economics", "University of Waikato, Hamilton", "Jan 2026 – Jun 2026 · sessional", [
        "Facilitated tutorials for diverse postgraduate cohorts, translating economic theory into practical business applications and structured problem-solving approaches"]),
    role("Consultant, Data Operations &amp; Client Solutions", "Arcesium (a D.E. Shaw Group company), Gurugram", "Mar 2022 – Jun 2025", [
        "Investigated and resolved 10–20 reconciliation exceptions a day across cash, positions and P&amp;L, tracing data lineage to root cause and driving fixes through the correct operational owners",
        "Wrote SQL daily across SQL Server and MySQL for reconciliation logic, exception analysis, extracts and reporting for 10+ global investment clients",
        "Built operational Power BI dashboards providing visibility into break trends, workflow health and reporting status",
        "Supported client onboarding and data-migration workstreams, working directly with clients and counterparties on requirements, analysis and project coordination",
        "Managed multiple concurrent client workstreams end to end: requirements, build, test, release and ongoing support"]),
    role("Underwriting Analyst", "Better.com, Gurugram", "Sep 2021 – Mar 2022", [
        "Verified income, asset and liability documentation to audit-ready standards, catching discrepancies before files progressed to submission",
        "Assessed borrower documentation and calculated DTI and LTV ratios in a team processing 100+ mortgage applications a week under compliance deadlines"]),
]

resume = head("Résumé | Ishan Mathur",
              "Résumé of Ishan Mathur, Data & BI Analyst in New Zealand. 4+ years across higher education and financial services. Power BI, SQL, Excel. PMP®.",
              "resume.html", "resume", "profile") + header("resume") + f'''
  <main id="main">
    <section class="case-hero">
      <div class="wrap">
        <p class="eyebrow">Résumé</p>
        <h1>Ishan Mathur</h1>
        <p class="lead">Data &amp; BI Analyst · Power BI, SQL, Excel · PMP®. Hamilton, New Zealand. NZ work rights, no
          sponsorship required. Open to relocating anywhere in NZ.</p>
        <div class="actions cv-actions">
          <a class="btn btn-primary" href="files/Ishan-Mathur-Resume.pdf" download>
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2.5v8M4.5 7 8 10.5 11.5 7M3 13.5h10" /></svg>
            Download PDF
          </a>
          <button class="btn" type="button" data-copy="mathur.ishan11@gmail.com">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5.5" y="5.5" width="8" height="8" rx="1.5" /><path d="M10.5 5.5v-2a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2" /></svg>
            Copy email
          </button>
        </div>
        <ul class="tools-row cv-contact" aria-label="Contact">
          <li><a href="mailto:mathur.ishan11@gmail.com">mathur.ishan11@gmail.com</a></li>
          <li><a href="https://www.linkedin.com/in/mathurishan" target="_blank" rel="noopener">linkedin.com/in/mathurishan</a></li>
          <li><a href="https://github.com/mathurishan" target="_blank" rel="noopener">github.com/mathurishan</a></li>
        </ul>
        <dl class="glance" aria-label="Key achievements">
          <div><dt>&lt;1 hr</dt><dd>for a recurring reporting task that took about 4 hours, using reusable templates</dd></div>
          <div><dt data-count="40" data-suffix="%">40%</dt><dd>less time to produce daily reconciliation reporting for 10+ global investment clients</dd></div>
          <div><dt data-count="5" data-suffix="+">5+</dt><dd>dashboards and reports for senior Library leadership, client groups and third-party stakeholders</dd></div>
        </dl>
      </div>
    </section>

    <section class="case-body">
      <div class="wrap">
        <div class="cv-row rise">
          <h2>Summary</h2>
          <div class="body prose">
            <p>Data and BI analyst with 4+ years across higher education and financial services, and over a year of
              continuous New Zealand experience. I build the reporting layer between messy source systems and the people
              who need answers, in Power BI, SQL and Excel, and publish it through SharePoint to the teams who use it.</p>
          </div>
        </div>
        <div class="cv-row rise" id="experience">
          <h2>Experience</h2>
          <div class="body">
          {"".join(ROLES)}</div>
        </div>
        <div class="cv-row rise">
          <h2>Skills</h2>
          <div class="body">
            <ul class="plain">
              <li>Power BI: DAX, Power Query, data modelling</li>
              <li>SQL: SQL Server, MySQL</li>
              <li>Excel: Power Pivot, VBA</li>
              <li>SharePoint and Power Automate</li>
              <li>Tableau, Google Analytics 4, HTML reporting dashboards</li>
              <li>Python: pandas, ad-hoc scripting</li>
              <li>AI-assisted development (Claude Code)</li>
              <li>JIRA, Confluence, GitHub</li>
            </ul>
          </div>
        </div>
        <div class="cv-row rise">
          <h2>Education</h2>
          <div class="body">
            <div class="role">
              <h3>Master of Management (Business Analytics)</h3>
              <p class="when">University of Waikato · 2026</p>
            </div>
            <div class="role">
              <h3>MBA, Finance &amp; Financial Management</h3>
              <p class="when">IMT Ghaziabad, India · 2017 – 2019</p>
            </div>
            <div class="role">
              <h3>B.Tech, Electronics &amp; Communication Engineering</h3>
              <p class="when">IPEC Ghaziabad, India · 2012 – 2016</p>
            </div>
          </div>
        </div>
        <div class="cv-row rise">
          <h2>Certifications</h2>
          <div class="body">
            <ul class="plain">
              <li>Project Management Professional (PMP®), PMI · Active</li>
              <li>Harnessing the Power of Data with Power BI, Microsoft / Coursera · Mar 2024</li>
              <li>Extract, Transform and Load Data in Power BI, Microsoft / Coursera · Mar 2024</li>
              <li>Preparing Data for Analysis with Microsoft Excel, Microsoft / Coursera · Mar 2024</li>
              <li>Getting Started with Data Analytics on AWS, AWS · Apr 2022</li>
            </ul>
          </div>
        </div>
        <div class="cv-row rise">
          <h2>Referees</h2>
          <div class="body">
            <p>Professional referees available on request. Full profile on
              <a href="https://www.linkedin.com/in/mathurishan" target="_blank" rel="noopener">LinkedIn</a>.</p>
          </div>
        </div>
      </div>
    </section>
  </main>
''' + footer()
open("resume.html", "w", encoding="utf-8", newline="\n").write(resume)
print("wrote resume.html")

def _absolute(markup):
    """404.html can be served at any path, so its links must be root-relative."""
    markup = markup.replace('href="./', 'href="/')
    return re.sub(r'href="(?!https?:|mailto:|/|#)([^"]*)"', r'href="/\1"', markup)


page404 = (head("Page not found | Ishan Mathur", "This page doesn't exist or has moved.", "404.html", "home", "website")
           .replace('href="favicon', 'href="/favicon').replace('href="apple-touch', 'href="/apple-touch').replace('href="site.webmanifest', 'href="/site.webmanifest')
           .replace('href="assets/', 'href="/assets/')
           .replace('<meta name="theme-color"', '<meta name="robots" content="noindex" />\n  <meta name="theme-color"', 1))
# GitHub Pages serves this page at whatever URL failed, so it gets no canonical or og:url.
page404 = re.sub(r'  <(?:link rel="canonical"|meta property="og:url")[^>]*>\n', '', page404) + '''
''' + _absolute(header()) + '''
  <main id="main">
    <section class="hero">
      <div class="wrap">
        <p class="eyebrow">404</p>
        <h1>This page doesn't exist or has moved.</h1>
        <div class="actions">
          <a class="btn btn-primary" href="/">Go to the homepage</a>
          <a class="btn" href="/resume.html">Résumé</a>
        </div>
      </div>
    </section>
  </main>
  <script src="/assets/js/site.js?v=9" defer></script>
</body>

</html>
'''
page404 = page404.replace("site.js?v=9", f"site.js?v={JS_V}")
open("404.html", "w", encoding="utf-8", newline="\n").write(page404)
print("wrote 404.html")


# --------------------------------------------------------------------------- notes (short articles)

from notes import NOTES  # noqa: E402
import html as _html  # noqa: E402
import re as _re  # noqa: E402
import extras  # noqa: E402
import extras2  # noqa: E402


def _colour_code(body):
    """Syntax-colour <pre><code> blocks in a note: SQL if it reads like SQL, otherwise DAX."""
    def repl(m):
        code = _html.unescape(m.group(1))
        coloured = extras.highlight(code) if _re.search(r"\bSELECT\b", code) else extras2.highlight_dax(code)
        return f"<pre><code>{coloured}</code></pre>"
    return _re.sub(r"<pre><code>(.*?)</code></pre>", repl, body, flags=_re.S)


# Each note gets a small drawing of its idea: beside it in note lists, large at the top of the note,
# and on the "Next note" card. Hovering a list row or card plays the drawing; an article plays it on load.
NOTE_ART = {
    "note-every-dashboard-is-a-small-project.html": """<svg class="nv nv-plan" viewBox="0 0 160 100" aria-hidden="true">
        <g class="nv-faint"><rect x="8" y="12" width="144" height="12" rx="3" /><rect x="8" y="32" width="144" height="12" rx="3" /><rect x="8" y="52" width="144" height="12" rx="3" /><rect x="8" y="72" width="144" height="12" rx="3" /></g>
        <rect class="nv-fill nv-grow g1" x="8" y="12" width="36" height="12" rx="3" />
        <rect class="nv-fill nv-grow g2" x="36" y="32" width="50" height="12" rx="3" />
        <rect class="nv-fill nv-grow g3" x="76" y="52" width="46" height="12" rx="3" />
        <path class="nv-fill nv-one" d="M136 70l9 8-9 8-9-8z" />
        <path class="nv-tick nv-on-fill t3" pathLength="1" d="M132.5 78l2.5 2.5 4.5-5" />
      </svg>""",
    "note-one-name-for-every-system.html": """<svg class="nv nv-merge" viewBox="0 0 160 100" aria-hidden="true">
        <path class="nv-flow m1" pathLength="1" d="M50 20 C78 20 78 50 104 50" />
        <path class="nv-flow m2" pathLength="1" d="M50 50 L104 50" />
        <path class="nv-flow m3" pathLength="1" d="M50 80 C78 80 78 50 104 50" />
        <g class="nv-regs"><rect x="8" y="10" width="42" height="20" rx="3" /><rect x="8" y="40" width="42" height="20" rx="3" /><rect x="8" y="70" width="42" height="20" rx="3" /></g>
        <g class="nv-regl"><rect x="14" y="18" width="22" height="4" rx="2" /><rect x="14" y="48" width="28" height="4" rx="2" /><rect x="14" y="78" width="18" height="4" rx="2" /></g>
        <rect class="nv-fill nv-one" x="104" y="34" width="48" height="32" rx="5" />
        <rect class="nv-onel" x="112" y="48" width="32" height="4" rx="2" />
      </svg>""",
    "note-a-number-needs-a-sentence.html": """<svg class="nv nv-say" viewBox="0 0 160 100" aria-hidden="true">
        <g class="nv-bars"><rect x="10" y="62" width="14" height="28" /><rect x="28" y="46" width="14" height="44" /></g>
        <rect class="nv-fill" x="46" y="30" width="14" height="60" />
        <path class="nv-bubble" d="M78 12h66a8 8 0 0 1 8 8v30a8 8 0 0 1-8 8H94l-14 12 2-12a8 8 0 0 1-12-8V20a8 8 0 0 1 8-8z" />
        <rect class="nv-line nv-write w1" x="82" y="24" width="58" height="5" rx="2.5" />
        <rect class="nv-line nv-write w2" x="82" y="34" width="46" height="5" rx="2.5" />
        <rect class="nv-fill nv-write w3" x="82" y="44" width="28" height="5" rx="2.5" />
      </svg>""",
    "note-half-a-day-to-under-an-hour.html": """<svg class="nv nv-time" viewBox="0 0 160 100" aria-hidden="true">
        <text class="nv-label" x="8" y="26">Before</text>
        <rect class="nv-track" x="8" y="32" width="144" height="14" rx="3" />
        <rect class="nv-before nv-grow" x="8" y="32" width="144" height="14" rx="3" />
        <text class="nv-label" x="8" y="66">After</text>
        <rect class="nv-track" x="8" y="72" width="144" height="14" rx="3" />
        <rect class="nv-fill nv-grow nv-after" x="8" y="72" width="26" height="14" rx="3" />
      </svg>""",
    "note-validate-before-you-visualise.html": """<svg class="nv nv-checks" viewBox="0 0 160 100" aria-hidden="true">
        <circle class="nv-ring" cx="36" cy="50" r="18" /><circle class="nv-ring" cx="80" cy="50" r="18" /><circle class="nv-ring" cx="124" cy="50" r="18" />
        <path class="nv-tick t1" pathLength="1" d="M28 50l6 6 11-12" /><path class="nv-tick t2" pathLength="1" d="M72 50l6 6 11-12" /><path class="nv-tick t3" pathLength="1" d="M116 50l6 6 11-12" />
      </svg>""",
    "note-start-with-a-star-schema.html": """<svg class="nv nv-star" viewBox="0 0 160 100" aria-hidden="true">
        <g class="nv-links"><line x1="80" y1="50" x2="80" y2="14" /><line x1="80" y1="50" x2="80" y2="86" /><line x1="80" y1="50" x2="26" y2="50" /><line x1="80" y1="50" x2="134" y2="50" /></g>
        <g class="nv-dims"><rect class="d-n" x="64" y="6" width="32" height="14" rx="3" /><rect class="d-s" x="64" y="80" width="32" height="14" rx="3" /><rect class="d-w" x="8" y="43" width="32" height="14" rx="3" /><rect class="d-e" x="120" y="43" width="32" height="14" rx="3" /></g>
        <rect class="nv-fill" x="62" y="38" width="36" height="24" rx="4" />
      </svg>""",
    "note-reading-rent-data-honestly.html": """<svg class="nv nv-hist" viewBox="0 0 160 100" aria-hidden="true">
        <g class="nv-bars"><rect x="14" y="74" width="14" height="16" /><rect x="32" y="56" width="14" height="34" /><rect x="50" y="32" width="14" height="58" /><rect x="68" y="22" width="14" height="68" /><rect x="86" y="40" width="14" height="50" /><rect x="104" y="60" width="14" height="30" /><rect x="122" y="72" width="14" height="18" /><rect x="140" y="80" width="10" height="10" /></g>
        <line class="nv-median" x1="76" y1="8" x2="76" y2="94" />
        <text class="nv-label" x="81" y="14">median</text>
      </svg>""",
}
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" /></svg>'



def note_rows(notes, numbered_from=1):
    """Numbered list rows with each note's drawing, shared by the notes page and the homepage."""
    return "\n".join(f"""          <li class="note-row nv-host rise{" r" + str(i) if 0 < i < 4 else ""}">
            <span class="nr-num" aria-hidden="true">{i + numbered_from:02d}</span>
            <div class="nr-text">
              <h3><a href="{n["file"]}">{_html.escape(n["title"])}</a></h3>
              <p>{_html.escape(n["card"])}</p>
              <span class="n-meta">{n["minutes"]} min read</span>
            </div>
            <div class="nr-art">
      {NOTE_ART[n["file"]]}
            </div>
            <span class="nr-go">{ARROW}</span>
          </li>""" for i, n in enumerate(notes))


for i, n in enumerate(NOTES):
    n["body"] = _colour_code(n["body"])
    nxt = NOTES[(i + 1) % len(NOTES)]
    page = head(f'{n["title"]} | Ishan Mathur', n["desc"], n["file"], "home") + header("notes") + f'''
  <div class="progress" aria-hidden="true"></div>
  <main id="main">
    <article class="article">
      <div class="wrap">
        <a class="back" href="notes.html">&larr; All notes</a>
        <p class="eyebrow">Note</p>
        <h1>{_html.escape(n["title"])}</h1>
        <p class="lead">{_html.escape(n["lead"])}</p>
        <div class="byline"><span>Ishan Mathur</span><span>September 2026</span><span>{n["minutes"]} min read</span></div>
        <div class="article-art nv-auto rise">
      {NOTE_ART[n["file"]]}
        </div>
        <div class="article-body">
{n["body"]}
        </div>
        <a class="next-card nv-host" href="{nxt["file"]}">
          <span class="nc-art">
      {NOTE_ART[nxt["file"]]}
          </span>
          <span class="nc-text">
            <span class="nc-label">Next note</span>
            <span class="nc-title">{_html.escape(nxt["title"])}</span>
            <span class="n-meta">{nxt["minutes"]} min read</span>
          </span>
          <span class="nr-go">{ARROW}</span>
        </a>
      </div>
    </article>
  </main>
''' + footer()
    open(n["file"], "w", encoding="utf-8", newline="\n").write(page)
    print("wrote", n["file"])


# --------------------------------------------------------------------------- about and notes index

import about_content  # noqa: E402

ABOUT_ACTIONS = """        <div class="actions">
          <a class="btn btn-primary" href="resume.html">Résumé</a>
          <a class="btn" href="files/Ishan-Mathur-Resume.pdf" download>Download PDF</a>
          <a class="btn" href="how-i-work.html">How I work</a>
          <button class="btn" type="button" data-copy="mathur.ishan11@gmail.com">Copy email</button>
        </div>"""

about_page = head("About | Ishan Mathur",
                  "About Ishan Mathur: Data & BI Analyst in New Zealand. Background, experience timeline and where each tool shows up across projects and roles.",
                  "about.html", "home", "profile", html_class="has-subnav") + header("about") + f"""
  <main id="main">
    <section class="case-hero">
      <div class="wrap">
        <p class="eyebrow">About</p>
        <h1>Ishan Mathur</h1>
        <p class="lead">Data &amp; BI Analyst in Hamilton, New Zealand. I build the reporting layer between messy source
          systems and the people who need answers.</p>
{ABOUT_ACTIONS}
      </div>
    </section>
{about_content.BACKGROUND}{about_content.EXPERIENCE}{about_content.TOOLS}{about_content.STATEMENT}  </main>
""" + footer()
open("about.html", "w", encoding="utf-8", newline="\n").write(about_page)
print("wrote about.html")

index_rows = note_rows(NOTES)
notes_page = head("Notes | Ishan Mathur",
                  "Short notes by Ishan Mathur on reporting: validation, data modelling, automating recurring reports and reading public data honestly.",
                  "notes.html", "home", "website") + header("notes") + f"""
  <main id="main">
    <section class="case-hero notes-hero">
      <div class="wrap">
        <p class="eyebrow">Notes</p>
        <h1>Notes on reporting</h1>
        <svg class="nh-line" viewBox="0 0 320 36" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M2 32 L40 27 L78 29 L118 19 L158 22 L200 12 L240 14 L280 7 L318 3" /></svg>
        <p class="lead">Short reads on how I build reporting people can trust: validation, modelling, automation and
          being honest about what the data can say.</p>
        <dl class="nh-stats">
          <div><dt>Notes</dt><dd>{len(NOTES)}</dd></div>
          <div><dt>Minutes to read them all</dt><dd>{sum(n["minutes"] for n in NOTES)}</dd></div>
        </dl>
      </div>
    </section>
    <section class="section notes-list" aria-labelledby="notes-list-title">
      <div class="wrap">
        <h2 class="sr-only" id="notes-list-title">All notes</h2>
        <ol class="note-index">
{index_rows}
        </ol>
      </div>
    </section>
  </main>
""" + footer()
open("notes.html", "w", encoding="utf-8", newline="\n").write(notes_page)
print("wrote notes.html")

home = open("index.html", encoding="utf-8").read()
start, end = "<!-- notes:start -->", "<!-- notes:end -->"
home = (home[:home.index(start) + len(start)] + "\n        <ol class=\"note-index\">\n" + note_rows(NOTES[:3])
        + "\n        </ol>\n        " + home[home.index(end):])
open("index.html", "w", encoding="utf-8", newline="\n").write(home)
print("updated notes on index.html")


# --------------------------------------------------------------------------- how I work

HOW_ART = {
    "decide": """<svg class="nv nv-aim" viewBox="0 0 160 100" aria-hidden="true">
        <circle class="nv-ring" cx="80" cy="50" r="38" /><circle class="nv-ring" cx="80" cy="50" r="25" />
        <circle class="nv-fill" cx="80" cy="50" r="11" />
        <path class="nv-tick t2" pathLength="1" d="M146 14 L91.4 43.8" /><path class="nv-tick t3" pathLength="1" d="M102.4 44.1 L91.4 43.8 L97.1 34.4" />
      </svg>""",
    "handover": """<svg class="nv nv-doc" viewBox="0 0 160 100" aria-hidden="true">
        <path class="nv-bubble" d="M44 8h52l16 16v68a4 4 0 0 1-4 4H44a4 4 0 0 1-4-4V12a4 4 0 0 1 4-4z" />
        <path class="nv-bubble" d="M96 8v16h16" />
        <rect class="nv-line nv-write w1" x="50" y="34" width="50" height="5" rx="2.5" />
        <rect class="nv-line nv-write w2" x="50" y="46" width="40" height="5" rx="2.5" />
        <rect class="nv-line nv-write w3" x="50" y="58" width="46" height="5" rx="2.5" />
        <circle class="nv-fill" cx="118" cy="78" r="16" />
        <path class="nv-tick nv-on-fill t3" pathLength="1" d="M110 78l6 6 10-11" />
      </svg>""",
}

STEPS = [
    ("Start with the decision", HOW_ART["decide"],
     "Before touching any data I ask what decision the report supports and who will read it. I work with managers and "
     "staff to turn reporting needs into practical dashboards, metrics and reporting frameworks.",
     "At Arcesium I gathered requirements from global investment clients and led structured discussions to clarify "
     "ambiguous business logic in reconciliation rules, which cut misalignment and rework between teams.",
     [("note-every-dashboard-is-a-small-project.html", "Every dashboard is a small project"),
      ("resume.html", "Résumé")]),
    ("Model the data", NOTE_ART["note-start-with-a-star-schema.html"],
     "I decide what one row means, then build a star schema: a fact table and a few clean dimensions, with one agreed "
     "name for everything.",
     "At Arcesium I designed data models on star and snowflake schema principles across multiple client datasets. "
     "In the Library I brought 58 systems under one naming layer, so every name means one thing.",
     [("note-start-with-a-star-schema.html", "Why my reports start with a star schema"),
      ("note-one-name-for-every-system.html", "One name for every system")]),
    ("Validate before building", NOTE_ART["note-validate-before-you-visualise.html"],
     "Totals add back to a trusted figure, the grain is written down, partial periods stay out of trends and personal "
     "data stays out of the release.",
     "Validation checks and SQL control routines cut the time to produce daily reconciliation reporting for 10+ global "
     "investment clients by 40%. A monthly Library report runs 36 cross-checks against its evidence workbook, and "
     "its release stops if any personal text survives.",
     [("note-validate-before-you-visualise.html", "Validate before you visualise"),
      ("sql-nz-building-consents.html", "NZ Building Consents project")]),
    ("Build for the reader", NOTE_ART["note-a-number-needs-a-sentence.html"],
     "Every page leads with a sentence that says what the chart shows. Labels use the reader's words, and "
     "disagreements in the data are shown, not hidden.",
     "I have built 5+ dashboards and reports for senior Library leadership, client groups and third-party "
     "stakeholders, covering Library service, technology and usage data.",
     [("note-a-number-needs-a-sentence.html", "A number needs a sentence"),
      ("powerbi-retail.html", "Retail Sales &amp; Returns dashboard")]),
    ("Automate the repeat work", NOTE_ART["note-half-a-day-to-under-an-hour.html"],
     "Anything that happens every month should be a template or a workflow, not a rebuild. The time saved goes back "
     "into the analysis.",
     "Reusable templates cut a recurring reporting task from about half a day to under an hour, and an API reporting "
     "workflow now runs monthly in production, with fortnightly reporting.",
     [("note-half-a-day-to-under-an-hour.html", "Half a day to under an hour")]),
    ("Document and hand over", HOW_ART["handover"],
     "I write down metric definitions, how every number traces to its source and how to refresh the report, then "
     "publish it where the people who use it will find it.",
     "On a Power BI prototype bringing three systems into one view, an evidence workbook of 11 tabs and 109 formulas "
     "traces every number to its source, and a written refresh procedure lets someone else continue it. Every Library "
     "dashboard and report is published through SharePoint to the site of the team it serves.",
     [("about.html", "About me")]),
]

# The PMI project lifecycle each step belongs to, shown beside its step number.
PHASES = ["Initiating", "Planning", "Monitoring &amp; controlling", "Executing", "Executing", "Closing"]
PHASE_SHORT = ["Initiate", "Plan", "Control", "Execute", "Execute", "Close"]

CHECK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 8.5l2.5 2.5L12 5.5" /></svg>'


def _figures(text):
    """Set the numbers in an evidence line apart so they can be skimmed."""
    return re.sub(r"(?<![\w-])(\d[\d,]*(?:\+|%)?)", r'<b class="hs-fig">\1</b>', text)


step_items = "\n".join(f"""          <li class="how-step nv-host rise" id="step-{i + 1}">
            <span class="hs-node" aria-hidden="true">{i + 1:02d}</span>
            <div class="hs-card">
              <div class="hs-text">
                <p class="hs-kicker">Step {i + 1:02d}<span class="hs-phase">{PHASES[i]}</span></p>
                <h2>{title}</h2>
                <p class="hs-what">{what}</p>
                <div class="hs-proof">
                  <p class="hs-proof-label"><span class="hs-badge">{CHECK}</span>In practice</p>
                  <p>{_figures(proof)}</p>
                </div>
                <p class="hs-links">{"".join(f'<a href="{h}">{t} {ARROW}</a>' for h, t in links)}</p>
              </div>
              <div class="hs-art">
                <span class="hs-water" aria-hidden="true">{i + 1:02d}</span>
      {art}
              </div>
            </div>
          </li>""" for i, (title, art, what, proof, links) in enumerate(STEPS))

step_map = "\n".join(f'            <li><a href="#step-{i + 1}"><span>{i + 1:02d}</span>{title}<small>{PHASE_SHORT[i]}</small></a></li>'
                     for i, (title, *_rest) in enumerate(STEPS))

how_page = head("How I work | Ishan Mathur",
                "How Ishan Mathur, PMP®, approaches a reporting job as a small project: start with the decision, model the data, validate, build for the reader, automate the repeat work, document and hand over.",
                "how-i-work.html", "home", "website") + header("how") + f"""
  <main id="main">
    <section class="case-hero notes-hero how-hero">
      <div class="wrap how-hero-grid">
        <div>
          <p class="eyebrow">Process</p>
          <h1>How I work</h1>
          <svg class="nh-line" viewBox="0 0 320 36" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M2 32 L40 27 L78 29 L118 19 L158 22 L200 12 L240 14 L280 7 L318 3" /></svg>
          <p class="lead">Six steps I follow on every reporting job, from the first question to the handover. Each
            one is backed by work I have delivered, and links to it.</p>
          <p class="how-pmp">I run each job as a small project. As a Project Management Professional (PMP®), I map
            every step to the project lifecycle: initiate, plan, execute, monitor and control, close.
            <a href="note-every-dashboard-is-a-small-project.html">Why it works at the size of a report {ARROW}</a></p>
        </div>
        <nav class="how-map" aria-label="The six steps">
          <p class="how-map-title">The six steps</p>
          <ol>
{step_map}
          </ol>
        </nav>
      </div>
    </section>
    <section class="section how-body" aria-label="Six steps">
      <div class="wrap">
        <ol class="how-steps">
{step_items}
        </ol>
      </div>
    </section>
    <section class="section band how-cta" aria-labelledby="how-cta-title">
      <div class="wrap">
        <p class="eyebrow">Next step</p>
        <h2 class="display rise" id="how-cta-title">Hiring for a data, BI or reporting role? I'd be glad to talk it through.</h2>
        <div class="actions">
          <a class="btn btn-primary" href="resume.html">View résumé</a>
          <button class="btn" type="button" data-copy="mathur.ishan11@gmail.com">Copy email</button>
          <a class="btn" href="https://www.linkedin.com/in/mathurishan" target="_blank" rel="noopener">LinkedIn</a>
        </div>
      </div>
    </section>
  </main>
""" + footer(dark=True)
open("how-i-work.html", "w", encoding="utf-8", newline="\n").write(how_page)
print("wrote how-i-work.html")


# --------------------------------------------------------------------------- sitemap

import datetime  # noqa: E402

SITEMAP_PAGES = ([""] + [p["file"] for p in __import__("build_site").PROJECTS]
                 + ["about.html", "how-i-work.html", "notes.html", "resume.html", "economics-game.html"]
                 + [n["file"] for n in NOTES])
today = datetime.date.today().isoformat()


def lastmod(page):
    """Date of the page's last commit, so a rebuild doesn't mark every URL as changed today."""
    import subprocess
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", page or "index.html"],
                             capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        out = ""
    return out or today


lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
lines += [f"  <url><loc>https://mathurishan.github.io/{p}</loc><lastmod>{lastmod(p)}</lastmod></url>" for p in SITEMAP_PAGES]
lines.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("wrote sitemap.xml")
