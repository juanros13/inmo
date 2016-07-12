from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apps.documentos.views',
    url(r'^propios/$', 'documento_propios_view', name="vista_documento_propios"),
    url(r'^inmueble/$', 'documento_inmueble_view', name="vista_documento_inmueble"),
    url(r'^propios/(?P<item_id>\d+)/$', 'documento_propios_detalle_view', name="vista_documento_propios_detalle"),
    url(r'^inmueble/(?P<item_id>\d+)/$', 'documento_inmueble_detalle_view', name="vista_documento_inmueble_detalle"),
    #url(r'^(?P<item_id>\d+)/$', 'documento_detalle_view', name='vista_documento_detalle'),

)