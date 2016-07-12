from django.db import models

MESES_NOMBRES = {
  1:"Enero",
  2:"Febrero",
  3:"Marzo",
  4:"Abril",
  5:"Mayo",
  6:"Junio",
  7:"Julio",
  8:"Agosto",
  9:"Septiembre",
  10:"Octubre",
  11:"Noviembre",
  12:"Diciembre",
}


class Edificio(models.Model):
  direccion = models.CharField(
    max_length=1000,
    null=True, 
    blank=True, 
    default=None

  )
  nombre = models.CharField(
    max_length=50,
    null=True, 
    blank=True, 
    default=None
  )
  metros_cuadrados = models.IntegerField(
    null=True, 
    blank=True, 
    default=None
  )
  numero_departamentos = models.IntegerField(
    null=True, 
    blank=True, 
    default=None
  )
  tipo_edificio = models.CharField(
    max_length=50,
    null=True, 
    blank=True, 
    default=None
  )
  antiguiedad = models.IntegerField(
    null=True, 
    blank=True, 
    default=None)
  tipo_edificio = models.CharField(
    max_length=50,
    null=True, 
    blank=True, 
    default=None

  )
  cp = models.CharField(
    max_length=10,
    null=True, 
    blank=True, 
    default=None
  )
  delegacion = models.CharField(
    max_length=100,
    null=True, 
    blank=True, 
    default=None
  )
  poblacion = models.CharField(
    max_length=100,
    null=True, 
    blank=True, 
    default=None
  )
  is_active = models.BooleanField(
    default=True,
  )

  def __unicode__(self):
    return self.nombre

  class Meta:
    verbose_name = "Edificio"
    verbose_name_plural = "Edificios"

class Concepto(models.Model):
  descripcion = models.CharField(max_length=250)
  id_edificio = models.IntegerField()
  class Meta:
    verbose_name = 'Concepto'
    verbose_name_plural = 'Conceptos'

  def __unicode__(self):
    return self.descripcion

class Egresos(models.Model):
  id_edificio = models.IntegerField()
  fecha_egr = models.DateField()
  ano_egr  =  models.IntegerField()
  mes_egr =  models.IntegerField()
  subtot_egr =  models.DecimalField(max_digits=16, decimal_places=2)
  total_egr = models.DecimalField(max_digits=16, decimal_places=2)
  concepto = models.ForeignKey(Concepto, blank=True, default=None)
  descripcion = models.DateField(null=True, blank=True, default=None)
  num_cheque =models.IntegerField()
  
class InmCuota(models.Model):
  id_inm = models.IntegerField()
  descripcion =  models.CharField(max_length=250)
