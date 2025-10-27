class KudiException(Exception): ...


class InvalidCurrencyCodeError(KudiException, ValueError):
    """Raised when the currency code cannot be determined"""


class InvalidCurrencyAlphaCodeError(InvalidCurrencyCodeError):
    """Raised when the currency alpha code cannot be determined"""


class InvalidCurrencyNumericCodeError(InvalidCurrencyCodeError):
    """Raised when the currency numeric code cannot be determined"""


class CurrencyMismatchError(KudiException):
    """Raised when you try to perform arithmetic operations on two different currencies"""
