from pathlib import Path
import sys
from sqlalchemy import text

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from config.database import engine

schema_path = ROOT / "database" / "schema.sql"

with open(schema_path, "r", encoding="utf-8") as file:
    sql_script = file.read()

# Execute each SQL statement
with engine.begin() as conn:
    for statement in sql_script.split(";"):
        statement = statement.strip()
        if statement:
            conn.execute(text(statement))

print("✅ InsightForge Workforce Database Initialized Successfully.")