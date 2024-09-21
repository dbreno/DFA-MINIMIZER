"""
=====================

LER ARQUIVO TEXT

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

            # Adiciona a transição para o símbolo fornecido
            afd['transicoes'][origem][simbolo] = destino

    return afd  # Retorna o AFD lido do arquivo

"""
=====================

VALIDAR AFD

=====================
"""

def validar_afd(afd):
    # Verificar se o estado inicial está nos estados
    if afd['inicial'] not in afd['estados']:
        # Se o estado inicial não estiver na lista de estados, imprime um erro e retorna False
        print(f"Erro: Estado inicial '{afd['inicial']}' não está nos estados.")
        return False

    # Verificar se todos os estados finais estão nos estados
    for final in afd['finais']:
        # Para cada estado final, verifica se ele está na lista de estados
        if final not in afd['estados']:
            # Se algum estado final não estiver na lista de estados, imprime um erro e retorna False
            print(f"Erro: Estado final '{final}' não está nos estados.")
            return False

    # Verificar se todas as transições são válidas
    for origem, transicoes in afd['transicoes'].items():

        # Para cada estado de origem nas transições, verifica se ele está na lista de estados
        if origem not in afd['estados']:
            # Se o estado de origem não estiver na lista de estados, imprime um erro e retorna False
            print(f"Erro: Estado '{origem}' não está nos estados.")
            return False
        
        # Verificar se o dicionário de transições tem a mesma quantidade de símbolos que o alfabeto
        if len(transicoes) != len(afd['alfa']):
            print(f"Erro: Estado '{origem}' não possui transições para todos os símbolos do alfabeto.")
            return False

        simbolos_vistos = {}
        for simbolo, destino in transicoes.items():
            # Para cada transição, verifica se o estado de destino está na lista de estados
            if destino not in afd['estados']:
                # Se o estado de destino não estiver na lista de estados, imprime um erro e retorna False
                print(f"Erro: Destino '{destino}' não está nos estados.")
                return False
            # Verifica se o símbolo da transição está no alfabeto
            if simbolo not in afd['alfa']:
                # Se o símbolo não estiver no alfabeto, imprime um erro e retorna False
                print(f"Erro: Símbolo '{simbolo}' não está no alfabeto.")
                return False
            
            if simbolo in simbolos_vistos:
                simbolos_vistos[simbolo] += 1
            else:
                simbolos_vistos[simbolo] = 1

        # Verificar se algum símbolo aparece mais de uma vez
        for simbolo, quantidade in simbolos_vistos.items():
            if quantidade > 1:
                    print(f"Erro: Símbolo '{simbolo}' aparece mais de uma vez nas transições do estado '{origem}'.")
                    return False
               
    # Se todas as verificações passarem, retorna True
    return True

"""
=====================

EXIBIR DIAGRAMA

=====================
"""

from graphviz import Digraph

def exibir_diagrama_afd(afd, nome_arquivo):
    dot = Digraph(comment=nome_arquivo)

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
    
    # Adicionar transições
    for origem, transicoes in afd['transicoes'].items():
        origem_str = str(origem)
        for simbolo, destino in transicoes.items():
            destino_str = str(destino)
            dot.edge(origem_str, destino_str, label=simbolo)
    
    # Gera o arquivo
    dot.render(f'{nome_arquivo}.gv', view=True)

"""
=====================

CÓDIGO PRINCIPAL

=====================
"""

def main():
    # Ler o AFD de um arquivo
    afd = ler_afd('afd.txt')

    exibir_diagrama_afd(afd, "afd_normal")

    # Validar o AFD
    if validar_afd(afd):
        print("AFD válido!")
        
        # (Aqui fica o código do algoritmo Myhill-Nerode)

        # Cria uma "matriz", onde seus indices serão os estados do AFD e a preenche completamente com -1
        matriz = {estado: {estado_destino: -1 for estado_destino in afd['estados']} for estado in afd['estados']}
        
        #
        # Percorre toda a matriz, mantendo os elementos da diagonal principal para cima com -1 (que serão ignorados no algoritmo), e adicionando 0 ou 1:
        #
        # Adiciona 1 na célula caso um, e somente um, de seus estados seja um estado final
        #
        # Adiciona 0 na célula caso os dois sejam estados não-finais ou os dois sejam estados finais
        #  
        for i in afd['estados']:
            for j in afd['estados']:
                if (i == j): # Ignora as células da diagonal principal para cima
                    break
                if (i in afd['finais']) != (j in afd['finais']): # Se apenas um dos estados for final, adiciona 1 na célula
                    matriz[i][j] = 1
                else: # Adiciona 0 caso contrário
                    matriz[i][j] = 0
            
        # Implementação do algoritmo
        # 
        # Para cada par de estados com 0 na matriz (pares não marcados), verifica a transição de cada um dos estados do par para cada um dos símbolos do alfabeto. 
        #
        # O resultado é um outro par de estados. Se esse par resultante estiver marcado com 1 na matriz, o par inicial será também marcado na matriz, do contrário nada será feito
        #

        for i in afd['estados']:
            for j in afd['estados']:
                if (i == j): # Ignora a diagonal principal para cima
                    break
                if matriz[i][j] == 0: # Se o par de estados não estiver marcado na matriz, fará a derivação
                    for simbo in afd['alfa']: # Faz a transição de cada estado do par para cada símbolo do alfabeto
                        q1 = afd['transicoes'][i][simbo]
                        q2 = afd['transicoes'][j][simbo]

                        if (matriz[q1][q2] == 1): # Se o par gerado estiver marcado na matriz, o par original também será marcadao
                            matriz[i][j] = 1
                            continue
                        
                        if (matriz[q2][q1] == 1): # Como a maior parte da matriz é ignorada, é necessário testar o par ao contrário também
                            matriz[i][j] = 1

        """
        ===================================================================================================================
        """

        estadosAfdMin = [] # Array de arrays de string. Cada um dos sub-arrays representa um dos estados do AFD minimizado (que são estados compostos por estados do AFD original, exemplo: (C, D, E))

        estadosUtilizados = {""} # Set de string que guardará todos os estados do AFD original que já foram utilizados nos estados compostos do AFD minimizado, para futura verificação de estados que continuarão isolados no AFD minimizado 

        for i in afd['estados']: # Adiciona todos os pares de estados não marcados na matriz: os estados do AFD minimizado serão criados a partir deles
            for j in afd['estados']:
                if (i == j): # Ignora os elementos da diagonal principal para cima
                    break
                
                if (matriz[i][j] == 0): # Se o par de estados não estiver marcado na matriz, adiciona o array que contém os dois em 'estadosAfdMin', como também adiciona os dois estados em 'estadosUtilizados'
                    estadosAfdMin.append([i, j])
                    estadosUtilizados.add(i)
                    estadosUtilizados.add(j)

        estadosUtilizados.remove("") # Apenas remove a string vazia que foi adicionada inicialmente para criar o set de string

        # Faz a junção de todos os estados do AFD minimizado que possuem alguma interseção de estados do AFD original

        i = 0
        while i < len(estadosAfdMin) - 1: # i vai até len(estadosAfdMin) - 1, pois j recebe i+1 sempre
            j = i + 1
            while j < len(estadosAfdMin):
                if (set(estadosAfdMin[i]) & set(estadosAfdMin[j])): # Se houver interseção, os estados dos dois arrays de estados são mesclados no primeiro array e o segundo array é excluído
                    estadosAfdMin[i] = list(set(estadosAfdMin[i]).union(set(estadosAfdMin[j])))
                    estadosAfdMin.pop(j)
                else:
                    j += 1
            i += 1

        # Se algum estado não fizer parte de algum estado composto do AFD minimizado, então ele permanecerá isolado no AFD minimizado
        estadosIsolados = set(afd['estados']) - estadosUtilizados

        # Adiciona os estados isolados aos estados do AFD minimizado
        estadosAfdMin.append(list(estadosIsolados))

        estadoInicialAfdMin = [] # Armazena o estado inicial do AFD minimizado
        estadosFinaisAfdMin = [] # Armazena os estados finais do AFD minimizado

        for estado in estadosAfdMin:

            # Se o estado inicial do AFD original faz parte de um dos estados compostos do AFD minimizado, então esse estado composto será o estado inicial do AFD minimizado
            if (afd['inicial'] in estado):
                estadoInicialAfdMin.append(estado)

            # Se o estado final do AFD original faz parte de um dos estados compostos do AFD minimizado, então esse estado composto será um dos estados finais do AFD minimizado
            if (set(estado) & set(afd['finais'])): # Testa se há interseção entre o estado composto atual com os estados finais do AFD original
                estadosFinaisAfdMin.append(estado)

        estadosAfdMin1 = [] # Array de strings que representarão cada um dos estados compostos do AFD minimizado. Esse tratamento é feito para acumular o nome do estado composto em apenas uma string
        for estadoComposto in estadosAfdMin:
            string = ""
            for estado in estadoComposto:
                string += str(estado) + ', '
            estadosAfdMin1.append(string[:-2]) # Retira o que resta no final da string: ', ', e a adiciona ao array de strings

        estadoInicialAfdMin1 = "" # String que armazerá o nome do estado inicial do AFD minimizado. O motivo para o tratamento é o mesmo: condensar o nome do estado em apenas uma string
        for estadoComposto in estadoInicialAfdMin:
            for estado in estadoComposto:
                estadoInicialAfdMin1 += estado + ', '
        estadoInicialAfdMin1 = estadoInicialAfdMin1[:-2]

        estadosFinaisAfdMin1 = [] # Array de strings que armazenará os estados finais compostos do AFD minimizado em strings
        for estadoComposto in estadosFinaisAfdMin:
            string = ''
            for estado in estadoComposto:
                string += estado + ', '
            estadosFinaisAfdMin1.append(string[:-2])

        """
        ===================================================================================================================
        """

        # Cria estrutura de transições do AFD minimizado:
        #
        # Será um dicionário no estilo:
        #
        # 'transicoes': {
        #     'A': {'0': 'B', '1': 'C'},
        #     'B': {'0': 'A', '1': 'D'},
        #     'C': {'0': 'E', '1': 'F'},
        #     'D': {'0': 'E', '1': 'F'},
        #     'E': {'0': 'E', '1': 'F'},
        #     'F': {'0': 'F', '1': 'F'},
        # }
        #
        # Onde cada chave inicial indica um estado do AFD que aponta para outro dicionário, onde cada chave representa um símbolo do alfabeto que aponta para o estado de destino da transição
        #
    
        transicoesAfdMin = {
            
            # Para cada estadoPartida no AFD minimizado (estadosAfdMin1) - será uma chave inicial do dicionário
            estadoPartida: {
                
                # Para cada símbolo 'simbo' no alfabeto (afd['alfa']) - será uma chave do dicionário interno
                simbo: next(
                    
                    # Encontra o primeiro estado no conjunto de estados minimizados que corresponde à transição
                    estado for estado1 in estadoPartida
                    for estado in estadosAfdMin1
                    
                    # Verifica se a transição do estado original (estado1) com o símbolo 'simbo' leva a um estado que está dentro do conjunto de estados minimizados (estado)
                    if afd['transicoes'][estado1][simbo] in estado
                    
                )  # next() retorna o primeiro estado que satisfaz a condição acima
                
                # Esse bloco é para cada símbolo 'simbo' no alfabeto do AFD original
                for simbo in afd['alfa']
            }
    
    # Esse bloco externo itera por todos os estados combinados (estadoPartida) no AFD minimizado
    for estadoPartida in estadosAfdMin1
}

        # Cria a estrutura do AFD minimizado: mesma do AFD original
        afd_minimizado = {
            'alfa': afd['alfa'],
            'estados': [estado for estado in estadosAfdMin1],
            'inicial': (estadoInicialAfdMin1),
            'finais': [estado for estado in estadosFinaisAfdMin1],
            'transicoes': {estadoOrigem: {simbo: estadoDestino for simbo, estadoDestino in transicoes.items()} for estadoOrigem, transicoes in transicoesAfdMin.items()}
        }

        # Exibe o AFD minimizado
        exibir_diagrama_afd(afd_minimizado, "afd_minimizado")

    else:
        print("AFD inválido. Corrija o arquivo e tente novamente.")

if __name__ == "__main__":
    main()