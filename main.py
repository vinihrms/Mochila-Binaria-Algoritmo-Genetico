# definição de constantes
POPULACAO_TAMANHO = 1000
GERACOES = 30
TAXA_MUTACAO = 0.01
TAXA_CRUZAMENTO = 0.8
TAXA_ELITISMO = 0.1

# definição do que se trata da mochila

with open('./entradas/Mochila50.txt', 'r') as entrada:
    linhas = entrada.readlines()

CAPACIDADE = int(linhas[0].strip())
beneficio_itens = list(map(int, linhas[1].split()))
peso_itens = list(map(int, linhas[2].split()))

itens = list(zip(beneficio_itens, peso_itens))

# será o teste inicial com o primeiro arquivo -> isso vai ficar dinamico depois
N_ITENS = len(itens)

import math
import random

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

# remove itens que fazem com que a mochila exceda a capaciadade
# remove os de menores benefícios 
# isso otimizou MUITO para as mochilas maiores
def repara_mochila(mochila):
    peso_atual = sum(
        peso_itens[i] for i, selecionado in enumerate(mochila)
        if selecionado == 1
    )

    if peso_atual <= CAPACIDADE:
        return mochila

    selecionados = sorted(
        (i for i, selecionado in enumerate(mochila) if selecionado == 1),
        key=lambda i: beneficio_itens[i] / peso_itens[i]
    )

    for item_removido in selecionados:
        mochila[item_removido] = 0
        peso_atual -= peso_itens[item_removido]
        if peso_atual <= CAPACIDADE:
            break

    return mochila

def cria_populacao(tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        
        #populacao.append(cria_mochila(N_ITENS))

        # reparar mochila na criação
        populacao.append(repara_mochila(cria_mochila(N_ITENS)))
        
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
    
    return mochila1[:], mochila2[:]

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
        # P(i) = (2 * (n - i)) / (n * (n + 1))
        p_i = (2 * (n - it)) / (n * (n + 1))
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

def ag():
    populacao = cria_populacao(POPULACAO_TAMANHO)
    
    for geracao in range(GERACOES):
        
        mochilas_calculadas = beneficio_peso(populacao)
        
        valores_fitness = []
        
        for beneficio, peso in mochilas_calculadas:
            valores_fitness.append(fitness(beneficio, peso))
        
        geracao_atual = list(zip(populacao, valores_fitness))
        
        populacao_sem_elite, elite = elitismo(geracao_atual)
        
        # passa elite para frente já
        nova_pop = []
        nova_pop.extend([mochila for mochila, fitness in elite])
        
        # cruzamento
        while len(nova_pop) < POPULACAO_TAMANHO:
            pai1 = selecao_ranking(populacao_sem_elite)
            pai2 = selecao_ranking(populacao_sem_elite)
            filho1, filho2 = cruzamento(pai1, pai2)
            
            # testes com e sem reparar a mochila de mutacao
            nova_pop.extend([mutacao(filho1),mutacao(filho2)])
            #nova_pop.extend([repara_mochila(mutacao(filho1)),repara_mochila(mutacao(filho2))])
            
            
            nova_pop = nova_pop[:POPULACAO_TAMANHO] # isso é para não aumentar cada população

        populacao = nova_pop
        
        melhor_mochila, _ = max(
            zip(populacao, [fitness(*atributos) for atributos in beneficio_peso(populacao)]),
            key=lambda par: par[1]
        )
        atributos_melhor_mochila = beneficio_peso([melhor_mochila])[0]
        
        print(f"Geração: {geracao + 1}")
        # print(f"Melhor mochila: {melhor_mochila}")
        print(f"Benefício: {atributos_melhor_mochila[0]}. Peso: {atributos_melhor_mochila[1]}/{CAPACIDADE}")
        
        if(geracao + 1 < GERACOES):
            print("\n")

ag()