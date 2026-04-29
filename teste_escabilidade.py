import random
import time
from index import OrganizadorTarefas, merge_sort_tarefas, selection_sort_tarefas

def executar_stress_test(quantidade):
    print(f"\n🚀 Iniciando Teste de Estresse com {quantidade} tarefas...")
    
    prioridades = ["urgente", "alta", "média", "baixa"]
    massa_dados = []

    # Gerando dados aleatórios
    for i in range(quantidade):
        massa_dados.append({
            "id": i,
            "titulo": f"Tarefa Aleatória {i}",
            "prioridade": random.choice(prioridades)
        })

    # --- Teste 1: Merge Sort (O(n log n)) ---
    dados_merge = massa_dados.copy()
    inicio = time.perf_counter()
    merge_sort_tarefas(dados_merge)
    fim = time.perf_counter()
    tempo_merge = (fim - inicio) * 1000
    print(f"✅ Merge Sort: {tempo_merge:.2f} ms")

    # --- Teste 2: Selection Sort (O(n²)) ---
    dados_selection = massa_dados.copy()
    inicio = time.perf_counter()
    selection_sort_tarefas(dados_selection)
    fim = time.perf_counter()
    tempo_selection = (fim - inicio) * 1000
    print(f"⚠️ Selection Sort: {tempo_selection:.2f} ms")

    print(f"\n📊 Resultado: O Merge Sort foi {tempo_selection/tempo_merge:.1f}x mais rápido!")

if __name__ == "__main__":
    qtd = int(input("Quantas tarefas deseja gerar para o teste? (Sugestão: 5000): "))
    executar_stress_test(qtd)