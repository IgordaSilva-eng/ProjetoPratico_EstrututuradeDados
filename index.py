def selection_sort_tarefas(lista_tarefas):
    """
    Implementação manual do Selection Sort (O(n²)).
    Ideal para demonstrar operações custosas em grandes volumes.
    """
    n = len(lista_tarefas)
    prioridades = {"urgente": 0, "alta": 1, "média": 2, "baixa": 3}

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            prio_j = prioridades.get(lista_tarefas[j]['prioridade'].lower(), 4)
            prio_min = prioridades.get(lista_tarefas[min_idx]['prioridade'].lower(), 4)
            
            if prio_j < prio_min:
                min_idx = j
        
        lista_tarefas[i], lista_tarefas[min_idx] = lista_tarefas[min_idx], lista_tarefas[i]
    
    return lista_tarefas


class OrganizadorTarefas:

    def ordenar_com_selection_sort(self):
        """Executa a ordenação O(n²) e registra a telemetria[cite: 115]."""
        inicio = time.perf_counter()
        
        lista_temp = self.tarefas_encadeadas.para_lista_python()
        lista_ordenada = selection_sort_tarefas(lista_temp)
        
        self.tarefas_encadeadas = ListaEncadeadaManual()
        self.tarefas_encadeadas.carregar_de_lista(lista_ordenada)
        
        fim = time.perf_counter()
        latencia = (fim - inicio) * 1000
        print(f"⏱️ Telemetria (Selection Sort): Concluído em {latencia:.4f} ms.")


def menu():
    app = OrganizadorTarefas()
    while True:
        print("\n--- Organizador de Tarefas Acadêmico ---")
        print("1. Criar Tarefa")
        print("2. Ordenar Rápido (Merge Sort - O(n log n))")
        print("3. Ordenar Simples (Selection Sort - O(n²))") # Novo requisito atendido
        print("4. Listar Todas")
        print("5. Salvar e Sair")
        
        op = input("Escolha: ")
        if op == "1":
            tit = input("Título: ")
            prio = input("Prioridade (urgente/alta/média/baixa): ").lower()
            app.criar_tarefa(tit, prio)
        elif op == "2":
            app.processar_e_ordenar() # Merge Sort
        elif op == "3":
            app.ordenar_com_selection_sort() # Selection Sort
        elif op == "4":
            for t in app.tarefas_encadeadas.para_lista_python():
                print(f"[{t['prioridade'].upper()}] ID {t['id']}: {t['titulo']}")
        elif op == "5":
            app.salvar_dados()
            break