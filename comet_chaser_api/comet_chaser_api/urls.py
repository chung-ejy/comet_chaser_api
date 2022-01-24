from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/backtest/",include("backtest.urls")),
    path("api/live/",include("live.urls")),
    path("api/reporter/",include("reporter.urls")),
    path("api/test/",include("test_bot.urls")),
    path("api/users/",include("users.urls")),
    path("api/roster/",include("roster.urls"))
]

