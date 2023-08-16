from django.urls import path
from django.urls import path
from .views import CreateUserView, UpdateDeleteUserView
from .views import CreateCursoView, UpdateDeleteCursoView

urlpatterns = [
    path('usuario/', CreateUserView.as_view(), name='criar_usuario'),
    path('usuario/<int:id>/', UpdateDeleteUserView.as_view(), name='atualizar_deletar_usuario'),
    path('curso/', CreateCursoView.as_view(), name='criar_curso'),
    path('curso/<int:id>/', UpdateDeleteCursoView.as_view(), name='atualizar_deletar_curso'),
]