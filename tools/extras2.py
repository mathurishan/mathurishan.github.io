"""More project-page sections: retail chart, raw-to-model comparison, DAX showcases."""
import html
import json
import re

E = html.escape

# ------------------------------------------------------------------ DAX highlighting

DAX_KEYWORDS = {"VAR", "RETURN", "IN", "NOT", "TRUE", "FALSE", "DESC", "ASC", "DENSE", "SKIP", "AND", "OR"}
DAX_TOKEN = re.compile(r"(//[^\n]*)|(\"(?:[^\"]|\"\")*\")|('[^']*'(?:\[[^\]]*\])?|[A-Za-z_][A-Za-z_0-9]*\[[^\]]*\]|\[[^\]]*\])"
                       r"|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z_0-9\.]*)(?=\s*\()|([A-Za-z_][A-Za-z_0-9]*)|(\s+|.)")


MEASURE_NAME = re.compile(r"^(?!VAR\b)([^\s/][^=\n]*?)(\s=)", re.M)


def highlight_dax(code):
    """Colour a DAX snippet. Measure names (text before ' =' at the start of a line) get their own colour."""
    parts, last = [], 0
    for m in MEASURE_NAME.finditer(code):
        parts.append(_dax_tokens(code[last:m.start()]))
        parts.append(f'<span class="tok-m">{E(m.group(1))}</span>{E(m.group(2))}')
        last = m.end()
    parts.append(_dax_tokens(code[last:]))
    return "".join(parts)


def _dax_tokens(code):
    out = []
    for c, s, ref, n, fn, w, other in DAX_TOKEN.findall(code):
        if c:
            out.append(f'<span class="tok-c">{E(c)}</span>')
        elif s:
            out.append(f'<span class="tok-s">{E(s)}</span>')
        elif ref:
            out.append(f'<span class="tok-r">{E(ref)}</span>')
        elif n:
            out.append(f'<span class="tok-n">{E(n)}</span>')
        elif fn:
            out.append(f'<span class="tok-f">{E(fn)}</span>')
        elif w:
            out.append(f'<span class="tok-k">{E(w)}</span>' if w in DAX_KEYWORDS else E(w))
        else:
            out.append(E(other))
    return "".join(out)


def code_tabs(section_id, title, sub_html, tabs, copy_label):
    """tabs: list of (tab label, intro sentence, code, language)."""
    heads, panels = [], []
    for i, (label, intro, code, lang) in enumerate(tabs):
        key = f"{section_id}-{i}"
        heads.append(f'<button type="button" role="tab" id="tab-{key}" aria-controls="panel-{key}" '
                     f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{E(label)}</button>')
        body = highlight_dax(code) if lang == "dax" else E(code)
        panels.append(f'''<div class="code-panel" role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}"{"" if i == 0 else " hidden"}>
            <p class="why">{intro}</p>
            <pre><code>{body}</code></pre>
          </div>''')
    return f'''
    <section class="section" id="{section_id}" aria-labelledby="{section_id}-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="{section_id}-title">{E(title)}</h2>
          {sub_html}
        </div>
        <div class="code-card rise" data-tabs>
          <div class="code-tabs" role="tablist" aria-label="{E(title)}">
            {"".join(heads)}
            <button type="button" class="copy" data-copy-code>{E(copy_label)}</button>
          </div>
          {"".join(panels)}
        </div>
      </div>
    </section>
'''


# ------------------------------------------------------------------ retail DAX

RETAIL_DAX = [
    ("Core measures", "<b>Base measures.</b> Every visual builds on a handful of explicit measures over the sales fact table, so a number means the same thing on every page.",
     """Gross Sales =
SUM ( Sales[Gross Sales] )

Return Value =
SUM ( Sales[Return Value] )

Net Sales =
[Gross Sales] - [Return Value]

Actual Demand =
SUM ( Sales[Demand Units] )

Return Rate % =
DIVIDE ( SUM ( Sales[Returned Units] ), [Actual Demand] )"""),
    ("Week on week", "<b>Time intelligence.</b> The data runs week by week, so the trend compares each week with the one before it, ignoring any other date filter.",
     """Net Sales Prior Week =
VAR CurrentWeek = MAX ( 'Date'[Week Number] )
RETURN
    CALCULATE (
        [Net Sales],
        REMOVEFILTERS ( 'Date' ),
        'Date'[Week Number] = CurrentWeek - 1
    )

Net Sales WoW % =
VAR PriorWeek = [Net Sales Prior Week]
RETURN
    IF (
        NOT ISBLANK ( PriorWeek ),
        DIVIDE ( [Net Sales] - PriorWeek, PriorWeek )
    )"""),
    ("Targets and ranking", "<b>Business rules.</b> The 2% return-rate target drives the red flags on the category pages, and the ranking follows whatever the report is filtered to.",
     """Return Rate Target = 0.02

Return Rate Status =
IF (
    [Return Rate %] > [Return Rate Target],
    "Above target",
    "Within target"
)

Category Rank =
RANKX (
    ALLSELECTED ( Product[Category] ),
    [Net Sales],
    ,
    DESC,
    DENSE
)

Snack and Bread Share =
DIVIDE (
    CALCULATE ( [Net Sales], Product[Category] IN { "Snack", "Bread" } ),
    CALCULATE ( [Net Sales], ALLSELECTED ( Product[Category] ) )
)"""),
    ("Field parameter", "<b>One visual, three breakdowns.</b> The Parameter buttons on the overview swap the chart between sales channel, purchaser and product category.",
     """Breakdown =
{
    ( "Sales Channel", NAMEOF ( Channel[Sales Channel] ), 0 ),
    ( "Purchaser", NAMEOF ( Purchaser[Purchaser] ), 1 ),
    ( "Product Category", NAMEOF ( Product[Category] ), 2 )
}"""),
]

AIRNZ_DAX = [
    ("Reliability KPIs", "<b>Headline measures.</b> The six cards on the executive summary come from a dedicated measures table, so rates are always recalculated from their parts.",
     """Total Arrivals =
SUM ( 'Table 1'[Arrival] )

Total Departures =
SUM ( 'Table 1'[Departure] )

Cancellations =
SUM ( 'Monthly Summary'[Cancelled Sectors] )

Scheduled Sectors =
SUM ( 'Monthly Summary'[Scheduled Sectors] )

Cancellation Rate =
DIVIDE ( [Cancellations], [Scheduled Sectors] )

Arrival OTP =
DIVIDE (
    SUM ( 'Monthly Summary'[On-time Arrivals] ),
    SUM ( 'Monthly Summary'[Flown Arrivals] )
)"""),
    ("Year on year", "<b>Recovery trend.</b> Year-on-year change drives the demand page; it stays blank where there is no prior year to compare with.",
     """Arrivals YoY % =
VAR ThisPeriod = [Total Arrivals]
VAR LastYear =
    CALCULATE ( [Total Arrivals], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
RETURN
    IF (
        NOT ISBLANK ( LastYear ),
        DIVIDE ( ThisPeriod - LastYear, LastYear )
    )

Departures YoY % =
VAR ThisPeriod = [Total Departures]
VAR LastYear =
    CALCULATE ( [Total Departures], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
RETURN
    IF (
        NOT ISBLANK ( LastYear ),
        DIVIDE ( ThisPeriod - LastYear, LastYear )
    )"""),
    ("Capacity and scenarios", "<b>What-if analysis.</b> Capacity measures feed the operational page, and the scenario slicer on the forecast page switches every visual at once.",
     """Capacity Utilisation =
DIVIDE (
    SUM ( 'Monthly Summary'[Seats Flown] ),
    SUM ( 'Monthly Summary'[Seats Scheduled] )
)

Net Engine Impact =
SUM ( 'Engine Availability & Compensation'[Compensation] )
    - SUM ( 'Engine Availability & Compensation'[Lost Revenue] )

Scenario RPK =
VAR SelectedScenario =
    SELECTEDVALUE ( 'Forecast & What-If Scenarios'[Scenario], "Base" )
RETURN
    CALCULATE (
        SUM ( 'Forecast & What-If Scenarios'[ForecastRPK] ),
        'Forecast & What-If Scenarios'[Scenario] = SelectedScenario
    )"""),
]


def dax_showcase(kind):
    tabs = RETAIL_DAX if kind == "retail" else AIRNZ_DAX
    return code_tabs("dax", "The DAX", '<span class="muted">Measures behind the report</span>',
                     [(label, intro, code, "dax") for label, intro, code in tabs], "Copy DAX")


# ------------------------------------------------------------------ retail chart (from the report's category table)

RETAIL_CATEGORIES = [
    # category, net sales (NZD), actual demand (units), return rate (%) — Product and Category Performance page
    ("Snack", 2607154.02, 325482, 0.8),
    ("Bread", 2280960.03, 111482, 3.6),
    ("Bun", 900037.21, 51910, 1.7),
    ("Tortilla", 560576.50, 42406, 2.5),
    ("Muffin", 344764.38, 39574, 0.8),
    ("Cake", 262698.16, 17314, 1.0),
    ("Donut", 146363.87, 18106, 2.8),
    ("Sandwich", 39747.36, 2348, 0.2),
    ("Breadcrumb", 30115.62, 3239, 1.4),
    ("Beverage", 1529.92, 292, 0.0),
]


def retail_chart():
    data = [{"label": c, "sales": round(s / 1e6, 3), "demand": d, "rate": r} for c, s, d, r in RETAIL_CATEGORIES]
    metrics = [{"key": "sales", "label": "Net sales", "prefix": "$", "suffix": "M", "decimals": 2},
               {"key": "demand", "label": "Demand"},
               {"key": "rate", "label": "Return rate", "suffix": "%", "decimals": 1, "threshold": 2}]
    seg = "".join(f'<button type="button" data-metric="{m["key"]}" aria-pressed="{"true" if i == 0 else "false"}">{E(m["label"])}</button>'
                  for i, m in enumerate(metrics))
    table = "".join(f'<tr><td>{E(c)}</td><td>${s:,.2f}</td><td>{d:,}</td><td>{r:.1f}%</td></tr>' for c, s, d, r in RETAIL_CATEGORIES)
    return f'''
    <section class="section" id="explore" aria-labelledby="explore-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="explore-title">Explore the data</h2>
          <span class="muted">Switch the measure to see the story change</span>
        </div>
        <div class="chart rise" data-chart="bar" data-metrics='{E(json.dumps(metrics))}'>
          <div class="chart-head">
            <div>
              <h3>Product categories</h3>
              <p>Net sales, demand and return rate by category, from the Product and Category Performance page.</p>
            </div>
            <div class="seg" aria-label="Measure">{seg}</div>
          </div>
          <div class="chart-canvas"></div>
          <p class="chart-note">On return rate, bars past the dashed line are above the 2% target.</p>
          <details>
            <summary>View as a table</summary>
            <table>
              <thead><tr><th>Category</th><th>Net sales</th><th>Demand</th><th>Return rate</th></tr></thead>
              <tbody>{table}</tbody>
            </table>
          </details>
          <script type="application/json">{json.dumps(data)}</script>
        </div>
      </div>
    </section>
'''


# ------------------------------------------------------------------ SQL: raw rows to modelled rows

def raw_to_model():
    raw = [("BLDQ.SF030002A1A", "2025.09", "949", "Number", "Waikato Region", "All buildings", "New", "Number"),
           ("BLDQ.SF030002A2A", "2025.09", "506230468", "Dollars", "Waikato Region", "All buildings", "New", "Value"),
           ("BLDQ.SF030002A3A", "2025.09", "191777", "SQM", "Waikato Region", "All buildings", "New", "Floor area")]
    fact = [("202507", "20", "1", "New", "292", "167,581,736", "60,950"),
            ("202508", "20", "1", "New", "340", "170,167,270", "59,421"),
            ("202509", "20", "1", "New", "317", "168,481,462", "71,406")]
    raw_rows = "".join("<tr>" + "".join(f"<td>{E(v)}</td>" for v in r) + "</tr>" for r in raw)
    fact_rows = "".join("<tr>" + "".join(f"<td>{E(v)}</td>" for v in r) + "</tr>" for r in fact)
    return f'''
    <section class="section" id="model" aria-labelledby="model-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="model-title">From raw CSV to star schema</h2>
          <span class="muted">Waikato, all buildings, new consents</span>
        </div>
        <div class="transform rise">
          <div class="t-card">
            <p class="t-label"><span>Before</span> Stats NZ publishes one row per measure</p>
            <div class="t-scroll">
              <table class="data-table">
                <thead><tr><th>Series_reference</th><th>Period</th><th>Data_value</th><th>Units</th><th>Series_title_1</th><th>Series_title_2</th><th>Series_title_3</th><th>Series_title_4</th></tr></thead>
                <tbody>{raw_rows}</tbody>
              </table>
            </div>
            <p class="t-foot">A sample of the long format from the December 2025 release (quarterly file, Q3 2025). Measures, geography and building type all sit in text columns.</p>
          </div>
          <div class="t-arrow" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v16M6 14l6 6 6-6"/></svg>
            <span>Pivot measures into columns, replace text with keys</span>
          </div>
          <div class="t-card">
            <p class="t-label"><span>After</span> fact_region_consents: one row per region, month, building type</p>
            <div class="t-scroll">
              <table class="data-table">
                <thead><tr><th>date_id</th><th>region_id</th><th>building_type_id</th><th>consent_nature</th><th>number_of_consents</th><th>value_nzd</th><th>floor_area_sqm</th></tr></thead>
                <tbody>{fact_rows}</tbody>
              </table>
            </div>
            <p class="t-foot">Keys join to dim_date, dim_region and dim_building_type, so every query filters and groups on clean dimensions.</p>
          </div>
          <div class="t-check">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3.5 8.5 3 3 6-7"/></svg>
            <p><strong>Reconciliation check:</strong> the three monthly fact rows add back to Stats NZ's published quarter exactly: 292 + 340 + 317 = 949 consents, $506,230,468 in value and 191,777 m² of floor area.</p>
          </div>
        </div>
      </div>
    </section>
'''


# ------------------------------------------------------------------ Air NZ: routes, head-to-head, gap to target

def airnz_chart():
    import os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "airnz_routes_may_oct_2025.json")
    d = json.load(open(path, encoding="utf-8"))
    routes, k, gap = d["routes"], d["kpis"], d["gap"]
    metrics = [{"key": "cancellations", "label": "Cancellations"},
               {"key": "rate", "label": "Cancellation rate", "suffix": "%", "decimals": 1, "threshold": 2},
               {"key": "otp", "label": "On-time arrivals", "suffix": "%", "decimals": 1, "threshold": 85, "below": True}]
    seg = "".join(f'<button type="button" data-metric="{m["key"]}" aria-pressed="{"true" if i == 0 else "false"}">{E(m["label"])}</button>'
                  for i, m in enumerate(metrics))
    table = "".join(f'<tr><td>{E(r["label"])}</td><td>{r["scheduled"]:,}</td><td>{r["cancellations"]}</td>'
                    f'<td>{r["rate"]:.1f}%</td><td>{r["otp"]:.1f}%</td></tr>' for r in routes)
    nz, js = k["Air NZ"], k["Jetstar"]

    def pct(v, dp=1):
        return f"{v * 100:.{dp}f}%"

    rows = [("Cancellation rate", pct(nz["cancellation_rate"]), pct(js["cancellation_rate"])),
            ("Arrival on-time rate", pct(nz["arrival_otp"]), pct(js["arrival_otp"])),
            ("Departure on-time rate", pct(nz["departure_otp"]), pct(js["departure_otp"])),
            ("Flight completion", pct(nz["flight_completion_rate"]), pct(js["flight_completion_rate"])),
            ("Sectors scheduled", f'{int(nz["sectors_scheduled"]):,}', f'{int(js["sectors_scheduled"]):,}')]
    h2h = "".join(f"<tr><th scope=\"row\">{E(a)}</th><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    extra_ot = round(float(gap["Extra on-time arrivals needed (to hit target)"]))
    avoid = round(float(gap["Cancellations to avoid (to hit target)"]))
    sched = int(gap["Scheduled sectors"])
    return f'''
    <section class="section" id="explore" aria-labelledby="explore-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="explore-title">Explore the data</h2>
          <span class="muted">Domestic network, May to October 2025</span>
        </div>
        <div class="chart rise" data-chart="bar" data-metrics='{E(json.dumps(metrics))}'>
          <div class="chart-head">
            <div>
              <h3>Top 20 routes by cancellations</h3>
              <p>Worst first on each measure. Targets: 2% cancellations, 85% on-time arrivals.</p>
            </div>
            <div class="seg" aria-label="Measure">{seg}</div>
          </div>
          <div class="chart-canvas"></div>
          <p class="chart-note">Highlighted bars miss the target on the selected measure.</p>
          <details>
            <summary>View as a table</summary>
            <table>
              <thead><tr><th>Route</th><th>Scheduled</th><th>Cancelled</th><th>Cancellation rate</th><th>On-time arrivals</th></tr></thead>
              <tbody>{table}</tbody>
            </table>
          </details>
          <script type="application/json">{json.dumps(routes, ensure_ascii=False)}</script>
        </div>

        <div class="duo rise">
          <div class="h2h">
            <h3>Air NZ against Jetstar</h3>
            <p class="muted">Domestic sectors, May to October 2025</p>
            <table>
              <thead><tr><th scope="col"></th><th scope="col">Air NZ</th><th scope="col">Jetstar</th></tr></thead>
              <tbody>{h2h}</tbody>
            </table>
          </div>
          <div class="gap">
            <h3>Gap to target</h3>
            <p class="muted">Air NZ's ten most-cancelled routes, {sched:,} scheduled sectors</p>
            <dl>
              <div><dt>{extra_ot:,}</dt><dd>more on-time arrivals needed to reach the 85% target</dd></div>
              <div><dt>{avoid}</dt><dd>fewer cancellations needed to reach the 2% target</dd></div>
            </dl>
          </div>
        </div>
      </div>
    </section>
'''


# ------------------------------------------------------------------ Air NZ: before and after slider

def before_after_airnz():
    import csv
    import os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "airnz_top20_routes_raw.csv")
    rows = list(csv.reader(open(path, encoding="utf-8")))
    head, body = rows[0], rows[1:17]
    cols = "".join(f"<th>{E(c) or '&nbsp;'}</th>" for c in ["", "A", "B", "C", "D", "E", "F", "G"][:len(head) + 1])
    header = "<tr><td>1</td>" + "".join(f"<th>{E(c)}</th>" for c in head) + "</tr>"
    lines = "".join("<tr><td>" + str(i + 2) + "</td>" + "".join(f"<td>{E(v)}</td>" for v in r) + "</tr>" for i, r in enumerate(body))
    return f'''
    <section class="section" id="before-after" aria-labelledby="ba-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="ba-title">Before and after</h2>
          <span class="muted">Drag the handle</span>
        </div>
        <div class="ba rise">
          <img src="images/projects/air-nz/executive-summary-overview.jpg" alt="The finished executive summary dashboard." width="1600" height="925" loading="lazy" />
          <div class="ba-raw" aria-hidden="true">
            <table>
              <thead><tr>{cols}</tr></thead>
              <tbody>{header}{lines}</tbody>
            </table>
          </div>
          <div class="ba-handle" aria-hidden="true"></div>
          <span class="ba-tag left">Raw CSV</span>
          <span class="ba-tag right">Dashboard</span>
          <input type="range" min="0" max="100" value="50" step="1" aria-label="Reveal the raw data or the finished dashboard" />
        </div>
        <p class="chart-note">Left: a route-level extract from the analysis, exactly as exported, unrounded. Right: the finished executive summary page.</p>
      </div>
    </section>
'''
