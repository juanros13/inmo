from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from apps.directorio import views as directorio_view

urlpatterns = [
	url(r'^$', directorio_view.directorio_view, name="vista_directorio"),
]
 