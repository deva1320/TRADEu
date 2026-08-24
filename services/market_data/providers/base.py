from abc import ABC, abstractmethod
from typing import Iterable

from ..instrument import InstrumentRecord


class MarketDataProvider(ABC):
    """Provider-neutral interface for market instrument data."""

    @abstractmethod
    def fetch_instruments(self) -> Iterable[InstrumentRecord]:
        """Return normalized instruments from the provider."""
        raise NotImplementedError
