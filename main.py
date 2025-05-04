from mdl import MDL
from problemas.lago_congelado import Lago
from problemas.carro import Carro

if __name__ == "__main__":
  ambiente = Lago()
  print(ambiente)

  mdl = MDL(ambiente)

  print("Calculando valores...")

  V, PI = mdl.calcular_valores()

  print("\nImprimindo Valores por estado:")
  print(ambiente.imprimir_valor(V))
  print("\nImprimindo Polítca ótima por estado:")
  print(ambiente.imprimir_politica(PI))

  print("\nIniciando simulação:")
  ambiente.simulacao(PI)