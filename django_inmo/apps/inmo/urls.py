"""django_plumbago URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from apps.usuarios.views import login_view, dashboard_view
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_view, name="view_login"),
    url(r'^dashboard/$', dashboard_view, name="dashboard"),
    url(r'^usuarios/', include('apps.usuarios.urls')),
    url(r'^encuestas/', include('apps.encuestas.urls')),
    url(r'^directorio/', include('apps.directorio.urls')),
    url(r'^avisos/', include('apps.avisos.urls')),
    url(r'^instalaciones/', include('apps.instalaciones.urls')),
    url(r'^inmuebles/', include('apps.inmuebles.urls')),
    url(r'^poblacion/', include('apps.poblacion.urls')),
    url(r'^solicitudes/', include('apps.solicitudes.urls')),
    url(r'^departamento/', include('apps.departamentos.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
