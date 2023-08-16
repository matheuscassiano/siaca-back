from django.urls import path
from .views import DisciplinaCreateView, DisciplinaUpdateDeleteView, SalaCreateView, SalaUpdateDeleteView

urlpatterns = [
    path('disciplinas/', DisciplinaCreateView.as_view(), name='disciplina-create'),
    path('disciplinas/<int:pk>/', DisciplinaUpdateDeleteView.as_view(), name='disciplina-detail'),
    path('salas/', SalaCreateView.as_view(), name='disciplina-create'),
    path('salas/<int:pk>/', SalaUpdateDeleteView.as_view(), name='disciplina-detail'),
]