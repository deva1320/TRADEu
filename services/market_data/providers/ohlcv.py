from abc import ABC, abstractmethod
from collections.abc import Iterable

from services.market_data.ohlcv import OHLCVRecord


class MarketDataProvider(ABC):
    @abstractmethod
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
    ) -> Iterable[OHLCVRecord]:
        """
        Fetch normalized OHLCV records for one instrument.
        """
        raise NotImplementedError
