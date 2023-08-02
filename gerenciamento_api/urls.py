from django.urls import path
from django.urls import path
from .views import CreateUserView, UpdateDeleteUserView

urlpatterns = [
    path('usuario/', CreateUserView.as_view(), name='criar_usuario'),
    path('usuario/<int:id>/', UpdateDeleteUserView.as_view(), name='atualizar_deletar_usuario'),
]