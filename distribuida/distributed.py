import asyncio
import time
import websockets
import json

matriz_distancias = [
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

def gerar_subproblemas(n_cidades):
    return [[0, i] for i in range(1, n_cidades)]

async def main():
    workers = [
        "ws://worker1:8765",
        "ws://worker2:8765",
        "ws://worker3:8765",
        "ws://worker4:8765",
        "ws://worker5:8765",
        "ws://worker6:8765",
    ]
    subproblemas = gerar_subproblemas(len(matriz_distancias))
    resultados = []

    tempo_inicio = time.time()

    async def enviar_tarefa(worker_url, tarefa):
        async with websockets.connect(worker_url) as ws:
            await ws.send(json.dumps({
                "matriz": matriz_distancias,
                "caminho_inicial": tarefa
            }))
            resposta = await ws.recv()
            return json.loads(resposta)

    tasks = [
        enviar_tarefa(workers[i % len(workers)], subproblemas[i])
        for i in range(len(subproblemas))
    ]
    resultados = await asyncio.gather(*tasks)

    melhor = min(resultados, key=lambda x: x["distancia"])
    tempo_fim = time.time()

    print("Resultado - Held-Karp (Distribuída)")
    print(f"Melhor caminho encontrado: {' -> '.join(map(str, melhor['caminho']))}")
    print(f"Distância total percorrida: {melhor['distancia']:.2f}")
    print(f"Tempo de execução distribuída: {tempo_fim - tempo_inicio:.6f} segundos")

if __name__ == "__main__":
    asyncio.run(main())