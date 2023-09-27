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

class IsCoordenadorCurso(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type() == 'coordenador':
            curso_id = int(request.data.get('curso'))
            if curso_id:
                # Verificar se o usuário logado é coordenador do curso
                # ao qual a disciplina está sendo associada
                return request.user.coordenador.curso.id == curso_id
        return False
    
class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verifica se user logado é Staff
        return (request.user.user_type() == 'staff')
    
class IsAluno(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verifica se o usuário logado é aluno
        return (request.user.user_type() == 'aluno')
    
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

class CanCreatePeriodo(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verificar se o usuário logado é coordenador ou membro da equipe
        return (
            request.user.user_type() == 'coordenador'
            or request.user.user_type() == 'staff'
        )

class CanUpdateDeletePeriodo(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Verificar se o usuário logado é coordenador, membro da equipe ou é o próprio usuário
        return (
            request.user.user_type() == 'coordenador'
            or request.user.user_type() == 'staff'
            or request.user.pk == obj.pk
        )

class CanUpdateDeletePeriodo(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Verificar se o usuário logado é coordenador, membro da equipe ou é o próprio usuário
        return (
            request.user.user_type() == 'coordenador'
            or request.user.user_type() == 'staff'
            or request.user.pk == obj.pk
        )

class IsOfertaFromCoordenadorCurso(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Verificar se o usuário logado é coordenador, e se o curso a qual a matricula pertence é o mesmo do coordenador
        if request.user.type_user() == 'coordenador':
            coordenador = request.user.coordenador
            if coordenador.curso.pk == obj.oferta.disciplina.curso.pk:
                return True
            else:
                return False
        else:
            return False