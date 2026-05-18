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
        if not self.tras:
            self.frente = self.tras = novo_no
            return
        self.tras.proximo = novo_no
        self.tras = novo_no

    def dequeue(self):
        if not self.frente:
            return None
        temp = self.frente
        self.frente = self.frente.proximo
        if not self.frente:
            self.tras = None
        return temp.dado

class PilhaManual:
    """Implementação LIFO para gerenciar o histórico de ações (Undo)."""
    def __init__(self):
        self.topo = None

    def push(self, acao):
        novo_no = No(acao)
        novo_no.proximo = self.topo
        self.topo = novo_no

    def pop(self):
        if not self.topo:
            return None
        temp = self.topo
        self.topo = self.topo.proximo
        return temp.dado

# --- ALGORITMOS DE ORDENAÇÃO MANUAIS ---
def mapear_prioridade(p):
    pesos = {"urgente": 4, "alta": 3, "média": 2, "baixa": 1}
    return pesos.get(p.lower(), 0)

def merge_sort_tarefas(lista):
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esq = merge_sort_tarefas(lista[:meio])
    dir = merge_sort_tarefas(lista[meio:])
    
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        if mapear_prioridade(esq[i]['prioridade']) >= mapear_prioridade(dir[j]['prioridade']):
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1
    resultado.extend(esq[i:])
    resultado.extend(dir[j:])
    return resultado

def selection_sort_tarefas(lista):
    n = len(lista)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if mapear_prioridade(lista[j]['prioridade']) > mapear_prioridade(lista[max_idx]['prioridade']):
                max_idx = j
        lista[i], lista[max_idx] = lista[max_idx], lista[i]
    return lista

# --- CONTROLADOR CENTRAL ---
class OrganizadorTarefas:
    def __init__(self, arquivo_dados="tarefas.json"):
        self.arquivo_dados = arquivo_dados
        self.tarefas_encadeadas = ListaEncadeadaManual()
        self.pilha_undo = PilhaManual()
        self.proximo_id = 1
        self.carregar_dados()

    def criar_tarefa(self, titulo, prioridade, disciplina, prazo):
        tarefa = {
            "id": self.proximo_id,
            "titulo": titulo,
            "prioridade": prioridade,
            "disciplina": disciplina,
            "prazo": prazo,
            "status": "pendente",
            "data_criacao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tarefas_encadeadas.inserir_no_final(tarefa)
        self.proximo_id += 1
        return tarefa

    def listar_tarefas(self):
        return self.tarefas_encadeadas.para_lista_python()

    def processar_e_ordenar(self, algoritmo="merge"):
        lista_temp = self.listar_tarefas()
        t0 = time.perf_counter()
        
        if algoritmo == "selection":
            lista_ordenada = selection_sort_tarefas(lista_temp)
        else:
            lista_ordenada = merge_sort_tarefas(lista_temp)
            
        tempo_gasto = (time.perf_counter() - t0) * 1000
        
        # Reconstrói a lista encadeada interna ordenada
        self.tarefas_encadeadas = ListaEncadeadaManual()
        self.tarefas_encadeadas.carregar_de_lista(lista_ordenada)
        return round(tempo_gasto, 4)

    def concluir_tarefa(self, id_tarefa):
        atual = self.tarefas_encadeadas.cabeca
        while atual:
            if atual.dado['id'] == id_tarefa:
                atual.dado['status'] = "concluída"
                self.pilha_undo.push({"tipo": "conclusao", "id": id_tarefa})
                return True
            atual = atual.proximo
        return False

    def sugerir_proxima_tarefa(self):
        fila_execucao = FilaManual()
        atual = self.tarefas_encadeadas.cabeca
        while atual:
            if atual.dado['status'] == "pendente":
                fila_execucao.enqueue(atual.dado)
            atual = atual.proximo
        return fila_execucao.dequeue()

    def desfazer_ultima_acao(self):
        ultima_acao = self.pilha_undo.pop()
        if not ultima_acao:
            return False

        if ultima_acao['tipo'] == "conclusao":
            atual = self.tarefas_encadeadas.cabeca
            while atual:
                if atual.dado['id'] == ultima_acao['id']:
                    atual.dado['status'] = "pendente"
                    return True
                atual = atual.proximo
        return False

    def salvar_dados(self):
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(self.listar_tarefas(), f, ensure_ascii=False, indent=4)

    def carregar_dados(self):
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    if dados:
                        self.tarefas_encadeadas.carregar_de_lista(dados)
                        self.proximo_id = max(t['id'] for t in dados) + 1
            except Exception:
                pass