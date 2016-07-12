from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from apps.instalaciones import views as instalaciones_views

urlpatterns = [
	url(r'^$', instalaciones_views.instalacion_view, name="vista_instalacion"),
	url(r'^crear/$', instalaciones_views.instalacion_crear_view, name="vista_instalacion_crear"),
	url(r'^reservacion/(?P<id_instalacion>\d+)/crear/$', instalaciones_views.reservacion_instalacion_crear_view, name="vista_reservacion_instalacion_crear"),
	url(r'^reservacion/(?P<id_instalacion>\d+)/detalle/$', instalaciones_views.reservacion_instalacion_detalle_view, name="vista_reservacion_instalacion_detalle"),
]
 