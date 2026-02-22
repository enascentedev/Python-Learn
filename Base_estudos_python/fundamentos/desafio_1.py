# Desafio 01
# Crie uma função que retorna se um número inteiro n (maior que zero) é primo.
# Dica: um número primo é um número que só é divisível por 1 ou por ele mesmo.


def numero_primo(numero):
    if numero <= 2:
        return True
    for divisor in range(2, numero):
        if numero % divisor == 0:
            return False
    return True


for numero in [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
]:
    print(f"Numero {numero} é primo? {numero_primo (numero)}")
