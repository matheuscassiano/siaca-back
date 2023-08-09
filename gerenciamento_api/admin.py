from django.contrib import admin
from autenticacao.models import User, Professor, Coordenador, Aluno
from django.contrib.auth.admin import UserAdmin

from models import Curso

admin.site.register(Coordenador)
admin.site.register(Professor)
admin.site.register(Aluno)

admin.site.register(User, UserAdmin)

admin.site.register(Curso)
