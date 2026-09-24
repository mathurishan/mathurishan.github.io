-- ============================================================================
-- NZ BUILDING CONSENTS: 10 ANALYTICAL SQL QUERIES
-- Database: nz_building_consents.db (SQLite)
-- Data source: Stats NZ Building Consents Issued, December 2025 release
-- ============================================================================


-- ============================================================================
-- QUERY 1: Regional Pipeline Overview
-- ============================================================================
-- BUSINESS QUESTION: Which regions are driving the most construction activity
-- in the latest full year? Rank all regions by total consent value to show
-- where the building pipeline is strongest.
-- Demonstrates: aggregation, RANK() window function, multiple metrics
-- ============================================================================

SELECT
    r.region_name                                       AS region,
    SUM(f.number_of_consents)                           AS total_consents,
    ROUND(SUM(f.value_nzd) / 1e6, 1)                   AS total_value_millions,
    ROUND(SUM(f.floor_area_sqm) / 1000, 0)             AS total_floor_area_000sqm,
    ROUND(SUM(f.value_nzd) / NULLIF(SUM(f.number_of_consents), 0), 0)
                                                        AS avg_value_per_consent,
    RANK() OVER (ORDER BY SUM(f.value_nzd) DESC)        AS value_rank
FROM fact_region_consents f
JOIN dim_date d          ON f.date_id = d.date_id
JOIN dim_region r        ON f.region_id = r.region_id
JOIN dim_building_type bt ON f.building_type_id = bt.building_type_id
WHERE d.year = 2025
  AND r.is_aggregate = 0
  AND bt.building_type_name = 'All buildings'
  AND f.consent_nature = 'New'
GROUP BY r.region_name
ORDER BY value_rank;


-- ============================================================================
-- QUERY 2: Year-over-Year Growth by Region
-- ============================================================================
-- BUSINESS QUESTION: Which regions have grown or shrunk their building consent
-- volumes over the last five years? Identify where construction momentum is
-- accelerating vs stalling so resource allocation can be prioritised.
-- Demonstrates: LAG() window function, YoY percentage change calculation
-- ============================================================================

WITH annual_consents AS (
    SELECT
        r.region_name,
        d.year,
        SUM(f.number_of_consents) AS annual_consents
    FROM fact_region_consents f
    JOIN dim_date d          ON f.date_id = d.date_id
    JOIN dim_region r        ON f.region_id = r.region_id
    JOIN dim_building_type bt ON f.building_type_id = bt.building_type_id
    WHERE d.year BETWEEN 2020 AND 2025
      AND r.is_aggregate = 0
      AND bt.building_type_name = 'All buildings'
      AND f.consent_nature = 'New'
    GROUP BY r.region_name, d.year
)
SELECT
    region_name,
    year,
    annual_consents,
    LAG(annual_consents) OVER (PARTITION BY region_name ORDER BY year)
                                                    AS prev_year_consents,
    ROUND(
        (annual_consents - LAG(annual_consents)
            OVER (PARTITION BY region_name ORDER BY year))
        * 100.0
        / NULLIF(LAG(annual_consents)
            OVER (PARTITION BY region_name ORDER BY year), 0),
        1
    )                                               AS yoy_change_pct
FROM annual_consents
ORDER BY region_name, year;


-- ============================================================================
-- QUERY 3: COVID Impact and Recovery
-- ============================================================================
-- BUSINESS QUESTION: How did the COVID-19 pandemic disrupt building consent
-- activity nationally, and how quickly did the market recover? Compare
-- average monthly consent volumes across pre-COVID, COVID trough, recovery,
-- and recent periods.
-- Demonstrates: CASE WHEN period grouping, comparative aggregate analysis
-- ============================================================================

WITH monthly_national AS (
    SELECT
        d.year,
        d.month,
        f.number_of_consents,
        f.value_nzd,
        CASE
            WHEN d.year = 2019                     THEN '1. Pre-COVID (2019)'
            WHEN d.year = 2020                     THEN '2. COVID Trough (2020)'
            WHEN d.year BETWEEN 2021 AND 2022      THEN '3. Recovery (2021-22)'
            WHEN d.year BETWEEN 2023 AND 2025      THEN '4. Recent (2023-25)'
        END AS period_group
    FROM fact_region_consents f
    JOIN dim_date d          ON f.date_id = d.date_id
    JOIN dim_region r        ON f.region_id = r.region_id
    JOIN dim_building_type bt ON f.building_type_id = bt.building_type_id
    WHERE r.region_name = 'New Zealand'
      AND bt.building_type_name = 'All buildings'
      AND f.consent_nature = 'New'
      AND d.year BETWEEN 2019 AND 2025
)
SELECT
    period_group,
    COUNT(*)                                        AS months_in_period,
    SUM(number_of_consents)                         AS total_consents,
    ROUND(AVG(number_of_consents), 0)               AS avg_monthly_consents,
    ROUND(SUM(value_nzd) / 1e9, 2)                  AS total_value_billions,
    ROUND(AVG(value_nzd) / 1e6, 1)                  AS avg_monthly_value_millions
FROM monthly_national
WHERE period_group IS NOT NULL
GROUP BY period_group
ORDER BY period_group;


-- ============================================================================
-- QUERY 4: Dwelling Type Mix Shift
-- ============================================================================
-- BUSINESS QUESTION: How has the national mix of housing types changed over
-- the last decade? Are apartments and townhouses taking a larger share from
-- standalone houses, signalling a shift toward higher-density living?
-- Demonstrates: percentage of total with SUM() OVER (PARTITION BY), trends
-- ============================================================================

WITH dwelling_annual AS (
    SELECT
        d.year,
        bt.building_type_name                       AS dwelling_type,
        SUM(f.number_of_consents)                   AS consents
    FROM fact_region_consents f
    JOIN dim_date d          ON f.date_id = d.date_id
    JOIN dim_region r        ON f.region_id = r.region_id
    JOIN dim_building_type bt ON f.building_type_id = bt.building_type_id
    WHERE r.region_name = 'New Zealand'
      AND bt.building_type_name IN (
            'Houses',
            'Apartments',
            'Townhouses, flats, units, and other dwellings',
            'Retirement village units'
          )
      AND f.consent_nature = 'New'
      AND d.year BETWEEN 2015 AND 2025
    GROUP BY d.year, bt.building_type_name
)
SELECT
    year,
    dwelling_type,
    consents,
    SUM(consents) OVER (PARTITION BY year)          AS year_total,
    ROUND(
        consents * 100.0
        / SUM(consents) OVER (PARTITION BY year),
        1
    )                                               AS share_pct
FROM dwelling_annual
ORDER BY year, share_pct DESC;


-- ============================================================================
-- QUERY 5: Seasonal Patterns
-- ============================================================================
-- BUSINESS QUESTION: Is there a seasonal rhythm to building consent activity
-- in New Zealand? Identify peak and trough months so that councils and
-- developers can anticipate workload cycles.
-- Demonstrates: seasonality analysis, GROUP BY month, descriptive statistics
-- ============================================================================

SELECT
    d.month,
    d.month_name,
    d.is_summer                                     AS nz_summer,
    COUNT(*)                                        AS data_points,
    ROUND(AVG(f.number_of_consents), 0)             AS avg_consents,
    MIN(f.number_of_consents)                       AS min_consents,
    MAX(f.number_of_consents)                       AS max_consents,
    ROUND(AVG(f.value_nzd) / 1e6, 1)               AS avg_value_millions
FROM fact_region_consents f
JOIN dim_date d          ON f.date_id = d.date_id
JOIN dim_region r        ON f.region_id = r.region_id
JOIN dim_building_type bt ON f.building_type_id = bt.building_type_id
WHERE r.region_name = 'New Zealand'
  AND bt.building_type_name = 'All buildings'
  AND f.consent_nature = 'New'
  AND d.year BETWEEN 2015 AND 2025
GROUP BY d.month, d.month_name, d.is_summer
ORDER BY d.month;


-- ============================================================================
-- QUERY 6: Top 10 Territorial Authorities by Consent Volume
-- ============================================================================
-- BUSINESS QUESTION: Which local councils are processing the most building
-- consent activity? Rank the top 10 territorial authorities by total consent
-- value for the latest full year and show their region, volumes, and average
-- consent size.
-- Demonstrates: multi-table JOIN, TOP-N with LIMIT, derived metrics
-- ============================================================================

SELECT
    a.authority_name                                AS territorial_authority,
    r.region_name                                   AS region,
    SUM(f.number_of_consents)                       AS total_consents,
    ROUND(SUM(f.value_nzd) / 1e6, 1)               AS total_value_millions,
    ROUND(
        SUM(f.value_nzd)
        / NULLIF(SUM(f.number_of_consents), 0),
        0
    )                                               AS avg_value_per_consent,
    ROUND(
        SUM(f.floor_area_sqm)
        / NULLIF(SUM(f.number_of_consents), 0),
        0
    )                                               AS avg_sqm_per_consent,
    RANK() OVER (ORDER BY SUM(f.value_nzd) DESC)    AS value_rank
FROM fact_ta_consents f
JOIN dim_date d          ON f.date_id = d.date_id
JOIN dim_authority a     ON f.authority_id = a.authority_id
JOIN dim_region r        ON a.region_id = r.region_id
JOIN dim_building_type bt ON f.building_type_id = bt.building_type_id
WHERE d.year = 2025
  AND a.authority_name NOT IN ('New Zealand', 'Area Outside Territorial Authority')
  AND bt.building_type_name = 'All buildings'
  AND f.consent_nature = 'New'
GROUP BY a.authority_name, r.region_name
ORDER BY value_rank
LIMIT 10;


-- ============================================================================
-- QUERY 7: Hamilton / Waikato Deep Dive
-- ============================================================================
-- BUSINESS QUESTION: How does Hamilton City's dwelling consent trend compare
-- to the national average? Use a 3-month moving average to smooth monthly
-- noise and highlight whether Hamilton is outpacing or trailing New Zealand.
-- Demonstrates: moving average window function, subquery comparison, local relevance
-- ============================================================================

WITH hamilton AS (
    SELECT
        d.date_id,
        d.year,
        d.month,
        f.number_of_consents                        AS hamilton_consents,
        f.value_nzd                                 AS hamilton_value
    FROM fact_ta_consents f
    JOIN dim_date d          ON f.date_id = d.date_id
    JOIN dim_authority a     ON f.authority_id = a.authority_id
    JOIN dim_building_type bt ON f.building_type_id = bt.building_type_id
    WHERE a.authority_name = 'Hamilton City'
      AND bt.building_type_name = 'Dwelling units'
      AND f.consent_nature = 'New'
      AND d.year >= 2019
),
national AS (
    SELECT
        d.date_id,
        f.number_of_consents                        AS nz_consents
    FROM fact_region_consents f
    JOIN dim_date d          ON f.date_id = d.date_id
    JOIN dim_region r        ON f.region_id = r.region_id
    JOIN dim_building_type bt ON f.building_type_id = bt.building_type_id
    WHERE r.region_name = 'New Zealand'
      AND bt.building_type_name = 'Dwelling units'
      AND f.consent_nature = 'New'
      AND d.year >= 2019
)
SELECT
    h.date_id,
    h.year,
    h.month,
    h.hamilton_consents,
    n.nz_consents,
    ROUND(AVG(h.hamilton_consents)
        OVER (ORDER BY h.date_id
              ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1)
                                                    AS hamilton_3mo_avg,
    ROUND(AVG(n.nz_consents)
        OVER (ORDER BY h.date_id
              ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1)
                                                    AS nz_3mo_avg,
    ROUND(h.hamilton_consents * 100.0
        / NULLIF(n.nz_consents, 0), 2)              AS hamilton_share_pct
FROM hamilton h
JOIN national n ON h.date_id = n.date_id
ORDER BY h.date_id;


-- ============================================================================
-- QUERY 8: High-Value Consent Analysis
-- ============================================================================
-- BUSINESS QUESTION: Which regions and building types dominate the premium
-- segment of the market? Classify regions into value quartiles based on
-- average consent value and identify where high-value construction is
-- concentrated.
-- Demonstrates: NTILE() window function, derived metrics, filtering on computed values
-- ============================================================================

WITH region_value_profile AS (
    SELECT
        r.region_name,
        SUM(f.number_of_consents)                   AS total_consents,
        ROUND(SUM(f.value_nzd) / 1e6, 1)           AS total_value_millions,
        ROUND(
            SUM(f.value_nzd)
            / NULLIF(SUM(f.number_of_consents), 0),
            0
        )                                           AS avg_value_per_consent,
        ROUND(
            SUM(f.floor_area_sqm)
            / NULLIF(SUM(f.number_of_consents), 0),
            0
        )                                           AS avg_sqm_per_consent
    FROM fact_region_consents f
    JOIN dim_date d          ON f.date_id = d.date_id
    JOIN dim_region r        ON f.region_id = r.region_id
    JOIN dim_building_type bt ON f.building_type_id = bt.building_type_id
    WHERE d.year BETWEEN 2023 AND 2025
      AND r.is_aggregate = 0
      AND bt.building_type_name = 'All buildings'
      AND f.consent_nature = 'New'
    GROUP BY r.region_name
),
quartiled AS (
    SELECT
        *,
        NTILE(4) OVER (ORDER BY avg_value_per_consent) AS value_quartile
    FROM region_value_profile
)
SELECT
    region_name,
    total_consents,
    total_value_millions,
    avg_value_per_consent,
    avg_sqm_per_consent,
    value_quartile,
    CASE value_quartile
        WHEN 4 THEN 'Premium'
        WHEN 3 THEN 'Above Average'
        WHEN 2 THEN 'Below Average'
        WHEN 1 THEN 'Budget'
    END                                             AS value_segment
FROM quartiled
ORDER BY avg_value_per_consent DESC;


-- ============================================================================
-- QUERY 9: Supply Concentration Risk
-- ============================================================================
-- BUSINESS QUESTION: How concentrated is New Zealand's dwelling supply
-- pipeline? What percentage of national consents come from the top 3 regions,
-- and has this concentration increased or decreased over the last decade?
-- Demonstrates: cumulative percentage, RANK(), trend analysis, strategic insight
-- ============================================================================

WITH regional_annual AS (
    SELECT
        d.year,
        r.region_name,
        SUM(f.number_of_consents)                   AS consents
    FROM fact_region_consents f
    JOIN dim_date d          ON f.date_id = d.date_id
    JOIN dim_region r        ON f.region_id = r.region_id
    JOIN dim_building_type bt ON f.building_type_id = bt.building_type_id
    WHERE r.is_aggregate = 0
      AND bt.building_type_name = 'Dwelling units'
      AND f.consent_nature = 'New'
      AND d.year BETWEEN 2015 AND 2025
    GROUP BY d.year, r.region_name
),
ranked AS (
    SELECT
        year,
        region_name,
        consents,
        RANK() OVER (PARTITION BY year ORDER BY consents DESC) AS rk,
        SUM(consents) OVER (PARTITION BY year)      AS national_total
    FROM regional_annual
)
SELECT
    year,
    GROUP_CONCAT(
        CASE WHEN rk <= 3 THEN region_name END, ', '
    )                                               AS top_3_regions,
    SUM(CASE WHEN rk <= 3 THEN consents ELSE 0 END)
                                                    AS top_3_consents,
    MAX(national_total)                             AS national_total,
    ROUND(
        SUM(CASE WHEN rk <= 3 THEN consents ELSE 0 END)
        * 100.0 / MAX(national_total),
        1
    )                                               AS top_3_share_pct
FROM ranked
GROUP BY year
ORDER BY year;


-- ============================================================================
-- QUERY 10: Quarterly Executive Summary View
-- ============================================================================
-- BUSINESS QUESTION: Provide a single view that a manager can query for any
-- quarter to see total consents, total value, average floor area, quarter-on-
-- quarter change, year-on-year change, and the top-performing region. This
-- serves as a go-to executive reporting layer.
-- Demonstrates: CREATE VIEW, multiple LAG() window functions, subquery for top region
-- ============================================================================

-- (See queries/create_view.sql for the CREATE VIEW statement)
-- This query selects from the view for the most recent 8 quarters:

SELECT *
FROM vw_quarterly_executive
ORDER BY year DESC, quarter DESC
LIMIT 8;
