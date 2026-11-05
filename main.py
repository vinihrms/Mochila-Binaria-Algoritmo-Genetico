# definição de constantes
POPULACAO_TAMANHO = 100
GERACOES = 70
TAXA_MUTACAO = 0.03
TAXA_CRUZAMENTO = 0.6
TAXA_ELITISMO = 0.01

# definição do que se trata da mochila
CAPACIDADE = 105
beneficio_itens = [3, 42, 5, 48, 42, 13, 3, 20, 12, 37]
peso_itens = [2, 35, 13, 29, 9, 25, 2, 14, 4, 17]

itens = list(zip(beneficio_itens, peso_itens))

# será o teste inicial com o primeiro arquivo -> isso vai ficar dinamico depois
N_ITENS = len(itens)

import random
import math

# função para criar mochila aleatória
def cria_mochila(n_itens):
    mochila = []
    
    for _ in range(n_itens):
        chance = random.random()
        if chance > 0.5:
            mochila.append(0)
        else:
            mochila.append(1)
    
    return mochila  

def cria_populacao(tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        populacao.append(cria_mochila(N_ITENS))
        
    return populacao

def beneficio_peso(populacao):
    beneficios = []
    pesos = []
    
    for mochila in populacao :
        peso = 0
        beneficio = 0
        for i, selecionado in enumerate(mochila):
            if(selecionado == 1):
                beneficio += beneficio_itens[i]
                peso += peso_itens[i]
        beneficios.append(beneficio)
        pesos.append(peso)

    mochilas_calculadas = list(zip(beneficios, pesos))
    
    return mochilas_calculadas

def fitness(beneficio, peso):
    if peso <= CAPACIDADE:
        return beneficio
    
    # aplicando penalização para mochilas excedentes saírem logo da geração
    excedente = peso - CAPACIDADE
    penalizacao = excedente * 10
    return beneficio - penalizacao

# cruzamento de um ponto (meio)
def cruzamento(mochila1, mochila2):
    chance = random.random()

    if(chance <= TAXA_CRUZAMENTO):
        corte = N_ITENS // 2
        filho1 = mochila1[:corte] + mochila2[corte:]
        filho2 = mochila2[:corte] + mochila1[corte:]
        return filho1, filho2
    
    return mochila1, mochila2

def mutacao(mochila):
    for i in range(len(mochila)):
        chance = random.random()
        if(chance <= TAXA_MUTACAO):
            mochila[i] = 1 - mochila[i]
    return mochila

# aqui tem que zipar acho a populacao com o um array armazenando todos os valores fitness
# deve receber pares de populacao e seu fitness
def elitismo(populacao_com_fitness, taxa=TAXA_ELITISMO):
    populacao_ordenada = sorted(populacao_com_fitness, key=lambda x: x[1], reverse=True)
    
    # usa o minímo para não permitir elite maior que a população
    tamanho_elite = min(math.ceil(len(populacao_ordenada) * taxa), len(populacao_ordenada))
    
    elite = populacao_ordenada[:tamanho_elite]
    populacao_sem_elite = populacao_ordenada[tamanho_elite:]
    return populacao_sem_elite, elite


# tem que vir o par (mochila, fitness)
def selecao_ranking(populacao):
    n = len(populacao)
    probabilidades = []
    for it in range(n):
        i = it + 1
        # P(i) = (2 * i) / (n * (n + 1))
        p_i = (2 * i) / (n * (n + 1))
        probabilidades.append(p_i)
        
    intervalo_chances = []
    acumulado = 0.0
    for probabilidade in probabilidades:
        acumulado += probabilidade
        intervalo_chances.append(acumulado)
    
    intervalo_chances[-1] = 1.0
    
    roleta = random.random()
    for i, chance in enumerate(intervalo_chances):
        if roleta <= chance:
            return populacao[i][0]
        
