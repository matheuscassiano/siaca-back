from .views import OfertaCreateView, OfertaUpdateDeleteView, MatriculaCreateView, MatriculaListView
from django.urls import path

urlpatterns = [
    path('ofertas/', OfertaCreateView.as_view(), name='oferta-create'),
    path('ofertas/<int:pk>/', OfertaUpdateDeleteView.as_view(), name='oferta-detail'),

    path('matriculas/', MatriculaCreateView.as_view(), name='matricula-create'),
    path('list-matriculas/', MatriculaListView.as_view(), name='matricula-list'),
]