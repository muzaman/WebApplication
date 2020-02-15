from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import never_cache
from django.views.static import serve
from WebApplication import settings

urlpatterns = [
    path('BAccount/', include('BAccount.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>',
                            never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
