from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from.import views
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('',views.holi,name='holi'),
                  url(r'^auth/', include('accounts.urls', namespace='authentication'), ),
                  url(r'^conn/', include('connections.urls', namespace='connection'), ),
                  url(r'^notification/', include('notification.urls', namespace='notification'), ),
                  path('chat/', include('chat.urls')),
                  path('post/', include('post.urls')),
                  path('home/', include('home.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = [
    ] + urlpatterns
