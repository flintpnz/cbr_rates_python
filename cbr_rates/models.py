from django.db import models
from django.urls import reverse

# Create your models here.


class Currency(models.Model):
    """
    Модель для валюты.
    """

    # Fields
    id = models.AutoField(primary_key=True)
    id_currency = models.CharField(max_length=7, help_text="Идентификатор валюты")
    name = models.CharField(max_length=255, help_text="Название валюты")

    # Metadata
    class Meta:
        ordering = ["name"]

    # Methods
    def get_absolute_url(self):
        """
        Возвращает url для конкретной валюты.
        """
        return reverse('currency-detail', args=[str(self.id)])

    def __str__(self):
        """
        Строка для представления объекта.
        """
        return self.name


class Rates(models.Model):
    """
    Модель для курса валюты.
    """

    # Fields
    id = models.AutoField(primary_key=True)
    id_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    nominal = models.IntegerField(help_text="Номинал валюты для курса")
    date = models.DateField(help_text="Дата курса валюты")
    value = models.DecimalField(max_digits=10, decimal_places=4, help_text="Курс валюты")

    # Metadata
    class Meta:
        ordering = ["-date", "id_currency"]

    # Methods
    def get_absolute_url(self):
        """
        Возвращает url для конкретной валюты.
        """
        return reverse('rate-detail', args=[str(self.id)])

    def __str__(self):
        """
        Строка для представления объекта.
        """
        return "{0} - {1}/{2} - {3}".format(self.id_currency.name, self.nominal, self.date, self.value)
