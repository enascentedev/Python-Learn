# Código que não gera erro, porém com bug na lógica
nomes = ['José', 'Bernardo', 'Paola', 'Fernando', 'Rita']
idades = [20, 16, 18, 40, 12]

for nome, idade in zip(nomes, idades):
    if idade > 18:
        maior_de_idade = True
    elif idade < 18:
        maior_de_idade = False
    print(f'{nome} tem {idade} anos. É maior de idade? {maior_de_idade}')


# Código que gera erro
nomes = ['José', 'Bernardo', 'Paola', 'Fernando', 'Rita']
idades = [18, 16, 18, 40, 12]

for nome, idade in zip(nomes, idades):
    if idade > 18:
        maior_de_idade = True
    elif idade < 18:
        maior_de_idade = False
    print(f'{nome} tem {idade} anos. É maior de idade? {maior_de_idade}')
    # NameError: name 'maior_de_idade' is not defined
