import datetime 
import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

def path_and_rename(instance, filename):
  ext = filename.split('.')[-1]
  # set filename as random string
  filename = '{}.{}'.format(uuid4().hex, ext)
  # return the whole path to the file
  return os.path.join('instalaciones', filename)

class Instalacion(models.Model):
  usuario_creo = models.ForeignKey(
    User
  )
  imagen = ImageField(upload_to=path_and_rename, blank=True)
  nombre = models.CharField(
    max_length=450
  )
  descripcion = models.TextField()
  reglamento = models.TextField()
  activo = models.BooleanField(default=1)
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def __str__(self):
    return self.nombre
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(Instalacion, self).save(*args, **kwargs)

class DiaDisponibleInstalacion(models.Model):
  DIAS_DE_LA_SEMANA = (
    (1, 'Lunes'),
    (2, 'Martes'),
    (3, 'Miercoles'),
    (4, 'Jueves'),
    (5, 'Viernes'),
    (6, 'Sabado'),
    (7, 'Domingo'),
  )
  instalacion = models.ForeignKey(
    Instalacion
  )
  dia = models.IntegerField(choices=DIAS_DE_LA_SEMANA)
  hora_desde = models.TimeField()
  hora_hasta = models.TimeField()
  disponible = models.BooleanField(default=1)
  disponible_todo_el_dia = models.BooleanField(default=1)
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)

  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(DiaDisponibleInstalacion, self).save(*args, **kwargs)

class ReservacionInstalacion(models.Model):
  usuario_creo = models.ForeignKey(
    User
  )
  instalacion = models.ForeignKey(
    Instalacion
  )
  fecha_reservacion = models.DateTimeField()
  hora_empieza = models.TimeField()
  hora_termina = models.TimeField()
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)

  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(ReservacionInstalacion, self).save(*args, **kwargs)

