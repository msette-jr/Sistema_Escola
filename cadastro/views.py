from django.shortcuts import render, redirect, get_object_or_404
import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponse
import csv
from .models import Aluno, Turma

def exportar_csv(request):
    """Exporta a lista de alunos e suas notas para um arquivo CSV."""
    # Configuração da resposta HTTP
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alunos.csv"'

    # Criação do writer CSV
    writer = csv.writer(response)
    writer.writerow(['Nome', 'Notas', 'Média', 'Situação'])  # Cabeçalho do CSV

    # Escrever os dados dos alunos no CSV
    for aluno in Aluno.objects.all():
        media_aluno = aluno.media_notas()
        if media_aluno >= 7:
            situacao = "Aprovado"
        elif media_aluno >= 5:
            situacao = "Recuperação"
        else:
            situacao = "Reprovado"

        writer.writerow([
            aluno.nome,
            ', '.join(map(str, aluno.notas)),  # Convertendo as notas para string separadas por vírgula
            f"{media_aluno:.2f}",  # Formatação da média com duas casas decimais
            situacao
        ])

    return response


    return response

def index(request):
    """ Exibe a página inicial com a lista de alunos, a média da turma e a situação de cada aluno. """
    alunos = Aluno.objects.all()
    turma = Turma.objects.first()
    media_turma = turma.media_notas() if turma else 0

    alunos_com_dados = []
    for aluno in alunos:
        media_aluno = aluno.media_notas() if aluno.notas else 0
        if media_aluno >= 7:
            situacao = "Aprovado"
        elif media_aluno >= 5:
            situacao = "Recuperação"
        elif aluno.notas:
            situacao = "Reprovado"
        else:
            situacao = "Sem notas"
        alunos_com_dados.append({
            'nome': aluno.nome,
            'notas': aluno.notas,
            'media': media_aluno,
            'situacao': situacao
        })

    return render(request, 'cadastro/index.html', {
        'alunos': alunos_com_dados,
        'media_turma': media_turma
    })

def adicionar_aluno(request):
    """ Adiciona um novo aluno à turma e ao banco de dados Django. """
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            if Aluno.objects.filter(nome=nome.strip()).exists():
                return render(request, 'cadastro/adicionar_aluno.html', {'error': 'O aluno já existe.'})
            aluno = Aluno.objects.create(nome=nome.strip(), notas=[])
            turma, _ = Turma.objects.get_or_create()
            turma.alunos.add(aluno)
            return redirect('index')
        else:
            return render(request, 'cadastro/adicionar_aluno.html', {'error': 'O nome do aluno não pode estar vazio.'})
    return render(request, 'cadastro/adicionar_aluno.html')

def adicionar_nota(request):
    """ Adiciona uma nota a um aluno e salva no banco de dados Django. """
    alunos = Aluno.objects.all()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        nota = request.POST.get('nota')
        if nome and nota:
            aluno = Aluno.objects.filter(nome=nome.strip()).first()
            if aluno:
                try:
                    nota = float(nota)
                    if 0 <= nota <= 10:
                        aluno.notas.append(nota)
                        aluno.save()
                        return redirect('index')
                    else:
                        raise ValueError("Nota fora do intervalo permitido (0-10).")
                except ValueError:
                    return render(request, 'cadastro/adicionar_nota.html', {
                        'alunos': alunos,
                        'error': 'A nota deve ser um número válido entre 0 e 10.'
                    })
            else:
                return render(request, 'cadastro/adicionar_nota.html', {
                    'alunos': alunos,
                    'error': 'Aluno não encontrado.'
                })
        else:
            return render(request, 'cadastro/adicionar_nota.html', {
                'alunos': alunos,
                'error': 'Os campos nome e nota são obrigatórios.'
            })
    return render(request, 'cadastro/adicionar_nota.html', {'alunos': alunos})

def remover_aluno(request, nome):
    """ Remove um aluno da turma e do banco de dados Django """
    aluno = Aluno.objects.filter(nome=nome.strip()).first()
    if aluno:
        aluno.delete()
    return redirect('index')

def grafico_comparacao(request, aluno_nome):
    """ Exibe um gráfico comparando a média do aluno com a média da turma. """
    aluno = get_object_or_404(Aluno, nome=aluno_nome.strip())
    turma = Turma.objects.first()

    media_aluno = aluno.media_notas() if aluno.notas else 0
    media_turma = turma.media_notas() if turma and turma.alunos.exists() else 0

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(['Média do Aluno', 'Média da Turma'], [media_aluno, media_turma], color=['blue', 'green'])
    ax.set_ylabel('Média')
    ax.set_title(f'Comparação da Média do Aluno: {aluno.nome}')
    ax.set_ylim(0, 10)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'cadastro/grafico.html', {
        'graphic': graphic,
        'aluno': aluno,
        'media_aluno': media_aluno,
        'media_turma': media_turma
    })


