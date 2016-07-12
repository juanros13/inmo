from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from apps.avisos import views as avisos_view

urlpatterns = [
	url(r'^$', avisos_view.aviso_view, name="vista_avisos"),
	url(r'^crear/$', avisos_view.avisos_crear_view, name="vista_avisos_crear"),
	url(r'^(?P<id_aviso>\d+)/$', avisos_view.aviso_detalle_view, name="vista_aviso_detalle"),
]
 