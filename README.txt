Ishan Mathur — portfolio site
https://mathurishan.github.io/

Static site served by GitHub Pages from the main branch. Hand-written HTML, one
stylesheet (assets/css/site.css) and two small scripts (assets/js/site.js for the
site, assets/js/charts.js for the interactive charts). No framework.

HOW TO EDIT
  Home page ........ edit index.html directly.
  Project pages .... edit the PROJECTS list in tools/build_site.py
  Charts, SQL, DAX . tools/extras.py and tools/extras2.py
  Résumé, 404 ...... tools/build.py
  Notes (articles) . tools/notes.py
  Then, from this folder:
      python tools/build.py        rebuilds every generated page and sitemap.xml
      python tools/check_site.py   checks links, images, headings and wording
  Link-preview cards: python tools/social_cards.py (needs Pillow; Windows fonts)
  PDF résumé: print resume.html to PDF (A4, no headers) as files/Ishan-Mathur-Resume.pdf

  After changing site.css or site.js, bump CSS_V / JS_V in tools/build_site.py
  (and the ?v= numbers in index.html) so browsers fetch the new files.

CHECKS
  .github/workflows/check.yml runs tools/check_site.py on every push. It fails on
  broken links or anchors, missing images, duplicate ids, missing alt text, and
  wording that must not appear (library system names, personal details, study
  described as unfinished, "case study", and similar).

PAGES
  index.html                              Home
  powerbi-retail.html                     Retail Sales & Returns Analysis (Power BI)
  powerbi-air-nz.html                     Air New Zealand Analysis (Power BI)
  sql-nz-building-consents.html           NZ Building Consents (SQL)
  python_nz_housing_affordability.html    NZ Housing Affordability (Python)
  python_business_financials.html         NZ Business Financials (Python)
  resume.html                             Résumé (+ files/Ishan-Mathur-Resume.pdf)
  note-*.html                             Notes
  powerbi.html / sql.html / python.html   Redirects to the homepage (old links)
  economics-game.html                     EcoQuest (side project)

Fonts: Newsreader and Inter from Google Fonts.
