from flask import Flask, render_template, request, jsonify, redirect, url_for
# import json
import os
import calendar
import datetime
import string
import random

# Obter o diretório atual do arquivo app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Definir o caminho para a pasta de templates
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'template')  # Volta um nível e entra em 'template'

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# Simulando um banco de dados em memória (em produção, use um banco real)
agenda_data = []


def gera_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def validar_data(data_str, formato="%d/%m/%Y"):
    """Valida se a data está no formato correto"""
    try:
        datetime.datetime.strptime(data_str, formato)
        return True
    except ValueError:
        return False


def validar_hora(hora_str, formato="%H:%M"):
    """Valida se a hora está no formato correto"""
    try:
        datetime.datetime.strptime(hora_str, formato)
        return True
    except ValueError:
        return False


def cal():
    """Página principal com calendário e lista de compromissos"""
    # Gerando calendário do mês atual
    data = datetime.datetime.now()
    ano = data.year
    mes = data.month

    meses_do_ano = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
        7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    mes_extenso = meses_do_ano[mes]
    calendario = calendar.month(ano, mes)
    compromissos = [
        {'data': '2025-05-30', 'hora': '10:00', 'descricao': 'Reunião de equipe'},
        {'data': '2025-06-15', 'hora': '14:30', 'descricao': 'Consulta médica'},
        {'data': '2025-06-20', 'hora': '09:00', 'descricao': 'Apresentação de projeto'}
    ]

    return calendario, mes_extenso, ano, compromissos


@app.route('/')
def index():
    calendario, mes_extenso, ano, compromissos = cal()
    return render_template('index.html',
                           calendario_html=calendario,
                           mes_extenso=mes_extenso,
                           ano=ano,
                           compromissos=compromissos)


"""def get_html_template():
    # Retorna o HTML como string para evitar problemas com templates

@app.route('/api/compromissos', methods=['GET'])
def listar_compromissos():
    #API para listar todos os compromissos
    return jsonify(agenda_data)

@app.route('/api/compromissos', methods=['POST'])
def agendar_compromisso():
    #API para criar um novo compromisso
    data = request.json

    # Validações
    if not validar_data(data.get('data', '')):
        return jsonify({'error': 'Data inválida. Use o formato DD/MM/AAAA'}), 400

    if not validar_hora(data.get('hora', '')):
        return jsonify({'error': 'Hora inválida. Use o formato HH:MM'}), 400

    if not data.get('descricao', '').strip():
        return jsonify({'error': 'Descrição é obrigatória'}), 400

    # Criar novo compromisso
    novo_compromisso = {
        'id': gera_id(),
        'data': data['data'],
        'hora': data['hora'],
        'descricao': data['descricao'].strip()
    }

    agenda_data.append(novo_compromisso)
    return jsonify(novo_compromisso), 201

@app.route('/api/compromissos/<int:indice>', methods=['PUT'])
def alterar_compromisso(indice):
    #API para alterar um compromisso existente
    if indice >= len(agenda_data):
        return jsonify({'error': 'Compromisso não encontrado'}), 404

    data = request.json

    # Validações opcionais (só valida se o campo foi enviado)
    if 'data' in data and not validar_data(data['data']):
        return jsonify({'error': 'Data inválida. Use o formato DD/MM/AAAA'}), 400

    if 'hora' in data and not validar_hora(data['hora']):
        return jsonify({'error': 'Hora inválida. Use o formato HH:MM'}), 400

    # Atualizar campos enviados
    if 'data' in data:
        agenda_data[indice]['data'] = data['data']
    if 'hora' in data:
        agenda_data[indice]['hora'] = data['hora']
    if 'descricao' in data:
        agenda_data[indice]['descricao'] = data['descricao'].strip()

    return jsonify(agenda_data[indice])

@app.route('/api/compromissos/<int:indice>', methods=['DELETE'])
def excluir_compromisso(indice):
    #API para excluir um compromisso
    if indice >= len(agenda_data):
        return jsonify({'error': 'Compromisso não encontrado'}), 404

    compromisso_removido = agenda_data.pop(indice)
    return jsonify({'message': 'Compromisso excluído com sucesso', 'compromisso': compromisso_removido})
"""
# Para desenvolvimento local
if __name__ == '__main__':
    app.run(debug=True)

"""# Para Vercel (serverless)
def handler(event, context):
    return app"""