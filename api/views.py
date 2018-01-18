import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .services import PaymentService
from .models import Transaction
from .exceptions import InsuficientFundsException, AccountNotFoundException, AuthorisationNotFoundException
from django.db import transaction

class TransactionsView(APIView):
    def __init__(self, payment_service_class=PaymentService):
        self.payment_service = payment_service_class()

    """
    API endpoint allow operation, authorization or presentment, to be posted
    """
    @transaction.atomic
    def post(self, request, format=None):
        try:
            self.payment_service.pay(request.data)
            return Response(None, status=status.HTTP_200_OK)
        except InsuficientFundsException:
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        except AccountNotFoundException:
            return Response(json.dumps({'error': 'account not found'}), status=status.HTTP_404_NOT_FOUND)
        except AuthorisationNotFoundException:
            return Response(json.dumps({'error': 'authorisation not found'}), status=status.HTTP_404_NOT_FOUND)
