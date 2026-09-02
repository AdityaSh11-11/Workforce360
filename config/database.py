import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

# Local Development
if DATABASE_URL is None:
    DATABASE_URL = (
        "postgresql+psycopg2://postgres:yourpassword@localhost:5432/workforce360"
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)
