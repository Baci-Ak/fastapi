import pytest
from app.calculations import add, multiply, divide, subtract, mod, cube, square, BankAccount

@pytest.fixture
def bank_account():
    return BankAccount(0)



@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 3), 
    (2, 2, 4),
    (3, 2, 5)])



def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_multiply():
    assert multiply(1, 2) == 2

def test_divide():
    assert divide(1, 2) == 0.5

def test_subtract():
    assert subtract(1, 2) == -1

def test_mod():
    assert mod(1, 2) == 1

    
@pytest.mark.parametrize("deposit, withdraw, expected", [
    (55, 100, 10), 
    (100, 50, 105.0),
    (100, 100, 55.0)])

def test_bank_account(bank_account, deposit, withdraw, expected):
    account = bank_account
    assert account.get_balance() == 0

    account.deposit(100)
    assert account.get_balance() == 100

    account.withdraw(50)
    assert account.get_balance() == 50

    account.collect_interest()
    assert round(account.get_balance(), 2) == 55.00

    account.deposit(deposit)
    account.withdraw(withdraw)
    assert account.get_balance() == expected

    
    