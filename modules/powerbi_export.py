import pandas as pd
from pathlib import Path

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

def export_powerbi_tables(df):

    exports = {}

    fact = df.copy()

    fact.to_csv(EXPORT_DIR/"fact_workforce.csv", index=False)
    exports["fact_workforce"] = EXPORT_DIR/"fact_workforce.csv"

    dim_department = (
        fact[["Department"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_department.insert(0,"department_id",range(1,len(dim_department)+1))

    dim_department.to_csv(
        EXPORT_DIR/"dim_department.csv",
        index=False
    )

    exports["dim_department"] = EXPORT_DIR/"dim_department.csv"

    dim_city = (
        fact[["City","State"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_city.insert(0,"city_id",range(1,len(dim_city)+1))

    dim_city.to_csv(EXPORT_DIR/"dim_city.csv",index=False)
    exports["dim_city"] = EXPORT_DIR/"dim_city.csv"

    dim_role = (
        fact[["Job_Role"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_role.insert(0,"role_id",range(1,len(dim_role)+1))

    dim_role.to_csv(EXPORT_DIR/"dim_role.csv",index=False)
    exports["dim_role"] = EXPORT_DIR/"dim_role.csv"

    return exports