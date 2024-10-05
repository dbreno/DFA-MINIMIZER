"""
=====================

LER ARQUIVO TXT

=====================
"""

def ler_afd(arquivo):
    # Abre o arquivo e lê todas as linhas
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

    # Inicializa a estrutura de dados do AFD com listas vazias e dicionários
    afd = {
        'alfa': [],         # Alfabeto
        'estados': [],      # Estados do autômato
        'inicial': '',      # Estado inicial
        'finais': [],       # Estados finais
        'transicoes': {}    # Transições do autômato
    }

    # Processa cada linha do arquivo
    for linha in linhas:
        linha = linha.strip()  # Remove espaços em branco nas extremidades da linha

        # Identifica a linha com o alfabeto e separa os símbolos
        if linha.startswith('alfabeto:'):
            afd['alfa'] = linha.split(':')[1].split(',')  # Divide a linha no ':' e pega o segundo elemento (alfabeto)

        # Identifica a linha com os estados e separa os estados
        elif linha.startswith('estados:'):
            afd['estados'] = linha.split(':')[1].split(',')  # Divide a linha no ':' e pega o segundo elemento (estados)

        # Identifica a linha com o estado inicial
        elif linha.startswith('inicial:'):
            afd['inicial'] = linha.split(':')[1]  # Divide a linha no ':' e pega o estado inicial

        # Identifica a linha com os estados finais e os separa
        elif linha.startswith('finais:'):
            afd['finais'] = linha.split(':')[1].split(',')  # Divide a linha no ':' e pega os estados finais

        # Ignora a linha de transições, pois ela será tratada a seguir
        elif linha.startswith('transicoes'):
            continue

        # As linhas restantes representam as transições do AFD
        else:
            origem, destino, simbolo = linha.split(',')  # Divide a linha nas vírgulas para pegar origem, destino e símbolo

            # Se a origem ainda não está no dicionário de transições, inicializa-a como um novo dicionário
            if origem not in afd['transicoes']:
                afd['transicoes'][origem] = {}

            # Verifica se já existe uma transição para o mesmo símbolo
            if simbolo in afd['transicoes'][origem]:
                print(f"Erro: Estado '{origem}' já possui uma transição para o símbolo '{simbolo}'.")
                return None  # Retorna um AFD inválido

            # Adiciona a transição para o símbolo fornecido
            afd['transicoes'][origem][simbolo] = destino

    return afd  # Retorna o AFD lido do arquivo

"""
=====================

VALIDAR AFD

=====================
"""

def validar_afd(afd):
    # Verifica se o estado inicial está nos estados
    if afd['inicial'] not in afd['estados']:
        # Se o estado inicial não estiver na lista de estados, imprime um erro e retorna False
        print(f"Erro: Estado inicial '{afd['inicial']}' não está nos estados.")
        return False

    # Verifica se todos os estados finais estão nos estados
    for final in afd['finais']:
        if final not in afd['estados']:
            print(f"Erro: Estado final '{final}' não está nos estados.")
            return False

    # Verifica se todos os estados das transições são válidos
    for estado in afd['transicoes']:
        if not estado in afd['estados']:
            print(f"Erro: Estado '{estado}' não está nos estados válidos.")
            return False

    # Verifica se todas as transições são válidas
    for origem in afd['estados']:
        if origem not in afd['transicoes']:
            print(f"Erro: Estado '{origem}' não possui transições.")
            return False
        
        transicoes = afd['transicoes'][origem]

        # Verifica se o número de transições é igual ao número de símbolos no alfabeto
        if len(transicoes) != len(afd['alfa']):
            print(f"Erro: Estado '{origem}' não possui transições para todos os símbolos do alfabeto.")
            return False

        # Verifica se há mais de uma transição para o mesmo símbolo
        simbolos_vistos = set()
        for simbolo, destino in transicoes.items():
            # Verifica se o destino é um estado válido
            if destino not in afd['estados']:
                print(f"Erro: O estado destino '{destino}' na transição do estado '{origem}' não é um estado válido.")
                return False

            # Verifica se o símbolo está no alfabeto
            if simbolo not in afd['alfa']:
                print(f"Erro: O símbolo '{simbolo}' não pertence ao alfabeto.")
                return False

            # Verifica se o símbolo já foi usado
            if simbolo in simbolos_vistos:
                print(f"Erro: O estado '{origem}' possui mais de uma transição para o símbolo '{simbolo}'.")
                return False

            simbolos_vistos.add(simbolo)

    # Se todas as verificações passarem, retorna True
    return True

"""
=====================

EXIBIR DIAGRAMA

=====================
"""

from graphviz import Digraph

def exibir_diagrama_afd(afd, nome_arquivo):
    # Cria o arquivo de exibição do AFD a partir da biblioteca Graphviz

    dot = Digraph(comment=nome_arquivo)

    # Define a direção do layout como da esquerda para a direita (horizontal)
    dot.attr(rankdir='LR')

    # Define a orientação como "paisagem"
    dot.attr(size='11.69,8.27') # A4 landscape
    dot.attr(ratio='fill')  # Ajusta a escala para preencher a página

    # Adiciona um nó inicial invisível
    dot.node('inicio', '', shape='point')  # Um ponto invisível para representar a entrada
    
    # Adiciona estados
    for estado in afd['estados']:
        if estado in afd['finais']:
            dot.node(str(estado), str(estado), shape='doublecircle')  # Estados finais com círculo duplo
        else:
            dot.node(str(estado), str(estado))

    # Adiciona uma transição do estado inicial invisível para o estado inicial do AFD
    dot.edge('inicio', afd['inicial'])  # Seta do ponto invisível para o estado inicial
    
     # Adiciona transições agrupadas
    for origem, transicoes in afd['transicoes'].items():
        origem_str = str(origem)
        
        # Dicionário para agrupar transições
        transicoes_agrupadas = {}

        for simbolo, destino in transicoes.items():
            destino_str = str(destino)
            
            # Agrupa os símbolos que têm o mesmo destino
            if destino_str not in transicoes_agrupadas:
                transicoes_agrupadas[destino_str] = []
            transicoes_agrupadas[destino_str].append(simbolo)
        
        # Adiciona transições agrupadas para o gráfico
        for destino_str, simbolos in transicoes_agrupadas.items():
            label = '\n'.join(simbolos)  # Coloca um símbolo por linha
            dot.edge(origem_str, destino_str, label=label)
    
    # Gera o arquivo
    dot.render(f'{nome_arquivo}.gv', view=True)

"""
=====================

CÓDIGO PRINCIPAL

=====================
"""

def mostra_matriz(matriz):
    
    # Imprime os cabeçalhos das colunas
    print('   ', end='')
    for estado in matriz:
        print(f'{estado:>2} ', end='') # Imprime o nome do estado com alinhamento à direita
    print()

    # Imprime a matriz linha por linha
    for estado in matriz:
        print(f'{estado:>2} ', end='') # Imprime o nome do estado na linha atual
        for estado_destino in matriz[estado]:
            # Imprime o valor da matriz na posição [estado][estado_destino] com alinhamento à direita
            print(f'{matriz[estado][estado_destino]:>2} ', end='')
        print() # Pula para a próxima linha

def mostra_diagonal_inferior(matriz):
    # Imprime os cabeçalhos das colunas
    print('   ', end='')
    for estado in matriz:
        print(f'{estado:>2} ', end='') # Imprime o nome do estado com alinhamento à direita
    print()
    # Imprime apenas os elementos da diagonal inferior da matriz
    for estado in matriz:
        print(f'{estado:>2} ', end='') # Imprime o nome do estado na linha atual
        for estado_destino in matriz[estado]:
            if estado_destino < estado:
                # Imprime o valor da matriz na posição [estado][estado_destino] se estiver na diagonal inferior
                print(f'{matriz[estado][estado_destino]:>2} ', end='')
            else:
                # Imprime espaços em branco para manter o alinhamento
                print('   ', end='')
        print() # Pula para a próxima linha

def preenche_matriz_inicial(afd, matriz):
    # Percorre toda a matriz, mantendo os elementos da diagonal principal para cima com -1 (que serão ignorados no algoritmo), e adicionando 0 ou 1:
    #
    # Adiciona 1 na célula caso um, e somente um, de seus estados seja um estado final
    #
    # Adiciona 0 na célula caso os dois sejam estados não-finais ou os dois sejam estados finais
    passo = 0 
    for i in afd['estados']:
        for j in afd['estados']:
            passo += 1
            print('-' * 50)
            print(f'Passo {passo}: comparando o estado {i} e o estado {j}\n')
            if i == j:
                print('Os estados são iguais, então ignoramos.')
                break

            # Se o par de estados contiver exclusivamente um estado final, a matriz é marcada com 1
            if (i in afd['finais']) != (j in afd['finais']):
                print(f'O estado {i} {'é' if i in afd['finais'] else 'não é'} final e o', end=" ")
                print(f'estado {j} {'é' if j in afd['finais'] else 'não é'} final')
                print(f'Logo, a posição {i}x{j} recebe um 1, matriz atualizada:')
                matriz[i][j] = 1
            # Caso contrário, é marcada com 0
            else:
                print(f'O estado {i} {'é' if i in afd['finais'] else 'não é'} final e o', end=" ")
                print(f'estado {j} {'é' if j in afd['finais'] else 'não é'} final')
                print(f'Logo, a posição {i}x{j} recebe um 0, matriz atualizada:')
                matriz[i][j] = 0
            mostra_matriz(matriz)

def deriva_estados_matriz(afd, matriz):
    print('=' * 50)
    print('\nSEGUNDA ETAPA DO ALGORITMO DE MYHILL-NERODE\n')
    print('=' * 50)

    print('Derivando os pares de estados não marcados na matriz:\n')
    # Segunda etapa
    passo = 0
    for i in afd['estados']:
        for j in afd['estados']:
            passo += 1
            print('-' * 50)
            if (i == j): # Ignora a diagonal principal para cima
                print(f'Passo {passo}: Os estados {i} e {j} são iguais, então ignoramos.')
                break
            if matriz[i][j] == 1:
                print(f'Passo {passo}: O par de estados {i} e {j} já está marcado na matriz, então ignoramos.')
                continue
            if matriz[i][j] == 0: # Se o par de estados não estiver marcado na matriz, fará a derivação
                print(f'Passo {passo}: Derivando o par de estados {i} e {j}\n')
                for simbo in afd['alfa']: # Faz a transição de cada estado do par para cada símbolo do alfabeto
                    q1 = afd['transicoes'][i][simbo]
                    q2 = afd['transicoes'][j][simbo]
                    print(f'{i} lendo {simbo} vai para {q1}')
                    print(f'{j} lendo {simbo} vai para {q2}\n')
                    if (matriz[q1][q2] == 1): # Se o par gerado estiver marcado na matriz, o par original também será marcadao
                        matriz[i][j] = 1
                        print(f'O par de estados {i} e {j} com o simbolo {simbo} foi derivado para o par de estados {q1} e {q2}')
                        print(f'que está marcado na matriz, então o par {i} e {j} também será marcado.\n')
                        continue
                    elif (matriz[q1][q2] != 1): # Se o par gerado não estiver marcado na matriz, imprime uma mensagem
                        print(f'O par de estados {i} e {j} com o simbolo {simbo} foi derivado para o par de estados {q1} e {q2}')
                        print(f'que não está marcado na matriz, então o par {i} e {j} não será marcado.\n')
                        continue
                    if (matriz[q2][q1] == 1): # Como a maior parte da matriz é ignorada, é necessário testar o par ao contrário também
                        matriz[i][j] = 1
                        print(f'O par de estados {i} e {j} com o simbolo {simbo} foi derivado para o par de estados {q1} e {q2}')
                        print(f'que está marcado na matriz, então o par {i} e {j} também será marcado.\n')
                        continue
                    elif (matriz[q2][q1] != 1): # Se o par gerado não estiver marcado na matriz, imprime uma mensagem
                        print(f'O par de estados {i} e {j} com o simbolo {simbo} foi derivado para o par de estados {q1} e {q2}')
                        print(f'que não está marcado na matriz, então o par {i} e {j} não será marcado.\n')
                        continue

def condensa_estados(afd, matriz):

    estadosAfdMin = [] # Array de arrays de string. Cada um dos sub-arrays representa um dos estados do AFD minimizado (que são estados compostos por estados do AFD original, exemplo: (C, D, E))

    estadosUtilizados = {""} # Set de string que guardará todos os estados do AFD original que já foram utilizados nos estados compostos do AFD minimizado, para futura verificação de estados que continuarão isolados no AFD minimizado 

    for i in afd['estados']: # Adiciona todos os pares de estados não marcados na matriz: os estados do AFD minimizado serão criados a partir deles
        for j in afd['estados']:
            if (i == j): # Ignora os elementos da diagonal principal para cima
                break
            
            if (matriz[i][j] == 0): # Se o par de estados não estiver marcado na matriz, adiciona o array que contém os dois em 'estadosAfdMin', como também adiciona os dois estados em 'estadosUtilizados'
                print(f'O par {i} e {j} foi marcado com 0')
                estadosAfdMin.append([i, j])
                estadosUtilizados.add(i)
                estadosUtilizados.add(j)

    # Faz a junção de todos os estados do AFD minimizado que possuem alguma interseção de estados do AFD original
    
    print('\nVamos olhar para as interseções nos estados agora:\n')
    
    i = 0
    while i < len(estadosAfdMin) - 1: # i vai até len(estadosAfdMin) - 1, pois j recebe i+1 sempre
        j = i + 1
        while j < len(estadosAfdMin):
            if (set(estadosAfdMin[i]) & set(estadosAfdMin[j])): # Se houver interseção, os estados dos dois arrays de estados são mesclados no primeiro array e o segundo array é excluído
                print(f'O par de estados {estadosAfdMin[i]} e {estadosAfdMin[j]} possui interseção, então eles serão mesclados.')
                estadosAfdMin[i] = list(set(estadosAfdMin[i]).union(set(estadosAfdMin[j])))
                estadosAfdMin.pop(j)
            else:
                j += 1
        i += 1

    estadosUtilizados.remove("") # Apenas remove a string vazia que foi adicionada inicialmente para criar o set de string

    # Se algum estado não fizer parte de algum estado composto do AFD minimizado, então ele permanecerá isolado no AFD minimizado
    estadosIsolados = set(afd['estados']) - estadosUtilizados
    print(f'O(s) estado(s) isolado(s) é(são): {estadosIsolados}')

    # Adiciona os estados isolados aos estados do AFD minimizado
    estadosAfdMin.append(list(estadosIsolados))

    estadoInicialAfdMin = [] # Armazena o estado inicial do AFD minimizado
    estadosFinaisAfdMin = [] # Armazena os estados finais do AFD minimizado

    for estado in estadosAfdMin:

        # Se o estado inicial do AFD original faz parte de um dos estados compostos do AFD minimizado, então esse estado composto será o estado inicial do AFD minimizado
        if (afd['inicial'] in estado):
            print(f'\nO estado inicial {afd["inicial"]} faz parte do estado composto {estado}')
            print(f'então {estado} será estado inicial do AFD minimizado.')
            estadoInicialAfdMin.append(estado)

        # Se o estado final do AFD original faz parte de um dos estados compostos do AFD minimizado, então esse estado composto será um dos estados finais do AFD minimizado
        if (set(estado) & set(afd['finais'])): # Testa se há interseção entre o estado composto atual com os estados finais do AFD original
            print(f'\nO estado final {list(set(estado) & set(afd["finais"]))[0]} faz parte do estado composto {estado}, ')
            print(f'então {estado} será final no AFD minimizado.')
            estadosFinaisAfdMin.append(estado)

    estadosAfdMin1 = [] # Array de strings que representarão cada um dos estados compostos do AFD minimizado. Esse tratamento é feito para acumular o nome do estado composto em apenas uma string
    for estadoComposto in estadosAfdMin:
        estadoComposto.sort() # Ordena os estados do AFD alfabeticamente
        string = ""
        for estado in estadoComposto:
            string += str(estado) + ', '
        estadosAfdMin1.append(string[:-2]) # Retira o que resta no final da string: ', ', e a adiciona ao array de strings

    estadoInicialAfdMin.sort() # Ordena o array de estado inicial alfabeticamente

    estadoInicialAfdMin1 = "" # String que armazerá o nome do estado inicial do AFD minimizado. O motivo para o tratamento é o mesmo: condensar o nome do estado em apenas uma string
    for estadoComposto in estadoInicialAfdMin:
        for estado in estadoComposto:
            estadoInicialAfdMin1 += estado + ', '
    estadoInicialAfdMin1 = estadoInicialAfdMin1[:-2]

    estadosFinaisAfdMin.sort() # Ordena o array de estados finais alfabeticamente

    estadosFinaisAfdMin1 = [] # Array de strings que armazenará os estados finais compostos do AFD minimizado em strings
    for estadoComposto in estadosFinaisAfdMin:
        string = ''
        for estado in estadoComposto:
            string += estado + ', '
        estadosFinaisAfdMin1.append(string[:-2])

    return estadosAfdMin1, estadoInicialAfdMin1, estadosFinaisAfdMin1

    
def preenche_transicoes(afd, estadosAfdMin):
    
    transicoesAfdMin = {}

    # Para cada estadoPartida no AFD minimizado
    for estadoPartida in estadosAfdMin:
        transicoesAfdMin[estadoPartida] = {}

        # Para cada símbolo no alfabeto do AFD
        for simbo in afd['alfa']:
            # Encontra o primeiro estado no conjunto de estados minimizados que corresponde à transição
            for estado1 in estadoPartida.split(', '):  # Aqui garantimos que cada estado dentro do estadoPartida seja tratado corretamente como string
                estado_destino = next(
                    estado for estado in estadosAfdMin
                    if afd['transicoes'][estado1][simbo] in estado.split(', ')
                )
                break

            # Preenche a transição
            transicoesAfdMin[estadoPartida][simbo] = estado_destino

            # Exibe a transição no terminal
            print('-' * 50)
            print(f"Preenchendo transição: {estadoPartida} --{simbo}--> {estado_destino}")
            print(f"Explicação: O estado {estadoPartida} contém o estado {estado1} do AFD original.")
            print(f"Para o símbolo '{simbo}', o estado {estado1} transita para {afd['transicoes'][estado1][simbo]} no AFD original.")
            print(f"Portanto, no AFD minimizado, o estado {estadoPartida} transita para {estado_destino} com o símbolo '{simbo}'.\n")

    return transicoesAfdMin


def myhill_nerode(afd):
    # Implementação do algoritmo
    # 
    # Para cada par de estados com 0 na matriz (pares não marcados), verifica a transição de cada um dos estados do par para cada um dos símbolos do alfabeto. 
    #
    # O resultado é um outro par de estados. Se esse par resultante estiver marcado com 1 na matriz, o par inicial será também marcado na matriz, do contrário nada será feito
    
    # Valida o AFD
    if validar_afd(afd):
        print("AFD válido!")

        print('=' * 50)
        print('\nPRIMEIRA ETAPA DO ALGORITMO DE MYHILL-NERODE\n')
        print('=' * 50)

        # Cria uma "matriz", onde seus indices serão os estados do AFD e a preenche completamente com -1
        matriz = {estado: {estado_destino: -1 for estado_destino in afd['estados']} for estado in afd['estados']}

        print("Matriz inicial: ")
        print("\n")
        mostra_matriz(matriz)

        # Faz o setup inicial da matriz: marcando com 1 os pares de estados que contiverem somente um estado final, e marcando com 0 caso contrário
        preenche_matriz_inicial(afd, matriz)

        print('\n\nMatriz após a primeira etapa:\n')
        mostra_matriz(matriz)
        print("\nOu, de forma mais compacta:\n")
        mostra_diagonal_inferior(matriz)

        # Aplica a regra do algoritmo na matriz
        deriva_estados_matriz(afd, matriz)
        print('=' * 50)
        print('\nTERCEIRA ETAPA DO ALGORITMO MYHILL NERODE\n')
        print('=' * 50)
        print('Agora, vamos minimizar o AFD condensando alguns estados em um só.')
        print('Basta verificar os pares de estados não marcados na matriz')
        print('Se eles possuem estados em comum, eles serão condensados em um só.\n')
        mostra_diagonal_inferior(matriz)

        estadosAfdMin, estadoInicialAfdMin, estadosFinaisAfdMin = condensa_estados(afd, matriz)

        transicoesAfdMin = preenche_transicoes(afd, estadosAfdMin)

        # Cria a estrutura do AFD minimizado: mesma do AFD original
        afd_minimizado = {
            'alfa': afd['alfa'],
            'estados': [estado for estado in estadosAfdMin],
            'inicial': (estadoInicialAfdMin),
            'finais': [estado for estado in estadosFinaisAfdMin],
            'transicoes': {estadoOrigem: {simbo: estadoDestino for simbo, estadoDestino in transicoes.items()} for estadoOrigem, transicoes in transicoesAfdMin.items()}
        }

        return afd_minimizado

    else:
        print("AFD inválido. Corrija o arquivo e tente novamente.")
        return {}

#################################################################################################

import json

def main():
    afd = ler_afd('afd.txt')  # Lê o AFD de um arquivo

    if afd is None:
        print("Erro ao carregar o AFD. Verifique o arquivo de entrada.")
        return

    if validar_afd(afd):
        exibir_diagrama_afd(afd, "afd_inicial")  # Exibe o AFD inicial
        afd_minimizado = myhill_nerode(afd)  # Recebe a estrutura do afd minimizado pelo algoritmo
        exibir_diagrama_afd(afd_minimizado, "afd_minimizado")  # Exibe o AFD minimizado
        afd_formatado = json.dumps(afd_minimizado, indent=4)
        print("Modelo do AFD minimizado: ")
        print(afd_formatado)
    else:
        print("AFD inválido. Corrija o arquivo e tente novamente.")

if __name__ == "__main__":
    main()