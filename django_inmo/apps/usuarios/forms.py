# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.widgets import Select, Textarea
from django.utils.encoding import smart_unicode
from apps.usuarios.models import UserProfile, UserMensaje
from apps.poblacion.models import Pais, Estado, Municipio, Colonia

#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, HTML
#from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

class UserEditForm(forms.ModelForm):
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


class UserProfileEditForm(forms.ModelForm):
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
  rfc = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'RFC',
      }
    ), 
    label = 'RFC',
    required=False
  )
 
  def clean_municipio(self):
    data = self.cleaned_data['municipio']
    if self.instance.municipio != data:
      if self.cleaned_data['municipio']:
        id_municipio = self.cleaned_data['municipio']
        estado = self.cleaned_data.get('estado')
        if Municipio.objects.filter(clave_municipio=id_municipio.clave_municipio, estado=estado).exists():
          municipio = Municipio.objects.get(clave_municipio=id_municipio.clave_municipio, estado=estado)
          return municipio
        else:
          raise ValidationError('Este municipio no es valido')
    return data
  class Meta:
    model = UserProfile
    fields = ('telefono', 'celular', 'rfc', 'pais','estado','municipio','colonia')
    widgets = {
      'pais': Select(attrs={'class': 'form-control selectpicker',}),
      'estado': Select(attrs={'class': 'form-control selectpicker',}),
      'municipio': Select(attrs={'class': 'form-control selectpicker',}),
      'colonia': Select(attrs={'class': 'form-control selectpicker',}),
    }



class UserForm(forms.ModelForm):
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


class UserProfileForm(forms.ModelForm):
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
  rfc = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'RFC',
      }
    ), 
    label = 'RFC',
    required=False
  )
  estado = forms.IntegerField(
    widget=forms.Select(
      attrs={
        'class': 'form-control selectpicker',
      }
    ), 
    label = 'Estado',
    required=False
  )
  municipio = forms.IntegerField(
    widget=forms.Select(
      attrs={
        'class': 'form-control selectpicker',
      }
    ), 
    label = 'Municipio',
    required=False
  )
  colonia = forms.IntegerField(
    widget=forms.Select(
      attrs={
        'class': 'form-control selectpicker',
      }
    ), 
    label = 'Colonia',
    required=False
  )
  def clean_estado(self):
    data = self.cleaned_data['estado']
    if self.cleaned_data['estado']:
      id_estado = int(self.cleaned_data['estado'])
      if Estado.objects.filter(pk=id_estado).exists():
        estado = Estado.objects.get(pk=id_estado)
        return estado
      else:
        raise ValidationError('Este estado no es valido')
    return data
  def clean_municipio(self):
    data = self.cleaned_data['municipio']
    if self.cleaned_data['municipio']:
      id_municipio = int(self.cleaned_data['municipio'])
      estado = self.cleaned_data.get('estado')
      if Municipio.objects.filter(clave_municipio=id_municipio, estado=estado).exists():
        municipio = Municipio.objects.get(clave_municipio=id_municipio, estado=estado)
        return municipio
      else:
        raise ValidationError('Este municipio no es valido')
    return data
  def clean_colonia(self):
    data = self.cleaned_data['colonia']
    if self.cleaned_data['colonia']:
      id_colonia = int(self.cleaned_data['colonia'])
      if Colonia.objects.filter(pk=id_colonia).exists():
        colonia = Colonia.objects.get(pk=id_colonia)
        return colonia
      else:
        raise ValidationError('Este estado no es valido')
    return data
  class Meta:
    model = UserProfile
    fields = ('telefono', 'celular', 'rfc', 'pais','estado','municipio','colonia')
    widgets = {
      'pais': Select(attrs={'class': 'form-control selectpicker',}),
    }

class UserLoginForm(forms.Form):
  username = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control form-control-solid placeholder-no-fix',
        'autocomplete' : 'off',
        'placeholder' : 'Usuario',
      }
    ), 
    label = 'Usuario',
    required=True
  )
  password = forms.CharField(
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        'class': 'form-control form-control-solid placeholder-no-fix',
        'autocomplete' : 'off',
        'placeholder' : 'Password',
      }
    ), 
    label = 'Contraseña',
    required=True
  )



class UserUpdatePassword(forms.ModelForm):
  password_actual = forms.CharField(
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Password actual',
      }
    ), 
    label = 'Contraseña actual',
    required=False
  )
  password1 = forms.CharField(
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Nuevo password',
      }
    ), 
    label = 'Nueva contraseña',
    required=False
  )
  password2 = forms.CharField(
    widget=forms.PasswordInput(
      render_value=False,
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'Confirma nuevo password',
      }
    ), 
    label = 'Confirma la contraseña',
    required=False
  )

  class Meta:
    model = User
    fields = ('password_actual', 'password1', 'password2', )
  
class UserUpdateProfile(forms.ModelForm):
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
  rfc = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
        'autocomplete' : 'off',
        'placeholder' : 'RFC',
      }
    ), 
    label = 'RFC',
    required=False
  )
  

  class Meta:
    model = UserProfile
    fields = ('telefono', 'celular', 'rfc', )
  
class UserUpdateAvatar(forms.ModelForm):
  avatar = forms.ImageField(required=True, error_messages = {'invalid':'Image files only'}, widget=forms.FileInput)
  class Meta:
    model = UserProfile
    fields = ('avatar',)
  
class UserMensajeForm(forms.ModelForm):
  class Meta:
    model = UserMensaje
    fields = ('usuario_recibe', 'mensaje')
    widgets = {
      'usuario_recibe': Select(attrs={'class': 'form-control selectpicker',}),
      'mensaje': Textarea(
        attrs={
          'class': 'form-control todo-taskbody-taskdesc',
          'rows' : '8',
          'placeholder' :'Mensaje'
        }
      ),
    }
  