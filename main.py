# definição de constantes
POPULACAO_TAMANHO = 100
GERACOES = 70
TAXA_MUTACAO = 0.03
TAXA_CRUZAMENTO = 0.6

# definição do que se trata da mochila
CAPACIDADE = 105
beneficio_itens = [3, 42, 5, 48, 42, 13, 3, 20, 12, 37]
peso_itens = [2, 35, 13, 29, 9, 25, 2, 14, 4, 17]

itens = list(zip(beneficio_itens, peso_itens))

# será o teste inicial com o primeiro arquivo -> isso vai ficar dinamico depois
N_ITENS = len(itens)

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

def cria_populacao(tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        populacao.append(cria_mochila(N_ITENS))
        
    return populacao

def beneficio_peso(populacao, itens):
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
