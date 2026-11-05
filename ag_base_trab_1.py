

# Indivíduo:

# para cada parte (x e y):
#   como os valores são multiplicados por 1000 para remover as casas decimais, facilitando o armazenamento e conversão, devemos escolher uma quantidade de bits compatível

#   valores entre [-10000, 10000]

#   13 bits para valor: 2^13 = faixa [-8129, 8192]
#   14 bits para valor: 2^14 = faixa [-16384, 16384] -> sobra valores

#   * 14 bits magnitude
#   * 1 sinal
#   * primeiro, gerar valores aleatórios de -[10, 10];
#   * ve o sinal, armazena no primeiro indice;
#   * pega o absoluto e converte
#   * ajusta precisao para 3 casas; depois multiplica por 1000.
#   * ---> bin para decimal -> bit 0 = sinal, converte os outros 14, divide por 1000.

# serão duas partes de 15 bits, então:
#   * genoma[0] = sinal x
#   * genoma[1-14] = valor x
#   * genoma[15] = sinal y
#   * genoma[16-30] valor y


#Início do programa

# Importações
import csv
import math
import os
import random
from decimal import Decimal

import matplotlib.pyplot as plt

# ## Função de tratar as partes do indivíduo
# Código que recebe o número aleatório com 3 casas decimais de cada uma das duas partes do indivíduo.
# Primeiro verifica o sinal e armazena o valor 0 para positivo e 1 para negativo.
# Com o sinal armazenado, é pego o valor absoluto (módulo) e multiplicado por 1000 para remover a vírgula.
# Em seguida, é convertido para uma string binária de 14 bits, que logo é percorrida e convertido cada bit para inteiro e armazenado na parte.

def trata_parte(parte_decimal):
  parte = []

  if(parte_decimal > 0):
    sinal = 0
  else:
    sinal = 1

  magnitude_decimal = round(abs(parte_decimal) * 1000) # comentario

  # significado agora armazena um valor inteiro, que após conversão
  #     deve ser dividido por 1000 e individuo[0] seu sinal

  magnitude_binaria = format(magnitude_decimal, "014b")

  # coloca o sinal
  parte = [sinal]

  # percorre a conversao em string binaria e converte cada bit em inteiro
  #   inclui no vetor parte ## ficará com parte[0] = sinal e parte[1-14] = maginitude
  for bit in magnitude_binaria:
    parte.append(int(bit))

  return parte

# Geração de parte sorteia um valor entre o intervalo definido na atribuição do trabalho [-10, 10], arredonda para 3 casas decimais e converte para binário em um array de 15 bits, sendo eles parte[0] = sinal, e parte[1-14] sua magnitude.

# Para evitar representação decimal, a magnitude gerada foi multiplicada por 1000 e deve ser tratada após a conversão para decimal novamente.


def gerar_parte():
  parte_decimal = round(random.uniform(-10, 10), 3)
  parte_binaria = trata_parte(parte_decimal)

  # Descomentar para TESTE 1.0
  # return parte_binaria, parte_decimal

  return parte_binaria

# Criação de indivíduo consiste em criar as duas partes juntá-las

def cria_individuo():
    # Descomentar para TESTE 1.0
    # parte_x, antes_x = gerar_parte()
    # parte_y, antes_y = gerar_parte()

    # return individuo, antes_x, antes_y


    parte_x = gerar_parte()
    parte_y = gerar_parte()

    individuo = parte_x + parte_y

    return individuo

## Conversão dos valores, retorna x e y

# Basicamente separa em partes, converte o array para string, converte para decimal de forma nativa e corrige a maginitude, dividindo por mil e verificando o sinal de cada parte

def converter(individuo):
  sinal_x = individuo[0]
  sinal_y = individuo[15]
  magnitude_x = conv_mag(individuo[1:15]) / 1000
  magnitude_y = conv_mag(individuo[16:30]) / 1000

  if sinal_x == 1:
    magnitude_x = -magnitude_x

  if sinal_y == 1:
    magnitude_y = -magnitude_y

  return magnitude_x, magnitude_y

def conv_mag(magnitute):
  string_binaria = "".join(str(bit) for bit in magnitute)
  numero_decimal = int(string_binaria, 2)
  return numero_decimal

## Criar população de indivíduos

def cria_populacao(tamanho_populacao):
  return [cria_individuo() for _ in range(tamanho_populacao)]

## Função de fitness

def fitness(individuo):
  x, y = converter(individuo)

  #penalizacao caso a mutaçao gere fora do intervalo
  #if abs(x) > 10 or abs(y) > 10:
   # return -1000 # menor valor de f(x, y) obtido é -365, retornando -1000 para penalizar um indivíduo fora do intevalo

  # penalização proporcional ao excesso,exemplo: para casos no qual o fitness seja 10.001, não ser tão penalizado
  if abs(x) > 10 or abs(y) > 10:
    excesso_x = max(0, abs(x) - 10)
    excesso_y = max(0, abs(y) - 10)
    penalidade = 10 * (excesso_x + excesso_y)
    return -penalidade

  else:
    z = 5 + (3 * x) - (4 * y) - (x ** 2) + (x * y) - (y ** 2)
    z = round(z, 3)
  return z

## Elitismo
# Pega os 1% melhores individuos da geração atual e passa automaticamente para a próxima geração

# Retorna população sem a elite, para cruzar e mutar
# Retorna a elite para passar para a próxima

def elitismo(populacao, percentual=0.01):
  # key=lambda x: x[1] ordena pelo segundo parametro (valores de fitness)
  # ordenacao do pior para o melhor
  populacao_ordenada = sorted(populacao, key=lambda x: x[1], reverse=False)

  tamanho_elite = max(1, math.ceil(len(populacao) * percentual))

  elite = populacao_ordenada[-tamanho_elite:]
  populacao_sem_elite = populacao_ordenada[:-tamanho_elite]
  return populacao_sem_elite, elite

## Seleção de pais (ranking)
# P(i) = (2 * i) / (n * (n + 1))

def selecao_ranking(populacao):
  n = len(populacao)

  probabilidades = []

  for it in range(n):
    i = it + 1
    p_i = (2 * i) / (n * (n + 1))
    probabilidades.append(p_i)

  roleta_acumulada = []
  acumulado = 0.0
  for probabilidade in probabilidades:
    acumulado += probabilidade
    roleta_acumulada.append(acumulado)

  roleta_acumulada[-1] = 1.0

  r = random.random()
  for i, limite in enumerate(roleta_acumulada):
    if r <= limite:
      return populacao[i][0]

## Cruzamento

# Se o valor sorteado for maior que 0.5, o gene do Filho 1 vem do Pai 1 (e o do Filho 2 vem do Pai 2).

# Se for menor, os papéis se invertem: o gene do Filho 1 vem do Pai 2 (e o do Filho 2 vem do Pai 1)

def cruzamento(pai1, pai2, TAXA_CRUZAMENTO):
  chance = random.random()
  if chance < TAXA_CRUZAMENTO:
    filho1 = []
    filho2 = []

    for i in range(29):
      if random.random() < 0.5:
        filho1.append(pai1[i])
        filho2.append(pai2[i])
      else:
        filho1.append(pai2[i])
        filho2.append(pai1[i])
    return filho1, filho2

  else:
    return pai1[:], pai2[:]


## Mutação

# Percorre o indivíduo a para cada bit ve se a probabiliade deu menor que a taxa definida, se sim, inverteo bit

def mutacao(individuo, TAXA_MUTACAO):
  for i in range(len(individuo)):
    if random.random() < TAXA_MUTACAO:
      individuo[i] = 1 - individuo[i] # resultado = 1 - 1 // resultado = 1 - 0 ## inversão fácil
  return individuo

#### Bancada de teste:
# Testes se o indivíduo está sendo gerado novamente

# TESTE 1.0 descomentar retorno nas funções:
# Objetivo: observar se a conversão de valores x e y para o indivíduo funcionou
#individuo, antes_x, antes_y = cria_individuo()
#print(f"Valores criados: x = {antes_x}, y = {antes_y}")
#print(f"Individuo: {individuo}")
#print(f"Pós-conversão: {converter_x_y(individuo)}")
########################################################


def monta_diretorio(POPULACAO_TAMANHO, GERACOES, TAXA_MUTACAO, TAXA_CRUZAMENTO):
  taxa_cruzamento = Decimal(str(TAXA_CRUZAMENTO))

  diretorio = f"P-{POPULACAO_TAMANHO}_G-{GERACOES}_M-{TAXA_MUTACAO}_C-{TAXA_CRUZAMENTO}"
  return diretorio

# Função para realizar a plotagem do gráfico de cada iteração

def plotar_populacao(populacao, geracao, diretorio):
    x_pop = []
    y_pop = []

    # Converte todos os indivíduos para coordenadas (x, y)
    for individuo in populacao:
        x, y = converter(individuo)
        x_pop.append(x)
        y_pop.append(y)

    # Encontra o melhor indivíduo da geração
    melhor_individuo = max(populacao, key=fitness)
    melhor_x, melhor_y = converter(melhor_individuo)

    # Cria o gráfico
    fig, ax = plt.subplots(figsize=(7, 5))

    ax.scatter(x_pop, y_pop, label='População')

    # Destaca o melhor indivíduo
    ax.scatter(
        melhor_x,
        melhor_y,
        s=150,
        marker='*',
        label='Melhor indivíduo'
    )

    # Ponto vermelho que índica o valor ótimo
    ax.scatter( 0.6667, -1.6667, s=30, color='red', label='Ponto ótimo' )

    # Representação da região permitida pelo domínio [-10, 10]
    ax.plot( [-10, 10, 10, -10, -10], [-10, -10, 10, 10, -10], color='green', label='Domínio permitido' )

    # Define o espaço de busca
    ax.set_xlim(-17, 17)
    ax.set_ylim(-17, 17)

    # Definição dos rótulos
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'População - Geração {geracao}')

    ax.grid(True)
    ax.legend(loc = 'lower right')

    # Exibe o gráfico
    diretorio_geracoes = f"./plotagem/{diretorio}/geracoes"
    os.makedirs(diretorio_geracoes, exist_ok=True)
    plt.savefig(f"{diretorio_geracoes}/geracao{geracao}.png", dpi=300, bbox_inches="tight")

# Algoritmo Genético!

def ag():
  
  POPULACAO_TAMANHO = int(input("Digite o tamanho da população: "))
  GERACOES = int(input("Digite a quantidade de geracoes da população: "))
  TAXA_MUTACAO = float(input("Digite a taxa de mutação: "))
  TAXA_CRUZAMENTO = float(input("Digite a taxa de cruzamento: "))

  diretorio = monta_diretorio(POPULACAO_TAMANHO, GERACOES, TAXA_MUTACAO, TAXA_CRUZAMENTO)

  populacao = cria_populacao(POPULACAO_TAMANHO)

  historico = []

# for individuo in populacao:
#   print(converter(individuo))

  for geracao in range(GERACOES):
    # primeiro calculo de fitness
    valores_fitness = [fitness(individuo) for individuo in populacao]
    nova_populacao = []

    # NOTA: talvez eu possa até ordenar ela antes de enviar e usar para mandar para o csv!!
    # elitismo -> separa o 1% melhor de cada geração
    geracao_atual = list(zip(populacao, valores_fitness))

    populacao_filtrada, elite = elitismo(geracao_atual)

    populacao_com_elite = populacao_filtrada + elite

    nova_populacao.extend([individuo for individuo, fitness in elite])



    # cruzar (metade da populacao porque tem pai 1 e pai 2) -> ranking (uniforme (taxa de 50% para para cada bit))
       # mutar os novos -> inversao do bit
    while len(nova_populacao) < POPULACAO_TAMANHO:
      pai1 = selecao_ranking(populacao_filtrada)
      pai2 = selecao_ranking(populacao_filtrada)
      filho1, filho2 = cruzamento(pai1, pai2, TAXA_CRUZAMENTO)
      nova_populacao.extend([mutacao(filho1, TAXA_MUTACAO), mutacao(filho2, TAXA_MUTACAO)])
      nova_populacao = nova_populacao[:POPULACAO_TAMANHO] # isso é para não aumentar cada população

    populacao = nova_populacao

    plotar_populacao(populacao, geracao+1, diretorio)
    

    valores_fitness = [fitness(individo) for individo in populacao]
    fitness_medio = sum(valores_fitness) / len(valores_fitness)
    melhor_fitness = max(valores_fitness)
    melhor_index = valores_fitness.index(melhor_fitness)
    melhor_individuo = populacao[melhor_index]
    melhor_x, melhor_y = converter(melhor_individuo)

    historico.append({
        "geracao": geracao+1,
        "fitness_medio": round(fitness_medio, 3),
        "melhor_fitness": melhor_fitness,
        "melhor_x": melhor_x,
        "melhor_y": melhor_y
    })

    #print(
    #f"Geração {geracao}: "
    #f"Fitness Médio = {fitness_medio:.3f} | "
    #f"Melhor Fitness = {melhor_fitness:.3f} | "
    #f"Melhor X = {melhor_x:.3f} | "
    #f"Melhor Y = {melhor_y:.3f} | "
    #f"Tamanho população = {len(populacao)}"
    #)

  melhor_index = valores_fitness.index(max(valores_fitness))
  melhor_solucao = populacao[melhor_index]

  print(f"Melhor solução = {melhor_solucao}")
  print(f"Melhor fitness = {fitness(melhor_solucao)}")

  return historico, diretorio

# execuçao
#ag()

## Execução e Plotagem de Histórico

historico_execucao, diretorio = ag()

nome_arquivo_csv = f"./plotagem/{diretorio}/resultado.csv"
elementos_csv = ["geracao", "fitness_medio", "melhor_fitness", "melhor_x", "melhor_y"]

# gravação em um arquivo .csv
with open(nome_arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo_csv:
    writer = csv.DictWriter(arquivo_csv, fieldnames=elementos_csv)
    writer.writeheader()
    writer.writerows(historico_execucao)

# dados necessários para gerar o gráfico
geracoes = [registro["geracao"] for registro in historico_execucao]
fitness_medios = [registro["fitness_medio"] for registro in historico_execucao]


plt.figure(figsize=(10, 5))
plt.plot(geracoes, fitness_medios, label="Fitness Médio", color="b", linewidth=1.5)

plt.title("Gráfico do Fitness Médio por Geração")
plt.xlabel("Geração")
plt.ylabel("Fitness Médio")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()

plt.savefig(f"./plotagem/{diretorio}/fitness_medio.png", dpi=300, bbox_inches="tight")
plt.show()