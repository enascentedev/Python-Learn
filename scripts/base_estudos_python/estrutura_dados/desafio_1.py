# valores = [30, 50, 100, 120]
# triplos = []

# for valor in valores:
# 		triplo = valor * 3
# 		triplos.append(triplo)

# print(triplos)


def multiplicar_valores_por_tres(valor):
    return valor * 3


valores = [30, 50, 100, 120]
triplos_compreensao_lista = [multiplicar_valores_por_tres(valor) for valor in valores]
print(triplos_compreensao_lista)
