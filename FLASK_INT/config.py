class Config:
    SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc://@SINDHU\\SQLEXPRESS/hr?driver=ODBC+Driver+17+for+SQL+Server"
   )
    SQLALCHEMY_TRACK_MODIFICATIONS = False