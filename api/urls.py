from django.urls import include, path
from .views import OperationsView
from django.conf.urls import url

urlpatterns = [
    url(r'^operation', OperationsView.as_view()),
]