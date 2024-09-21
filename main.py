"""""
Myhill Nerode (ou Table Filling Method)

Passos:

1) Desenhar a tabela dos pares de estados (tirar todos os pares da diagonal principal pra cima). OK

2) Marcar os pares de estados (q0, q1) em que ou q0 seja estado final, ou q1. (ou exclusivo) OK

3) Se houver pares não-marcados, cuja derivação* esteja marcada, marcar par não-marcado.
Repetir isso até que novas marcações não possam ser feitas.

* Derivação: para cada estado do par, realizar a transição para cada símbolo do alfabeto. Assim, tratando-se de um símbolo, será encontrado um novo par derivado.

4) Combinar todos os pares não-marcados e fazer um único estado no AFD minimizado.
"""

afd = {

    'alfa': ['0', '1'],
    'estados': ['A', 'B', 'C', 'D', 'E', 'F'],
    'inicial': 'A',
    'finais': ['C', 'D', 'E'],
    'transicoes': {

                    'A': {'0': 'B', '1': 'C'},
                    'B': {'0': 'A', '1': 'D'},
                    'C': {'0': 'E', '1': 'F'},
                    'D': {'0': 'E', '1': 'F'},
                    'E': {'0': 'E', '1': 'F'},
                    'F': {'0': 'F', '1': 'F'},
                
                }
}

# matriz = {

#     'A': {'A': -1, 'B': -1, 'C': -1, 'D': -1,'E': -1, 'F': -1},
#     'B': {'A': 0, 'B': -1, 'C': -1, 'D': -1,'E': -1, 'F': -1},
#     'C': {'A': 1, 'B': 1, 'C': -1, 'D': -1,'E': -1, 'F': -1},
#     'D': {'A': 1, 'B': 1, 'C': 0, 'D': -1,'E': -1, 'F': -1},
#     'E': {'A': 1, 'B': 1, 'C': 0, 'D': 0,'E': -1, 'F': -1},
#     'F': {'A': 0, 'B': 0, 'C': 1, 'D': 1,'E': 1, 'F': -1}

# }

matriz = {estado: {estado_destino: -1 for estado_destino in afd['estados']} for estado in afd['estados']}

for i in afd['estados']:
    for j in afd['estados']:
        if (i == j):
            break
        if (i in afd['finais']) != (j in afd['finais']):
            matriz[i][j] = 1
        else:
            matriz[i][j] = 0
    
# God demais
for i in afd['estados']:
    for j in afd['estados']:
        if (i == j):
            break
        if matriz[i][j] == 0:
            for simbo in afd['alfa']:
                q1 = afd['transicoes'][i][simbo]
                q2 = afd['transicoes'][j][simbo]

                if (matriz[q1][q2] == 1):
                    matriz[i][j] = 1
                    continue
                
                if (matriz[q2][q1] == 1):
                    matriz[i][j] = 1

"""
===================================================================================================================
"""

estadosAfdMin = []
estadosUtilizados = {""}

for i in afd['estados']:
    for j in afd['estados']:
        if (i == j):
            break
        
        if (matriz[i][j] == 0):
            estadosAfdMin.append([i, j])
            estadosUtilizados.add(i)
            estadosUtilizados.add(j)

estadosUtilizados.remove("")

# Analisar se a lógica está correta
i = 0
while i < len(estadosAfdMin) - 1:
    j = i + 1
    while j < len(estadosAfdMin):
        if (set(estadosAfdMin[i]) & set(estadosAfdMin[j])): # Há interseção 
            estadosAfdMin[i] = list(set(estadosAfdMin[i]).union(set(estadosAfdMin[j])))
            estadosAfdMin.pop(j)
        else:
            j += 1
    i += 1

estadosIsolados = set(afd['estados']) - estadosUtilizados

estadosAfdMin.append(list(estadosIsolados))

estadoInicialAfdMin = []

estadosFinaisAfdMin = []

for estado in estadosAfdMin:
    if (afd['inicial'] in estado):
        estadoInicialAfdMin.append(estado)

    if (set(estado) & set(afd['finais'])):
        estadosFinaisAfdMin.append(estado)


    
print("Estados utilizados", estadosUtilizados)
print("Estados isolados", estadosIsolados)
print("Estados AFD MIN: ", estadosAfdMin)
print("Estado inicial AFD MIN: ", estadoInicialAfdMin)
print("Estados finais AFD MIN: ", estadosFinaisAfdMin)

"""
===================================================================================================================
"""

# Verificar 

transicoesAfdMin = {
                    tuple(estadoPartida): {
                    simbo: next(
                        estado for estado1 in estadoPartida
                        for estado in estadosAfdMin
                        if afd['transicoes'][estado1][simbo] in estado
                    )           
                    for simbo in afd['alfa']
                }           
                for estadoPartida in estadosAfdMin
                }

print(transicoesAfdMin)

# for estadoComposto in estadosAfdMin:
#     for estado in estadoComposto:

# matriz = {estado: {estado_destino: -1 for estado_destino in afd['estados']} for estado in afd['estados']}

# {

#     'A': {'0': 'B', '1': 'C'},
#     'B': {'0': 'A', '1': 'D'},
#     'C': {'0': 'E', '1': 'F'},
#     'D': {'0': 'E', '1': 'F'},
#     'E': {'0': 'E', '1': 'F'},
#     'F': {'0': 'F', '1': 'F'},

# }