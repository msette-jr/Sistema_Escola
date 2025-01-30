class Aluno:
    def __init__(self, nome):
        self.__nome = nome
        self.__notas = []

    def adicionar_nota(self, nota):
        if not isinstance(nota, (int, float)):
            raise ValueError("A nota deve ser um número.")
        self.__notas.append(nota)

    def obter_nome(self):
        return self.__nome

    def obter_notas(self):
        return self.__notas

    def media_notas(self):
        return sum(self.__notas) / len(self.__notas) if self.__notas else 0

    def situacao(self):
        return "Aprovado" if self.media_notas() >= 6 else "Reprovado"


class Turma:
    def __init__(self):
        self.__alunos = []

    def adicionar_aluno(self, aluno):
        if not isinstance(aluno, Aluno):
            raise TypeError("Deve ser um objeto da classe Aluno.")
        self.__alunos.append(aluno)

    def obter_alunos(self):
        return self.__alunos

    def remover_aluno(self, nome):
        aluno = self.aluno_por_nome(nome)
        if aluno:
            self.__alunos.remove(aluno)

    def aluno_por_nome(self, nome):
        for aluno in self.__alunos:
            if aluno.obter_nome() == nome:
                return aluno
        return None

    def media_notas(self):
        total_notas = sum(aluno.media_notas() for aluno in self.__alunos)
        return total_notas / len(self.__alunos) if self.__alunos else 0

    def alunos_acima_da_media(self):
        media_turma = self.media_notas()
        return [aluno for aluno in self.__alunos if aluno.media_notas() > media_turma]