import time
import threading
import itertools
import queue


matriz_distancias_paralela = [
    [0.00, 10.77, 12.65, 19.80, 18.68, 20.88, 24.18, 25.61, 25.46, 26.08],
    [10.77, 0.00, 9.43, 10.77, 8.25, 17.46, 19.42, 14.32, 17.20, 24.33],
    [12.65, 9.43, 0.00, 10.77, 15.13, 8.00, 10.63, 20.40, 15.13, 14.42],
    [19.80, 10.77, 10.77, 0.00, 10.77, 9.22, 8.25, 12.17, 6.32, 13.89],
    [18.68, 8.25, 15.13, 10.77, 0.00, 17.46, 17.46, 6.32, 12.00, 22.63],
    [20.88, 17.46, 8.00, 9.22, 17.46, 0.00, 6.32, 20.88, 12.00, 6.32],
    [24.18, 19.42, 10.63, 8.25, 17.46, 6.32, 0.00, 18.44, 6.32, 10.00],
    [25.61, 14.32, 20.40, 12.17, 6.32, 20.88, 18.44, 0.00, 10.77, 24.83],
    [25.46, 17.20, 15.13, 6.32, 12.00, 12.00, 6.32, 10.77, 0.00, 16.12],
    [26.08, 24.33, 14.42, 13.89, 22.63, 6.32, 10.00, 24.83, 16.12, 0.00],
]

NUM_THREADS = 4  

def calcular_distancia_paralela(caminho):
    distancia = 0
    for i in range(len(caminho) - 1):
        distancia += matriz_distancias_paralela[caminho[i]][caminho[i + 1]]
    distancia += matriz_distancias_paralela[caminho[-1]][caminho[0]]  
    return distancia

def worker(par_queue, result_queue):
    melhor_distancia = float('inf')
    melhor_caminho = []

    while True:
        try:
            caminho = par_queue.get_nowait()
        except queue.Empty:
            break

        distancia = calcular_distancia_paralela(caminho)
        if distancia < melhor_distancia:
            melhor_distancia = distancia
            melhor_caminho = caminho

    result_queue.put((melhor_distancia, melhor_caminho))

def held_karp_paralelo():
    n = len(matriz_distancias_paralela)
    cidades = list(range(1, n))  
    permutacoes = list(itertools.permutations(cidades))
    tarefas = queue.Queue()
    resultados = queue.Queue()

    for p in permutacoes:
        tarefas.put([0] + list(p))

    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(tarefas, resultados))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    melhor_distancia = float("inf")
    melhor_caminho = []

    while not resultados.empty():
        dist, caminho = resultados.get()
        if dist < melhor_distancia:
            melhor_distancia = dist
            melhor_caminho = caminho

    melhor_caminho.append(0) 
    return melhor_distancia, melhor_caminho

def executar_held_karp_paralelo():
    tempo_inicio_paralelo = time.time()
    menor_distancia_paralela, melhor_caminho_paralela = held_karp_paralelo()
    tempo_fim_paralelo = time.time()

    print("Resultado - Held-Karp (Paralela)")
    print(f"Melhor caminho encontrado: {' -> '.join(map(str, melhor_caminho_paralela))}")
    print(f"Distância total percorrida: {menor_distancia_paralela:.2f}")
    print(f"Tempo de execução paralela: {tempo_fim_paralelo - tempo_inicio_paralelo:.6f} segundos")

if __name__ == "__main__":
    executar_held_karp_paralelo()
