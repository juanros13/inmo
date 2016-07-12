# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.widgets import Select, Textarea
from apps.solicitudes.models import Mantenimiento, ComentarioMantenimiento

class MantenimientoForm(forms.ModelForm):
  problema = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'placeholder' : 'Ingresa tu problema',
      }
    ), 
    label = "Titulo del aviso",
  )
  class Meta:
    model = Mantenimiento
    fields = ('problema','descripcion', 'departamento')
    widgets = {
      'descripcion': Textarea(attrs={'class': 'form-control',}),
      'departamento': Select(attrs={'class': 'form-control',}),
    }

class ComentarioMantenimientoAddForm(forms.ModelForm):
  class Meta:
    model = ComentarioMantenimiento
    fields = ('comentario',)
    widgets = {
      'comentario': Textarea(
        attrs={
          'class': 'form-control',
        }
      ),
    }
