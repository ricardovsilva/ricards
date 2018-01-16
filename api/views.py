from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from services import PaymentService

class OperationsView(APIView):
    def __init__(self, payment_service_class=PaymentService):
        self.payment_service = payment_service_class()

    """
    API endpoint allow operation, authorization or presentment, to be posted
    """
    def post(self, request):
        pass
