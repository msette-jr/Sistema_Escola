from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    notas = models.JSONField(default=list)

    def media_notas(self):
        return sum(self.notas) / len(self.notas) if self.notas else 0

class Turma(models.Model):
    alunos = models.ManyToManyField(Aluno)

    def media_notas(self):
        total_notas = sum(aluno.media_notas() for aluno in self.alunos.all())
        return total_notas / self.alunos.count() if self.alunos.exists() else 0

    def alunos_acima_da_media(self):
        media_turma = self.media_notas()
        return [aluno for aluno in self.alunos.all() if aluno.media_notas() > media_turma]

