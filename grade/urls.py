from .views import OfertaCreateView, OfertaUpdateDeleteView, MatriculaCreateView, MatriculaListView, MyMatriculaListView, MyOfertaListView
from django.urls import path

urlpatterns = [
    path('ofertas/', OfertaCreateView.as_view(), name='oferta-create'),
    path('ofertas/<int:pk>/', OfertaUpdateDeleteView.as_view(), name='oferta-detail'),
    path('minhas-aulas/', MyOfertaListView.as_view(), name='professor-oferta-list'),

    path('matriculas/', MatriculaCreateView.as_view(), name='matricula-create'),
    path('list-matriculas/', MatriculaListView.as_view(), name='matricula-list'),
    path('minhas-matriculas/', MyMatriculaListView.as_view(), name='alunos-matricula-list'),
]