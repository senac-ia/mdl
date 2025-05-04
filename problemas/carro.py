import numpy as np
from problemas.ambiente import Ambiente 
import random

class Carro(Ambiente):
  def __init__(self):
    self.estados = np.array(["🥶", "🥵", "🔥"])
    self.acoes = np.array(["🐌", "🐇"])
    
  def T(self, estado, acao):
    estado_simb = self.estados[estado]
    acao_simb = self.acoes[acao] 
    probabilidade_transicao = []
    if estado_simb == "🥶":
      if acao_simb == "🐌":
        probabilidade_transicao.append((0, 1.0))
      else:
        probabilidade_transicao.append((0, 0.5))
        probabilidade_transicao.append((1, 0.5))
    elif estado_simb == "🥵":
      if acao_simb == "🐌":
        probabilidade_transicao.append((0, 0.5))
        probabilidade_transicao.append((1, 0.5))
      else:
        probabilidade_transicao.append((2, 1.0))
    elif estado_simb == "🔥":
      probabilidade_transicao.append((2, 1.0))

    return probabilidade_transicao

  def R(self, estado, acao, proximo_estado):
    if estado == "🔥":
      return -2
    else:
      if estado  == "🐌":
        return +1
      else:
        return +2

  def __str__(self):
    e = self.estados
    texto = "Estados:\n"
    for i in range(0, len(self.estados)):
      texto += (f"|\t{e[i]}\t|\n")
    return texto

  def imprimir_valor(self, V):
    valor_texto = ""
    for i in range(0, len(self.estados)):
       valor_texto += "|\t%s\t|\t%.2f\t|\n" % (self.estados[i],V[i])
    return valor_texto

  def imprimir_politica(self, politica):
    poltica_texto = ""
    ps = [] # política com símbolos
    for estado in politica:
      ps.append(self.acoes[estado])

    for i in range(0, len(self.estados)):
      poltica_texto += f"|\t%s\t|\t%s\t|\n" % (self.estados[i], ps[i])
    return poltica_texto

  def simulacao(self, PI):
    n = input("Escolha um tamanho de caminho em KM inteiro: ")
    n = int(n)
    estado_atual = 0 # "🥶"
    lista_estados = []
    lista_acoes = []

    for i in range(n):
      lista_estados.append(estado_atual)
      melhor_acao = PI[estado_atual]
      lista_acoes.append(melhor_acao)

      # sorteando os próximos estados
      prox_estados = self.T(estado_atual, melhor_acao)
      #https://acervolima.com/metodo-random-choices-em-python/
      estados = []
      probs = []
      for (estado,prob) in prox_estados:
        estados.append(estado)
        probs.append(prob)
      estado_atual = random.choices(estados, weights=probs)[0]

    saida = "KM, Estado, Ação:\n"
    for i in range(n):
      saida += "|%s" % (i)
    saida += "\n"
    for i in range(n):
      saida += "|%s" % (self.estados[lista_estados[i]])
    saida += "\n"
    for i in range(n):
      saida += "|%s" % (self.acoes[lista_acoes[i]])
    saida += "\n"

    print(saida)