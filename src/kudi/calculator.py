from kudi.types import Amount
import math


class Calculator:
    @staticmethod
    def add(a: Amount, b: Amount) -> Amount:
        return a + b

    @staticmethod
    def subtract(a: Amount, b: Amount) -> Amount:
        return a - b

    @staticmethod
    def multiply(a: Amount, b: int) -> Amount:
        return a * b

    @staticmethod
    def divide(a: Amount, d: int) -> Amount:
        return int(a / d)

    @staticmethod
    def modulus(a: Amount, d: int) -> Amount:
        return a % d

    @staticmethod
    def allocate(a: Amount, r: int, s: int) -> Amount:
        if a == 0 or s == 0:
            return 0
        return (a * r) // s

    @staticmethod
    def absolute(a: Amount) -> Amount:
        if a < 0:
            return -a
        return a

    @staticmethod
    def negative(a: Amount) -> Amount:
        if a > 0:
            return -a
        return a

    @staticmethod
    def round(a: Amount, e: int) -> Amount:
        if a == 0:
            return 0
        absam = Calculator.absolute(a)
        exp = int(math.pow(10, e))
        m = absam % exp

        if m > (exp / 2):
            absam += exp

        absam = (absam // exp) * exp

        if a < 0:
            a = -absam
        else:
            a = absam

        return a
