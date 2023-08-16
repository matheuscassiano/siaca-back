from rest_framework import permissions

class CanCreateUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verificar se o usuário logado é coordenador ou membro da equipe
        return (
            request.user.user_type() == 'coordenador'
            or request.user.user_type() == 'staff'
        )
    
class CanUpdateUserData(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Verificar se o usuário logado é coordenador, membro da equipe ou é o próprio usuário
        return (
            request.user.user_type() == 'coordenador'
            or request.user.user_type() == 'staff'
            or request.user.pk == obj.pk
        )

class CanCreateCurso(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verificar se o usuário logado é coordenador ou membro da equipe
        return (
            request.user.user_type() == 'coordenador'
            or request.user.user_type() == 'staff'
        )

class CanUpdateDeleteCurso(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Verificar se o usuário logado é coordenador, membro da equipe ou é o próprio usuário
        return (
            request.user.user_type() == 'coordenador'
            or request.user.user_type() == 'staff'
            or request.user.pk == obj.pk
        )