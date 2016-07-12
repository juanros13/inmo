# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.widgets import Select, Textarea
from apps.encuestas.models import Encuesta, Opcion, Voto, ComentarioEncuesta

  
class EncuestaAddForm(forms.ModelForm):
  titulo = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder' : 'Ingresa el titulo de la encuesta',
      }
    ), 
    label = "Titulo de la encuesta",
  )
  fecha_limite_para_votacion = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control date-picker',
        'placeholder' : 'Ingresa la fecha limite para participar en la encuesta ',
      }
    ), 
    label = "Fecha limite para participar en la encuesta",
  )
  class Meta:
    model = Encuesta
    fields = ('titulo', 'descripcion', 'fecha_limite_para_votacion')
    widgets = {
      'descripcion': Textarea(
        attrs={
          'class': 'form-control',
          'rows' : '8',
          'placeholder' :'Ingresa la descripción de la encuesta'
        }
      ),
    }

class OpcionAddForm(forms.ModelForm):
  opcion = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder' : 'Ingresa tu opcion',
      }
    ), 
    label = "Opciones",
    required=True,
  )
  def __init__(self, *arg, **kwarg):
    super(OpcionAddForm, self).__init__(*arg, **kwarg)
    self.empty_permitted = False
  class Meta:
    model = Opcion
    fields = ('opcion',)
   

class VotosAddForm(forms.ModelForm):
  class Meta:
    model = Voto
    fields = ('opcion',)


class ComentarioEncuestaAddForm(forms.ModelForm):
  class Meta:
    model = ComentarioEncuesta
    fields = ('comentario',)
    widgets = {
      'comentario': Textarea(
        attrs={
          'class': 'form-control c-square',
          'rows' : '8',
          'placeholder' :'Escribe tu comentario...'
        }
      ),
    }
