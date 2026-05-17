from flask import Flask, render_template, request, redirect, url_for
from core import OrganizadorTarefas
from teste_escabilidade import executar_comparativo_estatistico

app = Flask(__name__)
organizador = OrganizadorTarefas()

@app.route('/')
def index():
    tarefas = organizador.listar_tarefas()
    return render_template('index.html', tarefas=tarefas)

@app.route('/criar', methods=['POST'])
def criar():
    titulo = request.form.get('titulo')
    disciplina = request.form.get('disciplina')
    prazo = request.form.get('prazo')
    prioridade = request.form.get('prioridade')
    
    organizador.criar_tarefa(titulo, prioridade, disciplina, prazo)
    organizador.salvar_dados()
    
    return redirect(url_for('index'))

@app.route('/concluir/<int:id_tarefa>')
def concluir(id_tarefa):
    organizador.concluir_tarefa(id_tarefa)
    organizador.salvar_dados()
    return redirect(url_for('index'))

@app.route('/executar-teste')
def executar_teste():
    dados_dashboard = executar_comparativo_estatistico()
    tarefas = organizador.listar_tarefas()
    return render_template('index.html', tarefas=tarefas, dashboard=dados_dashboard)

if __name__ == '__main__':
    app.run(debug=True)