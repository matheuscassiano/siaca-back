from .views import OfertaCreateView, OfertaUpdateDeleteView
from django.urls import path

urlpatterns = [
    path('ofertas/', OfertaCreateView.as_view(), name='oferta-create'),
    path('ofertas/<int:pk>/', OfertaUpdateDeleteView.as_view(), name='oferta-detail'),
]