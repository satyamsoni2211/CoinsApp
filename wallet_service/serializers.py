import uuid
from typing import Dict, Any
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import models
from django.db import transaction

from wallet_service.models import UserAccount, Payment, PaymentDirectionChoices


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"


def create_instance(validated_data: Dict[str, Any],
                    klass: models.Model,
                    transaction_id: str):
    """
    Function to create **:py:obj::Payment** instance
    via serializer


    :param validated_data: data posted by user
    :param klass: Payment Model class
    :param transaction_id: transaction id for transfer
    :return: Payment instance
    """
    account, to_account, amount = validated_data.get("account"), validated_data.get(
        "to_account"), validated_data.get("amount")
    instance = klass.objects.create(account=account, to_account=to_account, amount=amount,
                                    direction=PaymentDirectionChoices.OUTGOING,
                                    transaction_id=transaction_id)
    klass.objects.create(account=to_account, from_account=account, amount=amount,
                         direction=PaymentDirectionChoices.INCOMING,
                         transaction_id=transaction_id)
    account.balance = account.balance - amount
    to_account.balance = to_account.balance + amount
    account.save()
    to_account.save()
    return instance


class PaymentSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        valid = super(PaymentSerializer, self).is_valid(raise_exception=raise_exception)
        data = self.validated_data
        account, amount, to_account = data.get("account"), \
                                      data.get("amount"), \
                                      data.get("to_account")
        if amount > account.balance:
            if raise_exception:
                raise ValidationError("Amount to be transferred cannot "
                                      "be more than account holdings")
            return False
        if account.currency != to_account.currency:
            if raise_exception:
                raise ValidationError(f"Only same currency allowed got "
                                      f"{account.currency} and {to_account.currency}")
            return False
        return valid

    def create(self, validated_data):
        klass = self.Meta.model
        transaction_id = str(uuid.uuid4())
        with transaction.atomic():
            instance = create_instance(validated_data, klass, transaction_id)
        return instance

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = (
            "from_account",
            "direction",
            "transaction_id"
        )
