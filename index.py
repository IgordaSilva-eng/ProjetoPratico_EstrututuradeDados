import datetime
import json
import os
import time

class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class ListaEncadeadaManual:
    def __init__(self):
        self.cabeca = None
        self._tamanho = 0

    def inserir_no_final(self, dado):
        novo_no = No(dado)
        if not self.cabeca:
            self.cabeca = novo_no
        else:
            atual = self.cabeca
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_no
        self._tamanho += 1

    def para_lista_python(self):
        lista = []
        atual = self.cabeca
        while atual:
            lista.append(atual.dado)
            atual = atual.proximo
        return lista

    def carregar_de_lista(self, lista_python):
        for item in lista_python:
            self.inserir_no_final(item)

def merge_sort_tarefas(lista_tarefas):
    if len(lista_tarefas) <= 1:
        return lista_tarefas
    meio = len(lista_tarefas) // 2
    esquerda = merge_sort_tarefas(lista_tarefas[:meio])
    direita = merge_sort_tarefas(lista_tarefas[meio:])
    return merge(esquerda, direita)

def merge(esquerda, direita):
    resultado = []
    i = j = 0
    prioridades = {"urgente": 0, "alta": 1, "média": 2, "baixa": 3}
    while i < len(esquerda) and j < len(direita):
        prio_esq = prioridades.get(esquerda[i]['prioridade'].lower(), 4)
        prio_dir = prioridades.get(direita[j]['prioridade'].lower(), 4)
        if prio_esq <= prio_dir:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado

def selection_sort_tarefas(lista_tarefas):
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
    def __init__(self):
        self.tarefas_encadeadas = ListaEncadeadaManual()
        self.ARQUIVO = "tarefas.json"
        self.id_contador = 1
        self.carregar_dados()

    def carregar_dados(self):
        if os.path.exists(self.ARQUIVO):
            try:
                with open(self.ARQUIVO, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.tarefas_encadeadas.carregar_de_lista(dados)
                    if dados:
                        self.id_contador = max(t['id'] for t in dados) + 1
            except:
                pass

    def salvar_dados(self):
        with open(self.ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump(self.tarefas_encadeadas.para_lista_python(), f, indent=4)

    def criar_tarefa(self, titulo, prioridade):
        tarefa = {
            "id": self.id_contador,
            "titulo": titulo,
            "prioridade": prioridade,
            "status": "pendente",
            "data_criacao": datetime.datetime.now().isoformat()
        }
        self.tarefas_encadeadas.inserir_no_final(tarefa)
        self.id_contador += 1
        print(f"✅ Tarefa '{titulo}' criada!")

    def processar_e_ordenar(self):
        inicio = time.perf_counter()
        lista_temp = self.tarefas_encadeadas.para_lista_python()
        lista_ordenada = merge_sort_tarefas(lista_temp)
        self.tarefas_encadeadas = ListaEncadeadaManual()
        self.tarefas_encadeadas.carregar_de_lista(lista_ordenada)
        fim = time.perf_counter()
        print(f"⏱️ Merge Sort concluído em {(fim - inicio)*1000:.4f} ms.")

    def ordenar_com_selection_sort(self):
        inicio = time.perf_counter()
        lista_temp = self.tarefas_encadeadas.para_lista_python()
        lista_ordenada = selection_sort_tarefas(lista_temp)
        self.tarefas_encadeadas = ListaEncadeadaManual()
        self.tarefas_encadeadas.carregar_de_lista(lista_ordenada)
        fim = time.perf_counter()
        print(f"⏱️ Selection Sort concluído em {(fim - inicio)*1000:.4f} ms.")

    def concluir_tarefa(self, id_tarefa):
        """Marca uma tarefa específica como concluída usando busca linear."""
        atual = self.tarefas_encadeadas.cabeca
        while atual:
            if atual.dado['id'] == id_tarefa:
                atual.dado['status'] = "concluída"
                print(f"✔️ Tarefa {id_tarefa} marcada como CONCLUÍDA.")
                return
            atual = atual.proximo
        print("❌ Erro: ID não encontrado.")

    def arquivar_tarefa(self, id_tarefa):
        """Altera o status para arquivado. Ela permanece na lista."""
        atual = self.tarefas_encadeadas.cabeca
        while atual:
            if atual.dado['id'] == id_tarefa:
                if atual.dado['status'] == "concluída":
                    atual.dado['status'] = "arquivada"
                    print(f"📦 Tarefa {id_tarefa} ARQUIVADA com sucesso.")
                else:
                    print("⚠️ Aviso: Apenas tarefas concluídas podem ser arquivadas.")
                return
            atual = atual.proximo
        print("❌ Erro: ID não encontrado.")

def menu():
    app = OrganizadorTarefas()
    while True:
        print("\n--- Organizador de Tarefas Acadêmico ---")
        print("1. Criar Tarefa")
        print("2. Ordenar Rápido (Merge Sort)")
        print("3. Ordenar Simples (Selection Sort)")
        print("4. Listar Todas")
        print("5. Concluir Tarefa")
        print("6. Arquivar Tarefa")
        print("7. Salvar e Sair")
        
        op = input("Escolha uma opção: ")
        
        try:
            if op == "1":
                tit = input("Título: ")
                prio = input("Prioridade (urgente/alta/média/baixa): ").lower()
                app.criar_tarefa(tit, prio)

            elif op == "2":
                app.processar_e_ordenar()

            elif op == "3":
                app.ordenar_com_selection_sort()

            elif op == "4":
                lista = app.tarefas_encadeadas.para_lista_python()
                if not lista:
                    print("📭 Nenhuma tarefa cadastrada.")
                for t in lista:
                    status_icon = "✅" if t['status'] == "concluída" else "📦" if t['status'] == "arquivada" else "⏳"
                    print(f"{status_icon} [{t['prioridade'].upper()}] ID {t['id']}: {t['titulo']} ({t['status']})")

            elif op == "5":
                id_sel = int(input("Digite o ID da tarefa para concluir: "))
                app.concluir_tarefa(id_sel)

            elif op == "6":
                id_sel = int(input("Digite o ID da tarefa para arquivar: "))
                app.arquivar_tarefa(id_sel)

            elif op == "7":
                app.salvar_dados()
                print("👋 Saindo e salvando dados...")
                break
            else:
                print("❌ Opção inválida.")
        except ValueError:
            print("❌ Erro: Por favor, digite um número válido para o ID.")

if __name__ == "__main__":
    menu()