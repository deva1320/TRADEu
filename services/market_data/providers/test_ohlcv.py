from collections.abc import Iterable
from datetime import datetime, timezone
from decimal import Decimal

from services.market_data.ohlcv import OHLCVRecord
from services.market_data.providers.ohlcv import MarketDataProvider


class TestOHLCVProvider(MarketDataProvider):
    source = "TEST"

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
    ) -> Iterable[OHLCVRecord]:

        if not symbol.strip():
            raise ValueError("symbol is required.")

        if not timeframe.strip():
            raise ValueError("timeframe is required.")

        yield OHLCVRecord(
            instrument_id=1,
            timeframe=timeframe.strip(),
            candle_time=datetime(
                2026,
                8,
                24,
                9,
                15,
                tzinfo=timezone.utc,
            ),
            open=Decimal("100.00"),
            high=Decimal("110.00"),
            low=Decimal("95.00"),
            close=Decimal("105.00"),
            volume=Decimal("100000"),
            source=self.source,
        )
