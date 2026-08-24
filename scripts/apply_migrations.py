import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]

load_dotenv(ROOT / "apps" / "api" / ".env")

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not configured.")

migrations_dir = ROOT / "database" / "migrations"
migration_files = sorted(migrations_dir.glob("*.sql"))

if not migration_files:
    raise RuntimeError("No migration files found.")

with psycopg.connect(database_url) as connection:
    for migration_file in migration_files:
        print(f"Applying {migration_file.name}...")

        sql = migration_file.read_text(
            encoding="utf-8-sig"
        ).strip()

        statements = [
            statement.strip()
            for statement in sql.split(";")
            if statement.strip()
        ]

        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)

        connection.commit()
        print(f"Applied {migration_file.name}")

print("All migrations applied successfully.")
