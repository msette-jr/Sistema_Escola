from django.shortcuts import render, redirect
from cadastro.backend import Aluno, Turma  # Importação correta do backend
import matplotlib.pyplot as plt
import io
import base64

# Instância única da turma
turma = Turma()

def index(request):
    """ Exibe a página inicial com a lista de alunos e a média da turma. """
    alunos = [
        {
            'nome': aluno.obter_nome(),
            'notas': aluno.obter_notas(),
            'media': aluno.media_notas(),
            'situacao': aluno.situacao()  # Mostra se o aluno foi aprovado ou reprovado
        }
        for aluno in turma.obter_alunos()
    ]
    media_turma = turma.media_notas()
    return render(request, 'cadastro/index.html', {'alunos': alunos, 'media_turma': media_turma})

def adicionar_aluno(request):
    """ Adiciona um novo aluno à turma. """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            novo_aluno = Aluno(nome.strip())
            turma.adicionar_aluno(novo_aluno)
            return redirect('index')
        else:
            return render(request, 'cadastro/adicionar_aluno.html', {'error': 'O nome do aluno não pode estar vazio.'})
    return render(request, 'cadastro/adicionar_aluno.html')

def adicionar_nota(request):
    """ Adiciona uma nota a um aluno existente. """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        nota = request.POST.get('nota')
        if nome and nota:
            aluno = turma.aluno_por_nome(nome.strip())
            if aluno:
                try:
                    aluno.adicionar_nota(float(nota))
                    return redirect('index')
                except ValueError:
                    return render(request, 'cadastro/adicionar_nota.html', {
                        'alunos': turma.obter_alunos(),
                        'error': 'A nota deve ser um número válido.'
                    })
            else:
                return render(request, 'cadastro/adicionar_nota.html', {
                    'alunos': turma.obter_alunos(),
                    'error': 'Aluno não encontrado.'
                })
        else:
            return render(request, 'cadastro/adicionar_nota.html', {
                'alunos': turma.obter_alunos(),
                'error': 'Os campos nome e nota são obrigatórios.'
            })
    return render(request, 'cadastro/adicionar_nota.html', {'alunos': turma.obter_alunos()})

def remover_aluno(request, aluno_nome):
    """ Remove um aluno da turma """
    aluno_nome = aluno_nome.strip()
    aluno = turma.aluno_por_nome(aluno_nome)
    if aluno:
        turma.remover_aluno(aluno_nome)
    return redirect('index')

def grafico_comparacao(request, aluno_nome):
    """ Exibe um gráfico comparando a média do aluno com a média da turma. """
    aluno = turma.aluno_por_nome(aluno_nome.strip())
    if not aluno:
        return redirect('index')

    media_turma = turma.media_notas()
    media_aluno = aluno.media_notas()

    # Criar o gráfico com Matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(['Aluno', 'Turma'], [media_aluno, media_turma], color=['blue', 'green'])
    ax.set_ylabel('Média')
    ax.set_title(f'Comparação Média: {aluno_nome}')
    ax.set_ylim(0, 10)

    # Converter gráfico para imagem
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'cadastro/grafico.html', {'graphic': graphic, 'aluno': aluno})
