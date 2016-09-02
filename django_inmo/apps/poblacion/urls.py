from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from apps.poblacion import views as poblacion_views

urlpatterns = [
	url(r'^pais/$', poblacion_views.get_pais_json_view, name="vista_get_pais_json"),
	url(r'^estado/(?P<id_pais>\d+)/$', poblacion_views.get_estados_json_view, name="vista_get_estados_json"),
	url(r'^municipio/(?P<id_estado>\d+)/$', poblacion_views.get_municipios_json_view, name="vista_get_municipios_json"),
	url(r'^colonia/(?P<id_estado>\d+)/(?P<id_municipio>\d+)/$', poblacion_views.get_colonias_json_view, name="vista_get_colonias_json"),
]
 