# -*- encoding: utf-8 -*-
from datetime import datetime, date, time
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.forms import formset_factory
from django.contrib.auth.models import User
from apps.avisos.forms import AvisoAddForm, ComentarioAddForm
from apps.avisos.models import Aviso, ComentarioAviso

@login_required(login_url='/')
def aviso_view(request):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  avisos = Aviso.objects.all()
  context = {
    'avisos': avisos,
    'message': message
  }
  return render(request, 'avisos/avisos.html',context)

@login_required(login_url='/')
def avisos_crear_view(request):
  url = reverse('vista_avisos')
  aviso_form = AvisoAddForm()
  if request.method == "POST":
    aviso_form = AvisoAddForm(request.POST)
    if aviso_form.is_valid() and aviso_form.is_valid():
      aviso = aviso_form.save(commit=False)
      aviso.usuario_creo = request.user
      aviso.save()
      request.session['_info_message']  = 'Aviso agregado correctamente'  
      return HttpResponseRedirect(url)

  context = {
    'aviso_form': aviso_form,
  }
  return render(request, 'avisos/crear_aviso.html',context)

@login_required(login_url='/')
def aviso_detalle_view(request, id_aviso):
  message = ''
  aviso = get_object_or_404(Aviso, pk=id_aviso)
  ultimos_avisos = Aviso.objects.all().order_by('-fecha_creacion')[:5]
  comentarios = ComentarioAviso.objects.filter(aviso=aviso)
  comentarios_form = ComentarioAddForm()
  if request.method == "POST":
    comentarios_form = ComentarioAddForm(request.POST)
    if comentarios_form.is_valid():
      aviso_guardar = comentarios_form.save(commit=False)
      aviso_guardar.usuario_creo = request.user
      aviso_guardar.aviso = aviso
      aviso_guardar.save()
      message = 'Comentario agregado correctamente'  
  context = {
    'aviso' : aviso,
    'ultimos_avisos': ultimos_avisos,
    'comentarios': comentarios,
    'message': message,
    'comentarios_form' : comentarios_form
  }
  return render(request, 'avisos/aviso_detalle.html',context)