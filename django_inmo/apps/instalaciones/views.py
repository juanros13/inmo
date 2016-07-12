# -*- encoding: utf-8 -*-
import random
from datetime import datetime, date, time
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.forms import formset_factory
from django.contrib.auth.models import User
from apps.instalaciones.forms import InstalacionAddForm, ReservacionInstalacionAddForm, DiaDisponibleInstalacionAddForm
from apps.instalaciones.models import Instalacion, ReservacionInstalacion

@login_required(login_url='/')
def instalacion_view(request):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  instalaciones = Instalacion.objects.all()
  context = {
    'message': message,
    'instalaciones': instalaciones,
  }
  return render(request, 'instalaciones/instalaciones.html',context)

@login_required(login_url='/')
def instalacion_crear_view(request):
  DIAS_DE_LA_SEMANA = (
    (1, 'Lunes'),
    (2, 'Martes'),
    (3, 'Miercoles'),
    (4, 'Jueves'),
    (5, 'Viernes'),
    (6, 'Sabado'),
    (7, 'Domingo'),
  )
  url = reverse('vista_instalacion')
  instalacion_form = InstalacionAddForm(prefix='instalacion')
  DiasDisponiblesFormSet= formset_factory(DiaDisponibleInstalacionAddForm, extra=len(DIAS_DE_LA_SEMANA), max_num=len(DIAS_DE_LA_SEMANA))
  dias_disponibles_formset = DiasDisponiblesFormSet(prefix='dias_disponibles',initial=[{
    'dia': x,
    'dia_valor':y,
    'hora_desde':'0:00',
    'hora_hasta':'0:00',
  } for x, y in DIAS_DE_LA_SEMANA])
  if request.method == "POST":
    instalacion_form = InstalacionAddForm(request.POST, request.FILES, prefix='instalacion')
    dias_disponibles_formset = DiasDisponiblesFormSet(request.POST, prefix='dias_disponibles')
    if instalacion_form.is_valid() and dias_disponibles_formset.is_valid():
      instalacion = instalacion_form.save(commit=False)
      instalacion.usuario_creo = request.user
      instalacion.save()
      for form in dias_disponibles_formset.forms:
        dias_habiles = form.save(commit=False)
        dias_habiles.instalacion = instalacion
        dias_habiles.save()
      request.session['_info_message']  = 'Instalacion agregada correctamente'  
      return HttpResponseRedirect(url)
  context = {
    'instalacion_form': instalacion_form,
    'dias_disponibles_formset':dias_disponibles_formset,
    'dias_semana': DIAS_DE_LA_SEMANA,
  }
  return render(request, 'instalaciones/crear_instalacion.html',context)


@login_required(login_url='/')
def reservacion_instalacion_crear_view(request, id_instalacion):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  instalacion = get_object_or_404(Instalacion, pk=id_instalacion)
  reservar_instalacion_form = ReservacionInstalacionAddForm(initial={'hora_empieza': '12:00','hora_termina': '12:00'})
  reservaciones = ReservacionInstalacion.objects.all()
  if request.method == "POST":
    reservar_instalacion_form = ReservacionInstalacionAddForm(request.POST)
    if reservar_instalacion_form.is_valid():
      reservacion = reservar_instalacion_form.save(commit=False)
      reservacion.usuario_creo = request.user
      reservacion.instalacion = instalacion
      reservacion.save()
  context = {
    'message': message,
    'instalacion': instalacion,
    'reservar_instalacion_form':reservar_instalacion_form,
    'reservaciones':reservaciones,
  }
  return render(request, 'instalaciones/crear_reservacion.html',context)

@login_required(login_url='/')
def reservacion_instalacion_detalle_view(request, id_instalacion):
  message = ''
  if request.session.get('_info_message'):
    message = request.session.get('_info_message')
  request.session['_info_message'] = ''
  instalacion = get_object_or_404(Instalacion, pk=id_instalacion)
  reservaciones = ReservacionInstalacion.objects.all()
  context = {
    'message': message,
    'instalacion': instalacion,
    'reservaciones':reservaciones,
  }
  return render(request, 'instalaciones/detalle_instalacion.html',context)
