# 🚀 Organizador de Tarefas Acadêmico — Análise de Performance

Este projeto foi desenvolvido como parte da **Missão Prática da disciplina de Estruturas de Dados I**. O objetivo é construir uma aplicação funcional que utilize estruturas de dados manuais e analise o impacto da complexidade algorítmica no desempenho do sistema.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.x
- **Estruturas de Dados:** Lista Encadeada Simples (Implementação Manual)
- **Persistência:** JSON para armazenamento de dados

## 📋 Funcionalidades Principal (Fase 2)
- **Criação de Tarefas:** Registro de atividades com títulos e níveis de prioridade.
- **Ordenação por Prioridade:** Implementação de dois motores de ordenação manuais:
  - **Merge Sort:** Algoritmo eficiente com complexidade $O(n \log n)$.
  - **Selection Sort:** Algoritmo de comparação com complexidade $O(n^2)$.
- **Telemetria:** Monitoramento em tempo real do tempo de processamento (latência) de cada operação de ordenação.

## 📊 Análise de Escalabilidade (Fase 3)
O projeto inclui um script de estresse (`teste_escabilidade.py`) projetado para gerar grandes volumes de dados e validar as curvas de complexidade computacional.
- **Objetivo:** Observar como o tempo de processamento cresce à medida que o volume de dados ($n$) aumenta, comparando a eficiência teórica com a prática.

## 🚀 Como Executar

1. **Aplicação Principal:**
   ```bash
   python index.py