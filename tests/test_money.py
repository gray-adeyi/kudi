from decimal import Decimal
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

    def test_creating_money_obj_from_float_amount(self):
        samples = [
            {"amount": 1.50, "expected": 150},
            {"amount": 1.45, "expected": 145},
            {"amount": 1.459, "expected": 146},
            {"amount": 1.452, "expected": 145},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check that creating money from a float value of {amount}"
                " results in a money with the amount of {expected}"
            ):
                m = Money(amount, "NGN")
                self.assertEqual(
                    m.amount, expected, f"Expected {expected} got {m.amount}"
                )

    def test_creating_money_obj_from_decimal_amount(self):
        samples = [
            {"amount": 1.50, "expected": 150},
            {"amount": 1.45, "expected": 145},
            {"amount": 1.459, "expected": 146},
            {"amount": 1.452, "expected": 145},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check that creating money from a float value of {amount}"
                " results in a money with the amount of {expected}"
            ):
                m = Money(Decimal(amount), "NGN")
                self.assertEqual(
                    m.amount, expected, f"Expected {expected} got {m.amount}"
                )

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

    def test_money_negative(self):
        samples = [
            {"amount": -1, "expected": -1},
            {"amount": 0, "expected": -0},
            {"amount": 1, "expected": -1},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check the negative of money evaluates to {expected} when amount is {amount}"
            ):
                m = Money(amount, "EUR").negative()
                self.assertEqual(
                    m.amount,
                    expected,
                    f"expected negative equivalent of money when amount is {amount} to be {expected}",
                )

    def test_money_negative_infix(self):
        samples = [
            {"amount": -1, "expected": 1},
            {"amount": 0, "expected": -0},
            {"amount": 1, "expected": -1},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check the negative of money evaluates to {expected} when amount is {amount}"
            ):
                m = -Money(amount, "EUR")
                self.assertEqual(
                    m.amount,
                    expected,
                    f"expected negative equivalent of money when amount is {amount} to be {expected}",
                )

    def test_can_add_money(self):
        samples = [
            {"amount1": 5, "amount2": 5, "expected": 10},
            {"amount1": 10, "amount2": 5, "expected": 15},
            {"amount1": 1, "amount2": -1, "expected": 0},
            {"amount1": 5, "amount2": 5, "amount3": 3, "expected": 13},
            {"amount1": 10, "amount2": 5, "amount3": 4, "expected": 19},
            {"amount1": 1, "amount2": -1, "amount3": 2, "expected": 2},
            {"amount1": 3, "amount2": -1, "amount3": -4, "expected": -2},
        ]
        for sample in samples:
            amount1 = sample["amount1"]
            amount2 = sample["amount2"]
            amount3 = sample.get("amount3", 0)
            has_three_operands = len(sample.keys()) == 4
            expected = sample["expected"]
            with self.subTest(
                f"check addition of monies with amount of {amount1}, {amount2}, {amount3}, to be {expected}"
            ):
                m1 = Money(amount1, "EUR")
                m2 = Money(amount2, "EUR")
                m3 = Money(amount3, "EUR")
                self.assertEqual(
                    (m1 + m2 + m3).amount if has_three_operands else (m1 + m2).amount,
                    expected,
                    f"expected {repr(m1)} + {repr(m2)} + {repr(m3)} to be {expected}",
                )

    def test_adding_monies_of_different_currencies_raises_error(self):
        m = Money(100, "eur")
        dm = Money(100, "gbp")
        with self.assertRaises(CurrencyMismatchError) as context:
            m + dm
        self.assertEqual(
            context.exception.args[0],
            "operations on monies with different currencies is not allowed",
        )

    def test_can_subtract_money(self):
        samples = [
            {"amount1": 5, "amount2": 5, "expected": 0},
            {"amount1": 10, "amount2": 5, "expected": 5},
            {"amount1": 1, "amount2": -1, "expected": 2},
            {"amount1": 5, "amount2": 5, "amount3": 3, "expected": -3},
            {"amount1": 10, "amount2": -5, "amount3": 4, "expected": 11},
            {"amount1": 1, "amount2": -1, "amount3": 2, "expected": 0},
            {"amount1": 7, "amount2": 1, "amount3": -4, "expected": 10},
        ]
        for sample in samples:
            amount1 = sample["amount1"]
            amount2 = sample["amount2"]
            amount3 = sample.get("amount3", 0)
            has_three_operands = len(sample.keys()) == 4
            expected = sample["expected"]
            with self.subTest(
                f"check addition of monies with amount of {amount1}, {amount2}, {amount3}, to be {expected}"
            ):
                m1 = Money(amount1, "EUR")
                m2 = Money(amount2, "EUR")
                m3 = Money(amount3, "EUR")
                self.assertEqual(
                    (m1 - m2 - m3).amount if has_three_operands else (m1 - m2).amount,
                    expected,
                    f"expected {repr(m1)} - {repr(m2)} - {repr(m3)} to be {expected}",
                )

    def test_subtracting_monies_of_different_currencies_raises_error(self):
        m = Money(100, "eur")
        dm = Money(100, "gbp")
        with self.assertRaises(CurrencyMismatchError) as context:
            m - dm
        self.assertEqual(
            context.exception.args[0],
            "operations on monies with different currencies is not allowed",
        )

    def test_can_multiply_money(self):
        samples = [
            {"amount1": 5, "amount2": 5, "expected": 25},
            {"amount1": 10, "amount2": 5, "expected": 50},
            {"amount1": 1, "amount2": -1, "expected": -1},
            {"amount1": 1, "amount2": 0, "expected": 0},
            {"amount1": 5, "amount2": 5, "multiplier": 5, "expected": 125},
            {"amount1": 10, "amount2": 5, "multiplier": -3, "expected": -150},
            {"amount1": 1, "amount2": -1, "multiplier": 6, "expected": -6},
            {"amount1": 1, "amount2": 0, "multiplier": 2, "expected": 0},
        ]
        for sample in samples:
            amount1 = sample["amount1"]
            amount2 = sample["amount2"]
            multiplier = sample.get("multiplier", 0)
            has_integer_multiplier = len(sample.keys()) == 4
            expected = sample["expected"]
            with self.subTest(
                f"check multiplication of monies with amount of {amount1}, {amount2}, {multiplier}, to be {expected}"
            ):
                m1 = Money(amount1, "EUR")
                m2 = Money(amount2, "EUR")
                self.assertEqual(
                    (m1 * m2 * multiplier).amount
                    if has_integer_multiplier
                    else (m1 * m2).amount,
                    expected,
                    f"expected {repr(m1)} * {repr(m2)} * {multiplier} to be {expected}"
                    if has_integer_multiplier
                    else f"expected {repr(m1)} * {repr(m2)} to be {expected}",
                )

    def test_can_round_money(self):
        samples = [
            {"amount": 125, "expected": 100},
            {"amount": 175, "expected": 200},
            {"amount": 349, "expected": 300},
            {"amount": 351, "expected": 400},
            {"amount": 0, "expected": 0},
            {"amount": -1, "expected": 0},
            {"amount": -75, "expected": -100},
        ]
        for sample in samples:
            amount = sample["amount"]
            expected = sample["expected"]
            with self.subTest(
                f"check rounding of money with amount of {amount} evaluates to {expected}"
            ):
                m = Money(amount, "EUR")
                self.assertEqual(
                    round(m).amount,
                    expected,
                    f"expected money is positive when amount is {amount} to be {expected}",
                )
        # round with exponential
        m = Money(12_555, "bhd")
        self.assertEqual(round(m).amount, 13_000)

    def test_can_split_money(self):
        samples = [
            {"amount": 100, "split": 3, "expected": [34, 33, 33]},
            {"amount": 100, "split": 4, "expected": [25, 25, 25, 25]},
            {"amount": 5, "split": 3, "expected": [2, 2, 1]},
            {"amount": -101, "split": 4, "expected": [-26, -25, -25, -25]},
            {"amount": -2, "split": 3, "expected": [-1, -1, 0]},
        ]
        for sample in samples:
            amount = sample["amount"]
            split = sample["split"]
            expected = sample["expected"]
            with self.subTest(
                f"check splitting of money with amount of {amount} by {split} results in "
                f"monies with the amounts {expected}"
            ):
                m = Money(amount, "EUR")
                splits = [money.amount for money in m.split(split)]
                self.assertListEqual(splits, expected)

    def test_can_allocate_money(self):
        samples = [
            {"amount": 100, "ratio": [50, 50], "expected": [50, 50]},
            {"amount": 100, "ratio": [30, 30, 30], "expected": [34, 33, 33]},
            {"amount": 200, "ratio": [25, 25, 50], "expected": [50, 50, 100]},
            {"amount": 5, "ratio": [50, 25, 25], "expected": [3, 1, 1]},
            {"amount": 0, "ratio": [0, 0, 0, 0], "expected": [0, 0, 0, 0]},
            {"amount": 0, "ratio": [50, 10], "expected": [0, 0]},
            {"amount": 10, "ratio": [0, 100], "expected": [0, 10]},
            {"amount": 10, "ratio": [0, 0], "expected": [0, 0]},
        ]
        for sample in samples:
            amount = sample["amount"]
            ratio = sample["ratio"]
            expected = sample["expected"]
            with self.subTest():
                m = Money(amount, "EUR")
                splits = [part.amount for part in m.allocate(*ratio)]
                self.assertListEqual(splits, expected)

    def test_money_str_representation(self):
        samples = [{"amount": 100, "code": "gbp", "expected": "£1.00"}]
        for sample in samples:
            amount = sample["amount"]
            code = sample["code"]
            expected = sample["expected"]
            with self.subTest(
                "check the string representation of money with "
                f"currency of {code} and amount of {amount} to be {expected}"
            ):
                m = Money(amount, code)
                self.assertEqual(str(m), expected)

    def test_money_representation(self):
        samples = [
            {"amount": 100, "code": "gbp", "expected": 'Money(amount=100, code="GBP")'}
        ]
        for sample in samples:
            amount = sample["amount"]
            code = sample["code"]
            expected = sample["expected"]
            with self.subTest(
                "check the string representation of money with "
                f"currency of {code} and amount of {amount} to be {expected}"
            ):
                m = Money(amount, code)
                self.assertEqual(repr(m), expected)

    def test_money_as_major_unit(self):
        samples = [
            {"amount": 100, "code": "aed", "expected": Decimal("1.0")},
            {"amount": 1, "code": "USD", "expected": Decimal("0.01")},
        ]
        for sample in samples:
            amount = sample["amount"]
            code = sample["code"]
            expected = sample["expected"]
            with self.subTest(
                f"check that money with amount of {amount} in minor unit is {expected} as a major unit"
            ):
                m = Money(amount, code)
                self.assertEqual(m.as_major_units(), expected)
