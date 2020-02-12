from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('BAccount/', include('BAccount.urls')),
    path('admin/', admin.site.urls),
]
