from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adicionar_aluno/', views.adicionar_aluno, name='adicionar_aluno'),
    path('adicionar_nota/', views.adicionar_nota, name='adicionar_nota'),
    path('grafico/<str:aluno_nome>/', views.grafico_comparacao, name='grafico_comparacao'),
    path('remover_aluno/<str:aluno_nome>/', views.remover_aluno, name='remover_aluno'),
]
