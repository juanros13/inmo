from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from apps.departamentos import views as departamento_vews

admin.autodiscover()

urlpatterns = [
    url(r'^adeudos/$', departamento_vews.adeudos_view, name="vista_departamento_adeudos"),
    url(r'^historial/$', departamento_vews.historial_view, name="vista_departamento_historial"),
    url(r'^historial/json$', departamento_vews.historial_json, name='json_historial_ajax'),
    url(r'^obtener_detalle/$', departamento_vews.obtener_detalle_view, name="vista_obtener_detalle"),

]