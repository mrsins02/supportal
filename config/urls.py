"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path(
        route="admin/",
        view=admin.site.urls,
    ),
    path(
        route="api-auth/",
        view=include(arg="rest_framework.urls"),
    ),
]

# static and Media
if settings.DEBUG:
    urlpatterns += static(
        prefix=settings.MEDIA_URL,
        document_root=settings.MEDIA_ROO,
    )
    urlpatterns += static(
        prefix=settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )

# Api Routes
urlpatterns += [
    path(
        route="api/v1/",
        view=include(arg="config.api_routes"),
    ),
]

# Api Docs
urlpatterns += [
    path(route="api/schema/", view=SpectacularAPIView.as_view(), name="schema"),
    path(
        route="api/docs/",
        view=SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
]
