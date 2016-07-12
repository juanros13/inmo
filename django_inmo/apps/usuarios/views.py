# -*- encoding: utf-8 -*-
import hashlib
import datetime
import json as simplejson
from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from apps.usuarios.models import UserMensaje
from apps.usuarios.forms import  UserLoginForm, UserUpdatePassword, UserUpdateProfile, UserUpdateAvatar, UserMensajeForm
from apps.instalaciones.models import ReservacionInstalacion
from apps.avisos.models import Aviso
from apps.inmuebles.models import Edificio

def get_mensajes_no_leidos(request):
  try:
    if request.user.is_authenticated():
      ultimos_mensajes = UserMensaje.objects.filter(usuario_recibe=request.user).order_by('-fecha_creacion')[:10]
      nuevos_mensajes = 0
      for mensaje in ultimos_mensajes:
        if mensaje.visto == 0:
          nuevos_mensajes = nuevos_mensajes + 1
      mensajes = { 'nuevos_mensajes': nuevos_mensajes, 'ultimos_mensajes' : ultimos_mensajes }
      context = {
        'mensajes_no_leidos' : mensajes
      }
      return context
    return {}
  except ObjectDoesNotExist:
    return {}

@login_required(login_url='/')
def cambiar_edificio_view(request, id_edificio):
  url = reverse('dashboard')
  edificio = get_object_or_404(Edificio, pk=id_edificio)
  if Edificio.objects.filter(administrador=request.user, pk=id_edificio).exists():
    request.session['edificio_actual'] = [edificio.nombre,edificio.id]
    request.session['_info_message'] = 'Edificio cambiado correctamente' 
  else:
    request.session['_info_message'] = 'No eres administrador de este edificio' 
  return HttpResponseRedirect(url)

def login_view(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect(reverse('apps.usuarios.views.dashboard_view'))
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  user_login_form = UserLoginForm()
  if request.method == "POST":
    login_form = UserLoginForm(request.POST)
    if login_form.is_valid():
      username = login_form.cleaned_data['username']
      password = login_form.cleaned_data['password']
      usuario = authenticate(username=username,password=password)
      if usuario is not None:
        if usuario.is_active:
          edificios = Edificio.objects.values_list('nombre', 'id').all()
          login(request, usuario)
          request.session['edificios_disponibles'] = []
          request.session['edificio_actual'] = edificios.first()
          for edificio in edificios:
            sessionlist = request.session['edificios_disponibles']
            sessionlist.append(edificio)
            request.session['edificios_disponibles'] = sessionlist
          # Redirect to a success page.
          return HttpResponseRedirect(reverse('apps.usuarios.views.dashboard_view'))
        message = 'El usuario se encuentra desactivado'
      message = 'El nombre de usuario o la contraseña no son correctos.'
    else:
      user_login_form = login_form
  context = {
    'login_form':user_login_form,
    'message':message
  }
  return render(request, 'usuarios/login.html',context)

@login_required(login_url='/')
def dashboard_view(request):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  reservaciones = ReservacionInstalacion.objects.all()
  avisos = Aviso.objects.all().order_by('-fecha_creacion')[:10]
  context = {
    'reservaciones' : reservaciones,
    'avisos' : avisos,
    'message':message,
  }
  return render(request, 'usuarios/dashboard.html',context)

@login_required(login_url='/')
def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/')


def olvide_mi_clave(request):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  return render(
    request, 
    'usuarios/olvide_mi_clave.html', 
    {
      'message':message,
    }
  )

@require_POST
def olvide_mi_clave_enviar_email(request):
  email = request.POST['email']
  url_warning = reverse('vista_olvide_mi_clave')
  url_success = reverse('view_login')
  if email:
    try:
      user = User.objects.get(email=email)
      now = datetime.datetime.now().strftime("%Y-%m-%d")
      #print now
      url = "http://%s%s?u=%s&email=%s" % (
        settings.DOMAIN_NAME, 
        reverse('vista_olvide_mi_clave_validar'),  
        hashlib.md5(settings.KEY_STRING+now+email).hexdigest(),
        email
      )

      subject, from_email, to = 'KRAKENS SOFT - Contraseña acceso al sistema ', 'me@juanros13.com', [email]
      html_content = render_to_string('include/mail/mail_recovery_password_usuario.html', {
        'user':user,
        'url':url
      }) 

      text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
      # create the email, and attach the HTML version as well.
      #mail = EmailMultiAlternatives(subject, text_content, from_email, to)
      #mail.attach_alternative(html_content, "text/html")
      #mail.send() 
      mail_bcc = EmailMultiAlternatives(subject, text_content, from_email, to=['juanros13@gmail.com'])
      mail_bcc.attach_alternative(html_content, "text/html")
      mail_bcc.send()
      #mail = EmailMessage('Contraseña sistema GM', message, to=[email], bcc=['juanros13@gmail.com'])
      #mail.send()
      request.session['_info_message'] = 'El correo de recuperacion fue enviado a %s' % email
      return HttpResponseRedirect(url_success)
    except User.DoesNotExist:
      request.session['_info_message'] = 'El correo (%s) no esta dado de alta en nuestra base de datos' % email
      return HttpResponseRedirect(url_warning)
  else:
    return HttpResponse('NO OK')

def olvide_mi_clave_validar(request):
  email = request.GET['email']
  key = request.GET['u']
  url = reverse('vista_olvide_mi_clave')
  now = datetime.datetime.now().strftime("%Y-%m-%d")
  try:
    user = User.objects.get(email=email)
    if hashlib.md5(settings.KEY_STRING+now+email).hexdigest() == key :
      if user.is_active:
        if not user.is_staff and not user.is_superuser:
          return render(request, 'usuarios/olvide_mi_clave_guardar.html', {
            'key':key,
            'email':email,
            }
          )
        else:
          return HttpResponse('Los miembros del staff no puede cambiar su password de esta forma')  
      else:
        return HttpResponse('Mientras tu usuario no este activo no puedes cambiar el password')  
    else:
      return HttpResponse('El key no es valido')
  except User.DoesNotExist:
    return HttpResponse('El usuario (%s) no existe' % email)
  return HttpResponse('NO OK')
  
@require_POST
def olvide_mi_clave_guardar(request):
  email = request.POST['email']
  key = request.POST['key']
  password = request.POST['password1']
  password2 = request.POST['password2']
  url = reverse('view_login')
  now = datetime.datetime.now().strftime("%Y-%m-%d")
  if password == password2:
    try:
      user = User.objects.get(email=email)
      if hashlib.md5(settings.KEY_STRING+now+email).hexdigest() == key :
        if user.is_active:
          if not user.is_staff and not user.is_superuser:
            user.set_password(password)
            user.userprofile.pass_user = password
            user.save()
            request.session['_info_message'] = 'El password fue cambiado correctamente (%s)' % email
            return HttpResponseRedirect(url)
          else:
            request.session['_info_message'] = 'Los miembros del staff no puede cambiar su password de esta forma'
            return HttpResponseRedirect(url)
        else:
          request.session['_info_message'] = 'Mientras tu usuario no este activo no puedes cambiar el password'
          return HttpResponseRedirect(url)
      else:
        request.session['_info_message'] = 'El key no es valido'
        return HttpResponseRedirect(url)
        #return HttpResponse('El key no es valido')
    except User.DoesNotExist:
      request.session['_info_message'] = 'El usuario (%s) no existe' % email
      return HttpResponseRedirect(url)
  else:
    request.session['_info_message'] = 'Los passwords no coniciden'
    return HttpResponseRedirect(url)
  return HttpResponse('NO OK')



@login_required(login_url='/')
def configuracion_view(request):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''

  
  instance = User.objects.get(username=request.user)
  instance_profile = request.user.userprofile

  user_update_pass_form = UserUpdatePassword(instance=instance)
  user_update_profile_form = UserUpdateProfile(instance=request.user.userprofile)
  user_update_avatar_form = UserUpdateAvatar(instance=request.user.userprofile)
  
  if request.method == "POST":
    type_form = request.POST['type_form']
    if type_form == "profile":
      user_update_profile_form = UserUpdateProfile(request.POST, instance=request.user.userprofile)
      if user_update_profile_form.is_valid():
        profile = user_update_profile_form.save(commit=False)
        profile.user = request.user
        profile.save()
        message = 'El perfil de usuario fue correctamente actualizado' 
    if type_form == "avatar":
      user_update_avatar_form = UserUpdateAvatar(request.POST, request.FILES, instance=request.user.userprofile)
      if user_update_avatar_form.is_valid():
        avatar = user_update_avatar_form.save(commit=False)
        avatar.user = request.user
        avatar.save()
        message = 'El avatar de usuario fue correctamente actualizado' 
  context = {
    'user_config_form':user_update_pass_form, 
    'user_update_profile_form' : user_update_profile_form,
    'user_update_avatar_form' : user_update_avatar_form,
    'message':message,
  }
  return render(request, 'usuarios/configuracion.html', context)

@login_required(login_url='/')
@require_POST
def configuracion_update_pass_view(request):
  password_actual = request.POST['password_actual']
  password_1 = request.POST['password1']
  password_2 = request.POST['password2']
  message = ''
  url = reverse('vista_configuracion')
  try:
    user = User.objects.get(username=request.user)
    if user.check_password(password_actual):
      if user.is_active:
        if not user.is_staff and not user.is_superuser:
          if password_1 == password_2:
            if len(password_1) >= 8:
              user.set_password(password_1)
              user.save()
              user_new_pass = authenticate(username=request.user,password=password_1)
              if user_new_pass is not None:
                if user_new_pass.is_active:
                  login(request, user_new_pass)
              request.session['_info_message'] = 'El password fue cambiado correctamente' 
            else:
              request.session['_info_message'] = 'La contraseña debe ser mayor a 8 caracteres.'    
          else:
            request.session['_info_message'] = 'Las contraseñas no concuerdan.'  
        else:
          request.session['_info_message'] = 'Los miembros del staff no puede cambiar su password de esta forma.'
      else:
        request.session['_info_message'] = 'Mientras tu usuario no este activo no puedes cambiar el password.'
    else:
      request.session['_info_message'] = 'El password actual es incorrecto.'
  except User.DoesNotExist:
    request.session['_info_message'] = 'El usuario no existe'  
  return HttpResponseRedirect(url)

@login_required(login_url='/')
@require_POST
def configuracion_update_profile_view(request):
  user = request.user
  profile = user.userprofile
  form = UserUpdateProfile(request.POST or None, instance=request.user.userprofile)
  url = reverse('vista_configuracion')
  if form.is_valid():
    profile = form.save(commit=False)
    profile.user = request.user
    profile.save()
    request.session['_info_message'] = 'El perfil de usuario fue correctamente actualizado'  
  else:
    errors_form = ''
    print form.errors
    for error in form.errors:
      print error
      errors_form = errors_form + error + error +"</br>"
    request.session['_info_message'] = form.errors
  return HttpResponseRedirect(url)

@login_required(login_url='/')
def mensajes_view(request):
  message = ''
  url = reverse('vista_mensajes')
  usuario_ultimo_mensaje = 0
  ultimos_mensajes = 0
  form_mensaje = UserMensajeForm(initial={'usuario_envia': request.user})
  if request.method == "POST":
    form_mensaje = UserMensajeForm(request.POST)
    if form_mensaje.is_valid():
      mensaje = form_mensaje.save(commit=False)
      mensaje.usuario_envia = request.user
      mensaje.save()
      return HttpResponseRedirect(url)
  ultima_interaccion_con_mensajes = UserMensaje.objects.filter(Q(usuario_envia=request.user) | Q(usuario_recibe=request.user)).order_by('-fecha_creacion')[:1]
  if ultima_interaccion_con_mensajes:
    if ultima_interaccion_con_mensajes[0].usuario_envia == request.user:
      usuario_ultimo_mensaje = ultima_interaccion_con_mensajes[0].usuario_recibe
    else:
      usuario_ultimo_mensaje = ultima_interaccion_con_mensajes[0].usuario_envia
    UserMensaje.objects.filter(Q(usuario_envia=usuario_ultimo_mensaje) & Q(usuario_recibe=request.user)).order_by('-fecha_creacion').update(visto=1)
    ultimos_mensajes = UserMensaje.objects.filter(Q(usuario_envia=request.user) & Q(usuario_recibe=usuario_ultimo_mensaje) | Q(usuario_envia=usuario_ultimo_mensaje) & Q(usuario_recibe=request.user)).order_by('-fecha_creacion')
    #mensajes = UserMensaje.objects.filter(Q(usuario=request.user) | Q(usuario_entrega=request.user)).order_by('fecha_creacion')
  usuarios = User.objects.all().exclude(username=request.user.username)
  form_mensaje.fields['usuario_recibe'].queryset = usuarios
  context = {
    'ultimos_mensajes' : ultimos_mensajes,
    'usuarios' : usuarios,
    'usuario_ultimo_mensaje' : usuario_ultimo_mensaje,
    'form_mensaje': form_mensaje,
    'message':message,
  }
  return render(request, 'usuarios/mensajes.html',context)

@login_required(login_url='/')
def mensajes_usuario_view(request, usuario):
  message = ''
  url = reverse('vista_mensajes')
  usuario_ultimo_mensaje = 0
  ultimos_mensajes = 0
  form_mensaje = UserMensajeForm(initial={'usuario_envia': request.user})
  usuario_ultimo_mensaje = get_object_or_404(User, username=usuario)
  UserMensaje.objects.filter(Q(usuario_envia = usuario_ultimo_mensaje) & Q(usuario_recibe = request.user)).order_by('-fecha_creacion').update(visto=1)
  ultimos_mensajes = UserMensaje.objects.filter(Q(usuario_envia=request.user) & Q(usuario_recibe=usuario_ultimo_mensaje) | Q(usuario_envia=usuario_ultimo_mensaje) & Q(usuario_recibe=request.user)).order_by('-fecha_creacion')
  usuarios = User.objects.all().exclude(username = request.user.username)
  form_mensaje.fields['usuario_recibe'].queryset = usuarios
  context = {
    'ultimos_mensajes' : ultimos_mensajes,
    'usuarios' : usuarios,
    'usuario_ultimo_mensaje' : usuario_ultimo_mensaje,
    'form_mensaje': form_mensaje,
    'message':message,
  }
  return render(request, 'usuarios/mensajes.html',context)

