import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.market_data.providers.nse.security_master import (
    NSESecurityMasterParser,
)
from services.market_data.validation.instruments import validate_instrument


file_path = (
    ROOT
    / "data"
    / "raw"
    / "nse"
    / "NSE_CM_security_21082026.csv"
)

parser = NSESecurityMasterParser()
instruments = parser.parse(file_path)

errors = []

for index, instrument in enumerate(instruments, start=1):
    try:
        validate_instrument(instrument)
    except Exception as exc:
        errors.append(
            f"{index}: {instrument.symbol}: {exc}"
        )

missing_isin = [
    instrument.symbol
    for instrument in instruments
    if not instrument.isin
]

inactive = [
    instrument.symbol
    for instrument in instruments
    if not instrument.is_active
]

non_equity = [
    instrument.symbol
    for instrument in instruments
    if instrument.instrument_type != "EQUITY"
]

symbol_isin_pairs = [
    (instrument.symbol, instrument.isin)
    for instrument in instruments
]

duplicate_pairs = [
    pair
    for pair, count in Counter(symbol_isin_pairs).items()
    if count > 1
]

isin_counts = Counter(
    instrument.isin
    for instrument in instruments
    if instrument.isin
)

duplicate_isins = [
    isin
    for isin, count in isin_counts.items()
    if count > 1
]

print("NSE PRODUCTION VALIDATION")
print("=" * 50)
print(f"Parsed instruments       : {len(instruments)}")
print(f"Validation errors        : {len(errors)}")
print(f"Missing ISIN             : {len(missing_isin)}")
print(f"Inactive instruments     : {len(inactive)}")
print(f"Non-equity instruments   : {len(non_equity)}")
print(f"Duplicate symbol+ISIN    : {len(duplicate_pairs)}")
print(f"Duplicate ISINs          : {len(duplicate_isins)}")

if duplicate_isins:
    print()
    print("Duplicate ISINs are allowed by the current")
    print("NSE instrument model because the database")
    print("uniqueness key is (exchange_id, symbol).")

print()
print("STATUS")

if (
    len(instruments) == 3557
    and not errors
    and not missing_isin
    and not inactive
    and not non_equity
    and not duplicate_pairs
):
    print("NSE PRODUCTION DATA: READY")
else:
    print("NSE PRODUCTION DATA: REVIEW REQUIRED")

if errors:
    print()
    print("Validation errors:")
    for error in errors[:20]:
        print(f"  {error}")

if duplicate_pairs:
    print()
    print("Duplicate symbol+ISIN:")
    for pair in duplicate_pairs[:20]:
        print(f"  {pair}")
