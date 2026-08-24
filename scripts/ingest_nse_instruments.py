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
from services.market_data.ingestion.instrument_repository import (
    InstrumentRepository,
)
from services.market_data.validation.instruments import validate_instrument


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


# ---------------------------------------------------------
# 1. Parse and validate the complete source before DB work
# ---------------------------------------------------------

parser = NSESecurityMasterParser()
instruments = parser.parse(file_path)

if len(instruments) != 3557:
    raise RuntimeError(
        f"Expected 3557 instruments, got {len(instruments)}."
    )

for instrument in instruments:
    validate_instrument(instrument)


print("NSE INGESTION")
print("=" * 50)
print(f"Validated instruments : {len(instruments)}")


# ---------------------------------------------------------
# 2. Open one transaction for the complete batch
# ---------------------------------------------------------

try:
    with psycopg.connect(database_url) as connection:

        repository = InstrumentRepository(connection)

        print("Beginning database transaction...")

        repository.upsert_many(instruments)

        # Verify the transaction-local database state.
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM market.instruments i
                JOIN market.exchanges e
                    ON e.id = i.exchange_id
                WHERE e.code = 'NSE'
            """)

            count = cursor.fetchone()[0]

        print(f"NSE records after upsert : {count}")

        if count != 3557:
            raise RuntimeError(
                f"Database verification failed. "
                f"Expected 3557 NSE records, got {count}."
            )

        print("Verification passed.")
        print("Committing transaction...")

        connection.commit()

        print("NSE INGESTION: SUCCESS")

except Exception:
    print("NSE INGESTION: FAILED")
    print("Transaction was rolled back.")
    raise
