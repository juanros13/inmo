# -*- encoding: utf-8 -*-
from datetime import datetime, date, time
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.forms import formset_factory
from django.contrib.auth.models import User
from apps.directorio.forms import EntidadAddForm, EntidadCategoriaAddForm
from apps.directorio.models import EntidadCategoria

@login_required(login_url='/')
def directorio_view(request):
  usuarios_condominio = User.objects.all()
  entidad_form = EntidadAddForm(prefix='entidad')
  entidad_categoria_form = EntidadCategoriaAddForm(prefix='categoriaEntidad')
  message = ''
  if request.method == "POST":
    entidad_form = EntidadAddForm(request.POST, prefix='entidad')
    if entidad_form.is_valid():
      entidad = entidad_form.save(commit=False)
      entidad.usuario_creo = request.user
      entidad_form.save()
      entidad_form = EntidadAddForm(prefix='entidad')
      entidad_categoria_form = EntidadCategoriaAddForm(prefix='categoriaEntidad')
      message = 'Entidad gudardada correctamente'
    entidad_categoria_form = EntidadCategoriaAddForm(request.POST, prefix='categoriaEntidad')
    if entidad_categoria_form.is_valid():
      entidad_categoria_form.save()
      entidad_form = EntidadAddForm(prefix='entidad')
      entidad_categoria_form = EntidadCategoriaAddForm(prefix='categoriaEntidad')
      message = 'Categoria gudardada correctamente'
  categorias_entidad = EntidadCategoria.objects.all()
  context = {
    'usuarios_condominio' : usuarios_condominio,
    'categorias_entidad' : categorias_entidad,
    'entidad_form' : entidad_form,
    'entidad_categoria_form': entidad_categoria_form,
    'message': message
  }
  return render(request, 'directorio/directorio.html',context)