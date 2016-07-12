# -*- encoding: utf-8 -*-
from datetime import datetime, date, time
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.forms import formset_factory
from apps.encuestas.models import Encuesta, Opcion, Voto, ComentarioEncuesta
from apps.encuestas.forms import EncuestaAddForm, OpcionAddForm, ComentarioEncuestaAddForm

@login_required(login_url='/')
def encuesta_view(request):
  encuestas = Encuesta.objects.all()
  for encuesta in encuestas:
    opciones = encuesta.opcion_set.all()
    opciones_total = opciones.count()
    votos_totales = 0
    for opcion in opciones:
      votos_totales += opcion.votos_total
    encuesta.cerrada = 0
    if encuesta.fecha_limite_para_votacion <= date.today():
      encuesta.cerrada = 1
    encuesta.opciones = opciones_total
    encuesta.votos = votos_totales
  context = {
    'encuestas' : encuestas
  }
  return render(request, 'encuestas/encuestas.html',context)

@login_required(login_url='/')
def encuesta_detalle_view(request, id_encuesta):
  message = ''
  encuesta = get_object_or_404(Encuesta, pk=id_encuesta)
  ultimas_encuestas = Encuesta.objects.all().order_by('-fecha_creacion')[:5]
  comentarios_encuesta = ComentarioEncuesta.objects.filter(encuesta=encuesta)
  if request.method == "POST":
    id_opcion = request.POST.get('opcion')
    if id_opcion:
      opcion = Opcion.objects.get(pk=id_opcion)
      opcion.votos_total += 1
      opcion.save()
      Voto.objects.create(usuario=request.user, opcion=opcion)
      message = 'Voto guardado correctamente'
    comentarios_form = ComentarioEncuestaAddForm(request.POST)
    if comentarios_form.is_valid():
      comentario = comentarios_form.save(commit=False)
      comentario.usuario = request.user
      comentario.encuesta = encuesta
      comentario.save()
      message = 'Comentario gudardado correctamente'
  comentarios_form = ComentarioEncuestaAddForm()
  context = {
    'encuesta' : encuesta,
    'ultimas_encuestas' : ultimas_encuestas,
    'comentarios_form' : comentarios_form,
    'comentarios_encuesta' : comentarios_encuesta,
    'message': message
  }
  return render(request, 'encuestas/encuesta_detalle.html',context)

@login_required(login_url='/')
def encuesta_crear_view(request):
  url = reverse('vista_encuesta_crear')
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''

  encuesta_form = EncuestaAddForm()
  OpcionFormset = formset_factory(OpcionAddForm, extra=2, max_num=5, validate_min=True)
  opcion_formset = OpcionFormset(prefix='opcion')
  if request.method == "POST":
    encuesta_form = EncuestaAddForm(request.POST)
    opcion_formset = OpcionFormset(request.POST, prefix='opcion')
    if encuesta_form.is_valid() and opcion_formset.is_valid():
      encuesta = encuesta_form.save(commit=False)
      encuesta.usuario_crea = request.user
      encuesta.save()
      for form in opcion_formset.forms:
        preguntas = form.save(commit=False)
        preguntas.encuesta = encuesta
        preguntas.votos_total = 0
        preguntas.save()
      request.session['_info_message']  = 'Encuesta agregada correctamente'  
      return HttpResponseRedirect(url)

  context = {
    'opcion_formset': opcion_formset,
    'encuesta_form' : encuesta_form,
    'message': message
  }
  return render(request, 'encuestas/encuesta_crear.html',context)
