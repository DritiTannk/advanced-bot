from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

urlpatterns = [
    path('', include('bot_interface.urls'), name='interface'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()


admin.site.site_header = "Chat BOT"
admin.site.site_title = "Chat BOT"
admin.site.index_title = "Welcome To Chat BOT Administration"