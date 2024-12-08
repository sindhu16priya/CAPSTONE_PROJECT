from flask import Blueprint, render_template
from models import DimCountry, DimIndicator, FactExportData
from models import db
from sqlalchemy.sql import text
import plotly.express as px
import pandas as pd 

# Create a Blueprint for the new route
new_routes3 = Blueprint('new_routes3', __name__)

@new_routes3.route('/visualizations3')
def visualizations3():
    try:
        query = text("""
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
        """)

        # Execute the query and fetch results
        result = db.session.execute(query).fetchall()

        # Convert result to a Pandas DataFrame
        data = [
            {
                "income_group": row.income_group,
                "indicator_name": row.indicator_name,
                "avg_export_value": row.avg_export_value
            }
            for row in result
        ]
        
        df = pd.DataFrame(data)

        # Create Pie charts for each indicator
        fig_fuel = px.pie(df[df['indicator_name'] == 'Fuel exports (% of merchandise exports)'], 
                          names='income_group', 
                          values='avg_export_value', 
                          title='Fuel Exports by Income Group')
        
        fig_goods = px.pie(df[df['indicator_name'] == 'Exports of goods and services (% of GDP)'], 
                           names='income_group', 
                           values='avg_export_value', 
                           title='Exports of Goods and Services by Income Group')
        
        fig_energy = px.pie(df[df['indicator_name'] == 'Energy imports, net (% of energy use)'], 
                            names='income_group', 
                            values='avg_export_value', 
                            title='Energy Imports by Income Group')
        
        fig_hightech = px.pie(df[df['indicator_name'] == 'High-technology exports (% of manufactured exports)'], 
                              names='income_group', 
                              values='avg_export_value', 
                              title='High-tech Exports by Income Group')

        # Convert figures to HTML for embedding in the template
        pie_fuel_html = fig_fuel.to_html(full_html=False)
        pie_goods_html = fig_goods.to_html(full_html=False)
        pie_energy_html = fig_energy.to_html(full_html=False)
        pie_hightech_html = fig_hightech.to_html(full_html=False)

        # Pass the figures to the template
        return render_template(
            'visualizations3.html',
            pie_fuel_html=pie_fuel_html,
            pie_goods_html=pie_goods_html,
            pie_energy_html=pie_energy_html,
            pie_hightech_html=pie_hightech_html
        )

    except Exception as e:
        return {"error": str(e)}
