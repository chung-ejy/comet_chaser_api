from django.urls import path, include
from .api import RegisterApi, LoginApi, UserApi
from knox import views as knox_views


urlpatterns = [
    path('auth/',include('knox.urls')),
    path('auth/register/',RegisterApi.as_view()),
    path('auth/login/',LoginApi.as_view()),
    path('auth/user/',UserApi.as_view()),
    path('auth/logout/',knox_views.LogoutView.as_view(),name="knox_logout")
]