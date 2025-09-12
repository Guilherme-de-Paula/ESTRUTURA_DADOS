from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask ('clientes')

app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_ClinicaVetBD'
mybd = SQLAlchemy(app)

class Clientes (mybd.Model):
    __tablename__ = 'tb_clientes'
    id_clientes = mybd.Column (mybd.Integer, primary_key = True)
    nome = mybd.Column (mybd.String (100) )
    endereco = mybd.Column (mybd.String (100) )
    telefone = mybd.Column (mybd.String (100) )


    def to_json (self):
        return {
            'id_clientes': self.id_clientes,
            'nome': self.nome,
            'endereco': self.endereco,
            'telefone': self.telefone
        }
 #---------------------GET------------------------------------------------------------------------ 
@app.route ('/clientes', methods = ['GET'])
def selecionar_cliente ():
    cliente_selecionado = Clientes.query.all()
    cliente_json = [cliente.to_json()
                    for cliente in cliente_selecionado]
    return gera_resposta (200, 'clientes', cliente_json)
#--------------------------------------------------------------------------------------------------

#---------------------POST-------------------------------------------------------------------------
@app.route ('/clientes', methods = ['POST'])
def criar_cliente():
    requisicao =  request.get_json()

    try:
        cliente = Clientes (
            id_clientes = requisicao['id_clientes'],
            nome = requisicao['nome'],
            endereco = requisicao['endereco'],
            telefone = requisicao['telefone']
        )

        mybd.session.add (cliente)
        mybd.session.commit ()
        return gera_resposta (201, cliente.to_json(), 'Criado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, 'Erro ao cadastra!')
#-------------------------------------------------------------------------------------------------

#--------------------------DELETE-----------------------------------------------------------------
@app.route ('/clientes/<id_clientes_pam>', methods = ['DELETE'])
def deletar_cliente(id_clientes_pam):
    cliente = Clientes.query.filter_by(id_clientes = id_clientes_pam).first()

    try:
        mybd.session.delete(cliente)
        mybd.session.commit()
        return gera_resposta (200, cliente.to_json(), 'Deletado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta (400, {}, 'Erro ao deletar!')
#------------------------------------------------------------------------------------------------

#----------------------------PUT-----------------------------------------------------------------
@app.route ('/clientes/<id_clientes_pam>', methods = ['PUT'])
def atualiza_cliente (id_clientes_pam):
    cliente = Clientes.query.filter_by(id_clientes = id_clientes_pam).first()
    requisicao = request.get_json()

    try:
        if ('nome' in requisicao):
            cliente.nome = requisicao ['nome']
        if ('endereco' in requisicao):
            cliente.endereco = requisicao ['endereco']
        if ('telefonr' in requisicao):
            cliente.telefone = requisicao ['telefone']

        mybd.session.add (cliente)
        mybd.session.commit ()
        return gera_resposta (200, cliente.to_json(), 'Clienta atualizado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta (400, {}, 'Erro ao atualizar!')
#----------------------------------------------------------------------------------------------------

# ----------------------------RESPOSTA PADRAO--------------------------------------------------------
def gera_resposta (status, conteudo, mensagem = False):
    body = {}
    body ['Lista de Clientes'] = conteudo
    if (mensagem):
        body ['mensagem'] = mensagem
    return Response (json.dumps(body), status = status, mimetype = 'application/json')
app.run (port = 5000, host = 'localhost', debug = True)