from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Lista para armazenar as pessoas e peculiaridades
pessoas = []
restricoes = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_pessoa', methods=['POST'])
def add_pessoa():
    nome = request.form['nome']
    if nome not in pessoas:
        pessoas.append(nome)
        restricoes[nome] = []
    return jsonify({'status': 'success', 'pessoas': pessoas})

@app.route('/add_restricao', methods=['POST'])
def add_restricao():
    pessoa = request.form['pessoa']
    restricao = request.form['restricao']
    if pessoa in pessoas and restricao in pessoas:
        restricoes[pessoa].append(restricao)
    return jsonify({'status': 'success', 'restricoes': restricoes})

@app.route('/sortear', methods=['GET'])
def sortear():
    if len(pessoas) < 2:
        return jsonify({'status': 'error', 'message': 'É necessário pelo menos 2 pessoas para o sorteio.'})

    sorteio = {}
    disponiveis = set(pessoas)

    for pessoa in pessoas:
        elegiveis = list(disponiveis - set(restricoes.get(pessoa, [])) - {pessoa})
        if not elegiveis:
            return jsonify({'status': 'error', 'message': f'Não é possível sortear para {pessoa} devido às restrições.'})

        escolhido = random.choice(elegiveis)
        sorteio[pessoa] = escolhido
        disponiveis.remove(escolhido)

    return jsonify({'status': 'success', 'sorteio': sorteio})

if __name__ == '__main__':
    app.run(debug=True)
