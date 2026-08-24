from services.market_data.ohlcv import OHLCVRecord


def validate_ohlcv(record: OHLCVRecord) -> None:
    if record.instrument_id <= 0:
        raise ValueError("instrument_id must be positive.")

    if not record.timeframe.strip():
        raise ValueError("timeframe is required.")

    if not record.source.strip():
        raise ValueError("source is required.")

    if record.open <= 0:
        raise ValueError("open must be positive.")

    if record.high <= 0:
        raise ValueError("high must be positive.")

    if record.low <= 0:
        raise ValueError("low must be positive.")

    if record.close <= 0:
        raise ValueError("close must be positive.")

    if record.high < record.low:
        raise ValueError("high cannot be lower than low.")

    if record.high < record.open:
        raise ValueError("high cannot be lower than open.")

    if record.high < record.close:
        raise ValueError("high cannot be lower than close.")

    if record.low > record.open:
        raise ValueError("low cannot be higher than open.")

    if record.low > record.close:
        raise ValueError("low cannot be higher than close.")

    if record.volume is not None and record.volume < 0:
        raise ValueError("volume cannot be negative.")
