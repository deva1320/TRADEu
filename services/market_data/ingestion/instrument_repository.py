from services.market_data.instrument import InstrumentRecord


class InstrumentRepository:
    def __init__(self, connection):
        self.connection = connection

    def upsert(self, instrument: InstrumentRecord) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO market.instruments (
                    exchange_id,
                    symbol,
                    name,
                    instrument_type,
                    exchange_symbol,
                    trading_symbol,
                    isin,
                    currency,
                    sector,
                    industry,
                    is_active
                )
                SELECT
                    e.id,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                FROM market.exchanges e
                WHERE e.code = %s
                ON CONFLICT (exchange_id, symbol)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    instrument_type = EXCLUDED.instrument_type,
                    exchange_symbol = EXCLUDED.exchange_symbol,
                    trading_symbol = EXCLUDED.trading_symbol,
                    isin = EXCLUDED.isin,
                    currency = EXCLUDED.currency,
                    sector = EXCLUDED.sector,
                    industry = EXCLUDED.industry,
                    is_active = EXCLUDED.is_active,
                    updated_at = NOW()
                """,
                (
                    instrument.symbol,
                    instrument.name,
                    instrument.instrument_type,
                    instrument.exchange_symbol,
                    instrument.trading_symbol,
                    instrument.isin,
                    instrument.currency,
                    instrument.sector,
                    instrument.industry,
                    instrument.is_active,
                    instrument.exchange_code,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Exchange not found: {instrument.exchange_code}"
                )

        self.connection.commit()
