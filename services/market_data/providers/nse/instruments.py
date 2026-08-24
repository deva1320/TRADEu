from dataclasses import dataclass
from typing import Iterable

from services.market_data.instrument import InstrumentRecord
from services.market_data.instrument_types import InstrumentType


@dataclass(frozen=True)
class NSEInstrumentRow:
    symbol: str
    series: str
    isin: str | None
    name: str | None
    is_active: bool = True


class NSEInstrumentProvider:
    """
    Adapter for NSE official security-master data.

    The provider is intentionally separated from normalization,
    validation, and database persistence.

    For the canonical NSE equity universe, only active EQ-series
    records are accepted.
    """

    exchange_code = "NSE"

    def normalize_row(self, row: NSEInstrumentRow) -> InstrumentRecord:
        if not row.is_active:
            raise ValueError(
                f"Inactive NSE instrument cannot be normalized: {row.symbol}"
            )

        instrument_type = self._map_instrument_type(row.series)

        return InstrumentRecord(
            exchange_code=self.exchange_code,
            symbol=row.symbol,
            name=row.name,
            instrument_type=instrument_type,
            exchange_symbol=row.symbol,
            trading_symbol=row.symbol,
            isin=row.isin,
            currency="INR",
            is_active=True,
        )

    @staticmethod
    def _map_instrument_type(series: str) -> str:
        series = series.strip().upper()

        if series == "EQ":
            return InstrumentType.EQUITY.value

        raise ValueError(
            f"Unsupported NSE security series for canonical equity import: {series}"
        )

    def transform_rows(
        self,
        rows: Iterable[NSEInstrumentRow],
    ) -> list[InstrumentRecord]:
        return [
            self.normalize_row(row)
            for row in rows
        ]
