import random
import time
import os             # operation system (funções relacionados ao s.o.)
from colorama import Fore, Back, Style

temp = "🐸🐸🦣🦣🦎🦎🐯🐯🐧🐧🦋🦋🐠🐠🦀🦀"
figuras = list(temp)

print("="*40)
print("Jogo da Memória")
print("="*40)

nome_jogador = input("Informe seu Nome: ")
total_pontos = 0

jogo = []
apostas = []

def preenche_matriz():
  for i in range(4):
    jogo.append([])
    apostas.append([]) 
    for _ in range(4):
      num = random.randint(0, len(figuras)-1)
      jogo[i].append(figuras[num])
      apostas[i].append("🟥")
      figuras.pop(num)

def mostra_tabuleiro():
  os.system("cls")          # limpa a tela
  print("   1   2   3   4")
  for i in range(4):
    print(f"{i+1}", end="")
    for j in range(4):
      print(f" {jogo[i][j]} ", end="")
    print("\n")  

  print("Memorize a posição dos bichos...") 
  time.sleep(2)

  print("Contagem regressiva: ", end="")
  for i in range(10, 0, -1):
    print(i, end=" ", flush=True)
    time.sleep(1)

  os.system("cls")

def mostra_apostas():
  os.system("cls")          # limpa a tela
  print("   1   2   3   4")
  for i in range(4):
    print(f"{i+1}", end="")
    for j in range(4):
      print(f" {apostas[i][j]} ", end="")
    print("\n")

preenche_matriz()
mostra_tabuleiro()
tempo_inicial = time.time()

def faz_aposta(num):
  while True:
    mostra_apostas()
    posicao = input(f"{num}ª Coordenada (2 números: linha e coluna): ")
    if len(posicao) != 2:
      print("Informe um dezena, por exemplo, 12, 24, 31, ...")
      time.sleep(2)
      continue 
    x = int(posicao[0])-1
    y = int(posicao[1])-1
    try:
      if apostas[x][y] == "🟥":
        apostas[x][y] = jogo[x][y]
        break
      else:
        print("Coordenada já apostada... escolha outra")
        time.sleep(2)
    except IndexError:
      print("Coordenada Inválida... repita")
      time.sleep(2)
  return x, y    

def verifica_tabuleiro():
  faltam = 0
  for i in range(4):
    for j in range(4):
      if apostas[i][j] == "🟥":
        faltam += 1
  return faltam

while True:
  x1, y1 = faz_aposta(1)
  x2, y2 = faz_aposta(2)
  mostra_apostas()

  if apostas[x1][y1] == apostas[x2][y2]:
    print("Parabéns! Você acertou! 🫠")
    total_pontos += 10
    contador = verifica_tabuleiro()
    if contador == 0:
      print("Parabéns! Você Venceu 🏆🏆")
      break
    else:
      print(f"Faltam {contador/2} bicho(s) para descobrir")
      time.sleep(2)
  else:
    print("Errou... Tente novamente. 😠")
    total_pontos -= 5
    time.sleep(2)
    apostas[x1][y1] = "🟥"
    apostas[x2][y2] = "🟥"
    sair = input("Deseja sair (S/N): ").upper()
    if sair == "S":
      break

tempo_final = time.time()
duracao_jogo = tempo_final - tempo_inicial

print()
print("*"*40)
print(f"Jogador: {nome_jogador}")
print(f"Total de Pontos: {total_pontos}")
print(f"Duração do Jogo: {int(duracao_jogo)} segundos")
print("*"*40)

#----- Rotina para salvar os dados no arquivo ranking.txt
dados = []
if os.path.isfile("ranking.txt"):
  with open("ranking.txt", "r") as arq:
    dados = arq.readlines()

dados.append(f"{nome_jogador};{total_pontos};{int(duracao_jogo)}\n")

with open("ranking.txt", "w") as arq:
  for dado in dados:
    arq.write(dado)

# ---- Rotina para classificar (Ranking)
nomes = []
pontos = []
tempos = []

for dado in dados:
  partes = dado.split(";")
  nomes.append(partes[0])
  pontos.append(int(partes[1]))
  tempos.append(int(partes[2])*-1)

# coloca as 3 listas em ordem (zipando as 3 listas)
juntas = sorted(zip(pontos, tempos, nomes), reverse=True)
# volta a separar as listas (faz um "unzip")
pontos2, tempos2, nomes2 = zip(*juntas)

print()
print("="*43)
print("---------< RANKING DOS JOGADORES >---------")
print("="*43)
print("Nº Nome do Jogador.........: Pontos Tempo.:")
        
for num, (nome, ponto, tempo) in enumerate(zip(nomes2, pontos2, tempos2), start=1):
  if nome == nome_jogador and ponto == total_pontos:    
    print(Fore.RED + f"{num:2d} {nome:25s}   {ponto:2d}   {tempo*-1:3d} seg", end="")
    print(Style.RESET_ALL)
  else:
    print(f"{num:2d} {nome:25s}   {ponto:2d}   {tempo*-1:3d} seg")
