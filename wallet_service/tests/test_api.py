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
        self.alice = UserAccount.objects.create(id="alice456",
                                                balance=80.23,
                                                currency=CurrencyChoices.EUR)
        self.accounts = "bob123", "alice456"

    def tearDown(self) -> None:
        UserAccount.objects.all().delete()

    def test_list_user_accounts(self):
        res = self.client.get(reverse('list_accounts'))
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertEquals(len(data), 2)
        for i in data:
            self.assertIn("id", i)
            self.assertIn("balance", i)
            self.assertIn("currency", i)
            self.assertIn(i.get("id"), self.accounts)

    def test_list_search_user_account(self):
        qdict = QueryDict(mutable=True)
        qdict["search"] = "USD"
        path = f"{reverse('list_accounts')}?{qdict.urlencode()}"
        res = self.client.get(path)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertEquals(len(data), 1)
        self.assertEquals("bob123", data[0].get("id"))
