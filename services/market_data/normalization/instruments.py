from services.market_data.instrument import InstrumentRecord


def normalize_instrument(
    *,
    exchange_code: str,
    symbol: str,
    name: str | None,
    instrument_type: str,
    exchange_symbol: str | None = None,
    trading_symbol: str | None = None,
    isin: str | None = None,
    currency: str = "INR",
    sector: str | None = None,
    industry: str | None = None,
    is_active: bool = True,
) -> InstrumentRecord:
    return InstrumentRecord(
        exchange_code=exchange_code.strip().upper(),
        symbol=symbol.strip().upper(),
        name=name.strip() if name else None,
        instrument_type=instrument_type.strip().upper(),
        exchange_symbol=exchange_symbol.strip() if exchange_symbol else None,
        trading_symbol=trading_symbol.strip() if trading_symbol else None,
        isin=isin.strip().upper() if isin else None,
        currency=currency.strip().upper(),
        sector=sector.strip() if sector else None,
        industry=industry.strip() if industry else None,
        is_active=is_active,
    )
