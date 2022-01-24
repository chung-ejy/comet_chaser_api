from . import views
from django.urls import path

urlpatterns = [
    path("",views.reporterView,name="reporter")
]