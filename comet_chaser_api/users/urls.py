from django.urls import path, include
from .api import RegisterApi, LoginApi, UserApi
from knox import views as knox_views


urlpatterns = [
    path('auth/',include('knox.urls')),
    path('register/',RegisterApi.as_view()),
    path('login/',LoginApi.as_view()),
    path('user/',UserApi.as_view()),
    path('logout/',knox_views.LogoutView.as_view(),name="knox_logout")
]