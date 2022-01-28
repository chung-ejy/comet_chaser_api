from . import views
from django.urls import path

urlpatterns = [
    path("",views.tradeParamsView,name="trade_params")
]