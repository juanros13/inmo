import datetime 
from django.db import models
from tinymce import models as tinymce_models
from apps.edificios.models import Edificio
from django.contrib.auth.models import User

class DocumentoInmueble(models.Model):
  ESTADOS_DE_LA_NOTA = (
    (1, 'Publicado'),
    (0, 'Draft'),
  )

  titulo = models.CharField(max_length=250)
  
  estatus = models.BooleanField(choices=ESTADOS_DE_LA_NOTA, default=0)
  es_local = models.BooleanField(choices=ESTADOS_DE_LA_NOTA, default=1, editable=False)
  mes = models.IntegerField(default=0, editable=False)
  anio = models.IntegerField(default=0, editable=False)
  archivo_tipo = models.CharField(
    max_length=10,
    blank=True,
    null=True,
    editable=False,
  )
  archivo = models.FileField(
    upload_to='uploads/documentos/%Y/%m/', 
    blank=True,
    null=True,

  )
  inmueble_id =  models.IntegerField()
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def get_absolute_url(self):
    return "/documento/inmueble/%s/" % (self.id)

  class Meta:
    verbose_name = 'Documento Inmueble'
    verbose_name_plural = 'Documentos Inmuebles'
    #abstract = True
  #def render(self, **kwargs):
  #  return textile(self.content)
  def __unicode__(self):
    return self.titulo
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(DocumentoInmueble, self).save(*args, **kwargs)


class DocumentoPropios(models.Model):
  ESTADOS_DE_LA_NOTA = (
    (1, 'Publicado'),
    (0, 'Draft'),
  )

  titulo = models.CharField(max_length=250)
  
  estatus = models.BooleanField(choices=ESTADOS_DE_LA_NOTA, default=0)
  es_local = models.BooleanField(choices=ESTADOS_DE_LA_NOTA, default=1, editable=False)
  mes = models.IntegerField(default=0, editable=False)
  anio = models.IntegerField(default=0, editable=False)
  archivo_tipo = models.CharField(
    max_length=10,
    blank=True,
    null=True,
    editable=False,
  )
  archivo = models.FileField(
    upload_to='uploads/documentos/%Y/%m/', 
    blank=True,
    null=True,

  )
  usuario_id = models.IntegerField()
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def get_absolute_url(self):
    return "/documento/propios/%s/" % (self.id)

  class Meta:
    verbose_name = 'Documento Propio'
    verbose_name_plural = 'Documentos Propios'
    #abstract = True
  #def render(self, **kwargs):
  #  return textile(self.content)
  def __unicode__(self):
    return self.titulo
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(DocumentoPropios, self).save(*args, **kwargs)

