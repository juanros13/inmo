from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from apps.encuestas import views as encuestas_view

urlpatterns = [
	url(r'^$', encuestas_view.encuesta_view, name="vista_encuestas"),
	url(r'^encuesta/crear/$', encuestas_view.encuesta_crear_view, name="vista_encuesta_crear"),
	url(r'^encuesta/(?P<id_encuesta>\d+)/$', encuestas_view.encuesta_detalle_view, name="vista_encuesta_detalle"),
]
 