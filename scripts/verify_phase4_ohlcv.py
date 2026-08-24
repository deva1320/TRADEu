import os
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import psycopg
from dotenv import load_dotenv

from services.market_data.ingestion.ohlcv_repository import OHLCVRepository
from services.market_data.ingestion.ohlcv_service import OHLCVIngestionService
from services.market_data.providers.raw_ohlcv import RawOHLCVCandle


load_dotenv(ROOT / "apps" / "api" / ".env")


TEST_INSTRUMENT_ID = 1388
TEST_SYMBOL = "20MICRONS"
TEST_TIMEFRAME = "1D"
TEST_SOURCE = "TEST"
TEST_CANDLE_TIME = datetime(
    2026,
    8,
    24,
    9,
    15,
    tzinfo=timezone.utc,
)


def main() -> None:
    row = RawOHLCVCandle(
        symbol=TEST_SYMBOL,
        timeframe=TEST_TIMEFRAME,
        candle_time=TEST_CANDLE_TIME,
        open=Decimal("100.00"),
        high=Decimal("110.00"),
        low=Decimal("95.00"),
        close=Decimal("105.00"),
        volume=Decimal("100000"),
    )

    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT symbol
                FROM market.instruments
                WHERE id = %s
                """,
                (TEST_INSTRUMENT_ID,),
            )

            instrument = cur.fetchone()

            if instrument is None:
                raise RuntimeError(
                    f"Test instrument {TEST_INSTRUMENT_ID} does not exist."
                )

            if instrument[0] != TEST_SYMBOL:
                raise RuntimeError(
                    f"Expected {TEST_SYMBOL}, found {instrument[0]}."
                )

        repository = OHLCVRepository(conn)
        service = OHLCVIngestionService(repository)

        count = service.ingest(
            [row],
            instrument_id=TEST_INSTRUMENT_ID,
            source=TEST_SOURCE,
        )

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM market.ohlcv
                WHERE instrument_id = %s
                  AND timeframe = %s
                  AND candle_time = %s
                  AND source = %s
                """,
                (
                    TEST_INSTRUMENT_ID,
                    TEST_TIMEFRAME,
                    TEST_CANDLE_TIME,
                    TEST_SOURCE,
                ),
            )

            stored = cur.fetchone()[0]

        print("PHASE 4 OHLCV VERIFICATION")
        print("=" * 50)
        print("Test instrument :", TEST_SYMBOL)
        print("Instrument ID    :", TEST_INSTRUMENT_ID)
        print("Records ingested :", count)
        print("Records stored   :", stored)

        if count != 1:
            raise RuntimeError(
                f"Expected 1 ingested record, got {count}."
            )

        if stored != 1:
            raise RuntimeError(
                f"Expected 1 stored record, got {stored}."
            )

        conn.rollback()

    print("Database transaction: ROLLED BACK")
    print("PHASE 4 OHLCV VERIFICATION: OK")


if __name__ == "__main__":
    main()
