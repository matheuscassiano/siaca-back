from django.urls import path
from .views import DisciplinaCreateView, DisciplinaUpdateDeleteView, SalaCreateUpdateDeleteView, SalaCreateView,\
CreateCursoView, UpdateDeleteCursoView, CreatePeriodoView, UpdateDeletePeriodoView, SalaListView, DisciplinaListView

urlpatterns = [
    path('disciplinas/', DisciplinaCreateView.as_view(), name='disciplina-create'),
    path('disciplinas/<int:pk>/', DisciplinaUpdateDeleteView.as_view(), name='disciplina-detail'),
    path('listas-disciplinas/', DisciplinaListView.as_view(), name='disciplina-list'),

    path('salas/', SalaCreateView.as_view(), name='sala-create'),
    path('salas/<int:id>/', SalaCreateUpdateDeleteView.as_view(), name='sala-get-update-delete'),
    path('listar-salas/', SalaListView.as_view(), name='sala-list'),

    path('curso/', CreateCursoView.as_view(), name='criar_curso'),
    path('curso/<int:id>/', UpdateDeleteCursoView.as_view(), name='atualizar_deletar_curso'),

    path('periodo/', CreatePeriodoView.as_view(), name='criar_periodo'),
    path('periodo/<int:id>/', UpdateDeletePeriodoView.as_view(), name='atualizar_deletar_periodo'),
]