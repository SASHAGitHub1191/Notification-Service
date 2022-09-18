from django.contrib import admin
from django.urls import path, include
# from .Notifications.views import SendMessage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Notifications.urls')),
]
