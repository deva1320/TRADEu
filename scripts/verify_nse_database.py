import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv(Path("apps/api/.env"))

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM market.instruments i
            JOIN market.exchanges e
                ON e.id = i.exchange_id
            WHERE e.code = 'NSE'
        """)
        print("NSE instrument count:", cur.fetchone()[0])

        cur.execute("""
            SELECT COUNT(*)
            FROM market.instruments i
            JOIN market.exchanges e
                ON e.id = i.exchange_id
            WHERE e.code = 'NSE'
              AND i.instrument_type = 'EQUITY'
              AND i.is_active = TRUE
        """)
        print("Active NSE equities:", cur.fetchone()[0])
