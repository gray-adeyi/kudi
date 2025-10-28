import math
from decimal import Decimal

from kudi.calculator import Calculator
from kudi.types import Amount


class Formatter:
    def __init__(
        self,
        minor_unit: int,
        minor_unit_separator: str,
        thousand_delimiter: str,
        symbol: str,
        template: str,
    ):
        self.minor_unit = minor_unit
        self.minor_unit_separator = minor_unit_separator
        self.thousand_delimiter = thousand_delimiter
        self.symbol = symbol
        self.template = template

    def format(self, amount: Amount) -> str:
        sa = f"{Calculator.absolute(amount)}"

        if len(sa) <= self.minor_unit:
            sa = f"{'0' * self.minor_unit - len(sa) + 1}{sa}"

        if self.thousand_delimiter != "":
            i = len(sa) - self.minor_unit - 3
            while i > 0:
                sa = sa[:i] + self.thousand_delimiter + sa[i:]

        if self.minor_unit > 0:
            sa = (
                sa[: len(sa) - self.minor_unit]
                + self.minor_unit_separator
                + sa[len(sa) - self.minor_unit :]
            )

        sa = self.template.replace("1", sa, 1)
        sa = sa.replace("$", self.symbol, 1)

        if amount < 0:
            sa = f"-{sa}"
        return sa

    def to_major_units(self, amount: Amount) -> Decimal:
        if self.minor_unit < 0:
            return Decimal(amount)
        return Decimal(amount) / Decimal(math.pow(10, self.minor_unit))
