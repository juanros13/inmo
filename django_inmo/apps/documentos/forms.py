# -*- encoding: utf-8 -*-
from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.contrib.auth.models import User
from apps.documentos.models import DocumentoPropios, DocumentoInmueble
from apps.edificios.models import Edificio



class DocumentosInmuebleForm(forms.ModelForm):
  inmueble_id = forms.ChoiceField(choices=[(ed.id, ed.nombre) for ed in Edificio.objects.all()])
  def clean_archivo(self):
    content = self.cleaned_data['archivo']
    if hasattr(content, 'content_type'):
      if content.content_type in settings.TASK_UPLOAD_FILE_TYPES:
        if content._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
          raise forms.ValidationError('El archivo debe tamaño maximo de %s. El archivo actual tiene un tamaño de %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(content._size))
      else:
        raise forms.ValidationError('Los archivos soportados son pdf, word, excel')
    return content
 
  def save(self, commit=False):
    documento = super(DocumentosInmuebleForm, self).save(commit=False)
    archivo = self.cleaned_data.get('archivo')
    if archivo:
      archivo = str(archivo)
      documento.archivo_tipo = archivo.split(".")[-1]
    else:
      documento.archivo_tipo = None
    documento.save()
    return documento
  class Meta:
    model = DocumentoInmueble

class DocumentosPropiosForm(forms.ModelForm):
  def clean_archivo(self):
    content = self.cleaned_data['archivo']
    if hasattr(content, 'content_type'):
      if content.content_type in settings.TASK_UPLOAD_FILE_TYPES:
        if content._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
          raise forms.ValidationError('El archivo debe tamaño maximo de %s. El archivo actual tiene un tamaño de %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(content._size))
      else:
        raise forms.ValidationError('Los archivos soportados son pdf, word, excel')
    return content
 
  def save(self, commit=False):
    documento = super(DocumentosPropiosForm, self).save(commit=False)
    archivo = self.cleaned_data.get('archivo')
    if archivo:
      archivo = str(archivo)
      documento.archivo_tipo = archivo.split(".")[-1]
    else:
      documento.archivo_tipo = None
    documento.save()
    return documento
  class Meta:
    model = DocumentoPropios