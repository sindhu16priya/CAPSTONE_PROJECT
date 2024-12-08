from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Models for Dimension Tables
class DimCountry(db.Model):
    __tablename__ = 'dim_country'
    country_id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(3), nullable=False)
    country_name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(100))
    income_group = db.Column(db.String(100))
    special_notes = db.Column(db.Text)
    create_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)

class DimIndicator(db.Model):
    __tablename__ = 'dim_indicator'
    indicator_id = db.Column(db.Integer, primary_key=True)
    indicator_code = db.Column(db.String(50), nullable=False)
    indicator_name = db.Column(db.String(255), nullable=False)
    source_note = db.Column(db.Text)
    source_organization = db.Column(db.String(255))
    indicator_category = db.Column(db.String(100))
    create_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)

class DimTime(db.Model):
    __tablename__ = 'dim_time'
    time_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    decade = db.Column(db.String(10))
    is_milestone_year = db.Column(db.Boolean, default=False)
    create_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)

# Model for Fact Table
class FactExportData(db.Model):
    __tablename__ = 'fact_export_data'
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('dim_country.country_id'), nullable=False)
    indicator_id = db.Column(db.Integer, db.ForeignKey('dim_indicator.indicator_id'), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('dim_time.time_id'), nullable=False)
    export_value = db.Column(db.Float, nullable=True)
    create_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)