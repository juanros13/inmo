import mimetypes, os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import InvalidPage, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from apps.departamentos.models import Departamento
from apps.documentos.models import DocumentoPropios, DocumentoInmueble
from apps.plumbago.paginator import Paginator


@login_required
def documento_inmueble_view(request):
  edificios = []
  profile = request.user.get_profile()
  departamentos = Departamento.objects.filter(idusuario=profile.id_inquilino)
  if departamentos:
    for dep in departamentos:
      if not dep.edificio_id in edificios:
        edificios.append(dep.edificio_id)
        #adeudos = Recibo.objects.filter(saldo__gt=0,departamento=dep, id_inquilino=profile.id_inquilino)
  else:
    edificios.append(0)
  
  documentos = DocumentoInmueble.objects.filter(estatus=1, inmueble_id__in=edificios).order_by('-fecha_creacion')
  paginator = Paginator(documentos, 10)

  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    doc= paginator.page(page)
  except PageNotAnInteger:
    doc = paginator.page(1)
  except (EmptyPage, InvalidPage):
    doc = paginator.page(paginator.num_pages)

  ctx = {'documentos':doc, 'documentos_meses':documentos, 'current_path': request.get_full_path()}
  return render_to_response('documentos/documento_inmueble.html',ctx,context_instance=RequestContext(request))


@login_required
def documento_propios_view(request):
  profile = request.user.get_profile()
  documentos = DocumentoPropios.objects.filter(estatus=1, usuario_id=profile.id_inquilino).order_by('-fecha_creacion')
  paginator = Paginator(documentos, 10)

  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    doc= paginator.page(page)
  except PageNotAnInteger:
    doc = paginator.page(1)
  except (EmptyPage, InvalidPage):
    doc = paginator.page(paginator.num_pages)

  ctx = {'documentos':doc, 'documentos_meses':documentos, 'current_path': request.get_full_path()}
  return render_to_response('documentos/documento_propios.html',ctx,context_instance=RequestContext(request))


@login_required(login_url='/')
def documento_propios_detalle_view(request, item_id):
  documento = get_object_or_404(DocumentoPropios, pk=item_id)
  profile = request.user.get_profile()
  if documento.usuario_id == profile.id_inquilino:
    try:
      pdf = open("%s/propios/%s/%s/%s/%s" % (settings.FACTURAS_PATH, request.user.id, documento.anio, documento.mes, documento.archivo), "rb").read()
      mimetype = mimetypes.guess_type(pdf)[0]
      response = HttpResponse(pdf, mimetype=mimetype)
      response["Content-Disposition"]= "attachment; filename=%s" % documento.archivo
      return response
    except:
      raise Http404
  else:
    raise Http404

@login_required(login_url='/')
def documento_inmueble_detalle_view(request, item_id):
  documento = get_object_or_404(DocumentoInmueble, pk=item_id)
  profile = request.user.get_profile()
  edificios = []
  departamentos = Departamento.objects.filter(idusuario=profile.id_inquilino)
  if departamentos:
    for dep in departamentos:
      if not dep.edificio_id in edificios:
        edificios.append(int(dep.edificio_id))
        #adeudos = Recibo.objects.filter(saldo__gt=0,departamento=dep, id_inquilino=profile.id_inquilino)
  else:
    edificios.append(0)
  print edificios
  print documento.inmueble_id
  if documento.inmueble_id in edificios:
    try:
      pdf = open("%s/inmuebles/%s/%s/%s/%s" % (settings.FACTURAS_PATH, documento.inmueble_id,  documento.anio, documento.mes, documento.archivo), "rb").read()
      mimetype = mimetypes.guess_type(pdf)[0]
      response = HttpResponse(pdf, mimetype=mimetype)
      response["Content-Disposition"]= "attachment; filename=%s" % documento.archivo
      return response
    except:
      raise Http404
  else:
    raise Http404


