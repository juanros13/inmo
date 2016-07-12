# -*- encoding: utf-8 -*-
from datetime import datetime, date, time
from django.contrib.auth.decorators import permission_required, login_required
from django.http import JsonResponse, Http404
from apps.poblacion.models import Pais, Estado, Municipio, Colonia
from django.core import serializers


@login_required(login_url='/')
def get_pais_json_view(request):

  return JsonResponse(dict(paises=list(Pais.objects.values('clave_pais', 'nombre'))))

@login_required(login_url='/')
def get_estados_json_view(request, id_pais):
  if Pais.objects.filter(pk=id_pais).exists():
    estados = list(Estado.objects.values('clave_estado', 'nombre').filter(pais=id_pais))
    return JsonResponse(dict(estados=estados))
  else:
    raise Http404


@login_required(login_url='/')
def get_municipios_json_view(request, id_estado):
  if Estado.objects.filter(pk=id_estado).exists():
    municipios = list(Municipio.objects.values('clave_municipio', 'nombre', 'estado').filter(estado=id_estado))
    return JsonResponse(dict(municipios=municipios))
  else:
    raise Http404

@login_required(login_url='/')
def get_colonias_json_view(request, id_estado, id_municipio):
  if Estado.objects.filter(pk=id_estado).exists() and Municipio.objects.filter(pk=id_municipio).exists() :
    colonias = list(Colonia.objects.values('municipio', 'nombre', 'cp','id').filter(municipio=id_municipio,estado=id_estado))
    return JsonResponse(dict(colonias=colonias))
  else:
    raise Http404