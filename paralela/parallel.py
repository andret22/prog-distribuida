import threading
import itertools
import queue
from typing import List, Tuple


distance_matrix = [
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


def calcular_distancia(path: List[int]) -> float:
    distancia = 0
    for i in range(len(path) - 1):
        distancia += distance_matrix[path[i]][path[i + 1]]
    distancia += distance_matrix[path[-1]][path[0]]  
    return distancia


def tsp_worker(permutations_queue: queue.Queue, result_queue: queue.Queue):
    melhor_caminho = []
    menor_distancia = float("inf")

    while not permutations_queue.empty():
        try:
            path = permutations_queue.get_nowait()
        except queue.Empty:
            break
        distancia = calcular_distancia(path)
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_caminho = path

    result_queue.put((menor_distancia, melhor_caminho))


def held_karp_paralelo():
    n = len(distance_matrix)
    cidades = list(range(1, n))  
    permutations = list(itertools.permutations(cidades))
    permutations_queue = queue.Queue()
    result_queue = queue.Queue()

    
    for p in permutations:
        permutations_queue.put([0] + list(p))

    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=tsp_worker, args=(permutations_queue, result_queue))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    menor_distancia = float("inf")
    melhor_caminho = []
    while not result_queue.empty():
        dist, caminho = result_queue.get()
        if dist < menor_distancia:
            menor_distancia = dist
            melhor_caminho = caminho + [0]

    return menor_distancia, melhor_caminho
