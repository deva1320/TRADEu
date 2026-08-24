from services.market_data.ohlcv import OHLCVRecord
from services.market_data.providers.raw_ohlcv import RawOHLCVCandle


def normalize_ohlcv(
    raw: RawOHLCVCandle,
    instrument_id: int,
    source: str,
) -> OHLCVRecord:
    if instrument_id <= 0:
        raise ValueError("instrument_id must be positive.")

    if not source.strip():
        raise ValueError("source is required.")

    return OHLCVRecord(
        instrument_id=instrument_id,
        timeframe=raw.timeframe.strip(),
        candle_time=raw.candle_time,
        open=raw.open,
        high=raw.high,
        low=raw.low,
        close=raw.close,
        volume=raw.volume,
        source=source.strip(),
    )
