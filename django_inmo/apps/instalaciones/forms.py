# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.widgets import Select, Textarea
from apps.instalaciones.models import Instalacion, ReservacionInstalacion, DiaDisponibleInstalacion



class InstalacionAddForm(forms.ModelForm):
  nombre = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control form-control-solid placeholder-no-fix',
        'autocomplete' : 'off',
        'placeholder' : 'Nombre de la instalacion',
      }
    ), 
    label = "Nombre",
    required=True
  )

  class Meta:
    model = Instalacion
    fields = ('imagen','nombre','descripcion','reglamento','activo')
    widgets = {
      'descripcion': Textarea(attrs={'class': 'form-control selectpicker',}),
      'reglamento': Textarea(attrs={'class': 'form-control selectpicker',}),
    }

class DiaDisponibleInstalacionAddForm(forms.ModelForm):
  dia = forms.CharField(widget=forms.HiddenInput())
  dia_valor = forms.CharField(widget=forms.HiddenInput())
  hora_desde = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'hora-hasta form-control timepicker timepicker-24',
      }
    ), 
    label = "Nombe",
    required=True
  )
  hora_hasta = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'hora-hasta form-control timepicker timepicker-24',
      }
    ), 
    label = "Nombe",
    required=True
  )
  disponible = forms.BooleanField(
    widget=forms.CheckboxInput(
      attrs={
        'class': 'dia-disponible',

      },
    ),
    initial = 1,
    required = False
  )
  disponible_todo_el_dia = forms.BooleanField(
    widget=forms.CheckboxInput(
      attrs={
        'class': 'disponible-todo-el-dia',
      }
    ),
    initial = 1,
    required = False
  )
  def clean(self):
    cleaned_data = super(DiaDisponibleInstalacionAddForm, self).clean()
    hora_desde = cleaned_data['hora_desde']
    hora_hasta = cleaned_data['hora_hasta']

    msg = "La hora donde empieza el evento no puede ser mayor a la que termina"
    if hora_desde > hora_hasta: 
      self.add_error('hora_desde', msg)
      self.add_error('hora_hasta', msg)

  class Meta:
    model = DiaDisponibleInstalacion
    fields = ('dia', 'dia_valor', 'disponible','disponible_todo_el_dia', 'hora_desde', 'hora_hasta' )

class ReservacionInstalacionAddForm(forms.ModelForm):
  fecha_reservacion = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'fecha-reservacion form-control',
      }
    ), 
    label = "Fecha reservacion",
  )
  hora_empieza = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control timepicker timepicker-24',
      }
    ), 
    label = "Hora empieza",
  )
  hora_termina = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control timepicker timepicker-24',
      }
    ), 
    label = "Hora termina",
  )
  def clean(self):
    cleaned_data = super(ReservacionInstalacionAddForm, self).clean()
    fecha_reservacion = cleaned_data['fecha_reservacion']
    hora_desde = cleaned_data['hora_empieza']
    hora_hasta = cleaned_data['hora_termina']
    fechas_reservaciones = ReservacionInstalacion.objects.filter(fecha_reservacion=fecha_reservacion)
    if fechas_reservaciones:
      self.add_error('hora_empieza', 'Este dia ya esta ocupado')

    msg = "La hora donde empieza el reservacion no puede ser mayor a la que termina"
    if hora_desde >= hora_hasta: 
      self.add_error('hora_empieza', msg)
      self.add_error('hora_termina', msg)
  class Meta:
    model = ReservacionInstalacion
    fields = ('fecha_reservacion', 'hora_empieza', 'hora_termina')
