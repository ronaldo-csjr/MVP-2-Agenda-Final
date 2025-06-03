import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import uuid # Para gerar IDs únicos

# Obter o diretório atual do arquivo app.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Definir o caminho para a pasta de templates (agora no mesmo nível)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# Simulando um banco de dados em memória (em produção, use um banco real)
agenda_data = []

def gera_id():
    """Gera um ID único universal (UUID)."""
    return str(uuid.uuid4())

def validar_data(data_str, formato="%Y-%m-%d"):
    """Valida se a data está no formato correto AAAA-MM-DD."""
    try:
        datetime.strptime(data_str, formato)
        return True
    except ValueError:
        return False

def validar_hora(hora_str, formato="%H:%M"):
    """Valida se a hora está no formato correto HH:MM."""
    try:
        datetime.strptime(hora_str, formato)
        return True
    except ValueError:
        return False

@app.route('/')
def index():
    """Página principal com a lista de compromissos."""
    # Os compromissos são passados diretamente da lista em memória
    return render_template('calendario.html', compromissos=agenda_data)

@app.route('/api/compromissos', methods=['GET'])
def listar_compromissos():
    """API para listar todos os compromissos."""
    return jsonify(agenda_data)

@app.route('/api/compromissos', methods=['POST'])
def agendar_compromisso():
    """API para criar um novo compromisso."""
    try:
        data = request.get_json()
    except Exception:
        return jsonify({'erro': 'JSON malformado ou inválido'}), 400

    if not data:
        return jsonify({'erro': 'Nenhum dado fornecido'}), 400

    # Validações dos campos obrigatórios e formatos
    titulo = data.get('titulo')
    data_str = data.get('data')
    hora_str = data.get('hora')
    descricao = data.get('descricao', '').strip() # Descrição é opcional

    if not titulo:
        return jsonify({'erro': 'Título é obrigatório'}), 400
    if not data_str:
        return jsonify({'erro': 'Data é obrigatória'}), 400
    if not hora_str:
        return jsonify({'erro': 'Hora é obrigatória'}), 400

    if not validar_data(data_str):
        return jsonify({'erro': 'Data inválida. Use o formato AAAA-MM-DD'}), 400
    if not validar_hora(hora_str):
        return jsonify({'erro': 'Hora inválida. Use o formato HH:MM'}), 400

    # Criar novo compromisso
    novo_compromisso = {
        'id': gera_id(),
        'titulo': titulo,
        'data': data_str,
        'hora': hora_str,
        'descricao': descricao
    }

    agenda_data.append(novo_compromisso)
    return jsonify(novo_compromisso), 201

@app.route('/api/compromissos/<string:compromisso_id>', methods=['GET'])
def obter_compromisso(compromisso_id):
    """API para obter um compromisso específico pelo ID."""
    compromisso = next((c for c in agenda_data if c['id'] == compromisso_id), None)
    if compromisso:
        return jsonify(compromisso)
    return jsonify({'erro': 'Compromisso não encontrado'}), 404

@app.route('/api/compromissos/<string:compromisso_id>', methods=['PUT'])
def alterar_compromisso(compromisso_id):
    """API para alterar um compromisso existente pelo ID."""
    try:
        data = request.get_json()
    except Exception:
        return jsonify({'erro': 'JSON malformado ou inválido'}), 400

    if not data:
        return jsonify({'erro': 'Nenhum dado fornecido para atualização'}), 400

    compromisso = next((c for c in agenda_data if c['id'] == compromisso_id), None)
    if not compromisso:
        return jsonify({'erro': 'Compromisso não encontrado'}), 404

    # Atualizar campos enviados (validações opcionais)
    if 'titulo' in data:
        if not data['titulo'].strip(): # Garante que título não seja vazio
            return jsonify({'erro': 'Título não pode ser vazio'}), 400
        compromisso['titulo'] = data['titulo'].strip()
    if 'data' in data:
        if not validar_data(data['data']):
            return jsonify({'erro': 'Data inválida. Use o formato AAAA-MM-DD'}), 400
        compromisso['data'] = data['data']
    if 'hora' in data:
        if not validar_hora(data['hora']):
            return jsonify({'erro': 'Hora inválida. Use o formato HH:MM'}), 400
        compromisso['hora'] = data['hora']
    if 'descricao' in data:
        compromisso['descricao'] = data['descricao'].strip()

    return jsonify(compromisso)

@app.route('/api/compromissos/<string:compromisso_id>', methods=['DELETE'])
def excluir_compromisso(compromisso_id):
    """API para excluir um compromisso pelo ID."""
    global agenda_data # Necessário para modificar a lista globalmente
    initial_len = len(agenda_data)
    agenda_data = [c for c in agenda_data if c['id'] != compromisso_id]

    if len(agenda_data) < initial_len:
        return jsonify({'mensagem': 'Compromisso excluído com sucesso', 'id': compromisso_id}), 200
    return jsonify({'erro': 'Compromisso não encontrado'}), 404

# Para desenvolvimento local
if __name__ == '__main__':
    app.run(debug=True, port=5500)
