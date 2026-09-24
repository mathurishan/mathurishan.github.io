"""Short articles ("Notes"). Imported by build.py, which writes one page per note."""

NOTES = [
    dict(
        file="note-validate-before-you-visualise.html",
        title="Validate before you visualise",
        desc="Why the checks that run before a dashboard matter more than the dashboard itself: reconciliation, grain and gaps.",
        lead="A dashboard is only as trustworthy as the checks that run before anyone sees it.",
        minutes=4,
        card="The most expensive dashboard is the one that is wrong and looks right. Three checks I run before building a single visual.",
        body="""
<p>The most expensive dashboard is the one that is wrong and looks right. Nobody questions a clean chart, so a
  small error in the data travels a long way before anyone notices.</p>

<p>I learned this in reconciliation work. For three years at Arcesium I investigated and resolved 10–20
  reconciliation exceptions a day across cash, positions and P&amp;L for global investment clients. That job
  teaches one habit above all: a number is not true because it appears on a screen. It is true when it agrees
  with an independent source.</p>

<h2>Three checks before the first visual</h2>

<p><strong>1. Does it add back?</strong> Totals should reconcile to a figure you trust. In my
  <a href="sql-nz-building-consents.html#model">NZ Building Consents</a> project, the monthly rows in my fact
  table for Waikato add back exactly to the quarter Stats NZ publishes: 949 consents, $506,230,468 in value and
  191,777 m² of floor area. If they had not matched, the problem would have been in my model, not in the chart.</p>

<pre><code>-- Do my monthly fact rows add back to the published quarter?
SELECT r.region_name,
       SUM(f.number_of_consents) AS consents,
       SUM(f.value_nzd)          AS value_nzd,
       SUM(f.floor_area_sqm)     AS floor_area_sqm
FROM fact_region_consents f
JOIN dim_date d   ON f.date_id = d.date_id
JOIN dim_region r ON f.region_id = r.region_id
WHERE r.region_name = 'Waikato Region'
  AND d.year = 2025 AND d.month IN (7, 8, 9)
  AND f.consent_nature = 'New'
GROUP BY r.region_name;</code></pre>

<p><strong>2. Is the grain what I think it is?</strong> Every table has a grain: one row per what? If a table I
  believe is one row per region per month is really one row per region per month per building type, every sum
  quietly multiplies. I write the grain down before I write a measure.</p>

<p><strong>3. What is missing?</strong> Blanks, suppressed values and partial periods do more damage than
  outliers, because they hide. A month that is only half loaded looks like a collapse on a trend line. Partial
  periods come out of trends until they are complete.</p>

<h2>Checks make reporting faster, not slower</h2>

<p>It is tempting to treat validation as a cost. My experience is the opposite. At Arcesium, introducing
  validation checks and SQL control routines cut the time to produce daily reconciliation reporting by 40%.
  The checks did not add work; they removed the manual chasing that happens when nobody trusts the first
  answer.</p>

<blockquote>Speed and trust come from the same place: knowing the numbers are right before anyone asks.</blockquote>

<p>So before I open Power BI, I ask three questions. Does it add back? What is one row? What is missing? A
  dashboard built on those answers rarely needs defending.</p>
""",
    ),
    dict(
        file="note-start-with-a-star-schema.html",
        title="Why my reports start with a star schema",
        desc="How a clear fact table and a few well-built dimensions make Power BI reports faster to build, easier to trust and simpler to extend.",
        lead="Before I drag a single visual onto a page, I decide what one row of the fact table means.",
        minutes=4,
        card="Flat files are quick to start and slow to trust. How a fact table and a few clean dimensions keep reports simple.",
        body="""
<p>Most reporting problems I see are not visual problems. They are shape problems. A single wide table works for
  the first chart and fights you on the fifth: totals change depending on which column you slice by, filters
  stop cooperating, and measures grow long and fragile.</p>

<p>So I start every report with the same question: <em>what does one row of the fact table mean?</em></p>

<h2>The shape</h2>

<p>A star schema has one job: separate the things that happened from the things that describe them.</p>

<ul>
  <li><strong>Fact tables</strong> hold events at a declared grain, such as a sale in a week, or consents for a
    region in a month. They hold keys and numbers, nothing else.</li>
  <li><strong>Dimension tables</strong> describe those events: date, product, channel, region. Each has one row per
    thing, with the labels and groupings people filter by.</li>
</ul>

<p>Relationships run one way, from dimension to fact. That single rule removes most of the surprises.</p>

<h2>What it bought me in practice</h2>

<p>In my <a href="powerbi-retail.html">Retail Sales &amp; Returns</a> report, six pages share one model. Because
  product category, sales channel and purchaser are clean dimensions, one visual can switch between all three
  with a field parameter, and the same measure works on every page without being rewritten.</p>

<p>In my <a href="sql-nz-building-consents.html">NZ Building Consents</a> project, Stats NZ publishes a long
  format with one row per measure. Pivoting that into a star schema, with four dimension tables and two fact
  tables, is what made the ten analytical queries short and readable. The hard work happens once, in the model,
  instead of in every query.</p>

<h2>Measures, not columns</h2>

<p>On top of the model I write explicit measures for anything that gets reported, and I build rates from their
  parts so they stay correct at every level of a hierarchy:</p>

<pre><code>Net Sales = [Gross Sales] - [Return Value]

Return Rate % =
DIVIDE ( SUM ( Sales[Returned Units] ), [Actual Demand] )</code></pre>

<p>A rate stored as a column averages badly the moment someone rolls it up. A rate built as a measure
  recalculates from its numerator and denominator wherever it appears.</p>

<blockquote>Model first. Once the shape is right, the visuals are the quick part.</blockquote>

<p>It takes a little longer on day one. It saves that time many times over the first time someone asks for a new
  breakdown, and the answer is a slicer rather than a rebuild.</p>
""",
    ),
    dict(
        file="note-reading-rent-data-honestly.html",
        title="Reading rent data honestly",
        desc="Medians, thresholds, backcasts and sample sizes: the choices that decide what a housing analysis can fairly claim.",
        lead="Housing numbers are emotive. The analysis has to be careful about what it can and cannot say.",
        minutes=4,
        card="Medians, thresholds, backcasts and small samples: the method choices that decide what a housing analysis can fairly claim.",
        body="""
<p>When I built my <a href="python_nz_housing_affordability.html">NZ Housing Affordability</a> analysis, the
  charts were the easy part. The harder part was deciding what the data could fairly support. Four choices
  mattered most.</p>

<h2>1. Medians over means</h2>

<p>Rents are skewed: a small number of expensive tenancies pull an average upwards. The tenancy bond data
  includes both, and I report the median, because it describes the typical renter rather than the top of the
  market. On that measure, national weekly rent rose 31.7% from Q1 2019 to Q4 2025, from $452 to $595.</p>

<h2>2. A threshold is a convention, so say so</h2>

<p>The 30% rent-to-income line is a widely used benchmark, not a law of nature. It is useful because it gives a
  shared reference point: six affordability geographies sat above it in the latest quarter, led by Northland at
  35.3%. I draw the line on the chart and name it as a benchmark, so nobody mistakes it for an official
  definition of unaffordable.</p>

<h2>3. Label every estimate</h2>

<p>Household income is not published every quarter for every region. For 2019 to 2022 I backcast income from
  observed 2023 to 2025 levels. That is a reasonable method, but it is still an estimate, so the note travels
  with the chart everywhere it appears, including the interactive version on the project page.</p>

<h2>4. Small samples swing</h2>

<p>Suburb-level data is where the most striking numbers live, and the least reliable ones. A suburb with a
  handful of new bonds can double its median rent through chance. I only ranked suburbs with an adequate
  number of bonds. Even then, Mayfield in Marlborough showed 58.2% two-year growth, which is a signal worth
  investigating rather than a headline to repeat.</p>

<blockquote>State the method next to the number, and let the reader check it.</blockquote>

<h2>Compare growth, not just levels</h2>

<p>Levels tell you where rent is highest; growth tells you where pressure is building. Hamilton City rents rose
  34.9% since Q1 2019, 3.2 percentage points faster than the national pace, even though Hamilton is not among
  the most expensive markets. Both views belong in the same analysis.</p>

<p>None of this makes the story less interesting. It makes it one you can defend in a room full of people who
  know the data as well as you do.</p>
""",
    ),
]
