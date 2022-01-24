from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/backtest/",include("backtest.urls")),
    path("api/reporter/",include("reporter.urls")),
    path("api/users/",include("users.urls")),
    path("api/roster/",include("roster.urls"))
]

