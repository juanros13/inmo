from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apps.usuarios.models import UserProfile, UserMensaje
from apps.encuestas.models import Encuesta, Opcion, Voto
from apps.instalaciones.models import Instalacion
from apps.inmuebles.models import Edificio, Departamento, UsuarioDepartamento
from apps.poblacion.models import Pais, Estado, Municipio


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Usuario Profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserMensaje)
admin.site.register(Encuesta)
admin.site.register(Opcion)
admin.site.register(Voto)
admin.site.register(Instalacion)
admin.site.register(Edificio)
admin.site.register(Pais)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(Departamento)
admin.site.register(UsuarioDepartamento)