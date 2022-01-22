from . import views
from django.urls import path

urlpatterns = [
    path("",views.liveView,name="test")
]