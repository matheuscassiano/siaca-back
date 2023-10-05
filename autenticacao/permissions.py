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
    def has_object_permission(self, request, view, obj):
        if request.user.user_type() == 'coordenador':
            # Verificar se o usuário logado é coordenador do curso
            # ao qual o objeto (por exemplo, uma disciplina) está associado
            return request.user.coordenador.curso == obj.curso
        return False
    
class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verifica se user logado é Staff
        return (request.user.user_type() == 'staff')
    
class IsAluno(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verifica se o usuário logado é aluno
        return (request.user.user_type() == 'aluno')

class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verifica se o usuário logado é professor
        return (request.user.user_type() == 'professor')
    
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
        if request.user.user_type() == 'coordenador':
            coordenador = request.user.coordenador
            if coordenador.curso.pk == obj.oferta.disciplina.curso.pk:
                return True
            else:
                return False
        else:
            return False

class IsDisciplinaFromCoordenadorCurso(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Verificar se o usuário logado é coordenador, e se o curso a qual a matricula pertence é o mesmo do coordenador
        if request.user.user_type() == 'coordenador':
            coordenador = request.user.coordenador
            if coordenador.curso.pk == obj.disciplina.curso.pk:
                return True
            else:
                return False
        else:
            return False