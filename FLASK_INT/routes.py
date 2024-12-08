from flask import Blueprint, render_template
from models import DimCountry, DimIndicator, DimTime, FactExportData
from models import db
from sqlalchemy.sql import text

# Create a Blueprint for routes
routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('dashboard.html')


@routes.route('/visualizations')
def visualizations():
    try:
        # Helper function to fetch export data for a given indicator
        def get_export_data(indicator_name):
            query = text("""
                WITH AvgExport AS (
                    SELECT 
                        c.country_id,
                        c.country_name,
                        AVG(e.export_value) AS avg_export
                    FROM fact_export_data e
                    JOIN dim_country c ON e.country_id = c.country_id
                    JOIN dim_indicator i ON e.indicator_id = i.indicator_id
                    WHERE i.indicator_name = :indicator_name AND e.export_value>0
                    GROUP BY c.country_id, c.country_name
                ),
                Top5Countries AS (
                    SELECT TOP 5 country_id
                    FROM AvgExport
                    ORDER BY avg_export DESC
                )
                SELECT 
                    c.country_name,
                    t.year,
                    e.export_value
                FROM fact_export_data e
                JOIN dim_country c ON e.country_id = c.country_id
                JOIN dim_indicator i ON e.indicator_id = i.indicator_id
                JOIN dim_time t ON e.time_id = t.time_id
                WHERE i.indicator_name = :indicator_name
                  AND c.country_id IN (SELECT country_id FROM Top5Countries)
                ORDER BY c.country_name, t.year;
            """)
            result = db.session.execute(query, {"indicator_name": indicator_name}).fetchall()
            
            # Convert result to a list of dictionaries
            data = [
                {
                    "country_name": row.country_name,
                    "year": row.year,
                    "export_value": row.export_value
                }
                for row in result
            ]
            return data

        # Fetch data for all 4 indicators
        fuel_exports = get_export_data("Fuel exports (% of merchandise exports)")
        high_tech_exports = get_export_data("High-technology exports (% of manufactured exports)")
        goods_services_exports = get_export_data("Exports of goods and services (% of GDP)")
        energy_imports = get_export_data("Energy imports, net (% of energy use)")

        # Pass data to the template
        return render_template(
            "visualizations.html",
            fuel_exports=fuel_exports,
            high_tech_exports=high_tech_exports,
            goods_services_exports=goods_services_exports,
            energy_imports=energy_imports,
        )
    except Exception as e:
        return {"error": str(e)}
