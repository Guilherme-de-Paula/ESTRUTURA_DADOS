# pip install flask
from flask import Flask, request, make_response, jsonify

# Importação da base de dados
from bd import carros

# Esse modulo do Flask vai subir a nossa API localmente
# Vamos instanciar o modulo Flask na nossa variavel app
app = Flask('carros')

# METODO 1 - visualização de dados (GET)
# 1 - o que esse metodo vai fazer?
# 2 - Onde ele vai fazer?
@app.route('/carrinho', methods= ['GET'])
def get_carros():
    return carros

# METODO 1.1 - visualzação de dados por id (GET)
@app.route('/carrinho/<int:id_pam>', methods= ['GET'])
def get_carros_Id(id_pam):
    for car in carros:
        if car.get('id') == id_pam:
            return jsonify(car)
        
# METODO 2 - criar novos registros (POST)
# Verificar os dados que estão sendo passados na requisição e armazenar na nossa base
@app.route('/carrinho', methods= ['POST'])
def criar_carro():
    car = request.json
    carros.append(car)
    return make_response(
        jsonify(
            mensagem = 'Carro cadastrado com sucesso!!',
            carrinho = car
        )
    )

# METODO 3 - deletar registros (DELETE)
@app.route('/carrinho/<int:id>', methods= ['DELETE'])
def excluir_carro(id):
    for indice, carro in enumerate(carros):
        if carro.get('id') == id:
            del carros[indice]
            return jsonify(
                {'mensagem': 'Carro excluido!!'}
            )
        
# METODO 4 - editar os registros (PUT)
@app.route('/carrinho/<int:id>', methods= ['PUT'])
def editar_carro(id):
    carro_alterado = request.get_json()
    for indice, carro in enumerate(carros):
        if carro.get('id') == id:
            carros[indice].update(carro_alterado)
            return jsonify(
                carros[indice]
            )
        





app.run(port=5000, host= 'localhost', debug= True)