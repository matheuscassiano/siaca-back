from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

class Curso(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    periodos = models.IntegerField(null=False, blank=False)
    ementa = models.BinaryField(null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    # created_by = models.ForeignKey(Coordenador, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("curso")
        verbose_name_plural = _("cursos")

    def __str__(self):
        return f"{self.id} | {self.nome}"

    def get_absolute_url(self):
        return reverse("view_curso", kwargs={"id_param": self.pk})

class Sala(models.Model):
    descricao = models.CharField(max_length=150, null=True, blank=True)
    lugares = models.IntegerField(null=False, blank=False)

    class Meta:
        verbose_name = _("sala")
        verbose_name_plural = _("salas")

    def __str__(self):
        return f"{self.pk}"

    def get_absolute_url(self):
        return reverse("view_sala", kwargs={"id_param": self.pk})

class Disciplina(models.Model):
    nome = models.CharField(max_length=50, null=False)
    descricao = models.TextField(null=True, blank=True)
    periodo = models.IntegerField(null=False, blank=False)
    ementa = models.BinaryField(null=True)
    carga_horaria = models.IntegerField(null=False, blank=False)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    pre_requisito = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("disciplina")
        verbose_name_plural = _("disciplinas")

    def __str__(self):
        return f"{self.id} | {self.nome}"

    def get_absolute_url(self):
        return reverse("disciplina_detail", kwargs={"pk": self.pk})