# 🚀 Gerenciador de Tarefas Acadêmico

Este projeto foi desenvolvido como parte da **Missão Prática da disciplina de Estruturas de Dados I**. O objetivo é construir uma aplicação web funcional utilizando estruturas de dados e algoritmos de ordenação implementados manualmente, permitindo analisar e comparar o impacto da complexidade algorítmica no desempenho do sistema através de telemetria em tempo real.

## 🛠️ Tecnologias e Conceitos Aplicados

Para cumprir o rigor técnico exigido, o sistema evita o uso de funções nativas de alto nível (como métodos `.sort()` ou listas dinâmicas prontas do Python) e foca na implementação base de estruturas de dados lineares:

- **Back-end:** Python 3.10+ com o micro-framework **Flask**.
- **Front-end:** Interface web construída com HTML5 e CSS3 customizado.
- **Estruturas de Dados (Implementação Manual em `core.py`):**
  - **Lista Encadeada Simples:** Utilizada para o armazenamento, leitura e manipulação das tarefas em memória.
  - **Pilha:** Utilizada para gerenciar a operação de "Desfazer" (*Undo*) da última ação realizada.
  - **Fila:** Utilizada para o motor de sugestão sequencial da próxima tarefa pendente.
- **Persistência de Dados:** Serialização de objetos em arquivo local no formato `JSON`.
- **Algoritmos de Ordenação Manual:**
  - **Merge Sort:** Algoritmo de divisão e conquista com complexidade estável de $O(n \log n)$.
  - **Selection Sort:** Algoritmo por seleção com complexidade de $O(n^2)$.

## 📋 Funcionalidades do Sistema

1. **Cadastro de Tarefas:** Registro de atividades contendo título, disciplina, prazo de entrega e nível de prioridade (Urgente, Alta, Média, Baixa).
2. **Controle de Estado:** Permite marcar tarefas como concluídas e gerenciar as pendências através da interface.
3. **Mecanismo de Undo:** Pilha interna que permite reverter a última conclusão de tarefa realizada através da rota `/desfazer`.
4. **Fila de Sugestões:** Algoritmo que indica ao estudante qual a próxima tarefa pendente a ser executada com base na ordem de prioridades.
5. **Painel de Telemetria (`teste_escabilidade.py`):** Executa testes estatísticos com um volume massivo de 10.000 tarefas simultâneas para medir e exibir o tempo exato de execução (em milissegundos) de cada algoritmo de ordenação diretamente no dashboard.

## 🚀 Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o Python 3.10 ou superior instalado em sua máquina.

### 1. Clonar o Repositório e Acessar o Diretório

```bash
git clone <url-do-seu-repositorio>
cd <nome-do-diretorio-do-projeto>
```
### 2. Instalar as Dependências

Este projeto utiliza o micro-framework **Flask**. Instale-o utilizando o gerenciador de pacotes `pip`:

```bash
pip install flask
```


### 3. Iniciar a Aplicação Web

O ponto de entrada do servidor web é o arquivo `main.py`. Execute o seguinte comando no seu terminal:

```bash
python main.py
```


Após a inicialização, o Flask disponibilizará o servidor local. Abra o seu navegador e acesse o endereço:
[http://127.0.0.1:5000](https://www.google.com/search?q=http://127.0.0.1:5000)

### 4. Executar os Testes de Escalabilidade e Desempenho

Dentro da interface web da aplicação, localize e utilize a opção de executar o teste de estresse (rota `/executar-teste`). O sistema acionará o script `teste_escabilidade.py` em segundo plano, rodando a simulação de ordenação com 10.000 registros e renderizando os tempos comparativos do **Merge Sort** contra o **Selection Sort** na tela.

## 📁 Estrutura de Arquivos do Projeto

* `main.py`: Inicialização do servidor Flask e gerenciamento de todas as rotas HTTP (`/`, `/criar`, `/concluir/<id>`, `/desfazer`, `/sugerir`, `/executar-teste`).
* `core.py`: Contém as implementações puras e manuais de `No`, `ListaEncadeadaManual`, `FilaManual`, `PilhaManual` e os algoritmos de ordenação (`merge_sort_tarefas` e `selection_sort_tarefas`).
* `teste_escabilidade.py`: Script responsável por gerar a massa de dados fictícia e cronometrar o desempenho computacional dos algoritmos.
* `templates/index.html`: Interface visual que consome o back-end, exibe as listas de tarefas e renderiza o dashboard de telemetria.
* `static/style.css`: Estilização estruturada e identidade visual da aplicação web.


