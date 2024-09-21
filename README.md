Universidade Federal da Paraíba
Centro de Informática
Disciplina: Linguagens Formais e Computabilidade
Professor: Bruno Bruck

Tema 2: Minimizador de Autômatos Finitos Determinísticos

  Nesse tema, houve a implementação de uma aplicação que, inicialmente, recebe como entrada um arquivo
  .txt contendo a descrição de Autômato Finito Determinístico (AFD) no seguinte formato:

    alfabeto: a,b,c,d                    # Lista de símbolos do alfabeto aceito pelo autômato;
    estados: q0,q1,q2                    # Lista de estados no autômato;
    inicial: q0                          # Indica qual é o estado inicial;
    finais: q1,q2                        # Especifica os estados finais do autômato;
    transicoes
    q0,q1,a                              # Representa uma transição de q0 para q1 com o símbolo "a";
    q1,q2,b                              # Representa uma transição de q1 para q2 com o símbolo "b".

  Em seguida, a aplicação deve utilizar o algoritmo de Myhill Nerode (ou Table Filling Method) para
  minimizar o AFD dado como entrada. O algoritmo deve mostrar na tela o passo-a-passo da sua execução
  e ao final utilizar alguma biblioteca ou software para exibir o diagrama de estados do AFD resultante.

Importante: E necessário verificar se o AFD passado como entrada é de fato válido antes de utilizar
o algoritmo de conversão.

  


  
  
