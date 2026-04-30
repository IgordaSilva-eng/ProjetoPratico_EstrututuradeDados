import random
import time
import sys

from index import merge_sort_tarefas, selection_sort_tarefas

def executar_comparativo_estatistico():
    # Volumes graduais para mostrar a curva de crescimento
    volumes = [8000, 10000, 15000, 25000] 
    prioridades = ["urgente", "alta", "média", "baixa"]
    
    print("="*50)
    print("RELATORIO DE TELEMETRIA E ESCALABILIDADE")
    print("="*50)
    print(f"{'Volume (n)':<12} | {'Merge Sort':<15} | {'Selection Sort':<15}")
    print("-" * 50)

    for qtd in volumes:
        # Gerar massa de dados única para ambos os testes
        massa = [{"id": i, "titulo": "T", "prioridade": random.choice(prioridades)} for i in range(qtd)]
        
        # Teste Merge Sort (O(n log n))
        copia_m = massa.copy()
        t0 = time.perf_counter()
        merge_sort_tarefas(copia_m)
        t_merge = (time.perf_counter() - t0) * 1000

        # Teste Selection Sort (O(n^2))
        copia_s = massa.copy()
        t1 = time.perf_counter()
        selection_sort_tarefas(copia_s)
        t_selection = (time.perf_counter() - t1) * 1000

        print(f"{qtd:<12} | {t_merge:>10.2f} ms | {t_selection:>10.2f} ms")

    print("="*50)
    print("CONCLUSAO TECNICA:")
    print("O Selection Sort cresce quadraticamente.")
    print("Para volumes maiores, a diferenca sera exponencial.")
    print("="*50)

if __name__ == "__main__":
    executar_comparativo_estatistico()