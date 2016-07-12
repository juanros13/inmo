# -*- encoding: utf-8 -*-
import json as simplejson
import datetime
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import connection
from django.db.models import Q , Count, Sum
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.utils import simplejson
from apps.edificios.models import Edificio, Egresos, Concepto
from apps.departamentos.models import  Departamento, Recibo
from apps.departamentos.models import MovimientosRecibo, Departamento, Recibo, Mantenimiento

@login_required
def adeudos_view(request):
  profile = request.user.get_profile()
  edificios = []
  edificios_con_adeudos = []
  older = []
  departamentos = Departamento.objects.filter(idusuario=profile.id_inquilino)
  if departamentos:
    for dep in departamentos:
      if not dep.edificio in edificios:
        edificios.append(dep.edificio)
  if edificios:
    for ed in edificios:
      adeudos = Recibo.objects.filter(id_edificio=ed.pk).extra(where=["saldo > 1"]).values("departamento", "anio").annotate(Sum("saldo")).order_by('-anio')
      edificios_con_adeudos.append({'id':ed.pk, 'nombre_edificio':ed.nombre, 'adeudos': adeudos, 'older': older})

  ctx = {'edificios':edificios_con_adeudos,'current_path': request.get_full_path()}
  return render_to_response('edificios/adeudos.html',ctx,context_instance=RequestContext(request))

@login_required
def obtener_saldo_view(request):
  
  if request.method == "POST":
    try:
      recibos = Recibo.objects.filter(departamento=request.POST['departamento'], anio=request.POST['anio']).extra(where=["saldo > 1"]).order_by('-mes')
      ctx = {'recibos':recibos,'current_path': request.get_full_path()}
      return render_to_response('edificios/adeudo_detalle.html',ctx,context_instance=RequestContext(request))
    except :
      raise Http404
  raise Http404


@login_required
def egresos_view(request):
  profile = request.user.get_profile()
  edificios = []
  edificios_con_adeudos = []
  older = []
  departamentos = Departamento.objects.filter(idusuario=profile.id_inquilino)
  if departamentos:
    for dep in departamentos:
      if not dep.edificio in edificios:
        edificios.append(dep.edificio)
  if edificios:
    for ed in edificios:
      tipos = Concepto.objects.filter(id_edificio=ed.pk).values("descripcion").annotate(Count("descripcion"))
      print tipos.query
      edificios_con_adeudos.append({'id':ed.pk, 'nombre_edificio':ed.nombre, 'tipos': tipos, 'older': older})

  ctx = {'edificios':edificios_con_adeudos,'current_path': request.get_full_path()}
  return render_to_response('edificios/egresos.html',ctx,context_instance=RequestContext(request))

@login_required
def egresos_json(request):
  profile = request.user.get_profile()
  id_edificio = request.GET.get('idEdificio')
  edificios = []
  items_list_dict  = {}
  my_json = []
  desplejar_desde = int(request.GET.get('iDisplayStart'))
  paginado = int(request.GET.get('iDisplayLength'))
 
  
  
  # Sacando todos edificios validos para el usuario
  edificios_usuario = []
  departamentos = Departamento.objects.filter(idusuario=profile.id_inquilino)
  if departamentos:
    for dep in departamentos:
      edificios.append(dep.edificio)
  if edificios:
    for ed in edificios:
      edificios_usuario.append(ed.id)

  # Filtros
  query_q = Q()
  filtro_global = request.GET.get('sSearch')
  

  filtro_fecha_desde = request.GET.get('sSearch_0')
  try:
    datetime.datetime.strptime(filtro_fecha_desde, '%Y-%m-%d')
  except ValueError:
    filtro_fecha_desde = False
  filtro_fecha_hasta = request.GET.get('sSearch_1')
  try:
    datetime.datetime.strptime(filtro_fecha_hasta, '%Y-%m-%d')
  except ValueError:
    filtro_fecha_hasta = False
  filtro_tipo = request.GET.get('sSearch_2')
  ahora = datetime.datetime.now()
  if filtro_global:
    query_q &= Q(descripcion__icontains=request.GET['sSearch'])
  if filtro_tipo:
    query_q &= Q(concepto__descripcion__icontains=filtro_tipo)

  if filtro_fecha_desde and filtro_fecha_hasta:
    query_q &= Q(fecha_egr__range=[filtro_fecha_desde, filtro_fecha_hasta])
  elif filtro_fecha_desde:
    query_q &= Q(fecha_egr__range=[filtro_fecha_desde, ahora.strftime('%Y-%m-%d')])
  # Validando que puedas ver este edificios
  try:
    id_edificio = id_edificio.split('--')
    if int(id_edificio[1]) in edificios_usuario:
      total = Egresos.objects.filter(id_edificio=id_edificio[1]).count()
      egresos = Egresos.objects.filter(id_edificio=id_edificio[1]).filter(query_q).order_by('-fecha_egr')[desplejar_desde:desplejar_desde+paginado]
      total_display = Egresos.objects.filter(id_edificio=id_edificio[1]).filter(query_q).order_by('ano_egr', 'mes_egr').count()
      for egreso in egresos:
        fecha = str(egreso.fecha_egr)
        total_egr = str(egreso.total_egr)
        num_cheque = egreso.num_cheque
        try:
          concepto = egreso.concepto.descripcion
        except:
          concepto = False
        if concepto:
          a = [fecha,concepto,egreso.descripcion, num_cheque,total_egr]
          my_json.append(a)
      items_list_dict.update({'aaData': my_json,'iTotalRecords':total, 'iTotalDisplayRecords':total_display,'sEcho':request.GET.get('sEcho')})
      data = simplejson.dumps(items_list_dict)
  except: 
    raise Http404
  # data = '{"sEcho": 1, "iTotalRecords": 57, "iTotalDisplayRecords": 57, "aaData": [ ["Gecko","Firefox 1.0","Win 98+ / OSX.2+","1.7","A"],["Gecko","Firefox 1.5","Win 98+ / OSX.2+","1.8","A"],["Gecko","Firefox 2.0","Win 98+ / OSX.2+","1.8","A"],["Gecko","Firefox 3.0","Win 2k+ / OSX.3+","1.9","A"],["Gecko","Camino 1.0","OSX.2+","1.8","A"],["Gecko","Camino 1.5","OSX.3+","1.8","A"],["Gecko","Netscape 7.2","Win 95+ / Mac OS 8.6-9.2","1.7","A"],["Gecko","Netscape Browser 8","Win 98SE+","1.7","A"],["Gecko","Netscape Navigator 9","Win 98+ / OSX.2+","1.8","A"],["Gecko","Mozilla 1.0","Win 95+ / OSX.1+","1","A"]] }'
  return HttpResponse(data, mimetype='application/json')
