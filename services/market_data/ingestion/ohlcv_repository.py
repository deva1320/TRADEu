from services.market_data.ohlcv import OHLCVRecord


class OHLCVRepository:
    def __init__(self, connection):
        self.connection = connection

    def upsert(self, record: OHLCVRecord) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO market.ohlcv (
                    instrument_id,
                    timeframe,
                    candle_time,
                    open,
                    high,
                    low,
                    close,
                    volume,
                    source
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                ON CONFLICT (
                    instrument_id,
                    timeframe,
                    candle_time
                )
                DO UPDATE SET
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low = EXCLUDED.low,
                    close = EXCLUDED.close,
                    volume = EXCLUDED.volume,
                    source = EXCLUDED.source
                """,
                (
                    record.instrument_id,
                    record.timeframe,
                    record.candle_time,
                    record.open,
                    record.high,
                    record.low,
                    record.close,
                    record.volume,
                    record.source,
                ),
            )

    def upsert_many(
        self,
        records: list[OHLCVRecord],
    ) -> None:
        for record in records:
            self.upsert(record)
