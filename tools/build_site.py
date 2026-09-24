"""Generate the portfolio pages from one set of templates so every page shares
the same head, header, footer and components. Run from the site root."""
import html
import re
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extras
import extras2
import diagrams

SITE = "https://mathurishan.github.io/"
CSS_V = "11"
JS_V = "11"
FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:ital,opsz,wght@"
         "0,6..72,400;0,6..72,500;1,6..72,400&display=swap")
ARROW = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>')
E = html.escape


def head(title, desc, path, og, og_type="article", html_class=""):
    cls = f' class="{html_class}"' if html_class else ""
    return f'''<!DOCTYPE html>
<html lang="en"{cls}>

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}" />
  <link rel="canonical" href="{SITE}{path}" />
  <meta property="og:title" content="{E(title)}" />
  <meta property="og:description" content="{E(desc)}" />
  <meta property="og:image" content="{SITE}images/social/{og}.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:url" content="{SITE}{path}" />
  <meta property="og:type" content="{og_type}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="theme-color" content="#faf9f5" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#1a1917" media="(prefers-color-scheme: dark)" />
  <link rel="icon" href="favicon.ico?v=3" sizes="any">
  <link rel="icon" type="image/svg+xml" href="favicon.svg?v=3">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png?v=3">
  <link rel="apple-touch-icon" href="apple-touch-icon.png?v=3">
  <link rel="manifest" href="site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/site.css?v={CSS_V}" />
  <script>(function(){{var d=document.documentElement;d.classList.add('js');try{{var t=localStorage.getItem('theme');if(t==='light'||t==='dark'){{d.setAttribute('data-theme',t);}}}}catch(e){{}}}})()</script>
</head>
'''


def header(current=None, home=False):
    """Site header. `current` is one of work, about, notes, resume, contact."""
    base = "" if home else "./"
    links = [(base + "#work", "Work", "work"), ("about.html", "About", "about"), ("notes.html", "Notes", "notes"),
             ("resume.html", "Résumé", "resume"), (base + "#contact", "Contact", "contact")]

    def a(href, label, key):
        cur = ' aria-current="page"' if current == key else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    nav = "\n          ".join(a(h, l, k) for h, l, k in links)
    sheet = "\n        ".join(a(h, l, k) for h, l, k in links)
    return f"""
<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="./">Ishan Mathur</a>
      <div class="header-end">
        <nav class="nav" aria-label="Main">
          {nav}
        </nav>
        <button class="search-btn" type="button" data-palette aria-label="Search the site (Ctrl+K)"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="m10.5 10.5 3 3"/></svg>Search<kbd>Ctrl K</kbd></button>
        <button class="theme-toggle" type="button" aria-label="Switch theme">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <mask id="theme-mask">
              <rect width="24" height="24" fill="#fff" />
              <circle class="shade" cx="30" cy="0" r="7" fill="#000" />
            </mask>
            <g mask="url(#theme-mask)">
              <circle class="core" cx="12" cy="12" r="5" />
            </g>
            <g class="rays" fill="none" stroke-width="1.6" stroke-linecap="round">
              <path d="M12 2.5v1.8M12 19.7v1.8M2.5 12h1.8M19.7 12h1.8M5.3 5.3l1.3 1.3M17.4 17.4l1.3 1.3M5.3 18.7l1.3-1.3M17.4 6.6l1.3-1.3" />
            </g>
          </svg>
        </button>
        <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu-sheet">
          <span class="bars" aria-hidden="true"><i></i><i></i></span><span class="menu-label">Menu</span>
        </button>
      </div>
    </div>
  </header>
  <div class="menu-sheet" id="menu-sheet" hidden>
    <nav aria-label="Menu">
        {sheet}
    </nav>
    <div class="menu-foot">
      <button class="menu-search" type="button" data-palette>Search the site</button>
      <a href="mailto:mathur.ishan11@gmail.com">mathur.ishan11@gmail.com</a>
    </div>
  </div>
"""


def footer(dark=False, links=None, charts=False):
    links = links or [("mailto:mathur.ishan11@gmail.com", "Email"),
                      ("https://www.linkedin.com/in/mathurishan", "LinkedIn"),
                      ("https://github.com/mathurishan", "GitHub")]
    cls = "site-footer on-band" if dark else "site-footer"
    chart_js = f'\n  <script src="assets/js/charts.js?v={JS_V}" defer></script>' if charts else ""
    items = "\n        ".join(f'<a href="{h}">{t}</a>' for h, t in links)
    return f'''
  <footer class="{cls}">
    <div class="wrap">
      <span>© 2026 Ishan Mathur</span>
      <nav aria-label="Footer">
        {items}
      </nav>
    </div>
  </footer>

  <script src="assets/js/site.js?v={JS_V}" defer></script>{chart_js}
</body>

</html>
'''


# --------------------------------------------------------------------------- projects

PROJECTS = [
    dict(
        file="powerbi-retail.html", og="retail", label="Power BI dashboard", tone="sand",
        title="Retail Sales & Returns Analysis",
        seo_title="Retail Sales & Returns Analysis (Power BI) | Ishan Mathur",
        desc="Power BI dashboard: sales, margin and returns across six linked pages, on a star-schema model with DAX time intelligence and drill-through pages.",
        lead="A six-page sales, margin and returns dashboard on a star-schema model, with DAX time intelligence and drill-through pages.",
        tools=["Power BI", "DAX", "Power Query", "Star schema"],
        link=("files/Retail-Sales-Returns-Analysis.pdf", "Full report (PDF)"),
        glance=[("6", "linked report pages"), ("4", "headline KPIs on the overview"), ("10", "product categories compared")],
        hero=("images/projects/retail/executive-overview.jpg", 1600, 925,
              "Executive Sales Overview page: net sales, gross sales, demand and return rate cards, net sales by product category, and weekly sales against return rate.",
              "Executive overview: headline sales, demand and return rate, with the weekly trend."),
        problem="<p>A retail business needs to see sales growth and returns side by side: which product categories, channels and stores drive revenue, and where returns eat into it.</p>",
        data="<p>Weekly sales, demand and returns data by product category, sales channel, purchaser and town, modelled as a star schema in Power BI.</p>",
        built="""<p>A sales, margin and returns dashboard across six linked pages:</p>
            <ul>
              <li><strong>Executive overview:</strong> net sales, gross sales, demand and return rate, with weekly trend</li>
              <li><strong>Product and category performance</strong></li>
              <li><strong>Geographical sales and returns</strong></li>
              <li><strong>Purchaser analysis</strong></li>
              <li><strong>Returns analysis</strong></li>
              <li><strong>AI insights:</strong> a Key Influencers view of what drives returns</li>
            </ul>
            <p>DAX time-intelligence measures drive the trends, and drill-through pages take the reader from a category or store down to its detail.</p>""",
        findings=["Snack and Bread bring in most of net sales.",
                  "Bread, Donut and Tortilla are the categories whose return rates sit above the 2% threshold.",
                  "Returns are concentrated in a small number of purchasers."],
        gallery=[("images/projects/retail/product-category-performance.jpg", 1600, 925,
                  "Product and Category Performance page: net sales, demand and return rate by product category, with categories above the 2% return threshold highlighted.",
                  "Product and category performance: net sales against return rate by category."),
                 ("images/projects/retail/returns-analysis.jpg", 1600, 925,
                  "Returns Analysis page: return value and rate by week, top ten purchasers by returns, and return rate by product category against a 2% threshold.",
                  "Returns analysis: which purchasers and categories drive returns.")],
    ),
    dict(
        file="powerbi-air-nz.html", og="air-nz", label="Power BI dashboard", tone="slate",
        title="Air New Zealand Analysis",
        seo_title="Air New Zealand Analysis (Power BI) | Ishan Mathur",
        desc="Power BI dashboard: Air New Zealand route, capacity and performance analysis built from public data, 2020 to 2025.",
        lead="Route, capacity and performance analysis built from public data, brought together in one Power BI data model.",
        tools=["Power BI", "DAX", "Power Query", "Public data"],
        link=None,
        glance=[("2020–25", "years of public data"), ("6", "headline KPIs on the overview"), ("5", "report views shown here")],
        hero=("images/projects/air-nz/executive-summary-overview.jpg", 1600, 925,
              "Air New Zealand Power BI executive dashboard showing arrivals, departures, cancellation rate, on-time performance, capacity utilisation, route cancellations and profitable sectors.",
              "Executive summary: traffic, reliability and capacity on one page, with route-level cancellations."),
        problem="<p>An airline network needs one view of demand, reliability and capacity: how traffic recovered after 2021, where cancellations and delays concentrate, and what a capacity shock such as engine groundings would mean.</p>",
        data="<p>Public data on Air New Zealand arrivals, departures, cancellations, on-time performance and capacity, 2020 to 2025, brought into one Power BI data model.</p>",
        built="""<p>A route, capacity and performance analysis in Power BI:</p>
            <ul>
              <li><strong>Executive summary:</strong> arrivals, departures, cancellation rate, on-time performance and capacity utilisation, with route-level cancellations</li>
              <li><strong>Passenger demand trends</strong>, 2020 to 2025</li>
              <li><strong>Operational performance:</strong> utilisation, cancellations and on-time performance by month</li>
              <li><strong>Demand and reliability trade-offs:</strong> traffic against cancellation rate and on-time arrival</li>
              <li><strong>Capacity shock scenario:</strong> the effect of engine groundings on capacity by segment</li>
            </ul>""",
        findings=["Passenger volumes recover from the 2021 low through to 2025.",
                  "Cancellations peak in June 2025.",
                  "A route-by-month view shows which routes carry the highest cancellation rates."],
        gallery=[("images/projects/air-nz/passenger-demand-trends.jpg", 1600, 925,
                  "Passenger demand trends dashboard showing arrivals, departures and year-over-year change from 2020 to 2025.",
                  "Passenger demand, 2020 to 2025: arrivals, departures and year-on-year change."),
                 ("images/projects/air-nz/operational-performance-snapshot.jpg", 1600, 925,
                  "Operational performance dashboard comparing capacity utilisation, cancellation rate, and arrival and departure on-time performance for 2025.",
                  "Operational performance, 2025: utilisation, cancellations and on-time performance by month."),
                 ("images/projects/air-nz/demand-reliability-tradeoffs.jpg", 1600, 925,
                  "Demand and reliability trade-off dashboard with bubble charts comparing arrivals, cancellation rate and arrival on-time performance in 2025.",
                  "Demand against reliability: traffic, cancellation rate and on-time arrival."),
                 ("images/projects/air-nz/capacity-shock-scenario-analysis.jpg", 1600, 925,
                  "Capacity shock dashboard showing revenue, load factor, engine grounding impact, fleet utilisation, forecast RPK, scenario comparison and segment-level ASK analysis.",
                  "Capacity shock scenario: what engine groundings mean for capacity by segment.")],
    ),
    dict(
        file="sql-nz-building-consents.html", og="sql", label="SQL analytics", tone="sage",
        title="NZ Building Consents",
        seo_title="NZ Building Consents (SQL) | Ishan Mathur",
        desc="SQL analytics: Stats NZ building consents 1990 to 2025 in a star-schema SQLite database, with ten analytical queries using window functions.",
        lead="A star-schema SQLite database and ten analytical queries on Stats NZ building consents, 1990 to 2025.",
        tools=["SQL (SQLite)", "Window functions", "CTEs", "Python load script"],
        link=("https://github.com/mathurishan/nz-building-consents-sql", "Code on GitHub"),
        glance=[("35", "years of data, 1990 to 2025"), ("16", "regions"), ("67", "territorial authorities"), ("10", "analytical SQL queries")],
        hero=("images/projects/sql/nz-building-consents/02_dwelling_mix_shift.png", 0, 0,
              "Stacked area chart showing the share of New Zealand dwelling consents shifting from standalone houses toward townhouses between 2015 and 2025.",
              "Dwelling type mix, 2015 to 2025: houses fell from 70% to 45% of new dwelling consents as townhouses rose from 14% to 44%."),
        problem="<p>Where is New Zealand's building pipeline strongest, how did COVID reshape consent activity, which dwelling types are gaining share, and is national supply becoming concentrated in a handful of regions?</p>",
        data="<p>The Stats NZ Building Consents Issued dataset (December 2025 release): 1990 to 2025, across 16 regions and 67 territorial authorities.</p>",
        built="""<p>A Python load script turns the long-format CSVs into a star-schema SQLite database (four dimension tables, two fact tables). Ten SQL queries then answer the questions above:</p>
            <ul>
              <li><strong>Regional pipeline and ranking:</strong> consents, value and floor area by region for 2025</li>
              <li><strong>Year-on-year growth:</strong> annual change by region, 2020 to 2025, with LAG window functions</li>
              <li><strong>COVID impact and recovery:</strong> national volumes across pre-COVID, trough, recovery and recent periods</li>
              <li><strong>Dwelling type mix:</strong> the share of houses, apartments and townhouses, 2015 to 2025</li>
              <li><strong>Seasonal patterns:</strong> average consent activity by month of year</li>
              <li><strong>Top 10 territorial authorities</strong> by consent value, joining fact and dimension tables</li>
              <li><strong>Hamilton deep dive:</strong> monthly dwelling consents with a 3-month moving average</li>
              <li><strong>Value quartiles:</strong> NTILE classification of regions by average consent value</li>
              <li><strong>Supply concentration:</strong> the top three regions' share of national dwelling consents</li>
              <li><strong>Executive summary view:</strong> a reusable view with totals, QoQ and YoY change and the top region for any quarter</li>
            </ul>""",
        findings=["Auckland led the 2025 pipeline with $9,747M in new consent value, more than double Canterbury ($4,043M) and almost five times Waikato ($2,015M).",
                  "Townhouses briefly overtook standalone houses in 2023. Houses fell from 70.2% of new dwelling consents in 2015 to 45.4% in 2025, while townhouses rose from 13.5% to 44.1%.",
                  "COVID barely dented national consents: the monthly average rose from 3,647 in 2019 to 3,717 in 2020, spiked to 4,529 in 2021–22, then eased to 3,277 in 2023–25.",
                  "Auckland, Canterbury and Waikato accounted for 70.9% of new dwelling consents in 2025, up from 62.3% in 2017.",
                  "Wellington posted the sharpest recent rebound, +17.0% in 2025 after falls of 36.3% in 2023 and 23.9% in 2024.",
                  "November is the busiest month (average 3,931 consents, 2015–2025), and the summer holiday month the quietest (2,594)."],
        gallery=[("images/projects/sql/nz-building-consents/03_covid_impact.png", 0, 0,
                  "Bar chart comparing average monthly consent volumes across pre-COVID, trough, recovery and recent periods.",
                  "COVID impact and recovery."),
                 ("images/projects/sql/nz-building-consents/04_yoy_growth_heatmap.png", 0, 0,
                  "Heatmap of year-over-year consent growth by New Zealand region from 2020 through 2025.",
                  "Year-on-year growth by region."),
                 ("images/projects/sql/nz-building-consents/05_top_10_tas.png", 0, 0,
                  "Horizontal bar chart of the top 10 New Zealand territorial authorities by 2025 consent value, with Hamilton highlighted.",
                  "Top 10 territorial authorities."),
                 ("images/projects/sql/nz-building-consents/06_hamilton_deep_dive.png", 0, 0,
                  "Hamilton City monthly dwelling consent trend with a 3-month moving average overlay.",
                  "Hamilton deep dive with a 3-month moving average."),
                 ("images/projects/sql/nz-building-consents/07_supply_concentration.png", 0, 0,
                  "Line chart tracking the share of national dwelling consents held by Auckland, Canterbury and Waikato from 2017 to 2025.",
                  "Supply concentration in the top three regions."),
                 ("images/projects/sql/nz-building-consents/09_value_quartiles.png", 0, 0,
                  "Horizontal bar chart classifying New Zealand regions into NTILE quartiles by average consent value.",
                  "Value quartiles by region (NTILE).")],
    ),
    dict(
        file="python_nz_housing_affordability.html", og="housing", label="Python analysis", tone="clay",
        title="NZ Housing Affordability",
        seo_title="NZ Housing Affordability (Python) | Ishan Mathur",
        desc="Python analysis of New Zealand rental affordability using MBIE tenancy bond data, Stats NZ household income and building consents.",
        lead="Where rental pressure is rising fastest across New Zealand, from tenancy bond, household income and building consent data.",
        tools=["Python", "pandas", "matplotlib", "seaborn"],
        link=None,
        glance=[("2019–25", "quarterly rent data"), ("3", "public data sources"), ("30%", "affordability threshold tested"), ("SA2", "suburb-level hotspots")],
        hero=("images/projects/python/nz-housing/09_affordability_risk_index.png", 0, 0,
              "Affordability risk index chart ranking New Zealand regions by rental pressure and supply-adjusted risk.",
              "Affordability risk index: where affordability, rent momentum and supply signals overlap."),
        problem="<p>Where has rental pressure intensified most since 2019, which regions now sit above the typical 30% affordability threshold, and which local markets show the strongest signs of accelerating stress?</p>",
        data="<p>MBIE tenancy bond data (national, regional and suburb level), Stats NZ median household income and Stats NZ building consents, Q1 2019 to Q4 2025. Household income for 2019 to 2022 is backcast from observed 2023 to 2025 levels.</p>",
        built="""<p>A Python analysis (pandas, matplotlib, seaborn), backed by reusable code, that cleans and harmonises the three sources and covers:</p>
            <ul>
              <li><strong>National and regional rent trends</strong> from Q1 2019 to Q4 2025</li>
              <li><strong>Affordability ratios</strong> combining quarterly rents with median household income</li>
              <li><strong>Local deep dives</strong> on Hamilton and Auckland</li>
              <li><strong>Supply context</strong> from building consents</li>
              <li><strong>Suburb hotspots</strong> from SA2-level tenancy data</li>
            </ul>""",
        findings=["National weekly rents rose 31.7% from Q1 2019 to Q4 2025, from $452 to $595.",
                  "Auckland was the most expensive region in the latest quarter at $650 a week, and Southland the least expensive at $474.",
                  "Six affordability geographies sat above the 30% threshold in the latest quarter, led by Northland at 35.3%.",
                  "Hamilton City rents rose 34.9% since Q1 2019, 3.2 percentage points faster than the national pace.",
                  "Mayfield in Marlborough recorded the strongest two-year suburb rent growth among adequately sampled suburbs, at 58.2%."],
        gallery=[("images/projects/python/nz-housing/01_national_rent_trends.png", 0, 0,
                  "National weekly rent trend chart for New Zealand from 2019 to 2025.", "National rent trends, 2019 to 2025."),
                 ("images/projects/python/nz-housing/03_affordability_ratios.png", 0, 0,
                  "Regional affordability ratio chart comparing rent to income across New Zealand.", "Rent as a share of household income, by region."),
                 ("images/projects/python/nz-housing/07_hamilton_deep_dive.png", 0, 0,
                  "Hamilton housing market deep dive chart showing rent movement and affordability context.", "Hamilton deep dive."),
                 ("images/projects/python/nz-housing/10_suburb_hotspots.png", 0, 0,
                  "Suburb hotspot chart highlighting areas with the strongest recent rent growth in New Zealand.", "Suburb hotspots: the strongest recent rent growth.")],
    ),
    dict(
        file="python_business_financials.html", og="financials", label="Python analysis", tone="lilac",
        title="NZ Business Financials",
        seo_title="NZ Business Financials (Python) | Ishan Mathur",
        desc="Python analysis of Stats NZ quarterly business financial data: sales and operating profit by industry, profit margins and post-COVID recovery.",
        lead="Which New Zealand industries earn the most, on what margins, and how sales recovered after COVID.",
        tools=["Python", "pandas", "matplotlib", "seaborn"],
        link=None,
        glance=[("4", "measures: sales, profit, assets, inventories"), ("Top 10", "industries by operating profit"), ("Pre / post", "COVID sales comparison")],
        hero=("images/projects/python/top_industries_by_profit.png", 0, 0,
              "Bar chart of the top 10 New Zealand industries by total operating profit, led by Rental, Hiring and Real Estate Services, then Wholesale Trade and Construction.",
              "Top 10 industries by total operating profit."),
        problem="<p>Which New Zealand industries earn the most, on what margins, and how did sales recover after COVID?</p>",
        data="<p>Stats NZ quarterly business financial data: sales (operating income), operating profit, assets and inventories, broken down by industry.</p>",
        built="""<p>A Python analysis in pandas, matplotlib and seaborn that cleans the quarterly series, builds subsets for sales, profit, assets and inventories, and charts:</p>
            <ul>
              <li>Top industries by sales and by operating profit</li>
              <li>A profitability scorecard: average margin against total profit, sized by sales</li>
              <li>Year-on-year sales growth and sector seasonality</li>
              <li>Average quarterly sales before and after COVID</li>
            </ul>""",
        findings=["Rental, Hiring and Real Estate Services earns the most operating profit, on the widest margin of any industry charted.",
                  "Wholesale Trade is second on profit but runs on one of the thinnest margins.",
                  "Retail Trade and Accommodation and Food Services both average higher quarterly sales after COVID than before it."],
        gallery=[("images/projects/python/industry_profitability_scorecard.png", 0, 0,
                  "Scatter chart of average profit margin against total operating profit by industry, bubbles sized by total sales.",
                  "Profitability scorecard: margin against total profit, sized by sales."),
                 ("images/projects/python/post_covid_recovery.png", 0, 0,
                  "Bar chart comparing average quarterly sales before and after COVID for Accommodation and Food Services and Retail Trade.",
                  "Post-COVID recovery: average quarterly sales before and after.")],
    ),
]


def dims(path, w, h):
    if w and h:
        return w, h
    from PIL import Image
    return Image.open(path).size


def figure(src, w, h, alt, cap, lazy=True, stage=None, vt=None):
    w, h = dims(src, w, h)
    lazy_attr = ' loading="lazy"' if lazy else ""
    img = f'<img src="{src}" alt="{E(alt)}" width="{w}" height="{h}"{lazy_attr} />'
    inner = f'<div class="frame">{img}</div>'
    if stage:
        vt_attr = f' style="view-transition-name: shot-{vt}"' if vt else ""
        inner = f'<div class="stage tone-{stage}"{vt_attr}>\n          {inner}\n        </div>'
    return f'''<figure class="shot">
        {inner}
        <figcaption>{E(cap)}</figcaption>
      </figure>'''


def project_page(p, nxt):
    tools = "".join(f"<li>{E(t)}</li>" for t in p["tools"])
    if p["link"]:
        tools += f'<li class="link"><a href="{p["link"][0]}">{E(p["link"][1])} &rarr;</a></li>'
    def glance_dt(v):
        m = re.fullmatch(r"(\d+)([%+]?)", v)
        if m:
            return f'<dt data-count="{m.group(1)}" data-suffix="{m.group(2)}">{E(v)}</dt>'
        return f"<dt>{E(v)}</dt>"
    glance = "\n          ".join(f"<div>{glance_dt(a)}<dd>{E(b)}</dd></div>" for a, b in p["glance"])
    findings = "\n          ".join(f'<div class="finding rise{" r" + str(i % 3) if i % 3 else ""}"><p>{E(f)}</p></div>'
                                   for i, f in enumerate(p["findings"]))
    gallery = "\n          ".join(figure(*g) for g in p["gallery"])
    hsrc, hw, hh, halt, hcap = p["hero"]
    note = ""
    if p.get("note"):
        note = (f'<p class="disclaimer"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" '
                f'stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="6.2"/><path d="M8 7.2v3.6M8 5.2v.1"/></svg>'
                f'{E(p["note"])}</p>')
    labels = [("problem", "Problem"), ("data", "Data"), ("built", "What I built")]
    extra = p.get("extra", "")
    found = [(extra.find(f'id="{sid}"'), sid, lab) for sid, lab in
             [("before-after", "Before and after"), ("explore", "Explore"), ("model", "Raw to model"),
              ("diagram", "Data flow" if "Data flow" in extra else "Model"), ("sql", "SQL"), ("dax", "DAX")]
             if f'id="{sid}"' in extra]
    for _, sid, lab in sorted(found):
        labels.append((sid, lab))
    labels += [("findings", "What changed"), ("gallery", "Gallery")]
    subnav = "".join(f'<a href="#{sid}">{lab}</a>' for sid, lab in labels)
    return (head(p["seo_title"], p["desc"], p["file"], p["og"], html_class="has-subnav") + header("work") + f'''
  <div class="progress" aria-hidden="true"></div>
  <main id="main">
    <section class="case-hero">
      <div class="wrap">
        <a class="back" href="./#work">&larr; All work</a>
        <p class="eyebrow">{E(p["label"])}</p>
        <h1>{E(p["title"])}</h1>
        <p class="lead">{E(p["lead"])}</p>
        <ul class="tools-row" aria-label="Tools">{tools}</ul>
        {note}
        <dl class="glance">
          {glance}
        </dl>
      </div>
    </section>

    <div class="wrap">
      {figure(hsrc, hw, hh, halt, hcap, lazy=False, stage=p["tone"], vt=p["og"])}
    </div>

    <nav class="subnav" aria-label="On this page">
      <div class="wrap">{subnav}</div>
    </nav>

    <section class="case-body">
      <div class="wrap">
        <div class="block rise" id="problem">
          <h2>Problem</h2>
          <div class="body">
            {p["problem"]}
          </div>
        </div>
        <div class="block rise" id="data">
          <h2>Data</h2>
          <div class="body">
            {p["data"]}
          </div>
        </div>
        <div class="block rise" id="built">
          <h2>What I built</h2>
          <div class="body">
            {p["built"]}
          </div>
        </div>
      </div>
    </section>

{p.get("extra", "")}
    <section class="section band" id="findings" aria-labelledby="findings-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="findings-title">What changed</h2>
          <span class="muted">What the analysis shows</span>
        </div>
        <div class="findings">
          {findings}
        </div>
      </div>
    </section>

    <section class="section" id="gallery" aria-labelledby="gallery-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="gallery-title">Gallery</h2>
          <span class="muted">Select an image to enlarge</span>
        </div>
        <div class="gallery">
          {gallery}
        </div>

        <div class="next">
          <span class="muted">Next project</span>
          <a href="{nxt["file"]}">{E(nxt["title"])} &rarr;</a>
        </div>
      </div>
    </section>
  </main>
''' + footer(charts="data-chart" in p.get("extra", "")))


for p in PROJECTS:
    if p["og"] == "sql":
        p["extra"] = extras.pipeline_chart() + extras2.raw_to_model() + diagrams.sql_model() + extras.sql_showcase()
    elif p["og"] == "housing":
        p["extra"] = diagrams.housing_flow() + extras.rent_chart()
    elif p["og"] == "financials":
        p["extra"] = diagrams.financials_flow()
    elif p["og"] == "retail":
        p["extra"] = extras2.retail_chart() + diagrams.retail_model() + extras2.dax_showcase("retail")
        p["note"] = "Independent portfolio project. Not affiliated with or endorsed by Grupo Bimbo."
    elif p["og"] == "air-nz":
        p["extra"] = extras2.before_after_airnz() + extras2.airnz_chart() + diagrams.airnz_model() + extras2.dax_showcase("airnz")
        p["note"] = "Independent analysis of public data. Not affiliated with or endorsed by Air New Zealand."

for i, p in enumerate(PROJECTS):
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    open(p["file"], "w", encoding="utf-8", newline="\n").write(project_page(p, nxt))
    print("wrote", p["file"])


# --------------------------------------------------------------------------- redirects for the old hub pages

for f, anchor in [("powerbi.html", "work"), ("sql.html", "work"), ("python.html", "work")]:
    open(f, "w", encoding="utf-8", newline="\n").write(f'''<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <title>Work | Ishan Mathur</title>
  <meta name="robots" content="noindex" />
  <link rel="canonical" href="{SITE}#{anchor}" />
  <meta http-equiv="refresh" content="0; url=./#{anchor}" />
</head>

<body>
  <p><a href="./#{anchor}">See all work</a></p>
</body>

</html>
''')
    print("wrote", f)
