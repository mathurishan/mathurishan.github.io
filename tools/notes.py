"""Short articles ("Notes"). Imported by build.py, which writes one page per note."""

NOTES = [
    dict(
        file="note-half-a-day-to-under-an-hour.html",
        title="Half a day to under an hour",
        desc="How templates, upfront checks and automated preparation took the manual work out of recurring reports, and how to state the time saved honestly.",
        lead="Most of the time spent on a recurring report goes on rebuilding it, not on the analysis.",
        minutes=4,
        card="What actually makes a recurring report faster: templates, checks at the front and automated preparation. And how to state the saving honestly.",
        body="""
<p>A recurring report rarely takes long because the analysis is hard. It takes long because someone rebuilds
  it every time: pulling the same extracts, reshaping the same columns, fixing the same formatting and chasing
  the same odd numbers. The thinking might take twenty minutes. The assembly takes the rest of the morning.</p>

<p>Two results on my résumé came from taking that assembly away. At the University of Waikato Library,
  reusable reporting templates cut a recurring manual reporting task from about half a day to under an hour.
  Before that, at Arcesium, validation checks and SQL control routines cut the time to produce daily
  reconciliation reporting for 10+ global investment clients by 40%. Different teams, different data, the same
  three moves.</p>

<h2>1. Make the decisions once</h2>

<p>Every run of a manual report quietly asks the same questions again. Which layout? Which definition of
  "active"? Which date range, which rounding, which chart? Each answer is small, but answering them every time
  is where the hours go, and answering them slightly differently each time is where inconsistency creeps in.</p>

<p>A template is those decisions written down once. At the Library I built reusable templates for executive
  briefs, Excel workbooks and dashboards, each with a fixed structure and consistent formatting. The next run
  starts from a finished shape and only the data changes. That is most of how half a day became under an
  hour.</p>

<p>A good template has a side effect that matters as much as the time saved: readers learn where to look. When
  the same number sits in the same place every period, people stop hunting for the figure and start comparing
  it.</p>

<h2>2. Put the checks at the front</h2>

<p>The slowest part of a manual report is often the end, when a figure looks wrong and someone has to trace it
  back by hand. At Arcesium the answer was to move that work to the start. SQL control routines ran before the
  reporting did, and exceptions were sorted into categories, so triage began with a label rather than a blank
  page.</p>

<p>A control check does not need to be clever. It needs to fail loudly before anyone publishes. Here is the kind
  of check I mean, written against the model from my
  <a href="sql-nz-building-consents.html#model">NZ Building Consents</a> project: any month where not every
  region has loaded is flagged before the report refreshes.</p>

<pre><code>-- Flag any month where not every region has loaded.
-- Run before the refresh: any rows returned mean stop and investigate.
SELECT d.year, d.month,
       COUNT(DISTINCT f.region_id) AS regions_loaded
FROM fact_region_consents f
JOIN dim_date d   ON f.date_id = d.date_id
JOIN dim_region r ON f.region_id = r.region_id
WHERE r.is_aggregate = 0
GROUP BY d.year, d.month
HAVING COUNT(DISTINCT f.region_id) &lt;
       (SELECT COUNT(*) FROM dim_region WHERE is_aggregate = 0)
ORDER BY d.year DESC, d.month DESC;</code></pre>

<p>An empty result means go ahead. Anything else means the problem is found in minutes, upstream, instead of by a
  stakeholder after the report has gone out. That shift, from chasing errors to preventing them, is what
  replaced the manual steps behind the 40%.</p>

<h2>3. Automate the preparation, keep the judgement</h2>

<p>Once the shape is fixed and the checks are in place, the manual work left is usually data preparation:
  getting data out of a system and into the shape the template expects. That is the part worth automating.
  Automating data preparation and standardising templates is how recurring Library reporting that used to take
  days now takes hours.</p>

<p>The fullest version of this is an API reporting workflow I built to turn booking and questionnaire data into
  reporting. It is in production, runs monthly with some reporting fortnightly, and was designed to be
  privacy-conscious from the start. The finished dashboards and reports are published through SharePoint to
  the teams who use them.</p>

<p>What I do not automate is the reading. The point of saving hours of assembly is to spend some of that time
  on what the numbers mean and what to say about them.</p>

<blockquote>Automate the assembly. Keep the thinking.</blockquote>

<h2>State the saving honestly</h2>

<p>One last habit. "Half a day to under an hour" is an observed before-and-after on a real recurring task, not a
  stopwatch study. So I say "about", and I do not sharpen it into a precise percentage it cannot support.</p>

<p>That matters for the same reason the checks do. A time saving is a number like any other, and it should be
  one you can explain when someone asks how you got it.</p>
""",
    ),
    dict(
        file="note-validate-before-you-visualise.html",
        title="Validate before you visualise",
        desc="Why the checks that run before a dashboard matter more than the dashboard itself: reconciliation, grain and gaps.",
        lead="A dashboard is only as trustworthy as the checks that run before anyone sees it.",
        minutes=3,
        card="The most expensive dashboard is the one that is wrong and looks right. Three checks I run before building a single visual.",
        body="""
<p>The most expensive dashboard is the one that is wrong and looks right. Nobody questions a clean chart, so a
  small error in the data travels a long way before anyone notices.</p>

<p>I learned this in reconciliation work. For more than three years at Arcesium I investigated and resolved 10–20
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
        minutes=2,
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
        minutes=2,
        card="Medians, thresholds, backcasts and small samples: the method choices that decide what a housing analysis can fairly claim.",
        body="""
<p>When I built my <a href="python_nz_housing_affordability.html">NZ Housing Affordability</a> analysis, the
  charts were the easy part. The harder part was deciding what the data could fairly support. Four choices
  mattered most.</p>

<h2>1. Medians over means</h2>

<p>Rents are skewed: a small number of expensive tenancies pull an average upwards. The tenancy bond data
  includes every bond lodged, cheap and expensive alike, so I report the median, because it describes the
  typical renter rather than the top of the market. On that measure, national weekly rent rose 31.7% from Q1 2019 to Q4 2025, from $452 to $595.</p>

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
