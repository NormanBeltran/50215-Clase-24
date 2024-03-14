from django.contrib import admin

# Register your models here.
from .models import *

class CursoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "comision")
    list_filter = ("nombre",)


admin.site.register(Curso, CursoAdmin)
admin.site.register(Profesor)
admin.site.register(Estudiante)
admin.site.register(Entregable)