from django.urls import include, path
from .views import TransactionsView
from django.conf.urls import url

urlpatterns = [
    url(r'^transaction', TransactionsView.as_view()),
]