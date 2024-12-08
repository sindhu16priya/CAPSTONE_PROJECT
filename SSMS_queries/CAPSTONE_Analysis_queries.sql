-------Query-1: Year-Wise Export Data for Top 5 Countries (based on avg(export_value)) for ALL EXPORTS
WITH AvgExport AS (
    SELECT 
        c.country_id,
        c.country_name,
        AVG(e.export_value) AS avg_export
    FROM fact_export_data e
    JOIN dim_country c ON e.country_id = c.country_id
    JOIN dim_indicator i ON e.indicator_id = i.indicator_id
    WHERE 
    i.indicator_name IN (
        'Fuel exports (% of merchandise exports)',
        'Exports of goods and services (% of GDP)',
        'Energy imports, net (% of energy use)',
        'High-technology exports (% of manufactured exports)'
    )
    GROUP BY c.country_id, c.country_name
),
Top5Countries AS (
    SELECT TOP 5 country_id
    FROM AvgExport
    ORDER BY avg_export DESC
)
SELECT 
    c.country_name,
    i.indicator_name,
    t.year,
    e.export_value
FROM fact_export_data e
JOIN dim_country c ON e.country_id = c.country_id
JOIN dim_indicator i ON e.indicator_id = i.indicator_id
JOIN dim_time t ON e.time_id = t.time_id
WHERE 
    i.indicator_name IN (
        'Fuel exports (% of merchandise exports)',
        'Exports of goods and services (% of GDP)',
        'Energy imports, net (% of energy use)',
        'High-technology exports (% of manufactured exports)'
    )
  AND c.country_id IN (SELECT country_id FROM Top5Countries)
ORDER BY c.country_name, t.year;


-----------------------------------------------------------------------------------------------------

----Query-1 for Best and Worst Export Categories for Each Country 

SELECT 
    c.country_name,
    i.indicator_name,
    MAX(f.export_value) AS best_export_value,
    MIN(f.export_value) AS worst_export_value
FROM 
    fact_export_data f
JOIN 
    dim_country c ON f.country_id = c.country_id
JOIN 
    dim_indicator i ON f.indicator_id = i.indicator_id
WHERE 
    i.indicator_name IN (
        'Fuel exports (% of merchandise exports)',
        'Exports of goods and services (% of GDP)',
        'Energy imports, net (% of energy use)',
        'High-technology exports (% of manufactured exports)'
    )
    --AND f.export_value IS NOT NULL
GROUP BY 
    c.country_name, i.indicator_name
ORDER BY 
    c.country_name, best_export_value DESC;

---------------------------------------------------------------------------------------
-----QUERY - The INCOME_GROUPS Contribution to ALL 4 EXPORTS.
SELECT 
    c.income_group,
    i.indicator_name,
    AVG(f.export_value) AS avg_export_value
FROM 
    fact_export_data f
JOIN 
    dim_country c ON f.country_id = c.country_id
JOIN 
    dim_indicator i ON f.indicator_id = i.indicator_id
WHERE 
    i.indicator_name IN (
        'Fuel exports (% of merchandise exports)',
        'Exports of goods and services (% of GDP)',
        'Energy imports, net (% of energy use)',
        'High-technology exports (% of manufactured exports)'
    )
    AND f.export_value > 0  -- Exclude negative and zero values
    AND c.income_group IS NOT NULL
GROUP BY 
    c.income_group, i.indicator_name
ORDER BY 
    c.income_group, i.indicator_name, avg_export_value DESC;

----------------------------------------------------------------------------------------
------QUERY - The BEST 5 Countries during the MILESTONE YEARS(1960's,1970's,....2010's,2020's)

WITH CountryAvg AS (
    SELECT 
        c.country_name,
        AVG(f.export_value) AS avg_export_value
    FROM 
        fact_export_data f
    JOIN 
        dim_country c ON f.country_id = c.country_id
    JOIN 
        dim_indicator i ON f.indicator_id = i.indicator_id
    JOIN 
        dim_time t ON f.time_id = t.time_id
    WHERE 
    i.indicator_name IN (
        'Fuel exports (% of merchandise exports)',
        'Exports of goods and services (% of GDP)',
        'Energy imports, net (% of energy use)',
        'High-technology exports (% of manufactured exports)'
    ) 
        AND t.is_milestone_year = 1
    GROUP BY 
        c.country_name
),
Top7Countries AS (
    SELECT TOP 7 
        country_name,
        avg_export_value
    FROM 
        CountryAvg
    ORDER BY 
        avg_export_value DESC
)
SELECT 
    c.country_name,
    t.year,
    f.export_value,
	i.indicator_name
FROM 
    fact_export_data f
JOIN 
    dim_country c ON f.country_id = c.country_id
JOIN 
    dim_indicator i ON f.indicator_id = i.indicator_id
JOIN 
    dim_time t ON f.time_id = t.time_id
JOIN 
    Top7Countries tc ON c.country_name = tc.country_name
WHERE 
    i.indicator_name IN (
        'Fuel exports (% of merchandise exports)',
        'Exports of goods and services (% of GDP)',
        'Energy imports, net (% of energy use)',
        'High-technology exports (% of manufactured exports)'
    )
    AND t.is_milestone_year = 1
ORDER BY 
    tc.avg_export_value DESC, t.year;

-----------------------------------------------------------------------------------

------QUERY - Export Trends for Emerging Markets" analysis, 
-----(we will focus on the export growth rate from last 5 years to the last year. (2018-2021))


WITH ExportValues AS (
    SELECT 
        f.country_id,
        i.indicator_name,
        t.year,
        f.export_value
    FROM 
        fact_export_data f
    JOIN 
        dim_indicator i ON f.indicator_id = i.indicator_id
    JOIN 
        dim_time t ON f.time_id = t.time_id
    WHERE 
        t.year IN (2018, 2021) -- Only consider the years 2018 and 2021
        AND f.export_value > 0  -- Only consider export values greater than 0
),
YearlyExportValues AS (
    SELECT 
        ev.country_id,
        ev.indicator_name,
        MAX(CASE WHEN ev.year = 2018 THEN ev.export_value END) AS export_value_2018,
        MAX(CASE WHEN ev.year = 2021 THEN ev.export_value END) AS export_value_2021
    FROM 
        ExportValues ev
    GROUP BY 
        ev.country_id, ev.indicator_name
),
ExportChanges AS (
    SELECT 
        c.country_name,
        yev.indicator_name,
        yev.export_value_2018,
        yev.export_value_2021,
        yev.export_value_2021 - yev.export_value_2018 AS absolute_change
    FROM 
        YearlyExportValues yev
    JOIN 
        dim_country c ON yev.country_id = c.country_id
),
RankedExportChanges AS (
    SELECT 
        ec.country_name,
        ec.indicator_name,
        ec.export_value_2018,
        ec.export_value_2021,
        ec.absolute_change,
        ROW_NUMBER() OVER (PARTITION BY ec.indicator_name ORDER BY ec.absolute_change DESC) AS rank_increase,
        ROW_NUMBER() OVER (PARTITION BY ec.indicator_name ORDER BY ec.absolute_change ASC) AS rank_decrease
    FROM 
        ExportChanges ec
)
SELECT 
    country_name,
    indicator_name,
    export_value_2018,
    export_value_2021,
    absolute_change
FROM 
    RankedExportChanges
WHERE 
    rank_increase <= 5 -- Top 5 countries with the largest increase
    OR rank_decrease <= 5 -- Top 5 countries with the largest decrease
ORDER BY 
    indicator_name, absolute_change DESC;

-----------------------------------------------------------------------------------------------------------

