from dataclasses import dataclass

from kudi.currency_codes import CurrencyCode
from kudi.currencies_data import CURRENCIES_DATA, CurrencyData
from kudi.formatter import Formatter


@dataclass(frozen=True)
class Currency:
    code: CurrencyCode
    minor_unit: int
    symbol: str
    template: str
    minor_unit_separator: str
    thousand_delimiter: str

    @property
    def formatter(self) -> Formatter:
        return Formatter(
            self.minor_unit,
            self.minor_unit_separator,
            self.thousand_delimiter,
            self.symbol,
            self.template,
        )

    def __eq__(self, other):
        return (
            self.code == other.code
            and self.minor_unit == other.minor_unit
            and self.symbol == other.symbol
            and self.template == other.template
            and self.minor_unit_separator == other.minor_unit_separator
            and self.thousand_delimiter == other.thousand_delimiter
            and self.thousand_delimiter == other.thousand_delimiter
        )


def _get_currency_init_kwargs(code: CurrencyCode, data: CurrencyData) -> dict:
    return {
        "code": code,
        "minor_unit": data["minor_unit"],
        "symbol": data["symbol"],
        "template": data["template"],
        "minor_unit_separator": data["minor_unit_separator"],
        "thousand_delimiter": data["thousand_delimiter"],
    }


CURRENCIES = {
    code: Currency(**_get_currency_init_kwargs(code, data))
    for code, data in CURRENCIES_DATA.items()
}


def _get_currency(code: CurrencyCode) -> Currency:
    currency = CURRENCIES.get(code, None)
    if not currency:  # TODO: Raise Error
        ...
    return currency
