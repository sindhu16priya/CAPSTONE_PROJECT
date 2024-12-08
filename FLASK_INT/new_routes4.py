from flask import Blueprint, render_template
from models import db  # Assuming 'db' is your SQLAlchemy object
from sqlalchemy import text

new_routes4 = Blueprint('visualizations4', __name__)

def row_to_dict(row):
    if hasattr(row, '_mapping'):
        return dict(row._mapping)
    return {f'column_{i}': value for i, value in enumerate(row)}

def fetch_top_7_countries(indicator_name):
    query = text(f"""
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
                i.indicator_name = :indicator_name
                AND t.is_milestone_year = 1
            GROUP BY 
                c.country_name
        ),
        Top10Countries AS (
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
            f.export_value
        FROM 
            fact_export_data f
        JOIN 
            dim_country c ON f.country_id = c.country_id
        JOIN 
            dim_indicator i ON f.indicator_id = i.indicator_id
        JOIN 
            dim_time t ON f.time_id = t.time_id
        JOIN 
            Top10Countries tc ON c.country_name = tc.country_name
        WHERE 
            i.indicator_name = :indicator_name
            AND t.is_milestone_year = 1
        ORDER BY 
            tc.avg_export_value DESC, t.year;
    """)
    return [row_to_dict(row) for row in db.session.execute(query, {'indicator_name': indicator_name})]

@new_routes4.route('/visualizations4')
def visualizations4():
    # Fetch data for all four indicators
    fuel_exports = fetch_top_7_countries('Fuel exports (% of merchandise exports)')
    high_tech_exports = fetch_top_7_countries('High-technology exports (% of manufactured exports)')
    goods_services_exports = fetch_top_7_countries('Exports of goods and services (% of GDP)')
    energy_imports = fetch_top_7_countries('Energy imports, net (% of energy use)')

    # Render the template with the fetched data
    return render_template(
        'visualizations4.html',
        fuel_exports=fuel_exports,
        high_tech_exports=high_tech_exports,
        goods_services_exports=goods_services_exports,
        energy_imports=energy_imports
    )
