from collections.abc import Iterable

from services.market_data.ingestion.ohlcv_repository import OHLCVRepository
from services.market_data.normalization.pipeline import (
    normalize_and_validate_ohlcv,
)
from services.market_data.providers.raw_ohlcv import RawOHLCVCandle


class OHLCVIngestionService:
    def __init__(self, repository: OHLCVRepository):
        self.repository = repository

    def ingest(
        self,
        rows: Iterable[RawOHLCVCandle],
        instrument_id: int,
        source: str,
    ) -> int:
        records = normalize_and_validate_ohlcv(
            rows,
            instrument_id=instrument_id,
            source=source,
        )

        self.repository.upsert_many(records)

        return len(records)
