import time
from itertools import permutations

# Matriz de distâncias entre as cidades
matriz_distancias_sequencial = [
    [  0.00, 10.77, 12.65, 19.80, 18.68, 20.88, 24.18, 25.61, 25.46, 26.08],
    [10.77,  0.00,  9.43, 10.77,  8.25, 17.46, 19.42, 14.32, 17.20, 24.33],
    [12.65,  9.43,  0.00, 10.77, 15.13,  8.00, 10.63, 20.40, 15.13, 14.42],
    [19.80, 10.77, 10.77,  0.00, 10.77,  9.22,  8.25, 12.17,  6.32, 13.89],
    [18.68,  8.25, 15.13, 10.77,  0.00, 17.46, 17.46,  6.32, 12.00, 22.63],
    [20.88, 17.46,  8.00,  9.22, 17.46,  0.00,  6.32, 20.88, 12.00,  6.32],
    [24.18, 19.42, 10.63,  8.25, 17.46,  6.32,  0.00, 18.44,  6.32, 10.00],
    [25.61, 14.32, 20.40, 12.17,  6.32, 20.88, 18.44,  0.00, 10.77, 24.83],
    [25.46, 17.20, 15.13,  6.32, 12.00, 12.00,  6.32, 10.77,  0.00, 16.12],
    [26.08, 24.33, 14.42, 13.89, 22.63,  6.32, 10.00, 24.83, 16.12,  0.00],
]

def brute_force_tsp(distancias):
    n = len(distancias)
    cidades = list(range(1, n))
    menor_distancia = float('inf')
    melhor_caminho = []

    for perm in permutations(cidades):
        caminho = [0] + list(perm) + [0]
        distancia = 0
        for i in range(n):
            distancia += distancias[caminho[i]][caminho[i+1]]
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_caminho = caminho

    return menor_distancia, melhor_caminho

def executar_brute_force_tsp():
    tempo_inicio = time.time()
    menor_distancia, melhor_caminho = brute_force_tsp(matriz_distancias_sequencial)
    tempo_fim = time.time()

    print("Resultado - TSP (Brute Force)")
    print(f"Melhor caminho encontrado: {' -> '.join(map(str, melhor_caminho))}")
    print(f"Distância total percorrida: {menor_distancia:.2f}")
    print(f"Tempo de execução brute force: {tempo_fim - tempo_inicio:.6f} segundos")

# Executa o algoritmo e mostra os resultados
executar_brute_force_tsp()
