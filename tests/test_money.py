from unittest import TestCase
from kudi import Money
from kudi.currency_codes import CurrencyCode
from kudi.exceptions import InvalidCurrencyAlphaCodeError, CurrencyMismatchError


class MoneyTestCase(TestCase):
    def test_can_create_money_obj(self):
        m = Money(1, "EUR")
        self.assertEqual(m.amount, 1, f"Expected {1} got {m.amount}")
        self.assertEqual(
            m.currency.code, CurrencyCode.EUR, f"Expected EUR got {m.currency.code}"
        )
        m = Money(-100, "eur")
        self.assertEqual(m.amount, -100)
        self.assertEqual(m.currency.code, CurrencyCode.EUR)

    def test_money_raises_error_on_wrong_currency(self):
        with self.assertRaises(InvalidCurrencyAlphaCodeError) as context:
            Money(100, "BTC")
        self.assertEqual(
            context.exception.args[0],
            "`BTC` is an invalid currency code, please use 3-letter ISO code e.g. `USD`",
        )

    def test_money_can_detect_same_currency(self):
        m = Money(0, "EUR")
        om = Money(0, "USD")
        self.assertFalse(
            m.is_same_currency_with(om),
            "expected money of difference currencies not to match",
        )
        om = Money(0, "EUR")
        self.assertTrue(
            m.is_same_currency_with(om), "expected money of similar currencies to match"
        )

    def test_can_evaluate_money_equality(self):
        m = Money(0, "EUR")
        samples = [
            {"amount": -1, "expected": False},
            {"amount": 0, "expected": True},
            {"amount": 1, "expected": False},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check equality of money with amount of 0 with money of amount {amount}"
            ):
                om = Money(amount, "EUR")
                self.assertEqual(
                    m == om,
                    expected,
                    f"expected money with amount of 0 to be == money of amount of {amount} to be {expected}",
                )

    def test_money_equality_on_different_currencies_raises_error(self):
        eur = Money(0, "EUR")
        usd = Money(0, "USD")
        with self.assertRaises(CurrencyMismatchError) as context:
            eur == usd
        self.assertEqual(
            context.exception.args[0],
            "operations on monies with different currencies is not allowed",
        )

    def test_can_evaluate_money_greater_than(self):
        m = Money(0, "EUR")
        samples = [
            {"amount": -1, "expected": True},
            {"amount": 0, "expected": False},
            {"amount": 1, "expected": False},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check greater than operation of money with amount of 0 with money of amount {amount}"
            ):
                om = Money(amount, "EUR")
                self.assertEqual(
                    m > om,
                    expected,
                    f"expected money with amount of 0 to be > money of amount of {amount} to be {expected}",
                )

    def test_can_evaluate_money_greater_than_or_equal(self):
        m = Money(0, "EUR")
        samples = [
            {"amount": -1, "expected": True},
            {"amount": 0, "expected": True},
            {"amount": 1, "expected": False},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check greater than or equal to operation of money with amount of 0 with money of amount {amount}"
            ):
                om = Money(amount, "EUR")
                self.assertEqual(
                    m >= om,
                    expected,
                    f"expected money with amount of 0 to be >= money of amount of {amount} to be {expected}",
                )

    def test_can_evaluate_money_less_than(self):
        m = Money(0, "EUR")
        samples = [
            {"amount": -1, "expected": False},
            {"amount": 0, "expected": False},
            {"amount": 1, "expected": True},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check less than operation of money with amount of 0 with money of amount {amount}"
            ):
                om = Money(amount, "EUR")
                self.assertEqual(
                    m < om,
                    expected,
                    f"expected money with amount of 0 to be < money of amount of {amount} to be {expected}",
                )

    def test_can_evaluate_money_less_than_or_equal(self):
        m = Money(0, "EUR")
        samples = [
            {"amount": -1, "expected": False},
            {"amount": 0, "expected": True},
            {"amount": 1, "expected": True},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check less than or equal to operation of money with amount of 0 with money of amount {amount}"
            ):
                om = Money(amount, "EUR")
                self.assertEqual(
                    m <= om,
                    expected,
                    f"expected money with amount of 0 to be <= money of amount of {amount} to be {expected}",
                )

    def test_money_is_zero(self):
        samples = [
            {"amount": -1, "expected": False},
            {"amount": 0, "expected": True},
            {"amount": 1, "expected": False},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check money is zero evaluates to {expected} when amount is {amount}"
            ):
                m = Money(amount, "EUR")
                self.assertEqual(
                    m.is_zero,
                    expected,
                    f"expected money is zero when amount is {amount} to be {expected}",
                )

    def test_money_is_negative(self):
        samples = [
            {"amount": -1, "expected": True},
            {"amount": 0, "expected": False},
            {"amount": 1, "expected": False},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check money is negative evaluates to {expected} when amount is {amount}"
            ):
                m = Money(amount, "EUR")
                self.assertEqual(
                    m.is_negative,
                    expected,
                    f"expected money is negative when amount is {amount} to be {expected}",
                )

    def test_money_is_positive(self):
        samples = [
            {"amount": -1, "expected": False},
            {"amount": 0, "expected": False},
            {"amount": 1, "expected": True},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check money is positive evaluates to {expected} when amount is {amount}"
            ):
                m = Money(amount, "EUR")
                self.assertEqual(
                    m.is_positive,
                    expected,
                    f"expected money is positive when amount is {amount} to be {expected}",
                )

    def test_money_absolute(self):
        samples = [
            {"amount": -1, "expected": 1},
            {"amount": 0, "expected": 0},
            {"amount": 1, "expected": 1},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check absolute money evaluates to {expected} when amount is {amount}"
            ):
                m = Money(amount, "EUR")
                self.assertEqual(
                    abs(m).amount,
                    expected,
                    f"expected absolute of money when amount is {amount} to be {expected}",
                )

    def test_money_negative(self): ...

    def test_can_add_money(self): ...

    def test_can_subtract_money(self): ...

    def test_can_multiply_money(self): ...

    def test_can_round_money(self): ...

    def test_can_split_money(self): ...

    def test_can_allocate_money(self): ...

    def test_money_str_representation(self): ...

    def test_money_representation(self): ...

    def test_money_as_major_unit(self): ...
