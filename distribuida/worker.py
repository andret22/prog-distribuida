import asyncio
import websockets
import json
from itertools import permutations

def brute_force_worker(matriz, caminho_inicial):
    n = len(matriz)
    start, next_city = caminho_inicial
    cidades_restantes = [i for i in range(n) if i not in caminho_inicial]
    custo_min = float('inf')
    melhor_caminho = []

    # Permutação entre os caminhos possível dentro do subproblema
    for perm in permutations(cidades_restantes):
        caminho = caminho_inicial + list(perm) + [start]
        custo = sum(matriz[caminho[i]][caminho[i+1]] for i in range(len(caminho)-1))
        # Verificação se o caminha é o melhor
        if custo < custo_min:
            custo_min = custo
            melhor_caminho = caminho

    return {"distancia": custo_min, "caminho": melhor_caminho}


# Handler de comunicação websocket
async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)
        matriz = data["matriz"]
        caminho_inicial = data["caminho_inicial"]
        resultado = brute_force_worker(matriz, caminho_inicial)
        await websocket.send(json.dumps(resultado))


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
