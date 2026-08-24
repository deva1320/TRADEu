from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class InstrumentRecord:
    exchange_code: str
    symbol: str
    name: Optional[str]
    instrument_type: str
    exchange_symbol: Optional[str] = None
    trading_symbol: Optional[str] = None
    isin: Optional[str] = None
    currency: str = "INR"
    sector: Optional[str] = None
    industry: Optional[str] = None
    is_active: bool = True
