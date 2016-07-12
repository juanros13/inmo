from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from apps.usuarios import views as usuarios_views

urlpatterns = [
	url(r'^mensajes/$', usuarios_views.mensajes_view, name="vista_mensajes"),
	url(r'^mensajes/(?P<usuario>\w+)/$', usuarios_views.mensajes_usuario_view, name="vista_mensajes_usuario"),
    url(r'^configuracion/$', usuarios_views.configuracion_view, name="vista_configuracion"),
    url(r'^configuracion/update_pass/$', usuarios_views.configuracion_update_pass_view, name="vista_configuracion_update_pass"),
    url(r'^configuracion/update_profile/$', usuarios_views.configuracion_update_profile_view, name="vista_configuracion_update_profile"),
    url(r'^logout/$', usuarios_views.logout_view, name="vista_logout"),
    
    url(r'^olvide_mi_clave/$', usuarios_views.olvide_mi_clave, name='vista_olvide_mi_clave'),
    url(r'^olvide_mi_clave_enviar_email/$', usuarios_views.olvide_mi_clave_enviar_email, name='vista_olvide_mi_clave_enviar_email'),
    url(r'^olvide_mi_clave_validar/$', usuarios_views.olvide_mi_clave_validar, name='vista_olvide_mi_clave_validar'),
    url(r'^olvide_mi_clave_guardar/$', usuarios_views.olvide_mi_clave_guardar, name='vista_olvide_mi_clave_guardar'),

    url(r'^cambiar-edificio/(?P<id_edificio>\w+)/$', usuarios_views.cambiar_edificio_view, name="vista_cambiar_edificio"),


]
 