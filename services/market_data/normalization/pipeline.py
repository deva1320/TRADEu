from collections.abc import Iterable

from services.market_data.ohlcv import OHLCVRecord
from services.market_data.normalization.ohlcv import normalize_ohlcv
from services.market_data.providers.raw_ohlcv import RawOHLCVCandle
from services.market_data.validation.ohlcv import validate_ohlcv


def normalize_and_validate_ohlcv(
    rows: Iterable[RawOHLCVCandle],
    instrument_id: int,
    source: str,
) -> list[OHLCVRecord]:
    records: list[OHLCVRecord] = []

    for row in rows:
        record = normalize_ohlcv(
            row,
            instrument_id=instrument_id,
            source=source,
        )

        validate_ohlcv(record)
        records.append(record)

    return records
