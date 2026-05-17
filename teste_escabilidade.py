import random
import time

# A importação agora aponta para core.py, onde os algoritmos estão isolados
from core import merge_sort_tarefas, selection_sort_tarefas

def executar_comparativo_estatistico():
    # Volume reduzido para uso web síncrono (evita travamento do navegador)
    volumes = [10000] 
    prioridades = ["urgente", "alta", "média", "baixa"]
    
    for qtd in volumes:
        massa = [{"id": i, "titulo": "T", "prioridade": random.choice(prioridades)} for i in range(qtd)]
        
        copia_m = massa.copy()
        t0 = time.perf_counter()
        merge_sort_tarefas(copia_m)
        t_merge = (time.perf_counter() - t0) * 1000

        copia_s = massa.copy()
        t1 = time.perf_counter()
        selection_sort_tarefas(copia_s)
        t_selection = (time.perf_counter() - t1) * 1000

        # Retorna os dados em formato de dicionário em vez de usar print()
        return {
            "volume": qtd,
            "tempo_merge": round(t_merge, 2),
            "tempo_selection": round(t_selection, 2)
        }