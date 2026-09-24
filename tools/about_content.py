"""Sections of about.html (moved from the homepage). Edit the HTML here, then run tools/build.py."""

BACKGROUND = '''
    <section class="section" id="about" aria-labelledby="about-title">
      <div class="wrap split">
        <div>
          <p class="kicker"><b>01</b> Background</p>
          <h2 id="about-title">How I got here</h2>
        </div>
        <div class="prose rise">
          <p>Data and BI analyst with 4+ years across higher education and financial services, now a Technology
            Services &amp; Collections Analyst at the University of Waikato Library. I build the reporting layer
            between messy source systems and the people who need answers: reusable templates that cut a recurring
            manual task from about 4 hours to under 1 hour, an API reporting workflow running monthly in production,
            and 5+ dashboards and reports for senior leadership, client groups and third-party stakeholders.</p>
          <p>Earlier, at Arcesium (a D.E. Shaw Group company), daily SQL for 10+ global investment clients and
            validation controls that cut the time to produce daily reconciliation reporting by 40%.</p>
          <p>I run reporting work as small projects, and hold the Project Management Professional (PMP®)
            certification. At Arcesium I managed several concurrent client workstreams end to end, from
            requirements through build, test, release and ongoing support, using clear scope, early risk
            identification, dependency mapping and timeline management to keep delivery predictable. I also
            supported release readiness through testing inputs, issue triage and stakeholder sign-off. At the
            Library the same habits show up as an 11-page working paper setting out a phased analytics roadmap,
            and as release gates that stop a monthly report if any personal text survives.
            <a href="note-every-dashboard-is-a-small-project.html">How that works at the size of a report &rarr;</a></p>
          <p>I work day to day in SharePoint (lists, libraries, permissions, reporting on SharePoint data) and Power
            Automate (approval, scheduled, file-handling and form-to-list flows); at the Library every dashboard I
            build is published through SharePoint to the team it serves.</p>

          <div class="cols">
            <div>
              <h3>Tools</h3>
              <ul class="plain">
                <li>Power BI: DAX, Power Query, data modelling</li>
                <li>SQL: SQL Server, MySQL</li>
                <li>Excel: Power Pivot, VBA</li>
                <li>SharePoint and Power Automate</li>
                <li>Tableau, Google Analytics 4, HTML reporting dashboards</li>
                <li>Python: pandas, ad-hoc scripting</li>
                <li>AI-assisted development (Claude Code)</li>
              </ul>
            </div>
            <div>
              <h3>Credentials</h3>
              <ul class="plain">
                <li>Master of Management (Business Analytics), University of Waikato, 2026</li>
                <li>Project Management Professional (PMP®), PMI</li>
                <li>MBA, Finance &amp; Financial Management, IMT Ghaziabad</li>
                <li>Microsoft Power BI and Excel courses (Coursera)</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

'''

EXPERIENCE = '''
    <section class="section" id="experience" aria-labelledby="experience-title">
      <div class="wrap">
        <p class="kicker"><b>02</b> Experience</p>
        <div class="section-head">
          <h2 id="experience-title">Where I've done it</h2>
          <a class="muted" href="resume.html">Full résumé &rarr;</a>
        </div>
        <ol class="timeline rise">
          <li>
            <span class="when">2021 – 2022</span>
            <h3>Better.com</h3>
            <p>Underwriting Analyst, in a team processing 100+ mortgage applications a week.</p>
          </li>
          <li>
            <span class="when">2022 – 2025</span>
            <h3>Arcesium</h3>
            <p>Consultant, Data Operations &amp; Client Solutions. Daily SQL and reconciliation reporting for 10+ global investment clients.
            </p>
          </li>
          <li>
            <span class="when">2025 – 2026</span>
            <h3>University of Waikato</h3>
            <p>Master of Management (Business Analytics), and Power BI dashboards for the Library.</p>
          </li>
          <li class="now">
            <span class="when">2026 – now</span>
            <h3>Waikato Library</h3>
            <p>Technology Services &amp; Collections Analyst. Dashboards, reporting workflows and templates.</p>
          </li>
        </ol>
      </div>
    </section>

'''

TOOLS = '''
    <section class="section" id="tools" aria-labelledby="tools-title">
      <div class="wrap">
        <p class="kicker"><b>03</b> Tools in practice</p>
        <div class="section-head">
          <h2 id="tools-title">Where each tool shows up</h2>
          <span class="muted">Every dot links to the evidence</span>
        </div>
        <div class="matrix-card rise">
          <table class="matrix">
            <thead><tr><th scope="col"><span class="sr-only">Tool</span></th><th scope="col" data-col="0"><a href="powerbi-retail.html">Retail Sales &amp; Returns</a><small>Power BI</small></th><th scope="col" data-col="1"><a href="powerbi-air-nz.html">Air New Zealand</a><small>Power BI</small></th><th scope="col" data-col="2"><a href="sql-nz-building-consents.html">Building Consents</a><small>SQL</small></th><th scope="col" data-col="3"><a href="python_nz_housing_affordability.html">Housing Affordability</a><small>Python</small></th><th scope="col" data-col="4"><a href="python_business_financials.html">Business Financials</a><small>Python</small></th><th scope="col" class="sep" data-col="5"><a href="resume.html#role-technology-services-collections-analyst">Waikato Library</a><small>2025 – now</small></th><th scope="col" data-col="6"><a href="resume.html#role-consultant-data-operations-client-solutions">Arcesium</a><small>2022 – 2025</small></th></tr></thead>
            <tbody>
              <tr><th scope="row">Power BI</th><td data-col="0"><a class="dot" href="powerbi-retail.html#built" aria-label="Power BI: see Retail Sales and Returns"></a></td><td data-col="1"><a class="dot" href="powerbi-air-nz.html#built" aria-label="Power BI: see Air New Zealand"></a></td><td data-col="2"><span class="sr-only">not used</span></td><td data-col="3"><span class="sr-only">not used</span></td><td data-col="4"><span class="sr-only">not used</span></td><td class="sep" data-col="5"><a class="dot" href="resume.html#role-student-assistant-library-collections-strategy-access" aria-label="Power BI: see Waikato Library"></a></td><td data-col="6"><a class="dot" href="resume.html#role-consultant-data-operations-client-solutions" aria-label="Power BI: see Arcesium"></a></td></tr>
              <tr><th scope="row">DAX</th><td data-col="0"><a class="dot" href="powerbi-retail.html#dax" aria-label="DAX: see Retail Sales and Returns"></a></td><td data-col="1"><a class="dot" href="powerbi-air-nz.html#dax" aria-label="DAX: see Air New Zealand"></a></td><td data-col="2"><span class="sr-only">not used</span></td><td data-col="3"><span class="sr-only">not used</span></td><td data-col="4"><span class="sr-only">not used</span></td><td class="sep" data-col="5"><a class="dot" href="resume.html#role-student-assistant-library-collections-strategy-access" aria-label="DAX: see Waikato Library"></a></td><td data-col="6"><a class="dot" href="resume.html#role-consultant-data-operations-client-solutions" aria-label="DAX: see Arcesium"></a></td></tr>
              <tr><th scope="row">Power Query</th><td data-col="0"><a class="dot" href="powerbi-retail.html#built" aria-label="Power Query: see Retail Sales and Returns"></a></td><td data-col="1"><a class="dot" href="powerbi-air-nz.html#built" aria-label="Power Query: see Air New Zealand"></a></td><td data-col="2"><span class="sr-only">not used</span></td><td data-col="3"><span class="sr-only">not used</span></td><td data-col="4"><span class="sr-only">not used</span></td><td class="sep" data-col="5"><a class="dot" href="resume.html#role-student-assistant-library-collections-strategy-access" aria-label="Power Query: see Waikato Library"></a></td><td data-col="6"><span class="sr-only">not used</span></td></tr>
              <tr><th scope="row">Data modelling</th><td data-col="0"><a class="dot" href="powerbi-retail.html#diagram" aria-label="Data modelling: see Retail Sales and Returns"></a></td><td data-col="1"><a class="dot" href="powerbi-air-nz.html#diagram" aria-label="Data modelling: see Air New Zealand"></a></td><td data-col="2"><a class="dot" href="sql-nz-building-consents.html#diagram" aria-label="Data modelling: see Building Consents"></a></td><td data-col="3"><span class="sr-only">not used</span></td><td data-col="4"><span class="sr-only">not used</span></td><td class="sep" data-col="5"><a class="dot" href="resume.html#role-technology-services-collections-analyst" aria-label="Data modelling: see Waikato Library"></a></td><td data-col="6"><a class="dot" href="resume.html#role-consultant-data-operations-client-solutions" aria-label="Data modelling: see Arcesium"></a></td></tr>
              <tr><th scope="row">SQL</th><td data-col="0"><span class="sr-only">not used</span></td><td data-col="1"><span class="sr-only">not used</span></td><td data-col="2"><a class="dot" href="sql-nz-building-consents.html#sql" aria-label="SQL: see Building Consents"></a></td><td data-col="3"><span class="sr-only">not used</span></td><td data-col="4"><span class="sr-only">not used</span></td><td class="sep" data-col="5"><a class="dot" href="resume.html#role-technology-services-collections-analyst" aria-label="SQL: see Waikato Library"></a></td><td data-col="6"><a class="dot" href="resume.html#role-consultant-data-operations-client-solutions" aria-label="SQL: see Arcesium"></a></td></tr>
              <tr><th scope="row">Excel</th><td data-col="0"><span class="sr-only">not used</span></td><td data-col="1"><span class="sr-only">not used</span></td><td data-col="2"><span class="sr-only">not used</span></td><td data-col="3"><span class="sr-only">not used</span></td><td data-col="4"><span class="sr-only">not used</span></td><td class="sep" data-col="5"><a class="dot" href="resume.html#role-technology-services-collections-analyst" aria-label="Excel: see Waikato Library"></a></td><td data-col="6"><a class="dot" href="resume.html#role-consultant-data-operations-client-solutions" aria-label="Excel: see Arcesium"></a></td></tr>
              <tr><th scope="row">Python</th><td data-col="0"><span class="sr-only">not used</span></td><td data-col="1"><span class="sr-only">not used</span></td><td data-col="2"><a class="dot" href="sql-nz-building-consents.html#model" aria-label="Python: see Building Consents"></a></td><td data-col="3"><a class="dot" href="python_nz_housing_affordability.html#built" aria-label="Python: see Housing Affordability"></a></td><td data-col="4"><a class="dot" href="python_business_financials.html#built" aria-label="Python: see Business Financials"></a></td><td class="sep" data-col="5"><span class="sr-only">not used</span></td><td data-col="6"><a class="dot" href="resume.html#role-consultant-data-operations-client-solutions" aria-label="Python: see Arcesium"></a></td></tr>
              <tr><th scope="row">SharePoint</th><td data-col="0"><span class="sr-only">not used</span></td><td data-col="1"><span class="sr-only">not used</span></td><td data-col="2"><span class="sr-only">not used</span></td><td data-col="3"><span class="sr-only">not used</span></td><td data-col="4"><span class="sr-only">not used</span></td><td class="sep" data-col="5"><a class="dot" href="resume.html#role-technology-services-collections-analyst" aria-label="SharePoint: see Waikato Library"></a></td><td data-col="6"><a class="dot" href="resume.html#role-consultant-data-operations-client-solutions" aria-label="SharePoint: see Arcesium"></a></td></tr>
              <tr><th scope="row">Power Automate</th><td data-col="0"><span class="sr-only">not used</span></td><td data-col="1"><span class="sr-only">not used</span></td><td data-col="2"><span class="sr-only">not used</span></td><td data-col="3"><span class="sr-only">not used</span></td><td data-col="4"><span class="sr-only">not used</span></td><td class="sep" data-col="5"><a class="dot" href="resume.html#role-technology-services-collections-analyst" aria-label="Power Automate: see Waikato Library"></a></td><td data-col="6"><a class="dot" href="resume.html#role-consultant-data-operations-client-solutions" aria-label="Power Automate: see Arcesium"></a></td></tr>
              <tr><th scope="row">Tableau</th><td data-col="0"><span class="sr-only">not used</span></td><td data-col="1"><span class="sr-only">not used</span></td><td data-col="2"><span class="sr-only">not used</span></td><td data-col="3"><span class="sr-only">not used</span></td><td data-col="4"><span class="sr-only">not used</span></td><td class="sep" data-col="5"><span class="sr-only">not used</span></td><td data-col="6"><a class="dot" href="resume.html#role-consultant-data-operations-client-solutions" aria-label="Tableau: see Arcesium"></a></td></tr>
              <tr><th scope="row">Google Analytics 4</th><td data-col="0"><span class="sr-only">not used</span></td><td data-col="1"><span class="sr-only">not used</span></td><td data-col="2"><span class="sr-only">not used</span></td><td data-col="3"><span class="sr-only">not used</span></td><td data-col="4"><span class="sr-only">not used</span></td><td class="sep" data-col="5"><a class="dot" href="resume.html#role-technology-services-collections-analyst" aria-label="Google Analytics 4: see Waikato Library"></a></td><td data-col="6"><span class="sr-only">not used</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

'''

STATEMENT = '''
    <section class="statement" aria-label="Approach">
      <div class="wrap">
        <blockquote class="rise">I build the reporting layer between messy source systems and <em>the people who need
            answers.</em></blockquote>
        <p class="by rise r1">Every dashboard I build at the Library is published through SharePoint to the team it
          serves.</p>
      </div>
    </section>

'''

