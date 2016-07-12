import datetime 
import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


class Pais(models.Model):
  clave_pais = models.IntegerField(primary_key=True)
  nombre = models.CharField(
    max_length=450,
  )
  nombre_abreviacion = models.CharField(
    max_length=450,
  )
  def __str__(self):
    return self.nombre.encode('utf8')

class Estado(models.Model):
  pais = models.ForeignKey(
    Pais
  )
  clave_estado = models.IntegerField(primary_key=True)
  nombre = models.CharField(
    max_length=450,
  )
  nombre_abreviacion = models.CharField(
    max_length=450,
  )
  def __str__(self):
    return self.nombre.encode('utf8')

class Municipio(models.Model):
  estado = models.ForeignKey(
    Estado
  )
  clave_municipio = models.IntegerField()
  nombre = models.CharField(
    max_length=450,
  )
  def __str__(self):
    return self.nombre.encode('utf8')

class Colonia(models.Model):
  estado = models.ForeignKey(
    Estado
  )
  municipio = models.IntegerField()
  cp = models.CharField(
    max_length=100,
  )
  nombre = models.CharField(
    max_length=450,
  )
  def __str__(self):
    return self.nombre.encode('utf8')