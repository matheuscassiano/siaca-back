from django.contrib import admin
from autenticacao.models import User, Professor, Coordenador, Aluno
from coordenacao.models import Curso, Disciplina, Sala
from django.contrib.auth.admin import UserAdmin

admin.site.register(Coordenador)
admin.site.register(Professor)
admin.site.register(Aluno)

admin.site.register(User, UserAdmin)

admin.site.register(Curso)
admin.site.register(Disciplina)
admin.site.register(Sala)