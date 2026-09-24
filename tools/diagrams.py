"""Data-model and data-flow diagrams, drawn as inline SVG that follows the site theme."""
import html

E = html.escape

ROW = 22      # height of one field row
HEAD = 34     # height of the table header
W = 196       # table width


def table(x, y, name, fields, kind="dim", w=W):
    """fields: list of (name, tag) where tag is 'pk', 'fk' or ''."""
    h = HEAD + ROW * len(fields) + 8
    cls = {"fact": "t-fact", "dim": "t-dim", "src": "t-src", "out": "t-out", "misc": "t-misc"}[kind]
    out = [f'<g class="erd-table {cls}" transform="translate({x},{y})">',
           f'<rect class="erd-box" width="{w}" height="{h}" rx="10"/>',
           f'<path class="erd-head" d="M0 10a10 10 0 0 1 10-10h{w - 20}a10 10 0 0 1 10 10v{HEAD - 10}H0z"/>',
           f'<text class="erd-name" x="14" y="22">{E(name)}</text>']
    for i, (f, tag) in enumerate(fields):
        fy = HEAD + 16 + i * ROW
        if tag:
            out.append(f'<text class="erd-tag erd-{tag}" x="{w - 14}" y="{fy}" text-anchor="end">{tag.upper()}</text>')
        out.append(f'<text class="erd-field{" erd-key" if tag else ""}" x="14" y="{fy}">{E(f)}</text>')
    out.append("</g>")
    return "".join(out), (x, y, w, h)


def anchor(box, side, index=None, fields=0):
    x, y, w, h = box
    if side == "l":
        return x, y + (HEAD + 12 + index * ROW if index is not None else h / 2)
    if side == "r":
        return x + w, y + (HEAD + 12 + index * ROW if index is not None else h / 2)
    if side == "t":
        return x + w / 2, y
    return x + w / 2, y + h


def link(a, b, many_at_b=True, dashed=False):
    """Orthogonal connector from a to b with a crow's foot at the 'many' end."""
    (x1, y1), (x2, y2) = a, b
    mx = (x1 + x2) / 2
    d = f"M{x1} {y1}H{mx}V{y2}H{x2}" if abs(y1 - y2) > 1 else f"M{x1} {y1}H{x2}"
    parts = [f'<path class="erd-link{" erd-dash" if dashed else ""}" d="{d}"/>']
    if many_at_b:
        s = -1 if x2 > x1 else 1          # direction the line arrives from
        fx = x2 + s * 12
        parts.append(f'<path class="erd-crow" d="M{fx} {y2}L{x2} {y2 - 6}M{fx} {y2}L{x2} {y2}M{fx} {y2}L{x2} {y2 + 6}"/>')
        parts.append(f'<path class="erd-one" d="M{x1 - s * 8} {y1 - 6}V{y1 + 6}"/>')
    return "".join(parts)


def arrow(a, b):
    (x1, y1), (x2, y2) = a, b
    mx = (x1 + x2) / 2
    d = f"M{x1} {y1}H{mx}V{y2}H{x2 - 2}" if abs(y1 - y2) > 1 else f"M{x1} {y1}H{x2 - 2}"
    return (f'<path class="erd-link" d="{d}"/>'
            f'<path class="erd-arrow" d="M{x2 - 9} {y2 - 5}L{x2} {y2}L{x2 - 9} {y2 + 5}"/>')


def svg(width, height, body, label):
    return (f'<svg class="erd" viewBox="0 0 {width} {height}" role="img" aria-label="{E(label)}" '
            f'preserveAspectRatio="xMidYMid meet">{body}</svg>')


def section(title, sub, diagram, legend, note):
    return f'''
    <section class="section" id="diagram" aria-labelledby="diagram-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="diagram-title">{E(title)}</h2>
          <span class="muted">{E(sub)}</span>
        </div>
        <div class="erd-card rise">
          <div class="erd-scroll">{diagram}</div>
          <div class="erd-legend">{legend}</div>
          <p class="chart-note">{note}</p>
        </div>
      </div>
    </section>
'''


LEGEND_ERD = ('<span><i class="lg-fact"></i>Fact table</span><span><i class="lg-dim"></i>Dimension</span>'
              '<span><b>PK</b> primary key</span><span><b>FK</b> foreign key</span>'
              '<span><svg viewBox="0 0 30 12" aria-hidden="true"><path d="M2 6H28M18 6L28 1M18 6L28 6M18 6L28 11" /></svg>one to many</span>')
LEGEND_FLOW = ('<span><i class="lg-src"></i>Source</span><span><i class="lg-dim"></i>Prepared data</span>'
               '<span><i class="lg-fact"></i>Analysis output</span>')


# ------------------------------------------------------------------ NZ Building Consents (exact schema)

def sql_model():
    parts = []
    dd, bdate = table(24, 150, "dim_date", [("date_id", "pk"), ("year", ""), ("quarter", ""), ("month", ""), ("month_name", ""), ("is_summer", "")])
    db, bbt = table(24, 360, "dim_building_type", [("building_type_id", "pk"), ("building_type_name", ""), ("is_residential", ""), ("is_aggregate", "")])
    fr, bfr = table(312, 40, "fact_region_consents", [("id", "pk"), ("date_id", "fk"), ("region_id", "fk"), ("building_type_id", "fk"), ("consent_nature", ""), ("number_of_consents", ""), ("value_nzd", ""), ("floor_area_sqm", "")], "fact", 214)
    ft, bft = table(312, 300, "fact_ta_consents", [("id", "pk"), ("date_id", "fk"), ("authority_id", "fk"), ("building_type_id", "fk"), ("consent_nature", ""), ("number_of_consents", ""), ("value_nzd", ""), ("floor_area_sqm", "")], "fact", 214)
    dr, br = table(620, 60, "dim_region", [("region_id", "pk"), ("region_name", ""), ("is_aggregate", "")])
    da, ba = table(620, 320, "dim_authority", [("authority_id", "pk"), ("authority_name", ""), ("region_id", "fk")])
    parts += [dd, db, fr, ft, dr, da]
    links = [
        link(anchor(bdate, "r", 0), anchor(bfr, "l", 1)),
        link(anchor(bdate, "r", 0), anchor(bft, "l", 1)),
        link(anchor(bbt, "r", 0), anchor(bfr, "l", 3)),
        link(anchor(bbt, "r", 0), anchor(bft, "l", 3)),
        link(anchor(br, "l", 0), anchor(bfr, "r", 2)),
        link(anchor(ba, "l", 0), anchor(bft, "r", 2)),
        link(anchor(br, "b"), anchor(ba, "t"), many_at_b=False, dashed=True),
    ]
    body = "".join(links) + "".join(parts)
    body += '<text class="erd-note" x="727" y="276">rolls up to a region</text>'
    return section("Data model", "SQLite star schema, exactly as built",
                   svg(840, 520, body, "Star schema: two fact tables for regional and territorial authority consents, joined to date, building type, region and authority dimensions."),
                   LEGEND_ERD,
                   "Two fact tables share the date and building-type dimensions; territorial authorities roll up to regions.")


# ------------------------------------------------------------------ Retail Sales & Returns (Power BI model)

def retail_model():
    fact, bf = table(322, 150, "Sales", [("Date Key", "fk"), ("Product Key", "fk"), ("Channel Key", "fk"), ("Purchaser Key", "fk"), ("Town Key", "fk"),
                                          ("Gross Sales", ""), ("Return Value", ""), ("Demand Units", ""), ("Returned Units", "")], "fact")
    d1, b1 = table(24, 60, "Date", [("Date Key", "pk"), ("Week Number", ""), ("Month", "")])
    d2, b2 = table(24, 300, "Product", [("Product Key", "pk"), ("Category", ""), ("Product", "")])
    d3, b3 = table(620, 30, "Channel", [("Channel Key", "pk"), ("Sales Channel", "")])
    d4, b4 = table(620, 190, "Purchaser", [("Purchaser Key", "pk"), ("Purchaser", "")])
    d5, b5 = table(620, 350, "Geography", [("Town Key", "pk"), ("Town", ""), ("Region", "")])
    links = [link(anchor(b1, "r", 0), anchor(bf, "l", 0)), link(anchor(b2, "r", 0), anchor(bf, "l", 1)),
             link(anchor(b3, "l", 0), anchor(bf, "r", 2)), link(anchor(b4, "l", 0), anchor(bf, "r", 3)),
             link(anchor(b5, "l", 0), anchor(bf, "r", 4))]
    body = "".join(links) + fact + d1 + d2 + d3 + d4 + d5
    return section("Data model", "Power BI star schema",
                   svg(840, 470, body, "Star schema: a Sales fact table joined to Date, Product, Channel, Purchaser and Geography dimensions."),
                   LEGEND_ERD,
                   "One fact table at week-by-product-by-purchaser grain; every page and measure reads from the same model.")


# ------------------------------------------------------------------ Air New Zealand (Power BI model)

def airnz_model():
    date, bd = table(322, 30, "Date", [("Date", "pk"), ("Year", ""), ("MonthName", ""), ("YearMonth", "")], "dim")
    t1, b1 = table(24, 40, "Table 1", [("Date", "fk"), ("Arrival", ""), ("Departure", "")], "fact")
    ms, bm = table(24, 200, "Monthly Summary", [("Date", "fk"), ("Scheduled Sectors", ""), ("Cancelled Sectors", ""), ("Flown Arrivals", ""), ("On-time Arrivals", "")], "fact")
    fc, bfc = table(620, 40, "Forecast & What-If", [("Date", "fk"), ("Scenario", ""), ("ForecastRPK", "")], "fact")
    en, be = table(620, 200, "Engine Availability", [("Date", "fk"), ("Compensation", ""), ("Lost Revenue", "")], "fact")
    s1, bs = table(322, 250, "Sheet1 (routes)", [("Airline", ""), ("Arriving Port", ""), ("Cancellation Rate", "")], "misc")
    rp, brp = table(322, 390, "Route Performance", [("Segment", ""), ("ASK", "")], "misc")
    rm, brm = table(620, 360, "Route Profitability", [("Route", ""), ("ProfitScore", "")], "misc")
    me, bme = table(24, 380, "Measure", [("Total Arrivals", ""), ("Cancellation Rate", ""), ("Arrival OTP", ""), ("Arrivals YoY %", "")], "out")
    links = [link(anchor(bd, "l", 0), anchor(b1, "r", 0)), link(anchor(bd, "l", 0), anchor(bm, "r", 0)),
             link(anchor(bd, "r", 0), anchor(bfc, "l", 0)), link(anchor(bd, "r", 0), anchor(be, "l", 0))]
    body = "".join(links) + date + t1 + ms + fc + en + s1 + rp + rm + me
    body += '<text class="erd-note" x="420" y="236" text-anchor="middle">route-level tables feed their own visuals</text>'
    return section("Data model", "Power BI report model",
                   svg(840, 520, body, "Report model: a shared Date table filters the traffic, monthly summary, forecast and engine tables; route tables stand alone; measures live in their own table."),
                   LEGEND_ERD + '<span><i class="lg-out"></i>Measures table</span>',
                   "A shared Date table filters every time-based table, so one date slicer drives the whole report.")


# ------------------------------------------------------------------ Python projects (data flow)

def housing_flow():
    s1, a = table(24, 30, "MBIE tenancy bonds", [("region / suburb (SA2)", ""), ("quarter", ""), ("median, mean rent", ""), ("active bonds", "")], "src", 210)
    s2, b = table(24, 205, "Stats NZ household income", [("region", ""), ("year", ""), ("median income", "")], "src", 210)
    s3, c = table(24, 355, "Stats NZ building consents", [("region", ""), ("year", ""), ("consents issued", "")], "src", 210)
    m1, d = table(318, 120, "rental_affordability", [("region", ""), ("quarter", ""), ("median_weekly_rent", ""), ("median_annual_income", ""), ("rent_to_income_ratio", ""), ("affordability_flag", ""), ("yoy_rent_change_pct", ""), ("consents_per_1000_bonds", "")], "dim", 214)
    m2, e = table(318, 390, "suburb_rental_data", [("suburb (SA2)", ""), ("quarter", ""), ("median rent", ""), ("bond count", "")], "dim", 214)
    o1, f = table(616, 120, "Outputs", [("rent trends", ""), ("affordability ratios", ""), ("Hamilton deep dive", ""), ("risk index", ""), ("suburb hotspots", "")], "fact", 200)
    body = "".join([arrow(anchor(a, "r"), anchor(d, "l", 1)), arrow(anchor(b, "r"), anchor(d, "l", 3)),
                    arrow(anchor(c, "r"), anchor(d, "l", 7)), arrow(anchor(a, "r"), anchor(e, "l", 0)),
                    arrow(anchor(d, "r", 4), anchor(f, "l", 1)), arrow(anchor(e, "r", 2), anchor(f, "l", 4))])
    body += s1 + s2 + s3 + m1 + m2 + o1
    return section("Data flow", "From three public sources to one analysis table",
                   svg(840, 520, body, "Data flow: tenancy bonds, household income and building consents are cleaned into a region-by-quarter affordability table and a suburb table, which feed the charts."),
                   LEGEND_FLOW, "Income for 2019 to 2022 is backcast from observed 2023 to 2025 levels before the ratio is calculated.")


def financials_flow():
    s, a = table(24, 120, "Stats NZ business financials", [("period (quarter)", ""), ("industry", ""), ("measure", ""), ("value", "")], "src", 220)
    p, b = table(322, 60, "Cleaned series", [("period → date", ""), ("industry", ""), ("sales", ""), ("operating profit", ""), ("assets", ""), ("inventories", "")], "dim", 200)
    o, c = table(612, 40, "Outputs", [("top industries by profit", ""), ("profitability scorecard", ""), ("year-on-year growth", ""), ("seasonality", ""), ("pre / post COVID", "")], "fact", 204)
    body = arrow(anchor(a, "r"), anchor(b, "l", 2)) + arrow(anchor(b, "r", 3), anchor(c, "l", 1)) + s + p + o
    return section("Data flow", "Long-format CSV to analysis-ready series",
                   svg(840, 290, body, "Data flow: the Stats NZ quarterly file is typed and reshaped into one series per measure, which feeds the charts."),
                   LEGEND_FLOW, "Dates are typed and numbers coerced safely before any subset is built.")
