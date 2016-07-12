# -*- encoding: utf-8 -*-
from datetime import datetime, date, time
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from apps.inmuebles.forms import EdificioAddForm, DepartamentoAddForm, TorreAddForm, UsuarioDepartamentoForm, UserCondominoForm, UserProfileCondominoForm, UsuarioDepartamentoCondominoForm
from apps.inmuebles.models import Edificio, Departamento, Torre, UsuarioDepartamento
from apps.usuarios.models import UserProfile
from apps.usuarios.forms import UserProfileForm, UserForm, UserProfileEditForm, UserEditForm
from apps.poblacion.models import Pais, Estado, Municipio, Colonia

@login_required(login_url='/')
def torre_view(request):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  torres  = Torre.objects.all()
  context = {
    'message': message,
    'torres' : torres,
  }
  return render(request, 'inmuebles/torre.html',context)

@login_required(login_url='/')
def torre_crear_view(request):
  url = reverse('vista_torre')
  torre_form = TorreAddForm()
  if request.method == "POST":
    torre_form = TorreAddForm(request.POST)
    if torre_form.is_valid():
      torre_form.save()
      request.session['_info_message']  = 'Torre agregada correctamente'  
      return HttpResponseRedirect(url)
  context = {
    'torre_form':torre_form,
  }
  return render(request, 'inmuebles/torre_crear.html',context)

@login_required(login_url='/')
def torre_editar_view(request, id_torre):
  url = reverse('vista_torre')
  torre = get_object_or_404(Torre, pk=id_torre)
  torre_form = TorreAddForm(instance=torre)
  if request.method == "POST":
    torre_form = TorreAddForm(request.POST, instance=torre)
    if torre_form.is_valid():
      torre_form.save()
      request.session['_info_message']  = 'Torre actualizada correctamente'  
      return HttpResponseRedirect(url)
  context = {
    'torre_form':torre_form,
    'torre': torre
  }
  return render(request, 'inmuebles/torre_editar.html',context)

@login_required(login_url='/')
def condomino_view(request):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  usuarios  = User.objects.all()
  context = {
    'message': message,
    'usuarios' : usuarios,
  }
  return render(request, 'inmuebles/condomino.html',context)

@login_required(login_url='/')
def condomino_crear_view(request):
  url = reverse('vista_condomino')
  user_profile_form = UserProfileForm()
  user_form = UserForm()
  if request.method == "POST":
    user_profile_form = UserProfileForm(request.POST)
    user_form = UserForm(request.POST)
    if user_form.is_valid() and user_profile_form.is_valid():
      #user_profile_form.save()
      usuario = user_form.save(commit=False)
      usuario.username = usuario.email
      usuario.password = make_password(user_form.cleaned_data['password'])
      usuario.save()
      usuario_profile = user_profile_form.save(commit=False)
      usuario_profile.user = usuario
      usuario_profile.save()
      request.session['_info_message']  = 'Condómino agregada correctamente'  
      return HttpResponseRedirect(url)
  context = {
    'user_profile_form': user_profile_form,
    'user_form':user_form,
  }
  return render(request, 'inmuebles/condomino_crear.html',context)


@login_required(login_url='/')
def condomino_editar_view(request, id_condomino):
  url = reverse('vista_condomino')
  usuario = get_object_or_404(User, pk=id_condomino)
  user_profile_form = UserProfileEditForm(instance=usuario.userprofile)
  if usuario.userprofile.municipio:
    user_profile_form.fields["municipio"].queryset = Municipio.objects.filter(estado=usuario.userprofile.estado)
  if usuario.userprofile.colonia or (usuario.userprofile.municipio and usuario.userprofile.estado ):
    user_profile_form.fields["colonia"].queryset = Colonia.objects.filter(estado=usuario.userprofile.estado.clave_estado, municipio=usuario.userprofile.municipio.clave_municipio)
  user_form = UserEditForm(instance=usuario)
  if request.method == "POST":
    user_profile_form = UserProfileEditForm(request.POST, instance=usuario.userprofile)
    user_form = UserEditForm(request.POST, instance=usuario)
    if user_form.is_valid() and user_profile_form.is_valid():
      #user_profile_form.save()
      usuario = user_form.save(commit=False)
      usuario.username = usuario.email
      if user_form.cleaned_data['password1']:
        usuario.password = make_password(user_form.cleaned_data['password1'])
      usuario.save()
      usuario_profile = user_profile_form.save(commit=False)
      usuario_profile.user = usuario
      usuario_profile.save()
      request.session['_info_message']  = 'Condómino editado correctamente'  
      return HttpResponseRedirect(url)
  context = {
    'user_profile_form': user_profile_form,
    'user_form':user_form,
    'usuario': usuario
  }
  return render(request, 'inmuebles/condomino_editar.html',context)

@login_required(login_url='/')
def edificio_view(request):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  edificios = Edificio.objects.all()
  context = {
    'message': message,
    'edificios' : edificios,
  }
  return render(request, 'inmuebles/edificio.html',context)

@login_required(login_url='/')
def edificio_crear_view(request):
  url = reverse('vista_edificio')
  edificio_form = EdificioAddForm()
  if request.method == "POST":
    edificio_form = EdificioAddForm(request.POST)
    if edificio_form.is_valid():
      edificio_form.save()
      request.session['_info_message']  = 'Edificio agregada correctamente'  
      return HttpResponseRedirect(url)
  context = {
    'edificio_form': edificio_form,
  }
  return render(request, 'inmuebles/edificio_crear.html',context)

@login_required(login_url='/')
def edificio_editar_view(request, id_edificio):
  url = reverse('vista_edificio')
  edificio = get_object_or_404(Edificio, pk=id_edificio)
  edificio_form = EdificioAddForm(instance=edificio)
  if request.method == "POST":
    edificio_form = EdificioAddForm(request.POST, request.FILES, instance=edificio)
    if edificio_form.is_valid():
      edificio_form.save()
      request.session['_info_message']  = 'Edificio actualizado correctamente'  
      return HttpResponseRedirect(url)
  context = {
    'edificio_form': edificio_form,
    'edificio':edificio,
  }
  return render(request, 'inmuebles/edificio_editar.html',context)

@login_required(login_url='/')
def departamento_view(request):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  edificio = get_object_or_404(Edificio, pk=request.session['edificio_actual'][1])
  departamentos = Departamento.objects.filter(edificio=edificio)
  context = {
    'message': message,
    'departamentos' : departamentos,
  }
  return render(request, 'inmuebles/departamento.html',context)


@login_required(login_url='/')
def departamento_crear_view(request):
  url = reverse('vista_departamento')
  departamento_form = DepartamentoAddForm()
  if request.method == "POST":
    departamento_form = DepartamentoAddForm(data=request.POST, edificio_id=request.session['edificio_actual'][1])
    if departamento_form.is_valid():
      departamento = departamento_form.save(commit=False)
      edificio = get_object_or_404(Edificio, pk=request.session['edificio_actual'][1])
      departamento.edificio = edificio
      departamento.save()
      messages.success(request, 'Departamento agregado correctamente')
      if 'guardar_con_condominos' in request.POST:
        url = reverse('vista_editar_departamento', kwargs={'id_departamento': departamento.id})
      return HttpResponseRedirect(url)
  context = {
    'departamento_form': departamento_form,
  }
  return render(request, 'inmuebles/departamento_crear.html',context)

@login_required(login_url='/')
def departamento_editar_view(request, id_departamento):
  departamento = get_object_or_404(Departamento, pk=id_departamento)
  url = reverse('vista_editar_departamento', kwargs={'id_departamento': departamento.id})
  error_crear_condomino = 0
  error_editar_condomino = 0
  departamento_form = DepartamentoAddForm(instance=departamento)
  user_profile_editar_form = ''
  user_editar_form = ''
  usuario_departamento_condomino_editar_form = ''
  if request.GET.get('editar_condomino_id'):
    id_usuario_editar = request.GET.get('editar_condomino_id')
    usuario_editar = User.objects.get(id=id_usuario_editar)
    user_profile_editar_form = UserProfileCondominoForm(instance=usuario_editar.userprofile)
    user_editar_form = UserEditForm(instance=usuario_editar)
    usuario_departamento_editar = UsuarioDepartamento.objects.get(usuario=usuario_editar, departamento=departamento)
    usuario_departamento_condomino_editar_form = UsuarioDepartamentoCondominoForm(instance=usuario_departamento_editar)
  user_profile_form = UserProfileCondominoForm()
  user_form = UserCondominoForm()
  usuario_departamento_condomino_form = UsuarioDepartamentoCondominoForm()
  usuario_departamento_form = UsuarioDepartamentoForm(initial={'departamento': departamento})
  list_ids_departamentousuario = []
  for departamanetousuario in departamento.usuariodepartamento_set.all():
    list_ids_departamentousuario.append(departamanetousuario.usuario.id)
  usuario_departamento_form.fields["usuario"].queryset = User.objects.exclude(id__in=list_ids_departamentousuario)
  if request.method == "POST":
    if request.POST.get('form_condomino_crear'):
      #validando el agregar condomino
      user_profile_form = UserProfileCondominoForm(request.POST)
      user_form = UserCondominoForm(request.POST)
      usuario_departamento_condomino_form = UsuarioDepartamentoCondominoForm(request.POST)
      if user_form.is_valid() and user_profile_form.is_valid() and usuario_departamento_condomino_form.is_valid():
        #user_profile_form.save()
        usuario = user_form.save(commit=False)
        usuario.username = usuario.email
        usuario.password = make_password(user_form.cleaned_data['password'])
        usuario.save()
        usuario_profile = user_profile_form.save(commit=False)
        usuario_profile.user = usuario
        usuario_profile.save()
        usuario_departamento_condomino = usuario_departamento_condomino_form.save(commit=False)
        usuario_departamento_condomino.usuario = usuario
        usuario_departamento_condomino.departamento = departamento
        usuario_departamento_condomino.save()
        messages.success(request, 'Condómino agregado correctamente')
      else:
        messages.error(request, 'El codómino tiene errores.')
        error_crear_condomino = 1
    elif request.POST.get('editar_condomino_id'):
      id_usuario_editar = request.POST.get('editar_condomino_id')
      usuario_editar = User.objects.get(id=id_usuario_editar)
      user_profile_editar_form = UserProfileCondominoForm(request.POST,instance=usuario_editar.userprofile)
      user_editar_form = UserEditForm(request.POST,instance=usuario_editar)
      usuario_departamento_editar = UsuarioDepartamento.objects.get(usuario=usuario_editar, departamento=departamento)
      usuario_departamento_condomino_editar_form = UsuarioDepartamentoCondominoForm(request.POST,instance=usuario_departamento_editar)
      if user_editar_form.is_valid() and user_profile_editar_form.is_valid() and usuario_departamento_condomino_editar_form.is_valid():
        #user_profile_form.save()
        usuario = user_editar_form.save(commit=False)
        usuario.username = usuario.email
        if user_editar_form.cleaned_data['password1']:
          usuario.password = make_password(user_editar_form.cleaned_data['password1'])
        usuario.save()
        usuario_profile = user_profile_editar_form.save(commit=False)
        usuario_profile.user = usuario
        usuario_profile.save()
        usuario_departamento_condomino = usuario_departamento_condomino_editar_form.save(commit=False)
        usuario_departamento_condomino.usuario = usuario
        usuario_departamento_condomino.departamento = departamento
        usuario_departamento_condomino.save()
        messages.success(request, 'Condómino editado correctamente')
        return HttpResponseRedirect(url)
      else:
        messages.error(request, 'El codómino tiene errores.')
        error_editar_condomino = 1
    else:
      departamento_form = DepartamentoAddForm(request.POST, request.FILES, instance=departamento)
      if departamento_form.is_valid():
        departamento_form.save()
        messages.success(request, 'Departamento actualizado correctamente')
      else:
        messages.error(request, 'El departamento tiene errores')
    #return HttpResponseRedirect(url)

  context = {
    'departamento_form': departamento_form,
    'departamento':departamento,
    'user_profile_form':user_profile_form,
    'user_form':user_form,
    'usuario_departamento_form':usuario_departamento_form,
    'usuario_departamento_condomino_form':usuario_departamento_condomino_form,
    'user_profile_editar_form':user_profile_editar_form, 
    'usuario_departamento_condomino_editar_form':usuario_departamento_condomino_editar_form, 
    'user_editar_form':user_editar_form,
    'error_crear_condomino':error_crear_condomino,
    'error_editar_condomino':error_editar_condomino
  }
  return render(request, 'inmuebles/departamento_editar.html',context)

@login_required(login_url='/')
def departamento_crear_usuariodepartamento_view(request):
  url = reverse('vista_departamento')
  if request.method == "POST":
    id_departamento = request.POST['id_departamento']
    departamento = get_object_or_404(Departamento, pk=id_departamento)
    departamento_usuario_form = UsuarioDepartamentoForm(request.POST)
    if departamento_usuario_form.is_valid():
      departamento_usuario = departamento_usuario_form.save(commit=False)
      departamento_usuario.departamento = departamento
      departamento_usuario.save()
      messages.success(request, 'Usuario agregado correctamente')
    else:
      messages.error(request, 'Debes seleccionar un usuario para agregar el departamento')

    url = reverse('vista_editar_departamento', kwargs={'id_departamento': departamento.id})  
    return HttpResponseRedirect(url)
  else:
    raise Http404("The silence is golden")

@login_required(login_url='/')
def departamento_quitar_usuariodepartamento_view(request):
  url = reverse('vista_departamento')
  if request.method == "POST":
    if request.POST.get('id_usuariodepartamento') and request.POST.get('id_departamento'):
      id_departamento = request.POST['id_departamento']
      departamento = get_object_or_404(Departamento, pk=id_departamento)
      url = reverse('vista_editar_departamento', kwargs={'id_departamento': departamento.id})
      id_usuariodepartamento = request.POST.get('id_usuariodepartamento')
      usuariodepartamento = get_object_or_404(UsuarioDepartamento, pk=id_usuariodepartamento)
      usuariodepartamento.delete()
      messages.success(request, 'Condómino quitado correctamente')
    else:
      messages.error(request, 'Problemas para eliminar el condómino')
    return HttpResponseRedirect(url)
  else:
    raise Http404("The silence is golden")



