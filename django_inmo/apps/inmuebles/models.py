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
  return os.path.join('edificios', filename)

class Edificio(models.Model):
  nombre = models.CharField(
    max_length=450,
  )
  direccion = models.TextField()
  imagen = ImageField(upload_to=path_and_rename, blank=True)
  administrador = models.ManyToManyField(
    User,
    blank=True,
    related_name='administradores'
  )
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def __str__(self):
    return self.nombre
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(Edificio, self).save(*args, **kwargs)

class Torre(models.Model):
  nombre = models.CharField(
    max_length=450,
  )
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def __str__(self):
    return self.nombre
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(Torre, self).save(*args, **kwargs)

class Departamento(models.Model):
  nombre = models.CharField(
    max_length=450,
  )
  observaciones = models.TextField()
  edificio = models.ForeignKey(
    Edificio,
  )
  torre = models.ForeignKey(
    Torre,
    null=True, 
    blank=True, 
    default=None
  )
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def get_torre(self):
    return self.torre if self.torre else ''
  def __str__(self):
    return self.nombre
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(Departamento, self).save(*args, **kwargs)

class UsuarioDepartamento(models.Model):
  usuario = models.ForeignKey(User, on_delete=models.CASCADE)
  departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
  es_propietario = models.BooleanField(default=False)
  es_habitante = models.BooleanField(default=False)
  es_principal = models.BooleanField(default=False)
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(UsuarioDepartamento, self).save(*args, **kwargs)


