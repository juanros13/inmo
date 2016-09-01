# -*- encoding: utf-8 -*-
import datetime
import calendar
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.edificios.models import Edificio, Concepto


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


YEAR_CHOICES = []
for r in range((datetime.datetime.now().year-1), (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

MONTH_CHOICES = []
for r in range(1,12):
  MONTH_CHOICES.append((r,r))

TIPO_DEPARTAMENTO = (
  ('departamento', 'Departamento'),
  ('oficina', 'Oficina'),
  ('local', 'Local'),
  ('casa', 'Casa'),
)
NUMERO_BANIOS = (
  ('0', 'Ninguno'),
  ('1', 'Uno'),
  ('1.5', 'Uno y medio'),
  ('2', 'Dos'),
  ('2.5', 'Dos y medio'),
  ('3', 'Tres'),
  ('3.5', 'Tres y medio'),
  ('4', 'Cuatro'),
  ('4.5', 'Cuatro y medio'),
  ('5', 'Cinco'),
  ('5.5', 'Cinco y medio'),
  ('6', 'Seis'),
  ('6.5', 'Seis y medio'),
  ('7', 'Siete'),
  ('7.5', 'Siete y medio'),
  ('8', 'Ocho'),
  ('8.5', 'Ocho y medio'),
  ('9', 'Nueve'),
  ('9.5', 'Nueve y medio'),
)
NUMERO_RECAMARAS = []
for r in range(0,12):
  NUMERO_RECAMARAS.append((r,r))

NUMERO_PISOS = []
for r in range(1,9):
  NUMERO_PISOS.append((r,r))

class DepartamentoWeb(models.Model):
  tipo = models.CharField(max_length=50, choices=TIPO_DEPARTAMENTO)

  metros_cuadrados = models.IntegerField(blank=True, default=None,null=True)
  estacionamientos = models.CharField(max_length=250,blank=True, default=None)
  renta = models.DecimalField(max_digits=9, decimal_places=2,blank=True, default=None,null=True)
  piso = models.IntegerField(choices=NUMERO_PISOS,blank=True, default=None,null=True)
  banios = models.CharField(max_length=150, choices=NUMERO_BANIOS)
  numero_recamaras = models.IntegerField(choices=NUMERO_RECAMARAS,blank=True, default=None,null=True)

  direccion = models.CharField(max_length=500)
  cp = models.IntegerField(blank=True, default=None,null=True)
  colonia = models.CharField(max_length=250)
  delegacion = models.CharField(max_length=250, default=None,null=True)
  estado = models.CharField(max_length=250, default=None,null=True)
  antiguedad = models.IntegerField(blank=True, default=None,null=True)

  cocina_integral = models.BooleanField()
  amueblado = models.BooleanField()
  cisterna = models.BooleanField()
  estudio = models.BooleanField()
  gas_natural = models.BooleanField()
  vigilancia_privada = models.BooleanField()
  linea_telefonica = models.BooleanField()
  internet = models.BooleanField()

  posicion = models.CharField(max_length=450)

  descripcion = models.TextField(blank=True, default=None)

  def __unicode__(self):
    return 'Departamento - %s - %s' % (self.colonia, self.direccion)
  
  def get_absolute_url(self):
    return "/inmuebles/%s" % self.pk
  class Meta:
    verbose_name = "Departamento web"
    verbose_name_plural = "Departamentos web"

def content_file_name(instance, filename):
  return '/'.join([str(instance.departamento_web.pk), filename])

class DepartamentoWebImage(models.Model):
  departamento_web = models.ForeignKey(DepartamentoWeb, related_name='imagenes')
  # Need to be defined before the field
  imagen = models.ImageField(upload_to=content_file_name)
  class Meta:
    verbose_name = "Imagene Departamento"
    verbose_name_plural = "Imagenes Departamentos"

class Departamento(models.Model):
  """docstring for Departamento"""
  edificio = models.ForeignKey(Edificio)
  numero_de_departamento = models.CharField(primary_key=True,max_length=250)
  numero_personas = models.IntegerField()
  metros_cuadrados = models.IntegerField()
  id_usuario = models.IntegerField()
  def __unicode__(self):
    return 'Departamento  %s' % (self.numero_de_departamento)

  class Meta:
    verbose_name = "Departamento"
    verbose_name_plural = "Departamentos"

class Recibo(models.Model):
  numero_de_recibo = models.IntegerField(unique=True)
  concepto =  models.CharField(max_length=250)
  iva = models.DecimalField(max_digits=16, decimal_places=2)
  isr = models.DecimalField(max_digits=16, decimal_places=2)
  subtotal = models.DecimalField(max_digits=16, decimal_places=2)
  total = models.DecimalField(max_digits=5, decimal_places=2)
  saldo = models.DecimalField(max_digits=5, decimal_places=2)
  mes = models.IntegerField(choices=MONTH_CHOICES)
  anio = models.IntegerField(choices=YEAR_CHOICES)
  cantidad  = models.IntegerField(default=1)
  departamento = models.ForeignKey(Departamento)
  numero_de_referencia =  models.CharField(max_length=500)
  status_pago = models.BooleanField()
  fecha_creacion = models.DateTimeField(editable=False, auto_now=True)
  id_inquilino = models.IntegerField()
  id_edificio = models.IntegerField()
  def get_total(self):
    if self.total:
      return self.total
    else:
      return 0
  def get_total_pagado(self):
    if self.total_pagado:
      return self.total_pagado
    else:
      return 0
  def __unicode__(self):
    return 'id: %s - Total a pagar: %s' % (self.pk, self.total)
  def nombre_mes(self):
    return MESES_NOMBRES[self.mes]

  class Meta:
    verbose_name = "Recibo"
    verbose_name_plural = "Recibos"

class MovimientosRecibo(models.Model):
  recibo = models.ForeignKey(Recibo)
  cantidad  = models.IntegerField(default=1)
  importe = models.DecimalField(max_digits=5, decimal_places=2)
  descripcion =  models.CharField(max_length=250)
  fecha_pago = models.DateField(null=True, blank=True, default=None)
  def __unicode__(self):
    return 'Movimiento del recibo : %s' % (self.recibo.numero_de_recibo)

  class Meta:
    verbose_name = "Movimientos Recibo"
    verbose_name_plural = "Movimientos Recibos"

class ReciboPagado(models.Model):
  numero_de_recibo = models.IntegerField(unique=True)
  concepto =  models.CharField(max_length=250)
  iva = models.DecimalField(max_digits=16, decimal_places=2)
  isr = models.DecimalField(max_digits=16, decimal_places=2)
  subtotal = models.DecimalField(max_digits=16, decimal_places=2)
  total = models.DecimalField(max_digits=5, decimal_places=2)
  saldo = models.DecimalField(max_digits=5, decimal_places=2)
  mes = models.IntegerField(choices=MONTH_CHOICES)
  anio = models.IntegerField(choices=YEAR_CHOICES)
  cantidad  = models.IntegerField(default=1)
  departamento = models.ForeignKey(Departamento)
  numero_de_referencia =  models.CharField(max_length=500)
  status_pago = models.BooleanField()
  fecha_creacion = models.DateTimeField(editable=False, auto_now=True)
  id_inquilino = models.IntegerField()
  id_edificio = models.IntegerField()
  total_pagado = models.DecimalField(max_digits=5, decimal_places=2)
  fecha_pagado = models.DateTimeField(editable=False, auto_now=True)
  def get_total(self):
    if self.total:
      return self.total
    else:
      return 0
  def get_total_pagado(self):
    if self.total_pagado:
      return self.total_pagado
    else:
      return 0
  def __unicode__(self):
    return 'id: %s - Total a pagar: %s' % (self.pk, self.total)
  def nombre_mes(self):
    return MESES_NOMBRES[self.mes]

class  ReciboPagadoDet(models.Model):
  idpagado  = models.IntegerField()
  idCuota = models.IntegerField()
  importe = models.DecimalField(max_digits=5, decimal_places=2)

class ReciboEdoCuenta(models.Model):
  numero_recibo = models.IntegerField()
  fecha = models.DateTimeField()
  importe = models.DecimalField(max_digits=5, decimal_places=2)
  referencia =  models.CharField(max_length=250)
  tipo =  models.IntegerField()
  edificio =  models.IntegerField()
  localidad =  models.CharField(max_length=250)
  numero_detalle =  models.IntegerField()
  def get_importe(self):
    if self.importe:
      return self.importe
    else:
      return 0

class Responsable(models.Model):
  nombre = models.CharField(max_length=120)
  correo = models.EmailField()
  edificio = models.ForeignKey(Edificio)

