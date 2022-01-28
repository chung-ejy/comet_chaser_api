from . import views
from django.urls import path


urlpatterns = [
    path("iteration/",views.iterationView,name="iteration"),
    path("trade/",views.tradeView,name="trade"),
    path("order/",views.orderView,name="order")

]