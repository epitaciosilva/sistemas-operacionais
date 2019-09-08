from utils import *

def soma_matrizes_processos(rowA, rowB, processo, results):
    processo = os.fork()
    if processo == 0:
        linha_somada = []
        for a,b in zip(rowA, rowB):
            linha_somada.append(b+a) # soma das matrizes

        results.append(linha_somada)
    else:
        os.waitpid(processo, 0)
    return processo  

def soma_matrizes_threads(elemt_A, elemt_B, posi_i, posi_j, results):
    threading.currentThread()
    results[posi_i][posi_j] = elemt_A + elemt_B

def unroll(args, func, method, results):
    matriz_aleatoria = matriz_randomica(len(args), len(args[0]))

    # ---------- Threads ----------
    # A soma de cada elemento é feito dentro de uma thread
    if method == "thread":
        # List das threads criadas
        threads = []

        # Dimensão das matrizes
        cols = len(args[0])
        rows = len(args)

        results = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(rows):
            for j in range(cols):
                threads.append([])
                threads[-1] = threading.Thread(target=func, args=(args[i][j], matriz_aleatoria[i][j], i, j, results))
                threads[-1].start()

        print("------ Args ------")
        print_matriz(args)

        print("\n------ Aleatoria ------")
        print_matriz(matriz_aleatoria)

        print("\n------ Matriz soma ------")
        print_matriz(results)
    
    # ---------- PROCESSOS ----------
    # Ainda não esta pronto, eh preciso fazer com os processos se comuniquem
    # provavelmente com memoria compartilhada so assim pra conseguir salvar os results 
    # de cada soma das linhas da matriz.
    # No caso o processo original devera imprimir a soma completa da matriz
    else: 
        processos = []

        for arg, row_aleatoria in zip(args, matriz_aleatoria):
            processos.append([])
            processo = func(arg, row_aleatoria, processos[-1], results)
            processos[-1] = processo

        if len(list(filter(lambda x: x != 0, processos))) == 0: # verifica se todos os processos são filhos
            print("------ Args ------")
            print_matriz(args)

            print("\n------ Aleatoria ------")
            print_matriz(matriz_aleatoria)

            print("\n------ Matriz soma ------")
            print_matriz(results)

if __name__ == '__main__':
    res = []
    unroll([[0, 1,3],[2,3,4],[4,5,7]], soma_matrizes_processos, 'proc', res)
    # unroll([[0, 1, 3, 4, 5],[2, 3, 1, 2, 3],[4, 5, 4, 2, 5]], soma_matrizes_threads, 'thread', res)