from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CurrencyChoices(models.TextChoices):
    USD = "USD", _("USD")
    EUR = "EUR", _("EUR")
    INR = "INR", _("INR")


class PaymentDirectionChoices(models.TextChoices):
    INCOMING = "INCOMING", _("INCOMING")
    OUTGOING = "OUTGOING", _("OUTGOING")


class UserAccount(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    balance = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    currency = models.CharField(default=CurrencyChoices.USD,
                                choices=CurrencyChoices.choices,
                                max_length=3)

    def __str__(self):
        return f"{self.id}"


class Payment(models.Model):
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                                related_name="payments",
                                related_query_name="payments")
    amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    to_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                                   related_name="payments_to",
                                   related_query_name="payments_to",
                                   null=True)
    from_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE,
                                     related_name="payments_from",
                                     related_query_name="payments_from",
                                     null=True)
    direction = models.CharField(max_length=20, choices=PaymentDirectionChoices.choices)
    transaction_id = models.CharField(max_length=100)
    transaction_date = models.DateTimeField(auto_now_add=True)
