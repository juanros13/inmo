# -*- encoding: utf-8 -*-
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import connection
from django.db.models import Count
from django.db.models import Q , Count, Sum
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
import json as simplejson
from apps.departamentos.models import MovimientosRecibo, Recibo, ReciboPagado, ReciboEdoCuenta
from apps.inmuebles.models import Departamento




@login_required
def adeudos_view(request):
 
  profile = request.user.userprofile

  deptos = []

  departamentos = Departamento.objects.filter(idusuario=profile.id_inquilino)
  if departamentos:
    for dep in departamentos:
      adeudos = Recibo.objects.filter(saldo__gt=0,departamento=dep, id_inquilino=profile.id_inquilino)
      total = Recibo.objects.filter(saldo__gt=0,departamento=dep, id_inquilino=profile.id_inquilino).extra(select={'total': "SUM(saldo)"})
      total = total[0].total
      for adeudo in adeudos:
        query = "SELECT *, GROUP_CONCAT(descripcion ORDER BY inmcuota_id SEPARATOR '/')  AS conceptoss FROM departamentos_movimientosrecibo WHERE recibo_id="+ str(adeudo.id) +"  GROUP BY recibo_id "
        descripcion = MovimientosRecibo.objects.raw(query)
        adeudo.desc = descripcion[0].conceptoss
        
      deptos.append({'id':dep.pk, 'nombre_edificio':dep.edificio.nombre, 'adeudos': adeudos, 'numero': dep.numero_de_departamento})
  ctx = {'total':total, 'departamentos':deptos,'current_path': request.get_full_path()}
  return render_to_response('departamentos/adeudos.html',ctx,context_instance=RequestContext(request))


def obtener_anios_historial():
  cursor = connection.cursor()
  cursor.execute("SELECT YEAR(fecha) FROM `departamentos_reciboedocuenta` GROUP BY YEAR(fecha) ORDER BY YEAR( fecha ) DESC")
  row = [item[0] for item in cursor.fetchall()]
  return row

@login_required
def historial_view(request):
  profile = request.user.userprofile

  deptos = []
  today = date.today()
  departamentos = Departamento.objects.filter(idusuario=profile.id_inquilino)
  if departamentos:
    for dep in departamentos:
      historial = ""
      deptos.append({'id':dep.pk, 'nombre_edificio':dep.edificio.nombre, 'historial': historial, 'numero': dep.numero_de_departamento})
  anios = obtener_anios_historial()
  ctx = {'departamentos':deptos,'current_path': request.get_full_path(), 'anios':anios}
  return render_to_response('departamentos/historial.html',ctx,context_instance=RequestContext(request))



@login_required
def historial_json(request):
  profile = request.user.userprofile

  id_departamento = request.GET.get('idDepartamento')
  items_list_dict  = {}
  my_json = []
  today = date.today()
  departamentos = []

  # Sacando todos departamentos validos para el usuario
  departamentos_list = Departamento.objects.filter(idusuario=profile.id_inquilino)
  if departamentos_list:
    for dep in departamentos_list:
      departamentos.append(dep.pk)
  # Filtros
  query_q = Q()
  filtro_global = request.GET.get('sSearch')
  filtro_anio = request.GET.get('sSearch_0')
  if filtro_global:
    query_q &= Q(numero_recibo=request.GET['sSearch'])
  if filtro_anio:
    query_q &= Q(fecha__year=filtro_anio)
  else:
    anios = obtener_anios_historial()
    query_q &= Q(fecha__year=anios[0])
  # Validando que puedas ver este edificios
  if departamentos:
    id_departamento = id_departamento.split('---')
    if str(id_departamento[1]) in departamentos:
      total = ReciboEdoCuenta.objects.filter(localidad = id_departamento[1]).count()
      historial = ReciboEdoCuenta.objects.filter(localidad = id_departamento[1]).filter(query_q).order_by('-fecha').extra(
        select={'anioorder': 'YEAR(fecha)', 'mesorder': 'MONTH(fecha)', 'diaorder': 'DAY(fecha)'},
        order_by=['-anioorder', '-mesorder', 'diaorder' ]
      )
      total_display = ReciboEdoCuenta.objects.filter(localidad = id_departamento[1]).filter(query_q).order_by('fecha').count()
      for hist in historial:
        fecha_numero = str(hist.fecha.strftime("%Y%m"))
        numero_recibo = str(hist.numero_recibo)
        fecha = str(hist.fecha)
        importe_importe, importe_recibo = " ", " "
        if hist.tipo == 1:
          importe_recibo = "$ " + str(hist.importe)
        if hist.tipo == 2:
          importe_importe = "$ " + str(hist.importe)
        a = [fecha_numero, numero_recibo, fecha, importe_recibo, importe_importe]
        my_json.append(a)
      items_list_dict.update({'aaData': my_json,'iTotalRecords':total, 'iTotalDisplayRecords':total_display,'sEcho':request.GET.get('sEcho')})
      data = simplejson.dumps(items_list_dict)
  # data = '{"sEcho": 1, "iTotalRecords": 57, "iTotalDisplayRecords": 57, "aaData": [ ["Gecko","Firefox 1.0","Win 98+ / OSX.2+","1.7","A"],["Gecko","Firefox 1.5","Win 98+ / OSX.2+","1.8","A"],["Gecko","Firefox 2.0","Win 98+ / OSX.2+","1.8","A"],["Gecko","Firefox 3.0","Win 2k+ / OSX.3+","1.9","A"],["Gecko","Camino 1.0","OSX.2+","1.8","A"],["Gecko","Camino 1.5","OSX.3+","1.8","A"],["Gecko","Netscape 7.2","Win 95+ / Mac OS 8.6-9.2","1.7","A"],["Gecko","Netscape Browser 8","Win 98SE+","1.7","A"],["Gecko","Netscape Navigator 9","Win 98+ / OSX.2+","1.8","A"],["Gecko","Mozilla 1.0","Win 95+ / OSX.1+","1","A"]] }'
  return HttpResponse(data, mimetype='application/json')


def obtener_referecia(recibo):
  cursor = connection.cursor()
  cursor.execute("SELECT django_gm.ReferenciaCZ( 1, 1, 1, 1) as referencia ")[0]
  return cursor

def dictfetchall(cursor):
  "Returns all rows from a cursor as a dict"
  desc = cursor.description
  return [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
  ]

def obtener_detalle_adeudo(recibo):
  cursor = connection.cursor()
  cursor.execute(
    "SELECT q1.descripcion, q1.importe, IF(SUM( q3.importe ),SUM( q3.importe ),0) AS pagado " + 
    "FROM departamentos_movimientosrecibo q1 "+ 
    "LEFT JOIN departamentos_recibopagado q2 ON q1.recibo_id = q2.id_recibo " +
    "LEFT JOIN departamentos_recibopagadodet q3 ON q2.id = q3.idpagado AND q1.inmcuota_id = q3.idcuota " +
    "LEFT JOIN edificios_inmcuota q4 ON q4.id_cuota = q1.inmcuota_id " + 
    "WHERE q1.recibo_id = %s GROUP BY q1.inmcuota_id", recibo)
  rows = dictfetchall(cursor)
  return rows

@login_required
def obtener_detalle_view(request):
  if request.method == "POST":
    #print request.POST['no_recibo']
    #query = 'SELECT *, juanros13_gm.ReferenciaBZ(id_edificio , departemanto_id, id_inquilino) AS numero_de_referencia FROM departamentos_recibo WHERE id = %s LIMIT 1' % request.POST['id_recibo']
    #recibo = Recibo.objects.raw('SELECT * FROM departamentos_recibo WHERE id = %s LIMIT 1', [request.POST['id_recibo']])[0]
    movimientos = obtener_detalle_adeudo(request.POST['id_recibo'])
    #recibo = Recibo.objects.extra(select={'age': "juanros13_gm.ReferenciaBZ(id_edificio , departemanto_id, id_inquilino)"})
   
    ctx = {'movimientos':movimientos,'current_path': request.get_full_path()}
    return render_to_response('departamentos/adeudo_detalle.html',ctx,context_instance=RequestContext(request))
  serialized = simplejson.dumps(to_return)
  return HttpResponse(serialized, mimetype="application/json")

