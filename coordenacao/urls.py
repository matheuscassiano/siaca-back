from django.urls import path
from .views import DisciplinaCreateView, DisciplinaUpdateDeleteView, SalaCreateView, SalaUpdateDeleteView, \
CreateCursoView, UpdateDeleteCursoView, CreatePeriodoView, UpdateDeletePeriodoView, OfertaCreateView, OfertaUpdateDeleteView

urlpatterns = [
    path('disciplinas/', DisciplinaCreateView.as_view(), name='disciplina-create'),
    path('disciplinas/<int:pk>/', DisciplinaUpdateDeleteView.as_view(), name='disciplina-detail'),
    path('salas/', SalaCreateView.as_view(), name='disciplina-create'),
    path('salas/<int:pk>/', SalaUpdateDeleteView.as_view(), name='disciplina-detail'),
    path('curso/', CreateCursoView.as_view(), name='criar_curso'),
    path('curso/<int:id>/', UpdateDeleteCursoView.as_view(), name='atualizar_deletar_curso'),
    path('periodo/', CreatePeriodoView.as_view(), name='criar_periodo'),
    path('periodo/<int:id>/', UpdateDeletePeriodoView.as_view(), name='atualizar_deletar_periodo'),
    path('ofertas/', OfertaCreateView.as_view(), name='oferta-create'),
    path('ofertas/<int:pk>/', OfertaUpdateDeleteView.as_view(), name='oferta-detail'),
]