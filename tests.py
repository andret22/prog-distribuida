import unittest
from sequencial.sequencial import held_karp_sequencial
from distribuida.worker import brute_force_worker
from distribuida.distributed import gerar_subproblemas
from paralela.parallel import brute_force_paralelo

matriz_distancias = [
    [0.00, 10.77, 12.65, 19.80, 18.68, 20.88, 24.18, 25.61, 25.46, 26.08],
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
best_distance = 87.12


class TestSequentionTSP(unittest.TestCase):
    def test_sequential_result(self):
        menor_distancia_sequencial, melhor_caminho_sequencial = held_karp_sequencial(matriz_distancias)
        self.assertEqual(round(menor_distancia_sequencial, 2), best_distance)
        self.assertEqual(melhor_caminho_sequencial, [0, 2, 5, 9, 6, 8, 3, 7, 4, 1, 0])


class TestDistributedTSPMaster(unittest.TestCase):
    def test_subproblem_generation(self):
        n_cidades = 4
        expected = [[0, 1], [0, 2], [0, 3]]
        result = gerar_subproblemas(n_cidades)
        assert result == expected


class TestDistributedTSPWorker(unittest.TestCase):
    def test_brute_force_worker(self):
        matriz = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]
        caminho_inicial = [0, 1]
        result = brute_force_worker(matriz, caminho_inicial)
        self.assertEqual(result["distancia"], 80)
        self.assertEqual(result["caminho"], [0, 1, 3, 2, 0])


class TestParallelTSP(unittest.TestCase):
    def test_parallel_result(self):
        menor_distancia_paralela, melhor_caminho_paralela = brute_force_paralelo()
        self.assertEqual(round(menor_distancia_paralela, 2), best_distance)
        self.assertEqual(melhor_caminho_paralela, [0, 2, 5, 9, 6, 8, 3, 7, 4, 1, 0])


if __name__ == '__main__':
    unittest.main()




