from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from apps.inmuebles import views as inmuebles_view

urlpatterns = [
	url(r'^edificio/$', inmuebles_view.edificio_view, name="vista_edificio"),
	url(r'^edificio/crear/$', inmuebles_view.edificio_crear_view, name="vista_edificio_crear"),
	url(r'^edificio/(?P<id_edificio>\d+)/$', inmuebles_view.edificio_editar_view, name="vista_editar_edificio"),
	url(r'^departamento/$', inmuebles_view.departamento_view, name="vista_departamento"),
	url(r'^departamento/crear$', inmuebles_view.departamento_crear_view, name="vista_departamento_crear"),
	url(r'^departamento/crear/usuariodepartamento$', inmuebles_view.departamento_crear_usuariodepartamento_view, name="vista_departamento_crear_usuariodepartamento"),
	url(r'^departamento/quitar/usuariodepartamento$', inmuebles_view.departamento_quitar_usuariodepartamento_view, name="vista_departamento_quitar_usuariodepartamento"),
	url(r'^departamento/(?P<id_departamento>\d+)/$', inmuebles_view.departamento_editar_view, name="vista_editar_departamento"),
	url(r'^condomino/$', inmuebles_view.condomino_view, name="vista_condomino"),
	url(r'^condomino/crear$', inmuebles_view.condomino_crear_view, name="vista_condomino_crear"),
	url(r'^condomino/(?P<id_condomino>\d+)/$', inmuebles_view.condomino_editar_view, name="vista_condomino_editar"),
	url(r'^torre/$', inmuebles_view.torre_view, name="vista_torre"),
	url(r'^torre/crear$', inmuebles_view.torre_crear_view, name="vista_torre_crear"),
	url(r'^torre/(?P<id_torre>\d+)/$', inmuebles_view.torre_editar_view, name="vista_torre_editar"),
]
 