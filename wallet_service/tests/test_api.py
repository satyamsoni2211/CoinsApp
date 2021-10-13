from rest_framework.test import APITestCase
from rest_framework import status
from wallet_service.models import UserAccount, CurrencyChoices
from django.shortcuts import reverse
from django.http import QueryDict


class TestAPI(APITestCase):
    def setUp(self) -> None:
        self.bob = UserAccount.objects.create(id="bob123",
                                              balance=100.23,
                                              currency=CurrencyChoices.USD)
        self.satyam = UserAccount.objects.create(id="satyam123",
                                                 balance=100.23,
                                                 currency=CurrencyChoices.USD)
        self.alice = UserAccount.objects.create(id="alice456",
                                                balance=80.23,
                                                currency=CurrencyChoices.EUR)
        self.accounts = UserAccount.objects.all().values_list("id", flat=True)

    def tearDown(self) -> None:
        UserAccount.objects.all().delete()

    def test_list_user_accounts_api(self):
        res = self.client.get(reverse('list_accounts'))
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertEquals(len(data), UserAccount.objects.all().count())
        for i in data:
            self.assertIn("id", i)
            self.assertIn("balance", i)
            self.assertIn("currency", i)
            self.assertIn(i.get("id"), self.accounts)

    def test_list_user_account_api_filter_via_currency(self):
        qdict = QueryDict(mutable=True)
        qdict["search"] = "USD"
        path = f"{reverse('list_accounts')}?{qdict.urlencode()}"
        res = self.client.get(path)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertEquals(len(data), UserAccount.objects.filter(currency="USD").count())
        self.assertEquals("bob123", data[0].get("id"))

    def test_create_payment_api(self):
        res = self.client.post(reverse("create_payments"), data={
            "account": "satyam123",
            "to_account": "bob123",
            "amount": 1.0
        })
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        data = res.data
        self.assertEquals(data.get("account"), "satyam123")
        self.assertEquals(data.get("to_account"), "bob123")
        self.assertEquals(data.get("from_account"), None)
        self.assertEquals(float(data.get("amount")), 1.0)

    def test_create_payment_api_with_exceeding_balance(self):
        res = self.client.post(reverse("create_payments"), data={
            "account": "satyam123",
            "to_account": "bob123",
            "amount": 1e4
        })
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        error = str(res.data[0])
        self.assertEquals("Amount to be transferred "
                          "cannot be more than account holdings", error)

    def test_create_payment_api_with_different_currency(self):
        res = self.client.post(reverse("create_payments"), data={
            "account": "alice456",
            "to_account": "bob123",
            "amount": 1
        })
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        error = str(res.data[0])
        self.assertIn("Only same currency allowed got", error)
