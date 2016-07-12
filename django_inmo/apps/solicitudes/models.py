import datetime 
from django.db import models
from django.contrib.auth.models import User
from apps.inmuebles.models import Departamento
from django.db.models.signals import post_save

class Mantenimiento(models.Model):
  usuario_creo = models.ForeignKey(
    User
  )
  departamento = models.ForeignKey(
    Departamento
  )
  problema = models.CharField(
    max_length=450
  )
  descripcion = models.TextField()
  fecha_creacion =  models.DateTimeField(editable=False)
  fecha_modificacion =  models.DateTimeField(editable=False)

  def save(self, *args, **kwargs):
    ''' On save, update timestamps '''
    if not self.id:
      self.fecha_creacion = datetime.datetime.today()
    self.fecha_modificacion = datetime.datetime.today()
    super(Mantenimiento, self).save(*args, **kwargs)


class ComentarioMantenimiento(models.Model):
  comentario = models.TextField()
  mantenimiento = models.ForeignKey(
    Mantenimiento
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
    super(ComentarioMantenimiento, self).save(*args, **kwargs)

def enviar_mail_mantenimiento(sender, **kwargs):
  obj = kwargs['instance']

  departamento = Departamento.objects.filter(pk=obj.departamento.pk, idusuario=obj.usuario.get_profile().id_inquilino)[0]
  #responsables = Responsable.objects.filter(edificio=departamento.edificio)
  # Enviando el correo de confirmacion operario
  subject, from_email, to = 'PLUMBAGO - Nuevo mantenimiento - %s ' % obj, 'juanros13@gmail.com', ['juanros13@gmail.com', 'edgarcisneros88@gmail.com', 'alejandro@poware.com']
  html_content = render_to_string('include/mail_mantenimiento.html', {
    'edificio':departamento.edificio, 
    'departamento':departamento,
    'mantenimiento':obj,
    'usuario':obj.usuario.get_profile(),
    'correo':obj.usuario.email
  }) 

  text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
  # create the email, and attach the HTML version as well.
  mail = EmailMultiAlternatives(subject, text_content, from_email, to)
  mail.attach_alternative(html_content, "text/html")
  mail.send()


   # Enviando el correo de confirmacion usuario
  subject, from_email, to = 'PLUMBAGO - Se ha creado un nuevo mantenimiento', 'juanros13@gmail.com', ['juanros13@gmail.com', 'edgarcisneros88@gmail.com', 'alejandro@poware.com']
  html_content = render_to_string('include/mail_mantenimiento_usuario.html', {
    'mantenimiento':obj,
  }) 
  
  text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
  # create the email, and attach the HTML version as well.
  mail = EmailMultiAlternatives(subject, text_content, from_email, to)
  mail.attach_alternative(html_content, "text/html")
  mail.send()

post_save.connect(enviar_mail_mantenimiento, sender=Mantenimiento)