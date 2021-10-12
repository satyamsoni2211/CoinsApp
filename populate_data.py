import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CoinsApp.settings")

import django

django.setup()

import random
from wallet_service.models import UserAccount, CurrencyChoices

user_accounts = ["bob123", "alice456", "satyam123", "vedika234"]

for user in user_accounts:
    amount = random.randint(50, 100) + random.random()
    UserAccount.objects.create(id=user, balance=amount, currency=random.choice(CurrencyChoices.choices)[0])
