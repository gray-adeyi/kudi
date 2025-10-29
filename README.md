# Kùdí 💰 (WIP)

“Kùdí” (also spelled “kudi”) is a Hausa word that means money 💰. Kudi is a python implementation of Fowler's Money
pattern inspired by [Rhymond/go-money](https://github.com/Rhymond/go-money)

## Installation

```bash
uv add kudi
```

## Usage

```python
from kudi import Money, CurrencyCode

m1 = Money(50, 'USD')  # Fifty cents
m2 = Money('1.50', 'USD')  # One dollar and fifty cents
m3 = Money(-100, 'usd')
m4 = Money(0, CurrencyCode.EUR)

# Arithmetic
print(m2 + m1)
print(m2 - m2)
print(m2 + m1 - m2)
print(m1 + m4) # will raise an exception, arithmetic on monies in different currencies is not allowed
print(m1 * 4)
print(-m2)
print(abs(m3))  # Absolute
print(m1.negative())  # Not to be confused with `-m1`, `.negative` will
# always result in a negative value

# Assertions
print(m3.is_negative)
print(m4.is_zero)
print(m1.is_positive)

# Allocations
# In order to split Money for parties without losing any pennies due
# to rounding differences, use `split`.
# After division leftover pennies will be distributed round-robin amongst
# the parties. This means that parties listed first will likely receive
# more pennies than ones that are listed later.
pound = Money(100, 'GBP')
allocations = pound.split(3)
print(allocations)

# To perform splits in ratios, use `allocate`.
# It splits money using the given ratios without losing pennies and as
# Split operations distributes leftover pennies amongst the parties
# with round-robin principle.
allocations = pound.allocate([33,33,33])
```
