import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]

load_dotenv(ROOT / "apps" / "api" / ".env")

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not configured.")

seeds_dir = ROOT / "database" / "seeds"
seed_files = sorted(seeds_dir.glob("*.sql"))

if not seed_files:
    raise RuntimeError("No seed files found.")

with psycopg.connect(database_url) as connection:
    for seed_file in seed_files:
        print(f"Applying {seed_file.name}...")

        sql = seed_file.read_text(
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
        print(f"Applied {seed_file.name}")

print("All seeds applied successfully.")
