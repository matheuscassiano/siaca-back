from django.contrib import admin
from autenticacao.models import User, Professor, Coordenador, Aluno
from coordenacao.models import Curso, Disciplina, Sala, Periodo
from django.contrib.auth.admin import UserAdmin
from grade.models import Oferta

admin.site.register(Coordenador)
admin.site.register(Professor)
admin.site.register(Aluno)

admin.site.register(User, UserAdmin)

admin.site.register(Curso)
admin.site.register(Disciplina)
admin.site.register(Sala)
admin.site.register(Periodo)

admin.site.register(Oferta)