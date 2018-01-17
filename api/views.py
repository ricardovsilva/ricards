from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .services import PaymentService
from .models import Transaction

class TransactionsView(APIView):
    def __init__(self, payment_service_class=PaymentService):
        self.payment_service = payment_service_class()

    """
    API endpoint allow operation, authorization or presentment, to be posted
    """
    def post(self, request, format=None):
        transaction = Transaction.from_json(request.data)

        if self.payment_service.pay(transaction):
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_403_FORBIDDEN)
