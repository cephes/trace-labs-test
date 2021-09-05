from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'ethcrawler'

urlpatterns = [
    url('history', views.check_by_block, name='history'),
    url('balance', views.check_balance, name='balance'),
    url('', views.home, name='home')

]