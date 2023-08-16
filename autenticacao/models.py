from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext as _
from coordenacao.models import Curso

class User(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=50)
    endereco = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.cpf} | {self.first_name}"
    
    def user_type(self):
        user_type = None
        try:
            bol = self.coordenador is not None
            user_type = 'coordenador'
        except:
            try:
                bol = self.professor is not None
                user_type = 'professor'
            except:
                try:
                    bol = self.aluno is not None
                    user_type = 'aluno'
                except:
                    user_type = 'staff'
        return user_type

    
class Coordenador(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING, null=True, blank=True)
    class Meta:
        verbose_name = _("coordenador")
        verbose_name_plural = _("coordenadores")

    def __str__(self):
        return f"{self.user.cpf} | {self.user.username}"


class Professor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    lattes = models.CharField(max_length=50)
    area_atuacao = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("professor")
        verbose_name_plural = _("professores")

    def __str__(self):
        return f"{self.user.cpf} | {self.user.first_name}"
    
class Aluno(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # curso = models.ForeignKey()
    # periodo_ingresso = models.ForeignKey()
    class Meta:
        verbose_name = _("aluno")
        verbose_name_plural = _("alunos")

    def __str__(self):
        return f"{self.user.cpf} | {self.user.first_name}"