# main.py
from flask import Flask, render_template, request, redirect, url_for, flash
from core import OrganizadorTarefas
from teste_escabilidade import executar_comparativo_estatistico

app = Flask(__name__)
app.secret_key = "chave_segura_ED1"
organizador = OrganizadorTarefas()

@app.route('/')
def index():
    tarefas = organizador.listar_tarefas()
    sugestao = organizador.sugerir_proxima_tarefa()
    return render_template('index.html', tarefas=tarefas, sugestao=sugestao)

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

@app.route('/ordenar/<string:algoritmo>')
def ordenar(algoritmo):
    if algoritmo in ['merge', 'selection']:
        tempo = organizador.processar_e_ordenar(algoritmo)
        organizador.salvar_dados()
        flash(f"Lista de tarefas reais ordenada via {algoritmo.upper()} em {tempo} ms!", "success")
    return redirect(url_for('index'))

@app.route('/desfazer')
def desfazer():
    sucesso = organizador.desfazer_ultima_acao()
    if sucesso:
        organizador.salvar_dados()
        flash("Última conclusão de tarefa desfeita com sucesso!", "success")
    else:
        flash("Nenhuma ação para desfazer na pilha.", "error")
    return redirect(url_for('index'))

@app.route('/executar-teste')
def executar_teste():
    dados_dashboard = executar_comparativo_estatistico()
    tarefas = organizador.listar_tarefas()
    sugestao = organizador.sugerir_proxima_tarefa()
    return render_template('index.html', tarefas=tarefas, dashboard=dados_dashboard, sugestao=sugestao)

if __name__ == '__main__':
    app.run(debug=True)