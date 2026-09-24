"""Interactive chart and SQL showcase sections for the project pages."""
import html
import json
import re

import os
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def script_json(value, **kw):
    """JSON for a <script type="application/json"> block; "</" is escaped so data can't end the tag."""
    return json.dumps(value, ensure_ascii=False, **kw).replace("</", "<\\/")


SQL_FILE = os.path.join(DATA, "analysis_queries.sql")  # copy of the nz-building-consents-sql repo file
E = html.escape

# ------------------------------------------------------------------ SQL highlighting

KEYWORDS = {"SELECT", "FROM", "WHERE", "JOIN", "ON", "AND", "OR", "AS", "GROUP", "BY", "ORDER", "WITH", "OVER",
            "PARTITION", "ROWS", "BETWEEN", "PRECEDING", "CURRENT", "ROW", "CASE", "WHEN", "THEN", "END", "IS",
            "NOT", "NULL", "DESC", "ASC", "LIMIT", "HAVING", "IN", "DISTINCT", "UNION", "ALL", "LEFT", "INNER"}
FUNCS = {"SUM", "ROUND", "RANK", "LAG", "AVG", "COUNT", "NULLIF", "NTILE", "MAX", "MIN", "LEAD", "COALESCE", "CAST"}
TOKEN = re.compile(r"(--[^\n]*)|('(?:[^']|'')*')|(\b\d+(?:\.\d+)?(?:e\d+)?\b)|([A-Za-z_][A-Za-z_0-9]*)|(\s+|.)")


def highlight(sql):
    out = []
    for c, s, n, w, other in TOKEN.findall(sql):
        if c:
            out.append(f'<span class="tok-c">{E(c)}</span>')
        elif s:
            out.append(f'<span class="tok-s">{E(s)}</span>')
        elif n:
            out.append(f'<span class="tok-n">{E(n)}</span>')
        elif w:
            u = w.upper()
            if u in FUNCS:
                out.append(f'<span class="tok-f">{E(w)}</span>')
            elif u in KEYWORDS:
                out.append(f'<span class="tok-k">{E(w)}</span>')
            else:
                out.append(E(w))
        else:
            out.append(E(other))
    return "".join(out)


def query(number):
    """Return (business question, demonstrates, SQL body) for QUERY n in the repo file."""
    text = open(SQL_FILE, encoding="utf-8").read()
    start = text.index(f"-- QUERY {number}:")
    end = text.find("-- QUERY", start + 10)
    block = text[start:end if end != -1 else len(text)]
    header, _, body = block.partition("-- ============================================================================\n\n")
    q_lines = []
    capture = False
    for l in header.splitlines():
        if l.startswith("-- BUSINESS QUESTION:"):
            capture = True
            q_lines.append(l.split(":", 1)[1].strip())
            continue
        if l.startswith("-- Demonstrates"):
            capture = False
        elif capture and l.startswith("-- "):
            q_lines.append(l[3:].strip())
    demo = [l.split(":", 1)[1].strip() for l in header.splitlines() if l.startswith("-- Demonstrates")][0]
    body = body.strip()
    body = body.rsplit("\n\n\n", 1)[0].strip() if body.count("\n\n\n") else body
    return " ".join(q_lines), demo, body


def sql_showcase():
    picks = [(1, "Rank regions"), (2, "Year-on-year growth"), (7, "3-month moving average")]
    tabs, panels = [], []
    for i, (n, name) in enumerate(picks):
        q, demo, body = query(n)
        sel = "true" if i == 0 else "false"
        tabs.append(f'<button type="button" role="tab" id="sqltab-{n}" aria-controls="sqlpanel-{n}" '
                    f'aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{E(name)}</button>')
        panels.append(f'''<div class="code-panel" role="tabpanel" id="sqlpanel-{n}" aria-labelledby="sqltab-{n}"{"" if i == 0 else " hidden"}>
            <p class="why"><b>Query {n}.</b> {E(q)} <span class="tech">Techniques: {E(demo.rstrip("."))}.</span></p>
            <pre><code>{highlight(body)}</code></pre>
          </div>''')
    return f'''
    <section class="section" id="sql" aria-labelledby="sql-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="sql-title">The SQL</h2>
          <a class="muted" href="https://github.com/mathurishan/nz-building-consents-sql/blob/main/queries/analysis_queries.sql" target="_blank" rel="noopener">All ten queries on GitHub &rarr;</a>
        </div>
        <div class="code-card rise" data-tabs>
          <div class="code-tabs" role="tablist" aria-label="SQL queries">
            {"".join(tabs)}
            <button type="button" class="copy" data-copy-code>Copy SQL</button>
          </div>
          {"".join(panels)}
        </div>
      </div>
    </section>
'''


# ------------------------------------------------------------------ charts

def pipeline_chart():
    rows = json.load(open(os.path.join(DATA, "regional_pipeline_2025.json"), encoding="utf-8"))
    data = []
    for r in rows:
        label = r["region"].replace(" Region", "")
        label = "Manawatū-Whanganui" if label.startswith("Manawat") else label
        data.append({"label": label, "short": "Manawatū-Wh." if label.startswith("Manawat") else label,
                     "value": r["value"], "consents": r["consents"], "area": r["area"], "avg": r["avg"]})
    metrics = [{"key": "value", "label": "Consent value", "prefix": "$", "suffix": "M"},
               {"key": "consents", "label": "Consents"},
               {"key": "area", "label": "Floor area", "suffix": "k m²"},
               {"key": "avg", "label": "Value per consent", "prefix": "$"}]
    seg = "".join(f'<button type="button" data-metric="{m["key"]}" aria-pressed="{"true" if i == 0 else "false"}">{E(m["label"])}</button>'
                  for i, m in enumerate(metrics))
    table = "".join(f'<tr><td>{E(d["label"])}</td><td>${d["value"]:,.1f}M</td><td>{int(d["consents"]):,}</td>'
                    f'<td>{int(d["area"]):,}k m²</td><td>${int(d["avg"]):,}</td></tr>' for d in data)
    return f'''
    <section class="section" id="explore" aria-labelledby="explore-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="explore-title">Explore the data</h2>
          <span class="muted">Hover or tab through the bars</span>
        </div>
        <div class="chart rise" data-chart="bar" data-metrics='{E(json.dumps(metrics, ensure_ascii=False))}'>
          <div class="chart-head">
            <div>
              <h3>Regional building pipeline, 2025</h3>
              <p>New consents for all buildings, by region. Output of Query 1 below.</p>
            </div>
            <div class="seg" aria-label="Measure">{seg}</div>
          </div>
          <div class="chart-canvas"></div>
          <details>
            <summary>View as a table</summary>
            <div class="table-scroll">
              <table>
                <thead><tr><th>Region</th><th>Value</th><th>Consents</th><th>Floor area</th><th>Per consent</th></tr></thead>
                <tbody>{table}</tbody>
              </table>
            </div>
          </details>
          <script type="application/json">{script_json(data)}</script>
        </div>
      </div>
    </section>
'''


def rent_chart():
    data = json.load(open(os.path.join(DATA, "rent_by_region.json"), encoding="utf-8"))
    default = ["New Zealand", "Auckland", "Waikato", "Northland"]
    last = data["quarters"][-1]
    rows = sorted(data["series"].items(), key=lambda kv: -kv[1]["rent"][-1])
    table = "".join(f'<tr><td>{E(k)}</td><td>${v["rent"][0]}</td><td>${v["rent"][-1]}</td><td>{v["ratio"][-1]}%</td></tr>' for k, v in rows)
    return f'''
    <section class="section" id="explore" aria-labelledby="explore-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="explore-title">Explore the data</h2>
          <span class="muted">Pick up to five regions</span>
        </div>
        <div class="chart rise" data-chart="line" data-default='{E(json.dumps(default, ensure_ascii=False))}'>
          <div class="chart-head">
            <div>
              <h3>Rents by region, 2019 to 2025</h3>
              <p>Quarterly median weekly rent from MBIE tenancy bonds, and rent as a share of median household income.</p>
            </div>
            <div class="seg" aria-label="Measure">
              <button type="button" data-metric="rent" aria-pressed="true">Weekly rent</button>
              <button type="button" data-metric="ratio" aria-pressed="false">Share of income</button>
            </div>
          </div>
          <div class="chips" aria-label="Regions"></div>
          <div class="chart-canvas"></div>
          <p class="chart-note">Household income for 2019 to 2022 is backcast from observed 2023 to 2025 levels.</p>
          <details>
            <summary>View as a table</summary>
            <div class="table-scroll">
              <table>
                <thead><tr><th>Region</th><th>{E(data["quarters"][0])}</th><th>{E(last)}</th><th>Share of income, {E(last)}</th></tr></thead>
                <tbody>{table}</tbody>
              </table>
            </div>
          </details>
          <script type="application/json">{script_json(data, separators=(",", ":"))}</script>
        </div>
      </div>
    </section>
'''
