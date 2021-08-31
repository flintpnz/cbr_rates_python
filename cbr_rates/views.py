import datetime

from django.shortcuts import render
from .models import Currency, Rates
from django.views import generic
import xml.etree.ElementTree as ET
import urllib.request
from decimal import Decimal


# Create your views here.
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_currencies = Currency.objects.all().count()
    num_rates = Rates.objects.all().count()

    start_date = datetime.date.today()
    end_date = datetime.date.today()

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    currencies = Currency.objects.all()
    return render(
        request,
        'index.html',
        context={'num_currencies': num_currencies,
                 'num_rates': num_rates,
                 'currencies': currencies,
                 'start_date': start_date.strftime('%Y-%m-%d'),
                 'end_date': end_date.strftime('%Y-%m-%d')},
    )


def update(request):
    """
    Функция отображения для страницы оновления курсов с сайта ЦБР.
    """
    if 'from' in request.GET:
        try:
            start_date = datetime.datetime.strptime(request.GET['from'], '%Y-%m-%d').date()
        except ValueError:
            start_date = datetime.date.today()
    else:
        start_date = datetime.date.today()
    if 'to' in request.GET:
        try:
            end_date = datetime.datetime.strptime(request.GET['to'], '%Y-%m-%d').date()
        except ValueError:
            end_date = datetime.date.today()
    else:
        end_date = datetime.date.today()

    date = start_date
    while date <= end_date:
        url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(date.strftime('%d/%m/%Y'))
        with urllib.request.urlopen(url) as response:
            html = response.read()
        xml = ET.fromstring(html.decode('windows-1251'))
        xml_date = datetime.datetime.strptime(xml.attrib['Date'], '%d.%m.%Y').date()
        if xml_date == date:
            for valute in xml:
                nominal = valute.find('Nominal').text
                value = valute.find('Value').text
                currency = Currency.objects.get(id_currency__exact=valute.attrib['ID'])
                try:
                    rate = Rates.objects.filter(date=date).get(id_currency__exact=currency.id)
                except Rates.DoesNotExist:
                    Rates.objects.create(id_currency=currency, nominal=nominal, date=date,
                                         value=Decimal(value.replace(',', '.')))
                else:
                    rate.id_currency = currency
                    rate.nominal = nominal
                    rate.date = start_date
                    rate.value = Decimal(value.replace(',', '.'))
                    rate.save()
        date += datetime.timedelta(days=1)

    currencies = Currency.objects.all()
    return render(
        request,
        'update.html',
        context={'currencies': currencies,
                 'start_date': start_date.strftime('%Y-%m-%d'),
                 'end_date': end_date.strftime('%Y-%m-%d')},
    )


class CurrencyListView(generic.ListView):
    model = Currency
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CurrencyListView, self).get_context_data(**kwargs)
        context['start_date'] = datetime.date.today().strftime('%Y-%m-%d')
        context['end_date'] = datetime.date.today().strftime('%Y-%m-%d')
        context['currencies'] = currencies = Currency.objects.all()
        return context


class CurrencyDetailView(generic.DetailView):
    model = Currency

    def get_context_data(self, **kwargs):
        context = super(CurrencyDetailView, self).get_context_data(**kwargs)
        context['start_date'] = datetime.date.today().strftime('%Y-%m-%d')
        context['end_date'] = datetime.date.today().strftime('%Y-%m-%d')
        context['currencies'] = currencies = Currency.objects.all()
        return context


class RatesListView(generic.ListView):
    model = Rates
    paginate_by = 34

    def get_queryset(self):
        if self.request.GET.get('order', 'desc') == 'asc':
            return Rates.objects.all().order_by('date')
        else:
            return Rates.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RatesListView, self).get_context_data(**kwargs)
        context['start_date'] = datetime.date.today().strftime('%Y-%m-%d')
        context['end_date'] = datetime.date.today().strftime('%Y-%m-%d')
        context['currencies'] = currencies = Currency.objects.all()
        return context


class RateIdListView(generic.ListView):
    model = Rates
    paginate_by = 10
    template_name = 'cbr_rates/rateid_list.html'

    def get_queryset(self):
        if self.request.GET.get('order', 'desc') == 'asc':
            return Rates.objects.filter(id_currency__exact=self.kwargs['id_currency']).order_by('date')
        else:
            return Rates.objects.filter(id_currency__exact=self.kwargs['id_currency'])

    def get_context_data(self, **kwargs):
        context = super(RateIdListView, self).get_context_data(**kwargs)
        if self.request.GET.get('order', 'desc') == 'asc':
            context['reverse'] = True
        context['start_date'] = datetime.date.today().strftime('%Y-%m-%d')
        context['end_date'] = datetime.date.today().strftime('%Y-%m-%d')
        context['currencies'] = currencies = Currency.objects.all()
        context['id_currency'] = int(self.kwargs['id_currency'])
        return context
