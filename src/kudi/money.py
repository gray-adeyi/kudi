from __future__ import annotations
from decimal import Decimal

from kudi.calculator import Calculator
from kudi.currencies_data import _get_currency_code_from_numeric_code
from kudi.currency_codes import CurrencyCode

from kudi.currency import _get_currency, Currency
from kudi.exceptions import (
    InvalidCurrencyAlphaCodeError,
    InvalidCurrencyNumericCodeError,
    CurrencyMismatchError,
)


class Money:
    def __init__(
        self, amount: str | int | float | Decimal, code: int | str | CurrencyCode
    ):
        self._currency: Currency = _get_currency(self._normalize_code(code))
        self._amount: int = self._normalize_amount(amount, self._currency)

    @property
    def amount(self) -> int:
        """Returns the money value"""
        return self._amount

    @property
    def currency(self) -> Currency:
        """Returns the currency used by the money"""
        return self._currency

    def is_same_currency_with(self, other: "Money") -> bool:
        """Checks if the other money provided is of the same currency with this one."""
        return self.currency == other.currency

    @property
    def is_zero(self) -> bool:
        return self.amount == 0

    @property
    def is_positive(self) -> bool:
        return self.amount > 0

    @property
    def is_negative(self) -> bool:
        return self.amount < 0

    def split(self, n: int) -> list["Money"]:
        if n <= 0:
            raise ValueError("n must be greater than 0")
        a = Calculator.divide(self.amount, n)
        ms = []
        i = 0
        while i < n:
            ms.append(Money(a, self.currency.code))
            i += 1
        r = Calculator.modulus(self.amount, n)
        l_ = Calculator.absolute(r)
        # Add leftovers to the first parties.
        v = 1
        if self.amount < 0:
            v = -1
        p = 0
        while l_ != 0:
            ms[p].amount = Calculator.add(ms[p].amount, v)
            l_ -= 1
        return ms

    def allocate(self, *rs: int) -> list["Money"]:
        if len(rs) == 0:
            raise ValueError("no ratios specified")
        # calculate the sum of ratios.
        for r in rs:
            if r < 0:
                raise ValueError("negative ratios not allowed, ratios must be positive")
        sum_ = sum(rs)

        total = 0
        ms = []
        for r in rs:
            party = Money(Calculator.allocate(self.amount, r, sum_), self.currency.code)
            ms.append(party)
            total += party.amount

        # if the sum of all ratios is zero, then we just return zeros and don't do anything
        # with the leftover
        if sum_ == 0:
            return ms

        # Calculate leftover value and divide to first parties.
        lo = self.amount - total
        sub = 1
        if lo < 0:
            sub = -sub

        p = 0
        while lo != 0:
            ms[p].amount = Calculator.add(ms[p].amount, sub)
            lo -= sub
        return ms

    def as_major_units(self): ...

    def _normalize_code(self, code: int | str | CurrencyCode) -> CurrencyCode:
        if isinstance(code, CurrencyCode):
            return code
        if isinstance(code, int):
            code = str(code)
            if 3 < len(code) > 3:
                raise InvalidCurrencyNumericCodeError(
                    f"`{code}` is an invalid numeric currency code, please use 3-digit ISO code e.g.`840` for `USD`"
                )
        if code.isnumeric():
            return _get_currency_code_from_numeric_code(code)
        if len(code) < 3:
            raise InvalidCurrencyAlphaCodeError(
                f"`{code}` is an invalid currency code, please use 3-letter ISO code e.g. `USD`"
            )
        try:
            return CurrencyCode(code.upper())
        except ValueError:
            raise InvalidCurrencyAlphaCodeError(
                f"`{code}` is an invalid currency code, please use 3-letter ISO code e.g. `USD`"
            )

    def _normalize_amount(
        self, amount: str | int | float | Decimal, currency: Currency
    ) -> int:
        if isinstance(amount, int):
            return amount
        if isinstance(amount, str):
            if not amount.isnumeric():
                raise ValueError(f"`{amount}` is not a valid amount")
        if isinstance(amount, float):
            ...
        if isinstance(amount, Decimal):
            ...
        raise ValueError(f"`{amount}` is not a valid amount")

    def _assert_is_same_currency_with(self, other: "Money"):
        try:
            assert self.is_same_currency_with(other)
        except AssertionError:
            raise CurrencyMismatchError(
                "operations on monies with different currencies is not allowed"
            )

    def _compare(self, other: "Money") -> int:
        if self.amount > other.amount:
            return 1
        if self.amount < other.amount:
            return -1
        return 0

    def __eq__(self, other: "Money") -> bool:
        self._assert_is_same_currency_with(other)
        return self._compare(other) == 0

    def __gt__(self, other: "Money") -> bool:
        self._assert_is_same_currency_with(other)
        return self._compare(other) == 1

    def __ge__(self, other: "Money") -> bool:
        self._assert_is_same_currency_with(other)
        return self._compare(other) >= 0

    def __lt__(self, other: "Money") -> bool:
        self._assert_is_same_currency_with(other)
        return self._compare(other) == -1

    def __le__(self, other: "Money") -> bool:
        self._assert_is_same_currency_with(other)
        return self._compare(other) <= 0

    def __abs__(self):
        return Money(Calculator.absolute(self.amount), self.currency.code)

    def __neg__(self):
        return Money(Calculator.negative(self.amount), self.currency.code)

    def __add__(self, other: "Money") -> Money:
        self._assert_is_same_currency_with(other)
        return Money(Calculator.add(self.amount, other.amount), self.currency.code)

    def __sub__(self, other: "Money"):
        self._assert_is_same_currency_with(other)
        return Money(Calculator.subtract(self.amount, other.amount), self.currency.code)

    def __mul__(self, by: int) -> Money:
        # TODO: Check if by is int
        return Money(Calculator.multiply(self.amount, by), self.currency.code)

    def __round__(self, n=None):
        return Money(
            Calculator.round(self.amount, self.currency.minor_unit), self.currency.code
        )

    def __str__(self): ...

    def __repr__(self):
        return f"Money(amount={self.amount}, code={self.currency.code})"
