# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.widgets import Select, Textarea, SelectMultiple, CheckboxInput
from apps.inmuebles.models import Edificio, Departamento, Torre, UsuarioDepartamento
from apps.usuarios.models import UserProfile

class UserCondominoEditForm(forms.ModelForm):
  email = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Ingresa el correo electronico',
      }
    ), 
    label = 'E-mail',
    required=True
  )
  first_name = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Ingresa el nombre',
      }
    ), 
    label = 'Nombre(s)',
    required=True
  )
  last_name = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Ingresa el apellido',
      }
    ), 
    label = 'Apellidos',
    required=True
  )
  password1 = forms.CharField(
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Ingresa el password',
      }
    ), 
    label = 'Password',
    required=False
  )
  password2 = forms.CharField(
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Confirma el password',
      }
    ), 
    label = 'Confirma el password',
    required=False
  )
  def clean_email(self):
    data = self.cleaned_data['email']
    if self.instance.email != data:
      if User.objects.filter(username=data).exists():
          raise ValidationError('Este correo ya esta dado de alta en el sistema.')
    return data
  def clean_password1(self):
    password1 = self.cleaned_data.get('password1')

    if password1:
      if len(password1)<8:
        raise forms.ValidationError("La contraseña debe ser mayor a 8 digitos")
    return password1
  def clean_password2(self):
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')

    if password1 != password2:
        raise forms.ValidationError("Las contraseñas no concuerdan")
    return password2
  class Meta:
    model = User
    fields = ['email', 'password1','password2','first_name','last_name','is_active']


class UserCondominoForm(forms.ModelForm):
  email = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Ingresa el correo electronico',
      }
    ), 
    label = 'E-mail',
    required=True
  )
  first_name = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Ingresa el nombre',
      }
    ), 
    label = 'Nombre(s)',
    required=True
  )
  last_name = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Ingresa el apellido',
      }
    ), 
    label = 'Apellidos',
    required=True
  )
  password = forms.CharField(
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Ingresa el password',
      }
    ), 
    label = 'Password',
    required=True
  )
  password2 = forms.CharField(
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Confirma el password',
      }
    ), 
    label = 'Confirma el password',
    required=True
  )
  def clean_email(self):
    data = self.cleaned_data['email']
    if User.objects.filter(username=data).exists():
        raise ValidationError('Este correo ya esta dado de alta en el sistema.')
    return data
  def clean_password(self):
    password = self.cleaned_data.get('password')

    if not password:
        raise forms.ValidationError("Debes confimrar tu contraseña")
    if len(password)<8:
        raise forms.ValidationError("La contraseña debe ser mayor a 8 digitos")
    return password
  def clean_password2(self):
    password1 = self.cleaned_data.get('password')
    password2 = self.cleaned_data.get('password2')

    if not password2:
        raise forms.ValidationError("Debes confimrar tu contraseña")
    if password1 != password2:
        raise forms.ValidationError("Las contraseñas no concuerdan")
    return password2
  class Meta:
    model = User
    fields = ['email', 'password','password2','first_name','last_name','is_active']


class UserProfileCondominoForm(forms.ModelForm):
  telefono = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Telefono',
      }
    ), 
    label = 'Telefono',
    required=False
  )
  celular = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Celular',
      }
    ), 
    label = 'Celular',
    required=False
  )
  
  class Meta:
    model = UserProfile
    fields = ('telefono', 'celular')

class UsuarioDepartamentoCondominoForm(forms.ModelForm):
  class Meta:
    model = UsuarioDepartamento
    fields = ('es_propietario', 'es_habitante', 'es_principal')
    widgets = {
      'es_propietario': CheckboxInput(attrs={'class': 'form-control',}),
      'es_habitante': CheckboxInput(attrs={'class': 'form-control',}),
      'es_principal': CheckboxInput(attrs={'class': 'form-control',}),
    }

class UsuarioDepartamentoForm(forms.ModelForm):
  class Meta:
    model = UsuarioDepartamento
    fields = ('usuario','es_propietario', 'es_habitante', 'es_principal')
    widgets = {
      'es_propietario': CheckboxInput(attrs={'class': 'form-control',}),
      'es_habitante': CheckboxInput(attrs={'class': 'form-control',}),
      'es_principal': CheckboxInput(attrs={'class': 'form-control',}),
      'usuario': Select(attrs={'class': 'form-control',}),
    }

class EdificioAddForm(forms.ModelForm):
  nombre = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control form-control-solid placeholder-no-fix',
        'placeholder' : 'Nombre del edificio',
      }
    ), 
    label = "Nombre",
    required=True
  )
  class Meta:
    model = Edificio
    fields = ('nombre','direccion', 'imagen', 'administrador')
    widgets = {
      'direccion': Textarea(attrs={'class': 'form-control',}),
      'administrador': SelectMultiple(attrs={'class': 'form-control administradores',}),
    }

class DepartamentoAddForm(forms.ModelForm):
  nombre = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control form-control-solid placeholder-no-fix',
        'placeholder' : 'Nombre del departamento',
      }
    ), 
    label = "Nombre",
    required=True
  )
  
  def __init__(self, *args, **kwargs):
    self.edificio_id = kwargs.pop('edificio_id', None)
    super(DepartamentoAddForm, self).__init__(*args, **kwargs)
  def clean_nombre(self):
    nombre = self.cleaned_data.get('nombre')
    if Departamento.objects.filter(nombre=nombre, edificio=self.edificio_id).count():
      raise forms.ValidationError("Este nombre de departamento ya esta dado de alta en el sistema")
    return nombre
  class Meta:
    model = Departamento
    fields = ('nombre', 'torre', 'observaciones')
    widgets = {
      'observaciones': Textarea(attrs={'class': 'form-control',}),
      'torre': Select(attrs={'class': 'form-control',}),
    }


class TorreAddForm(forms.ModelForm):
  nombre = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control form-control-solid placeholder-no-fix',
        'placeholder' : 'Nombre de la torre',
      }
    ), 
    label = "Nombre",
    required=True
  )
  class Meta:
    model = Torre
    fields = ('nombre',)
