from django.contrib import admin
from .models import Currency, Rates

# Register your models here.
admin.site.register(Currency)
admin.site.register(Rates)
