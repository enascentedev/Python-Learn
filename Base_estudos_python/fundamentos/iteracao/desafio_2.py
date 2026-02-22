# Desafio 02
# Imagine que você tem um restaurante com os seguintes itens no seu menu:
import itertools

comidas = {
    "Prato Feito": 24.90,
    "Salada": 21.90,
    "Strogonoff": 29.90,
    "Feijoada": 32.90,
}
bebidas = {
    "Água": 3.90,
    "Refrigerante": 5.90,
    "Suco": 7.90,
}
entradas = {
    "Batata Frita": 12,
    "Picadinho": 15,
}

# Crie um novo dicionário chamado combos onde cada chave é uma tupla contendo (comida,
# bebida), e o seu respectivo valor é o preço daquela combinação de comida e bebida.

combo = {}
for tuplas in itertools.product(comidas.items(), bebidas.items(), entradas.items()):
    chave_combo = tuple(tup[0] for tup in tuplas)
    preco_combo = sum(tup[1] for tup in tuplas)
    combo[chave_combo] = round(preco_combo, 2)
print(combo)
