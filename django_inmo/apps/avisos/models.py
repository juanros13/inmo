import datetime 
from django.db import models
from django.contrib.auth.models import User

class Aviso(models.Model):
  YEAR_IN_SCHOOL_CHOICES = (
    ('AVISO', 'Aviso'),
    ('EVENTO', 'Evento'),
  )
  usuario_creo = models.ForeignKey(
    User
  )
  tipo = models.CharField(
    max_length=450,
    choices=YEAR_IN_SCHOOL_CHOICES,
    default = 'AVISO'
  )
  titulo = models.CharField(
    max_length=450
  )
  contenido = models.TextField()
  mantener_al_principio = models.BooleanField()
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def get_absolute_url(self):
    from django.core.urlresolvers import reverse
    return reverse('vista_aviso_detalle', args=[str(self.id)])


  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(Aviso, self).save(*args, **kwargs)

class ComentarioAviso(models.Model):
  comentario = models.TextField()
  aviso = models.ForeignKey(
    Aviso
  )
  usuario_creo = models.ForeignKey(
    User
  )
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(ComentarioAviso, self).save(*args, **kwargs)

