-----common metadata table
select * from Metadata_Country;

----indicator tables;
select * from Fuel_exports_Metadata_Indicator;
select * from Goods_Serv_exports_Metadata_Indicator;
select * from Energy_Imports_Metadata_Indicator;
select * from High_tech_Metadata_Indicator;

-----STGing Table(Normalized)
select * from STGing_ExportData;

CREATE TABLE STGing_ExportData (
    CountryName VARCHAR(255),
    CountryCode VARCHAR(10),
    IndicatorName VARCHAR(255),
    IndicatorCode VARCHAR(50),
    Year INT, -- Normalized: Each row corresponds to one year
    Value FLOAT NULL, -- Holds the value for the year
);

-------------------------------------------------------------------------
----DIMENSION TABLES : dim_country,dim_indicator,dim_time 

-------------------------dim_country 

CREATE TABLE dim_country (
    country_id INT PRIMARY KEY NOT NULL,
    country_code VARCHAR(3) NOT NULL,
    country_name VARCHAR(255) NOT NULL,
    region VARCHAR(100),
    income_group VARCHAR(100),
    special_notes TEXT,
	create_date DATETIME ,
	update_date DATETIME
);
select * from dim_country;
---------------------------dim_time----------------------------

CREATE TABLE dim_time (
    time_id INT PRIMARY KEY NOT NULL,
    year INT NOT NULL,
    decade VARCHAR(10), -- Derived column: Represents the decade (e.g., '1960s', '1970s').
    is_milestone_year BIT DEFAULT 0, -- Derived column: Flag for significant years (e.g., 2000, 2010).
	create_date DATETIME ,
	update_date DATETIME
);

select * from dim_time;

---------------------dim_indicator----------------------------------

CREATE TABLE dim_indicator (
    indicator_id INT PRIMARY KEY NOT NULL,
    indicator_code VARCHAR(50) NOT NULL,
    indicator_name VARCHAR(255) NOT NULL,
    source_note TEXT,
    source_organization VARCHAR(255),
    indicator_category VARCHAR(100), 
	create_date DATETIME ,
	update_date DATETIME
);

select * from dim_indicator; 

---------------------------------------------------------------------------

-----------FACT TABLE---------------

CREATE TABLE fact_export_data (
    Id INT PRIMARY KEY,    
    country_id INT NOT NULL,                  
    indicator_id INT NOT NULL,                 
    time_id INT NOT NULL,                     
    export_value FLOAT,     
    create_date DATETIME,   
    update_date DATETIME,   

    -- Foreign key constraints
    CONSTRAINT fk_country FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
    CONSTRAINT fk_time FOREIGN KEY (time_id) REFERENCES dim_time(time_id),
    CONSTRAINT fk_indicator FOREIGN KEY (indicator_id) REFERENCES dim_indicator(indicator_id)
);
select * from fact_export_data;

-----------------------------------------------------------------------------------------------