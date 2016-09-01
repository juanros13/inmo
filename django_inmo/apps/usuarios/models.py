import datetime 
from django.db import models
from django.contrib.auth.models import User
from apps.poblacion.models import Pais, Estado, Municipio, Colonia
from apps.departamentos.models import Departamento

class UserProfile(models.Model):
  # This field is required.
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  nombre_inquilino = models.CharField(max_length=500)

  curp = models.CharField(
    max_length=21, 
    null=True, 
    blank=True, 
    default=None
  )
  telefono = models.CharField(
    max_length=21, 
    null=True, 
    blank=True, 
    default=None
  )
  celular = models.CharField(
    max_length=21, 
    null=True, 
    blank=True, 
    default=None
  )
  rfc = models.CharField(
    max_length=18,
    null=True, 
    blank=True, 
    default=None 
  )
  # Este seria el nombre en caso de que estuviera lleno
  razon_social = models.CharField(
    max_length=400,
    null=True, 
    blank=True, 
    default=None 
  )

  direccion_fisica = models.CharField(
    max_length=450,
    null=True, 
    blank=True, 
    default=None  
  )
  
  colonia_fisica = models.CharField(
    max_length=450,
    null=True, 
    blank=True, 
    default=None  
  )
  cp_fisico = models.CharField(
    max_length=450,
    null=True, 
    blank=True, 
    default=None  
  )
  delegacion_fisica = models.CharField(
    max_length=450,
    null=True, 
    blank=True, 
    default=None  
  )
  poblacion_fisica = models.CharField(
    max_length=450,
    null=True, 
    blank=True, 
    default=None  
  )
  pais = models.ForeignKey(
    Pais,
    null=True, 
    blank=True, 
    default=None 
  )
  estado = models.ForeignKey(
    Estado,
    null=True, 
    blank=True, 
    default=None 
  )
  municipio = models.ForeignKey(
    Municipio,
    null=True, 
    blank=True, 
    default=None 
  )
  colonia = models.ForeignKey(
    Colonia,
    null=True, 
    blank=True, 
    default=None 
  )
  avatar = models.FileField(
    upload_to='avatars/%Y/%m/%d'
  )

  pass_user = models.CharField(
    max_length=10,
    null=True, 
    blank=True, 
    default=None  
  )
  #departamento = models.ManyToManyField(Departamento)
  id_inquilino = models.IntegerField()

  def get_absolute_url_mensajes(self):
    return "/usuarios/mensajes/%s/" % (self.user.username)

class UserMensaje(models.Model):
  usuario_envia = models.ForeignKey(
    User,
    related_name='usuario_crea'
  )
  usuario_recibe = models.ForeignKey(
    User,
    related_name='usuario_entrega'
  )
  mensaje = models.TextField(
    default=None 
  )
  visto = models.BooleanField(
    default=0
  )
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)
  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(UserMensaje, self).save(*args, **kwargs)










