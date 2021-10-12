from django.contrib import admin

# Register your models here.
from .models import UserAccount, Payment

admin.site.register(UserAccount)
admin.site.register(Payment)
