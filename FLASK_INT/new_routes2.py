from flask import Blueprint, render_template
from models import db
from sqlalchemy.sql import text

# Create a new Blueprint for additional visualizations
new_routes2 = Blueprint('new_routes2', __name__)

@new_routes2.route('/visualizations2')
def best_worst_exports():
    try:
        # Helper function to fetch data for a specific indicator
        def get_export_stats(indicator_name):
            query = text("""
                WITH CountryExportStats AS (
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
                        i.indicator_name = :indicator_name
                        AND c.country_name NOT IN ('Other small states', 'Small states')
                    GROUP BY 
                        c.country_name, i.indicator_name
                )
                SELECT TOP 5 *
                FROM CountryExportStats
                ORDER BY best_export_value DESC;
            """)
            result = db.session.execute(query, {"indicator_name": indicator_name}).fetchall()
            
            # Convert result to a list of dictionaries
            data = [
                {
                    "country_name": row.country_name,
                    "indicator_name": row.indicator_name,
                    "best_export_value": row.best_export_value,
                    "worst_export_value": row.worst_export_value,
                }
                for row in result
            ]
            return data

        # Fetch data for each export category
        fuel_exports = get_export_stats("Fuel exports (% of merchandise exports)")
        high_tech_exports = get_export_stats("High-technology exports (% of manufactured exports)")
        goods_services_exports = get_export_stats("Exports of goods and services (% of GDP)")
        energy_imports = get_export_stats("Energy imports, net (% of energy use)")

        # Pass data to the template
        return render_template(
            "visualizations2.html",
            fuel_exports=fuel_exports,
            high_tech_exports=high_tech_exports,
            goods_services_exports=goods_services_exports,
            energy_imports=energy_imports,
        )
    except Exception as e:
        return {"error": str(e)}
