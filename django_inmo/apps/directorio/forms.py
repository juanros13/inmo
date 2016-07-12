# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.widgets import Select, Textarea
from apps.directorio.models import Entidad, EntidadCategoria

class EntidadAddForm(forms.ModelForm):
  nombre = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder' : 'Ingresa el nombre de la Entidad',
      }
    ), 
    label = "Nombre de la entidad",
  )
  telefono = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder' : 'Ingresa el telefono',
      }
    ), 
    label = "Telefono",
  )
  correo = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder' : 'Ingresa el correo',
      }
    ), 
    label = "Correo electronico",
    required=False,
  )
  pagina_web = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder' : 'Ingresa la pagina web',
      }
    ), 
    label = "Pagina web",
    required=False,
  )
  ubicacion = forms.CharField(
    widget=forms.Textarea(
      attrs={
          'class': 'form-control',
          'rows' : '8',
          'placeholder' :'Ingresa la ubicacion'
        }
    ),
    required=False,
  )
  categoria = forms.ModelChoiceField(
    queryset = EntidadCategoria.objects.all(),
    widget=forms.Select(
      attrs={
        'class': 'form-control',
      }
    )
  )
  class Meta:
    model = Entidad
    fields = ('nombre','telefono', 'correo', 'pagina_web', 'ubicacion','categoria')

class EntidadCategoriaAddForm(forms.ModelForm):
  nombre = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder' : 'Ingresa el titulo de la encuesta',
      }
    ), 
    label = "Nombre de la entidad",
  )

  descripcion = forms.CharField(
    widget=forms.Textarea(
      attrs={
          'class': 'form-control',
          'rows' : '8',
          'placeholder' :'Ingresa la descripcion'
        }
    ),
    required=False,
  )
  class Meta:
    model = EntidadCategoria
    fields = ('nombre','descripcion',)
