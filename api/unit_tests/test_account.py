from django.test import TestCase
from assertpy import assert_that
from api.models import Account
from api.exceptions import InsuficientFundsException

class AccountTestCase(TestCase):
    def test__reserve_money__insuficient_funds__should_raise_insuficient_funds_exception(self):
        target = Account()
        target.money = 100
        assert_that(target.reserve_money).raises(InsuficientFundsException).when_called_with(200)

    def test__reserve_money__account_has_funds__account_reserved_money_should_increase(self):
        target = Account()
        target.money = 100
        target.reserve_money(50)
        assert_that(target.reserved_money).is_equal_to(50)

    def test__reserve_money__account_with_100_reserve_40__should_have_60_available(self):
        target = Account()
        target.money = 100
        target.reserve_money(60)
        assert_that(target.get_available_money()).is_equal_to(40)

    def test__execute_presentment__acount_with_100_reserved__should_execute_presentment(self):
        target = Account()
        target.money = 100
        target.reserve_money(60)
        assert_that(target.execute_presentment(60))
