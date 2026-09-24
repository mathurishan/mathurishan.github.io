"""Short articles ("Notes"). Imported by build.py, which writes one page per note."""

NOTES = [
    dict(
        file="note-every-dashboard-is-a-small-project.html",
        title="Every dashboard is a small project",
        desc="How PMP® project discipline scales down to reporting work: a one-paragraph charter, mapped dependencies, a risk list with a control for each risk, quality gates before release and a proper handover.",
        lead="A dashboard has a sponsor, a scope, risks, a release and a handover. It is a project whether or not anyone calls it one.",
        minutes=4,
        card="What project management looks like at the size of a report: a short charter, a risk list with a control for each risk, a gate before release and a real handover.",
        body="""
<p>I hold the Project Management Professional (PMP®) certification. People tend to associate it with large
  programmes, Gantt charts and steering committees. I find it most useful on small work, because small work is
  where nobody writes anything down. A dashboard gets requested in passing, built in a hurry and quietly
  abandoned, and nobody can say whether it did what it was for.</p>

<p>So I run every reporting job as a small project. It adds very little paperwork: a paragraph, a short list
  and a checklist. These five habits come straight from the PMP® lifecycle, scaled down to the size of a
  report.</p>

<h2>1. Initiate: a charter in one paragraph</h2>

<p>Before any data, I write down what decision the report supports, who will read it and what is out of
  scope. At Arcesium I gathered requirements from global investment clients and turned them into reporting
  outputs, and I led structured discussions to clarify ambiguous business logic in reconciliation rules.
  Clearer requirements at the start were how we reduced rework later.</p>

<p>The paragraph also protects the scope. When someone later asks for "just one more page", there is a written
  purpose to check the request against. Sometimes the answer is yes; it should never be yes by accident.</p>

<h2>2. Plan: map the dependencies, not just the visuals</h2>

<p>A report depends on things outside the report: access to a source, an agreed definition, an owner who can
  confirm a number. At Arcesium I managed several client workstreams at once, each end to end from
  requirements through build, test, release and ongoing support. What made delivery predictable was the
  unglamorous part: a clear scope, risks named early, dependencies mapped and a realistic timeline.</p>

<p>The same thinking shaped an 11-page working paper I wrote for the University of Waikato Library, setting
  out a phased roadmap for how the Library can make better use of its service, systems and technology data.
  A phased roadmap is a dependency map in plain language: what has to be in place before the next step is
  worth taking.</p>

<h2>3. A risk list for data</h2>

<p>Reporting risks are specific, which makes them easy to manage once they are written down. Each one on my list
  gets a control:</p>

<ul>
  <li><strong>Double counting.</strong> In one usage analysis, 3,157 events, about 24%, would have been counted
    twice. The control was de-duplication against a kept archive.</li>
  <li><strong>Personal data leaving the building.</strong> The control is a gate that blocks any release still
    containing personal data.</li>
  <li><strong>Two sources, two answers.</strong> Consolidating 58 Library systems turned up 8 conflicting
    statuses. Each went to the owner of that system as an issue to resolve, rather than being settled quietly
    by me.</li>
</ul>

<h2>4. Monitor and control: a quality gate before release</h2>

<p>A project has acceptance criteria. A report should too. A monthly Library report I built runs 36
  cross-checks confirming the report and its evidence workbook agree, and the release stops if any personal
  text survives. The consolidated systems view runs 68 automated checks and is now in use at version 15.</p>

<p>At Arcesium the same discipline applied to releases: coordinated testing inputs, issue triage and
  stakeholder sign-off before anything went live, including scheduled and out-of-hours releases.</p>

<h2>5. Close: hand it over properly</h2>

<p>Closing a project means someone else can run what you built. On a Power BI prototype bringing three systems
  into one view, an evidence workbook of 11 tabs and 109 formulas traces every number to its source, and a
  written refresh procedure lets someone else continue it. Every Library dashboard and report is published
  through SharePoint to the site of the team or stakeholder group it serves, so it lives where its readers
  already are.</p>

<blockquote>A report nobody scoped gets rebuilt. A report nobody handed over gets abandoned.</blockquote>

<h2>Proportion is part of the method</h2>

<p>None of this means heavy process. PMP® is as much about tailoring as about templates: a one-paragraph
  charter, a risk list of a few lines and a release checklist are enough for most reports. The point is not
  the documents. It is that scope, risk and quality get decided on purpose, before a reader finds out the hard
  way. The <a href="how-i-work.html">six steps I follow on every reporting job</a> are this lifecycle in
  practice.</p>
""",
    ),
    dict(
        file="note-one-name-for-every-system.html",
        title="One name for every system",
        desc="How three separate registers became one searchable view of 58 Library systems: a naming layer, conflicts reported rather than hidden, automated checks and views built around real questions.",
        lead="Three registers described the same systems in three different ways. The fix was not a better spreadsheet but one agreed name for everything.",
        minutes=3,
        card="Three registers, three sets of names, one question nobody could answer quickly. How 58 systems became one view people trust.",
        body="""
<p>At the University of Waikato Library, three registers each described part of the same landscape: one for
  services, one for technical solutions and one for integrations. Each was reasonable on its own. Together they
  could not answer simple questions such as which systems the Library runs, who owns each one and what connects
  to what. The same system could appear under different names in different registers, so every answer started
  with detective work.</p>

<p>I brought the three registers together into one searchable dashboard that gives Library leadership a single
  view of systems, ownership and integrations. It now covers 58 systems and is in use at version 15. Four design
  decisions did most of the work.</p>

<h2>1. A naming layer before anything else</h2>

<p>The first job was not a chart. It was deciding what each thing is called. Every alias found in the source
  registers maps to one canonical record, so a system appears once, under one name, wherever it is referenced.
  This is the same idea as a clean dimension table in a star schema: agree the entities first, and everything
  built on them stays simple.</p>

<h2>2. Report conflicts, do not resolve them quietly</h2>

<p>When registers disagree, it is tempting to pick the value that looks most recent and move on. I did not. The
  consolidation found 8 conflicting statuses, and each one went back to the person who owns that system. The
  owner knows which answer is right. My job was to make the disagreement visible, not to guess.</p>

<h2>3. Checks that run every time</h2>

<p>A consolidated view is only useful if people can trust it after the next update, not just on the day it was
  built. The view has 68 automated checks that confirm the data still hangs together. Relationships between
  systems were checked against platform investigation and web analytics evidence, so connections were verified
  rather than assumed.</p>

<h2>4. Views built around questions</h2>

<p>Different readers ask different questions. A manager wants to know what they own; someone planning a change
  wants to know what depends on what. Rather than one crowded page, the dashboard has 11 views, each shaped
  around one kind of question.</p>

<blockquote>A register records what someone knew. A consolidated view has to show what is true, and say plainly
  where nobody knows yet.</blockquote>
""",
    ),
    dict(
        file="note-a-number-needs-a-sentence.html",
        title="A number needs a sentence",
        desc="How to explain numbers to people who do not work with data: lead with the sentence, use their words, say what the number cannot tell you and show where the data disagrees.",
        lead="Most people who read my reports do not work with data. They have a decision to make, and the number is only useful if it helps them make it.",
        minutes=3,
        card="Most people who read a report do not work with data. Four habits that make a number easy to understand and hard to misread.",
        body="""
<p>A chart on its own asks the reader to do the analysis. Someone who works with data every day will manage it.
  A manager with ten minutes before a meeting will not. They will skim the chart, guess what it means, and
  sometimes guess wrong.</p>

<p>Teaching sharpened this for me. As a sessional assistant on a postgraduate
  economics paper at the University of Waikato, I ran tutorials for mixed groups of students and spent most of
  that time turning theory into practical business examples. The job taught me one thing: if people leave
  unsure what the point was, the explanation failed, however good the material. I now build dashboards and
  reports for senior Library leadership, client groups and third-party stakeholders, and the same rule
  applies.</p>

<h2>1. Lead with the sentence, then the chart</h2>

<p>Every page of a report should say in words what the chart shows and why it matters: what changed, by how
  much, and what the reader might do about it. The chart is the evidence for that sentence. If I cannot write
  the sentence, I do not understand the data well enough to put it in front of anyone.</p>

<h2>2. Use their words, not the system's</h2>

<p>Source systems name things for the software, not for the reader. In the Power BI dashboards I built for
  reading-list processing, I replaced raw URLs with clean, clickable labels so people who did not work with
  data could use the dashboards without decoding them. When I brought 58 Library systems into one
  consolidated view, every alias was mapped to one agreed name, so a reader sees one thing called one thing,
  wherever it appears.</p>

<h2>3. Say what the number cannot tell you</h2>

<p>Precision can mislead. When templates cut a recurring reporting task from about half a day to under an
  hour, I say "about" and "under" because the before-and-after was observed, not timed. Turning that into a
  percentage would sound more rigorous and be less honest.</p>

<p>The same goes for corrections. In one usage analysis, 3,157 events, about 24%, would have been counted twice
  without de-duplication. "About a quarter of the activity was not real" is a sentence a manager can act on.
  The exact count belongs in the notes for anyone who wants to check it.</p>

<h2>4. Show where the data disagrees</h2>

<p>It is tempting to tidy disagreements away before anyone sees them. When consolidating those Library systems I
  found 8 conflicting statuses. I reported each one to its owner instead of quietly picking a winner. Readers
  trust a report more when it shows its open questions, and the people closest to the data are usually the
  ones who can settle them.</p>

<p>When a number turns out wrong, I fix the formula, not the chart, and write down why. On a Power BI prototype
  I corrected the fill-rate calculation and recorded the reason, so the next reader of that number knows what
  it means and why it changed.</p>

<blockquote>If a reader needs me in the room to understand the chart, the chart is not finished.</blockquote>

<p>None of this is about simplifying the analysis. The analysis stays rigorous. The explanation is what gets
  simpler, and that is the part most readers see.</p>
""",
    ),
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
