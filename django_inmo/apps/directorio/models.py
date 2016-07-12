import datetime 
from django.db import models
from django.contrib.auth.models import User

class EntidadCategoria(models.Model):
  nombre = models.CharField(
    max_length=450,
  )
  descripcion = models.TextField()
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def __str__(self):
    return self.nombre
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(EntidadCategoria, self).save(*args, **kwargs)


class Entidad(models.Model):
  usuario_creo = models.ForeignKey(
    User
  )
  nombre = models.CharField(
    max_length=450
  )
  telefono = models.CharField(
    max_length=450
  )
  correo = models.EmailField(
  )
  pagina_web = models.CharField(
    max_length=450
  )
  categoria = models.ForeignKey(
    EntidadCategoria
  )
  ubicacion = models.TextField()
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)

  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(Entidad, self).save(*args, **kwargs)



