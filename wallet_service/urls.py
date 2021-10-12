from django.urls import path
from .api import ListAccounts, ListPaymentAPI, CreatePaymentAPI

urlpatterns = [
    path('list_accounts/', ListAccounts.as_view(), name="list_accounts"),
    path('list_payments/', ListPaymentAPI.as_view(), name="list_payments"),
    path('create_payments/', CreatePaymentAPI.as_view(), name="create_payments"),
]
