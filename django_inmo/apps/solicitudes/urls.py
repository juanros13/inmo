from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from apps.solicitudes import views as solicitudes_view

urlpatterns = [
	url(r'^$', solicitudes_view.mantenimiento_view, name="vista_solicitud_mantenimiento"),
	url(r'^crear/$', solicitudes_view.mantenimiento_crear_view, name="vista_solicitud_mantenimiento_crear"),
	url(r'^detalle/(?P<id_mantenimiento>\d+)/$', solicitudes_view.mantenimiento_detalle_view, name="vista_solicitud_mantenimiento_detalle"),
]
 