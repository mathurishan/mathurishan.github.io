"""Rebuild the generated pages.

Run from the site root:  python tools/build.py

Importing build_site writes the five project pages and the three redirect pages;
this file then writes resume.html and 404.html. index.html and economics-game.html
are edited by hand.
"""
import sys, os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import head, header, footer  # noqa: E402  (also rebuilds project pages)


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
          <li><a href="https://www.linkedin.com/in/mathurishan">linkedin.com/in/mathurishan</a></li>
          <li><a href="https://github.com/mathurishan">github.com/mathurishan</a></li>
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
              <a href="https://www.linkedin.com/in/mathurishan">LinkedIn</a>.</p>
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
           .replace('<meta name="theme-color"', '<meta name="robots" content="noindex" />\n  <meta name="theme-color"')) + '''
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
        <div class="article-body">
{n["body"]}
        </div>
        <div class="article-end">
          <span class="muted">Next note</span>
          <a class="next-note" href="{nxt["file"]}">{_html.escape(nxt["title"])} &rarr;</a>
        </div>
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

note_cards = "\n".join(f"""          <article class="note-card rise{" r" + str(i % 3) if i % 3 else ""}">
            <p class="n-meta">Note · {n["minutes"]} min read</p>
            <h3><a href="{n["file"]}">{_html.escape(n["title"])}</a></h3>
            <p>{_html.escape(n["card"])}</p>
            <span class="more">Read the note <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" /></svg></span>
          </article>""" for i, n in enumerate(NOTES))
notes_page = head("Notes | Ishan Mathur",
                  "Short notes by Ishan Mathur on reporting: validation, data modelling, automating recurring reports and reading public data honestly.",
                  "notes.html", "home", "website") + header("notes") + f"""
  <main id="main">
    <section class="case-hero">
      <div class="wrap">
        <p class="eyebrow">Notes</p>
        <h1>Notes on reporting</h1>
        <p class="lead">Short reads on how I build reporting people can trust: validation, modelling, automation and
          being honest about what the data can say.</p>
      </div>
    </section>
    <section class="section" aria-label="All notes">
      <div class="wrap">
        <div class="notes">
{note_cards}
        </div>
      </div>
    </section>
  </main>
""" + footer()
open("notes.html", "w", encoding="utf-8", newline="\n").write(notes_page)
print("wrote notes.html")


# --------------------------------------------------------------------------- sitemap

import datetime  # noqa: E402

SITEMAP_PAGES = ([""] + [p["file"] for p in __import__("build_site").PROJECTS]
                 + ["about.html", "notes.html", "resume.html"] + [n["file"] for n in NOTES])
today = datetime.date.today().isoformat()
lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
lines += [f"  <url><loc>https://mathurishan.github.io/{p}</loc><lastmod>{today}</lastmod></url>" for p in SITEMAP_PAGES]
lines.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("wrote sitemap.xml")
