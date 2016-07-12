import datetime 
from django.db import models
from django.contrib.auth.models import User

class Encuesta(models.Model):
  usuario_crea = models.ForeignKey(
    User
  )
  titulo = models.CharField(
    max_length=450
  )
  descripcion = models.TextField()
  fecha_limite_para_votacion = models.DateField()
  
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def __str__(self):
    return self.titulo
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(Encuesta, self).save(*args, **kwargs)


class Opcion(models.Model):
  opcion = models.CharField(
    max_length=450,
    blank=False,
  )
  votos_total = models.SmallIntegerField()
  encuesta = models.ForeignKey(
    Encuesta
  )
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def __str__(self):
    return self.opcion
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(Opcion, self).save(*args, **kwargs)


class Voto(models.Model):
  usuario = models.ForeignKey(
    User
  )
  opcion = models.ForeignKey(
    Opcion
  )
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def __str__(self):
    return 'Voto para la encuesta %s opcion  %s ' % (self.opcion.encuesta, self.opcion)
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(Voto, self).save(*args, **kwargs)

class ComentarioEncuesta(models.Model):
  comentario = models.TextField()
  encuesta = models.ForeignKey(
    Encuesta
  )
  usuario = models.ForeignKey(
    User
  )
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(ComentarioEncuesta, self).save(*args, **kwargs)





