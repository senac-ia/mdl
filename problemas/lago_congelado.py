import numpy as np
from problemas.ambiente import Ambiente 

# Problem Description:

# Imagine an agent in a frozen lake. The lake is divided into a 4x4 grid of squares. The agent's goal is to navigate from the starting point (S) in the top-left corner to the goal (G) in the bottom-right corner. The agent needs to avoid holes (H) in the ice, and every square has a probability of being slippery. If the agent slips, it moves to an adjacent square not in the intended direction.
class Lago(Ambiente):
  def __init__(self):
    self.estados = np.array([
      "🚩", "🧊", "🧊", "🧊", 
      "🧊", "🕳️", "🧊", "🕳️", 
      "🧊", "🧊", "🧊", "🕳️", 
      "🕳️", "🧊", "🧊", "🏁"
    ])
    self.acoes = np.array(["☝️", "👇", "👈", "👉"])
    
    # Discount Factor (𝛾): The discount factor is a value between 0 and 1. For this example, we'll use 𝛾 = 0.99.
    # Transitions (T): The agent has an 80% chance of moving in the intended direction and a 20% chance of slipping (moving to an adjacent square not in the intended direction). If the agent moves off the grid or into a hole, it is returned to the starting position.
  def T(self, estado, acao):
    # se está em um buraco ou final, fica lá
    if self.estados[estado] in ["🕳️", "🏁"]:
      return [(estado, 1.0)]

    x, y = estado % 4, estado // 4

    proximos_estados = [
      (x, max(y - 1, 0)),  # cima
      (x, min(y + 1, 3)),  # baixo
      (max(x - 1, 0), y),  # esquerda
      (min(x + 1, 3), y)  # direita
    ]

    if acao < 0 or acao >= len(self.acoes):
      raise ValueError("Ação inválida")

    # estado da ação tem probabilidade de 80%
    (next_x, next_y) = proximos_estados[acao]
    proximo_estado_acao = next_y * 4 + next_x
    transicoes = [(proximo_estado_acao, 0.8)]

    # outros estados têm 20% ao todo
    estados_alternativos = list(proximos_estados)
    del estados_alternativos[acao]
    prob_escorregar = 0.2 / len(estados_alternativos)

    for (next_x, next_y) in estados_alternativos:
      proximo_estado_escorregao = next_y * 4 + next_x
      transicoes.append((proximo_estado_escorregao, prob_escorregar))

    return transicoes

  # Rewards (R): The agent receives a reward of -0.04 for each step, -1 for falling into a hole, and +1 for reaching the goal.
  def R(self, estado, acao, proximo_estado):
    estado_valor = self.estados[proximo_estado]
    if estado_valor in ["🧊","🚩"]:
      return -0.04
    elif estado_valor == "🕳️":
      return -1.00
    elif estado_valor == "🏁":
      return +1.00
    else:
      raise ValueError("Estado inválido: " + estado_valor)

  def __str__(self):
    e = self.estados
    lago = "🚩 é o início, 🧊 é um congelado, 🕳️ é buraco, e 🏁 é o resultado\n"
    for i in range(0, 16, 4):
      lago += (f"|\t{e[i]}\t|\t{e[i+1]}\t|\t{e[i+2]}\t|\t{e[i+3]}\t|\n")
    return lago

  def imprimir_valor(self, V):
    valor_texto = ""
    for i in range(0, 16, 4):
       valor_texto += "|\t%.2f\t|\t%.2f\t|\t%.2f\t|\t%.2f\t|\n" % (V[i], V[i + 1], V[i + 2], V[i + 3])
    return valor_texto

  def imprimir_politica(self, politica):
    poltica_texto = ""
    ps = [] # política com símbolos
    for estado in politica:
      ps.append(self.acoes[estado])

    for i in range(0, 16, 4):
      for j in range(0,4):
        if self.estados[i+j] in ["🕳️", "🏁"]: ps[i+j] = self.estados[i+j]
        
      poltica_texto += f"|\t{ps[i]}\t|\t{ps[i+1]}\t|\t{ps[i+2]}\t|\t{ps[i+3]}\t|\n"
    return poltica_texto

  def simulacao(self, PI):
    estado = -1
    buraco = True
    while (estado < 0 or estado > 15 or buraco):
      estado = input("Escolha um estado [0-15] em que há movimentos possíveis: ")
      estado = int(estado)
      buraco = self.estados[estado] in ["🕳️", "🏁"]
  
    print(f"Se uma pessoa for jogada no estado {estado}, qual caminho fazer:")
    while not estado == 15:
      acao = PI[estado]
      estado = self.T(estado, acao)[0][0]
      print(self.acoes[acao], estado)