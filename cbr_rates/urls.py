from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^currencies/update/$', views.update, name='update'),
    url(r'^currencies/$', views.CurrencyListView.as_view(), name='currencies'),
    url(r'^currency/(?P<pk>\d+)$', views.CurrencyDetailView.as_view(), name='currency-detail'),
    url(r'^rates/$', views.RatesListView.as_view(), name='rates'),
    url(r'^rate/(?P<id_currency>\d+)$', views.RateIdListView.as_view(), name='rate-list'),
]
