import os
import sys
from django.test import TestCase
from assertpy import assert_that
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from .moq_services import AlwaysDenyPaymentService, AlwaysAllowPaymentService
from ..views import TransactionsView

class FooRequest(object):
    def __init__(self):
        self.data = 'foo'

class ViewsTestCase(TestCase):
    def test__post_operation__invalid_operation__should_return_403(self):
        view = TransactionsView(AlwaysDenyPaymentService)
        actual = view.post(FooRequest())
        assert_that(actual.status_code).is_equal_to(403)

    def test__post_operation__valid_operation__should_return_200(self):
        view = TransactionsView(AlwaysAllowPaymentService)
        actual = view.post(FooRequest())
        assert_that(actual.status_code).is_equal_to(200)
