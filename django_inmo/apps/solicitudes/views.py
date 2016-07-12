# -*- encoding: utf-8 -*-
from datetime import datetime, date, time
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.forms import formset_factory
from django.contrib.auth.models import User
from apps.solicitudes.forms import MantenimientoForm, ComentarioMantenimientoAddForm
from apps.solicitudes.models import Mantenimiento, ComentarioMantenimiento

@login_required(login_url='/')
def mantenimiento_view(request):
    
  mantenimientos = Mantenimiento.objects.all()
  context = {
    'mantenimientos':mantenimientos
  }
  return render(request, 'solicitudes/mantenimiento.html',context)

@login_required(login_url='/')
def mantenimiento_crear_view(request):
  url = reverse('vista_solicitud_mantenimiento')
  mantenimiento_form = MantenimientoForm()
  if request.method == "POST":
    mantenimiento_form = MantenimientoForm(request.POST)
    if mantenimiento_form.is_valid() and mantenimiento_form.is_valid():
      aviso = mantenimiento_form.save(commit=False)
      aviso.usuario_creo = request.user
      aviso.save()
      request.session['_info_message']  = 'Aviso agregado correctamente'  
      return HttpResponseRedirect(url)

  context = {
    'mantenimiento_form': mantenimiento_form,
  }
  return render(request, 'solicitudes/mantenimiento_crear.html',context)

@login_required(login_url='/')
def mantenimiento_detalle_view(request, id_mantenimiento):
  message = ''
  mantenimiento = get_object_or_404(Mantenimiento, pk=id_mantenimiento)
  ultimos_mantenimiento = Mantenimiento.objects.all().order_by('-fecha_creacion')[:5]
  comentarios = ComentarioMantenimiento.objects.filter(mantenimiento=mantenimiento)
  comentarios_form = ComentarioMantenimientoAddForm(request.POST)
  if request.method == "POST":
    if comentarios_form.is_valid():
      comentario_mantenimiento = comentarios_form.save(commit=False)
      comentario_mantenimiento.usuario_creo = request.user
      comentario_mantenimiento.mantenimiento = mantenimiento
      comentario_mantenimiento.save()
      message = 'Comentario agregado correctamente'  
  context = {
    'mantenimiento':mantenimiento,
    'comentarios':comentarios,
    'comentarios_form':comentarios_form,
    'message': message,
    'ultimos_mantenimiento':ultimos_mantenimiento
  }
  return render(request, 'solicitudes/mantenimiento_detalle.html',context)