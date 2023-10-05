from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from autenticacao.models import Professor, Aluno
from coordenacao.models import Periodo, Disciplina, Sala

class Oferta(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, null=False, blank=False)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=False, blank=False)
    professor = models.ForeignKey(Professor, on_delete=models.DO_NOTHING, null=True, blank=True)
    sala = models.ForeignKey(Sala, on_delete=models.DO_NOTHING, null=True, blank=True)
    aula_dias = models.CharField(max_length=7, null=False, blank=False) # '{0-6}' cada numero representa um dia da semana
    aula_hora_inicio = models.TimeField(null=False, blank=False)
    aula_hora_fim = models.TimeField(null=False, blank=False)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _("oferta")
        verbose_name_plural = _("ofertas")

    def __str__(self):
        if self.professor == None:
            return f"{self.pk} | {self.disciplina.nome} | Sem professor"
        else:
            return f"{self.pk} | {self.disciplina.nome} | {self.professor.user.first_name}"

    def get_absolute_url(self):
        return reverse("oferta_detail", kwargs={"pk": self.pk})
    
    def qtd_matriculas_relacionadas(self):
        matriculas_count = Matricula.objects.filter(oferta=self).count()
        return matriculas_count

    def matriculas_relacionadas(self):
        matriculas = Matricula.objects.filter(oferta=self)
        return matriculas

class Matricula(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    aprovado = models.BooleanField(default=False, blank=True)
    
    class Meta:
        verbose_name = _("matricula")
        verbose_name_plural = _("matriculas")

    def __str__(self):
        return f"{self.id} | {self.oferta.disciplina.nome} | {self.aluno.user.username}"

    def get_absolute_url(self):
        return reverse("matricula_detail", kwargs={"pk": self.pk})