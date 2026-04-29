# 🚀 Organizador de Tarefas Académico

Este projeto foi desenvolvido como parte da **Missão Prática da disciplina de Estruturas de Dados I**. O objetivo é construir uma aplicação funcional que utilize estruturas de dados manuais para analisar o impacto da complexidade algorítmica no desempenho do sistema.

## 🛠️ Tecnologias e Conceitos Aplicados
Para cumprir o rigor técnico da disciplina, o sistema evita o uso de funções nativas de alto nível (como `.sort()` ou listas dinâmicas prontas) e foca na implementação base:

- **Linguagem:** Python 3.10+
- **Estrutura de Dados:** Lista Encadeada Simples (Implementação Manual via Classes e Nós).
- **Persistência:** Serialização de dados em formato JSON.
- **Algoritmos de Ordenação:**
  - **Merge Sort:** Algoritmo eficiente com complexidade $O(n \log n)$.
  - **Selection Sort:** Algoritmo de comparação com complexidade $O(n^2)$.

## 📋 Funcionalidades Principais
1. **Criação de Tarefas:** Registo de atividades com título e prioridade (Urgente, Alta, Média, Baixa).
2. **Motores de Ordenação:** Dois botões distintos para ordenar a fila de tarefas, permitindo comparar a performance.
3. **Telemetria Integrada:** O sistema calcula e exibe o tempo exato (em milissegundos) que cada algoritmo levou para processar os dados.
4. **Persistência:** Carregamento automático de tarefas existentes no ficheiro `tarefas.json`.

## 📊 Análise de Escalabilidade e Performance
O repositório inclui um script de teste de estresse (`teste_escabilidade.py`) para validar as curvas de complexidade computacional.



Ao gerar volumes massivos de dados (ex: 5.000+ tarefas), é possível observar visualmente a eficiência do **Merge Sort** em relação ao **Selection Sort**, comprovando a teoria aprendida em aula através de telemetria real.

## 🚀 Como Executar

### Pré-requisitos
* Python instalado (versão 3.10 ou superior).
* Todos os ficheiros (`index.py` e `teste_escabilidade.py`) devem estar na mesma pasta.

### Passo 1: Aplicação Principal
Executa o menu interativo para gerir as tuas tarefas manualmente:
```bash
python index.py