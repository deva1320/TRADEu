from services.market_data.instrument import InstrumentRecord
from services.market_data.validation.instruments import validate_instrument


def normalize_and_validate(instrument: InstrumentRecord) -> InstrumentRecord:
    validate_instrument(instrument)
    return instrument
