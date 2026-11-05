# definição de constantes
POPULACAO_TAMANHO = 100
GERACOES = 70
TAXA_MUTACAO = 0.03
TAXA_CRUZAMENTO = 0.6

# será o teste inicial com o primeiro arquivo -> isso vai ficar dinamico depois
N_ITENS = 10

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



cria_mochila(N_ITENS)