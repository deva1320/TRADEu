import csv
from pathlib import Path
from typing import Iterable

from services.market_data.providers.nse.instruments import (
    NSEInstrumentProvider,
    NSEInstrumentRow,
)


class NSESecurityMasterParser:
    """
    Parses the official NSE CM-MII security-master CSV.

    Canonical equity scope:
        DelFlg = N
        SctySrs = EQ

    Known NSE test/dummy records are excluded from the
    production instrument universe.
    """

    REQUIRED_COLUMNS = {
        "TckrSymb",
        "SctySrs",
        "FinInstrmNm",
        "ISIN",
        "DelFlg",
    }

    def __init__(self, provider: NSEInstrumentProvider | None = None):
        self.provider = provider or NSEInstrumentProvider()

    @staticmethod
    def _is_test_record(symbol: str, isin: str | None) -> bool:
        symbol = symbol.strip().upper()
        isin = (isin or "").strip().upper()

        return (
            "NSETEST" in symbol
            or isin.startswith("DUMMY")
        )

    def read_rows(self, path: Path) -> Iterable[NSEInstrumentRow]:
        with path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:

            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError("NSE file has no header.")

            missing = self.REQUIRED_COLUMNS - set(reader.fieldnames)

            if missing:
                raise ValueError(
                    f"NSE file is missing required columns: {sorted(missing)}"
                )

            for row in reader:
                symbol = (row.get("TckrSymb") or "").strip()
                series = (row.get("SctySrs") or "").strip().upper()
                del_flag = (row.get("DelFlg") or "").strip().upper()
                isin = (row.get("ISIN") or "").strip() or None

                if not symbol:
                    continue

                if del_flag == "Y":
                    continue

                if series != "EQ":
                    continue

                if self._is_test_record(symbol, isin):
                    continue

                yield NSEInstrumentRow(
                    symbol=symbol,
                    series=series,
                    isin=isin,
                    name=(row.get("FinInstrmNm") or "").strip() or None,
                    is_active=True,
                )

    def parse(self, path: Path):
        return [
            self.provider.normalize_row(row)
            for row in self.read_rows(path)
        ]
