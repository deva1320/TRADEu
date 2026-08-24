from ..instrument import InstrumentRecord
from ..instrument_types import InstrumentType


SUPPORTED_TYPES = {item.value for item in InstrumentType}


def validate_instrument(instrument: InstrumentRecord) -> None:
    if not instrument.exchange_code.strip():
        raise ValueError("exchange_code is required")

    if not instrument.symbol.strip():
        raise ValueError("symbol is required")

    if instrument.instrument_type not in SUPPORTED_TYPES:
        raise ValueError(
            f"Unsupported instrument type: {instrument.instrument_type}"
        )

    if instrument.currency != "INR":
        raise ValueError(
            f"Unsupported currency for Indian market instrument: "
            f"{instrument.currency}"
        )
