import os
import sys
from django.test import TestCase
from assertpy import assert_that
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unit_tests.moq_services import AlwaysDenyPaymentService, AlwaysAllowPaymentService
from views import OperationsView

class ViewsTestCase(TestCase):
    def test__post_operation__invalid_operation__should_return_403(self):
        view = OperationsView(AlwaysDenyPaymentService)
        actual = view.post('foo')
        assert_that(actual.status_code).is_equal_to(403)

    def test__post_operation__valid_operation__should_return_200(self):
        view = OperationsView(AlwaysAllowPaymentService)
        actual = view.post('foo')
        assert_that(actual.status_code).is_equal_to(200)
