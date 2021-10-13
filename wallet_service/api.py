from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .models import UserAccount, Payment
from .serializers import UserAccountSerializer, PaymentSerializer


class ListAccounts(ListAPIView):
    """
    API to List User accounts
    User accounts can also be searched via id or currency
    API accepts **search** query param for this purpose
    """
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ["id", "currency"]


class ListPaymentAPI(ListAPIView):
    """
    API to List all the payments
    Payments can also be filtered using **account_name**, **direction**
    and **transaction_id**
    Payments API accepts **search** query param for this purpose
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ["account__id", "direction", "transaction_id"]


class CreatePaymentAPI(CreateAPIView):
    """
    API to create Payments
    All of the business logic is diverted to
    serializer class `:py:obj::wallet_service.serializers.PaymentSerializer`
    """
    serializer_class = PaymentSerializer
