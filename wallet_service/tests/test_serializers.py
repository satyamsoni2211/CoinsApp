from django.test import TestCase
from wallet_service.models import UserAccount, CurrencyChoices
from wallet_service.serializers import PaymentSerializer, UserAccountSerializer
from rest_framework.exceptions import ValidationError


class BaseSerializerTest(TestCase):
    def setUp(self) -> None:
        self.bob = UserAccount.objects.create(id="bob123",
                                              balance=100.23,
                                              currency=CurrencyChoices.USD)
        self.alice = UserAccount.objects.create(id="alice456",
                                                balance=80.23,
                                                currency=CurrencyChoices.EUR)

    def tearDown(self) -> None:
        UserAccount.objects.all().delete()


class TestPaymentSerializers(BaseSerializerTest):

    def test_payment_for_invalid_amount(self):
        ser = PaymentSerializer(data={"account": "bob123",
                                      "to_account": "alice456",
                                      "amount": 1e4})
        try:
            ser.is_valid(raise_exception=True)
        except Exception as e:
            self.assertIsInstance(e, ValidationError)
            self.assertEquals("Amount to be transferred cannot be more than account holdings",
                              str(e.detail[0]))
            self.assertEquals("invalid",
                              e.detail[0].code)

    def test_payment_for_different_currencies(self):
        ser = PaymentSerializer(data={"account": "bob123",
                                      "to_account": "alice456",
                                      "amount": 10})

        try:
            ser.is_valid(raise_exception=True)
        except Exception as e:
            self.assertIsInstance(e, ValidationError)
            self.assertIn("Only same currency allowed got",
                          str(e.detail[0]))
            self.assertEquals("invalid",
                              e.detail[0].code)

    def test_payment_for_invalid_account(self):
        ser = PaymentSerializer(data={"account": "fakeaccount",
                                      "to_account": "alice456",
                                      "amount": 10})
        try:
            ser.is_valid(raise_exception=True)
        except Exception as e:
            self.assertIsInstance(e, ValidationError)
            detail = e.detail.get("account")
            self.assertIn("Invalid pk", str(detail[0]))
            self.assertEquals("does_not_exist",
                              detail[0].code)


class TestUserAccountSerializer(BaseSerializerTest):
    def test_user_account_serializer(self):
        ser = UserAccountSerializer(self.bob)
        data = ser.data
        self.assertIn("id", data)
        self.assertIn("balance", data)
        self.assertIn("currency", data)
