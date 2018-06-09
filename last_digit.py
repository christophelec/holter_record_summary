import pytest

def last_digit(n: int) -> int:
    ones = n % 10
    tens = n % 100 - ones
    return int(((ones ** n) + n * tens * (ones ** (n - 1))) % 100)


assert last_digit(5) == 25
assert last_digit(1) == 1
assert last_digit(347) == 44
assert last_digit(11) == 11