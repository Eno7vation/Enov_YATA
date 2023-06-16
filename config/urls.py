from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from main.views import Select_main
from allauth.account.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('account/', include('accounts.urls')),
    path('accounts/', include("allauth.urls")),
    path('introduce/', include("introduce.urls")),
    path('tech/', include("tech.urls")),
    path('summernote/', include('django_summernote.urls')),
    path('', RedirectView.as_view(url='/main', permanent=False))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]