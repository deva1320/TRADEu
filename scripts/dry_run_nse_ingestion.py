import os
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.market_data.providers.nse.security_master import (
    NSESecurityMasterParser,
)

load_dotenv(ROOT / "apps" / "api" / ".env")

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not configured.")

file_path = (
    ROOT
    / "data"
    / "raw"
    / "nse"
    / "NSE_CM_security_21082026.csv"
)

parser = NSESecurityMasterParser()
instruments = parser.parse(file_path)

print("NSE DATABASE DRY RUN")
print("=" * 50)
print(f"Incoming instruments : {len(instruments)}")

with psycopg.connect(database_url) as connection:
    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT id, code, name
            FROM market.exchanges
            WHERE code = 'NSE'
        """)

        exchange = cursor.fetchone()

        if exchange is None:
            raise RuntimeError(
                "NSE exchange does not exist in market.exchanges."
            )

        exchange_id, exchange_code, exchange_name = exchange

        print(f"Exchange              : {exchange_code}")
        print(f"Exchange ID           : {exchange_id}")
        print(f"Exchange name         : {exchange_name}")

        cursor.execute("""
            SELECT COUNT(*)
            FROM market.instruments
            WHERE exchange_id = %s
        """, (exchange_id,))

        existing_count = cursor.fetchone()[0]

        print(f"Existing NSE records  : {existing_count}")

        symbols = [
            instrument.symbol
            for instrument in instruments
        ]

        cursor.execute("""
            SELECT symbol
            FROM market.instruments
            WHERE exchange_id = %s
              AND symbol = ANY(%s)
        """, (exchange_id, symbols))

        existing_symbols = {
            row[0]
            for row in cursor.fetchall()
        }

        updates = [
            instrument
            for instrument in instruments
            if instrument.symbol in existing_symbols
        ]

        inserts = [
            instrument
            for instrument in instruments
            if instrument.symbol not in existing_symbols
        ]

        print(f"Incoming symbols      : {len(symbols)}")
        print(f"Already existing      : {len(updates)}")
        print(f"Would insert          : {len(inserts)}")
        print(f"Would update          : {len(updates)}")

        print()
        print("DRY RUN ONLY")
        print("No database changes were made.")

        if len(symbols) != len(set(symbols)):
            print()
            print("WARNING: duplicate incoming symbols detected.")

        else:
            print()
            print("Incoming symbol uniqueness: OK")
