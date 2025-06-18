import time
from itertools import combinations

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

def held_karp_sequencial(distancias_sequencial):
    quantidade_cidades_sequencial = len(distancias_sequencial)
    custo_minimo_sequencial = {}

    for destino_sequencial in range(1, quantidade_cidades_sequencial):
        custo_minimo_sequencial[(1 << destino_sequencial, destino_sequencial)] = (
            distancias_sequencial[0][destino_sequencial],
            [0, destino_sequencial]
        )

    for tamanho_sequencial in range(2, quantidade_cidades_sequencial):
        for subconjunto_sequencial in combinations(range(1, quantidade_cidades_sequencial), tamanho_sequencial):
            bits_sequencial = 0
            for cidade_sequencial in subconjunto_sequencial:
                bits_sequencial |= 1 << cidade_sequencial

            for destino_sequencial in subconjunto_sequencial:
                bits_anteriores_sequencial = bits_sequencial & ~(1 << destino_sequencial)
                resultados_sequencial = []

                for intermedia_sequencial in subconjunto_sequencial:
                    if intermedia_sequencial == destino_sequencial:
                        continue
                    custo_anterior_sequencial, caminho_anterior_sequencial = custo_minimo_sequencial[(bits_anteriores_sequencial, intermedia_sequencial)]
                    novo_custo_sequencial = custo_anterior_sequencial + distancias_sequencial[intermedia_sequencial][destino_sequencial]
                    resultados_sequencial.append((novo_custo_sequencial, caminho_anterior_sequencial + [destino_sequencial]))

                custo_minimo_sequencial[(bits_sequencial, destino_sequencial)] = min(resultados_sequencial)

    todos_visitados_sequencial = (2 ** quantidade_cidades_sequencial - 1) - 1
    resultados_finais_sequencial = []

    for destino_sequencial in range(1, quantidade_cidades_sequencial):
        custo_final_sequencial, caminho_final_sequencial = custo_minimo_sequencial[(todos_visitados_sequencial, destino_sequencial)]
        custo_total_sequencial = custo_final_sequencial + distancias_sequencial[destino_sequencial][0]
        resultados_finais_sequencial.append((custo_total_sequencial, caminho_final_sequencial + [0]))

    return min(resultados_finais_sequencial)

def executar_held_karp_sequencial():
    tempo_inicio_sequencial = time.time()
    menor_distancia_sequencial, melhor_caminho_sequencial = held_karp_sequencial(matriz_distancias_sequencial)
    tempo_fim_sequencial = time.time()

    print("Resultado - Held-Karp (Sequencial)")
    print(f"Melhor caminho encontrado: {' -> '.join(map(str, melhor_caminho_sequencial))}")
    print(f"Distância total percorrida: {menor_distancia_sequencial:.2f}")
    print(f"Tempo de execução sequencial: {tempo_fim_sequencial - tempo_inicio_sequencial:.6f} segundos")

executar_held_karp_sequencial()