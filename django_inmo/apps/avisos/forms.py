# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.widgets import Select, Textarea
from apps.avisos.models import Aviso, ComentarioAviso

class AvisoAddForm(forms.ModelForm):
  titulo = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder' : 'Ingresa el titulo del aviso',
      }
    ), 
    label = "Titulo del aviso",
  )
  class Meta:
    model = Aviso
    fields = ('tipo','titulo', 'contenido','mantener_al_principio')
    widgets = {
      'contenido': Textarea(
        attrs={
          'class': 'form-control',
        }
      ),
    }

class ComentarioAddForm(forms.ModelForm):
  class Meta:
    model = ComentarioAviso
    fields = ('comentario',)
    widgets = {
      'comentario': Textarea(
        attrs={
          'class': 'form-control',
        }
      ),
    }
