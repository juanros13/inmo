from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('apps.edificios.views',
    url(r'^adeudos/$', 'adeudos_view', name='vista_edificio_adeudos'),
    url(r'^adeudos/obtener_saldos/$','obtener_saldo_view', name='vista_obtener_saldo'),
    url(r'^egresos/$', 'egresos_view', name='vista_egresos'),
    url(r'^egresos/json$', 'egresos_json', name='json_egresos_ajax'),
)