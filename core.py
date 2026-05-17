# core.py
import datetime
import json
import os
import time

# --- ESTRUTURAS DE DADOS MANUAIS ---
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

class FilaManual:
    """Implementação FIFO para gerenciar a ordem de execução das tarefas."""
    def __init__(self):
        self.frente = None
        self.tras = None

    def enqueue(self, tarefa):
        novo_no = No(tarefa)
        if self.tras is None:
            self.frente = self.tras = novo_no
            return
        self.tras.proximo = novo_no
        self.tras = novo_no

    def dequeue(self):
        if self.frente is None:
            return None
        temp = self.frente
        self.frente = self.frente.proximo
        if self.frente is None:
            self.tras = None
        return temp.dado

class PilhaManual:
    """Implementação LIFO para o sistema de 'Desfazer' (Undo)."""
    def __init__(self):
        self.topo = None

    def push(self, acao):
        novo_no = No(acao)
        novo_no.proximo = self.topo
        self.topo = novo_no

    def pop(self):
        if self.topo is None:
            return None
        temp = self.topo
        self.topo = self.topo.proximo
        return temp.dado

# --- ALGORITMOS DE ORDENAÇÃO ---
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

# --- CLASSE PRINCIPAL ---
class OrganizadorTarefas:
    def __init__(self):
        self.tarefas_encadeadas = ListaEncadeadaManual()
        self.pilha_undo = PilhaManual()
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

    def criar_tarefa(self, titulo, prioridade, disciplina, prazo):
        tarefa = {
            "id": self.id_contador,
            "titulo": titulo,
            "disciplina": disciplina,
            "prazo": prazo,
            "prioridade": prioridade,
            "status": "pendente",
            "data_criacao": datetime.datetime.now().isoformat()
        }
        self.tarefas_encadeadas.inserir_no_final(tarefa)
        self.pilha_undo.push({"tipo": "criacao", "id": self.id_contador})
        self.id_contador += 1
        return f" Tarefa '{titulo}' de {disciplina} (Entrega: {prazo}) criada!"

    def processar_e_ordenar(self):
        inicio = time.perf_counter()
        lista_temp = self.tarefas_encadeadas.para_lista_python()
        lista_ordenada = merge_sort_tarefas(lista_temp)
        self.tarefas_encadeadas = ListaEncadeadaManual()
        self.tarefas_encadeadas.carregar_de_lista(lista_ordenada)
        fim = time.perf_counter()
        return f" Merge Sort concluído em {(fim - inicio)*1000:.4f} ms."

    def listar_tarefas(self):
        """Retorna a lista de tarefas para a interface renderizar."""
        return self.tarefas_encadeadas.para_lista_python()

    def concluir_tarefa(self, id_tarefa):
        atual = self.tarefas_encadeadas.cabeca
        while atual:
            if atual.dado['id'] == id_tarefa:
                atual.dado['status'] = "concluída"
                self.pilha_undo.push({"tipo": "conclusao", "id": id_tarefa})
                return f"✔️ Tarefa {id_tarefa} marcada como CONCLUÍDA."
            atual = atual.proximo
        return " Erro: ID não encontrado."

    def sugerir_proxima_tarefa(self):
        fila_execucao = FilaManual()
        atual = self.tarefas_encadeadas.cabeca
        while atual:
            if atual.dado['status'] == "pendente":
                fila_execucao.enqueue(atual.dado)
            atual = atual.proximo
        
        # Retorna o dicionário da tarefa ou None. A interface decide o que imprimir.
        return fila_execucao.dequeue() 

    def desfazer_ultima_acao(self):
        ultima_acao = self.pilha_undo.pop()
        if not ultima_acao:
            return " Nada para desfazer."

        if ultima_acao['tipo'] == "conclusao":
            atual = self.tarefas_encadeadas.cabeca
            while atual:
                if atual.dado['id'] == ultima_acao['id']:
                    atual.dado['status'] = "pendente"
                    return f" Desfeito: Tarefa {ultima_acao['id']} voltou para PENDENTE."
                atual = atual.proximo
        else:
            return " Ação de criação não pode ser revertida nesta versão."