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

#appPet = Flask ('pet')
#appPet.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#appPet.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_ClinicaVetBD'

class Pets (mybd.Model):
    __tablename__ = 'tb_Pets'
    id_pet = mybd.Column (mybd.Integer, primary_key = True)
    nome = mybd.Column (mybd.String (255))
    tipo = mybd.Column (mybd.String (255))
    raca = mybd.Column (mybd.String (255))
    data_nascimento = mybd.Column (mybd.String (255))
    id_clientes = mybd.Column (mybd.Integer, mybd.ForeignKey ('tb_Clientes.id_clientes'), nullable = False)
    idade = mybd.Column (mybd.Integer)

    def to_json (self):
        return {
            'id_pet': self.id_pet,
            'nome': self.nome,
            'tipo': self.tipo,
            'raca': self.raca,
            'data_nascimento': str(self.data_nascimento),
            'id_clientes': self.id_clientes,
            'idade': self.idade
        }
    
#---------------------- GET Pets -------------------------------
@app.route('/pets', methods = ['GET'])
def selecionar_pet ():
    pet_selecionado = Pets.query.all()
    pet_json = [pet.to_json()
                for pet in pet_selecionado]
    return gera_resposta (200, 'pets', pet_json)
#----------------------------------------------------------------

#-------------------- POST Pets --------------------------------
@app.route('/pets', methods = ['POST'])
def criar_pet():
    requisicao = request.get_json()

    try:
        pet = Pets (
            id_pet = requisicao['id_pet'],
            nome = requisicao['nome'],
            tipo = requisicao['tipo'],
            raca = requisicao['raca'],
            data_nascimento = requisicao['data_nascimento'],
            id_clientes = requisicao['id_clientes'],
            idade = requisicao['idade']
        )

        mybd.session.add(pet)
        mybd.session.commit()
        return gera_resposta (201, pet.to_json(), 'Criado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta (400, {}, 'Erro ao cadastrar!')
#--------------------------------------------------------------------------------------

#--------------------- DELETE Pets ------------------------------------------------
@app.route('/pets/<id_pet_pam>', methods = ['DELETE'])
def deleta_pet(id_pet_pam):
    pet = Pets.query.filter_by(id_pet = id_pet_pam).first()

    try:
        mybd.session.delete(pet)
        mybd.session.commit()
        return gera_resposta (200, pet.to_json(), 'Deletado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta (400, {}, 'Erro ao deletar!')
#------------------------------------------------------------------------------------

#---------------------------------- PUT Pets ----------------------------------------
@app.route('/pets/<id_pet_pam>', methods = ['PUT'])
def atualiza_pet(id_pet_pam):
    pet = Pets.query.filter_by(id_pet = id_pet_pam).first()
    requisicao = request.get_json()

    try:
        if ('nome' in requisicao):
            pet.nome = requisicao ['nome']
        if ('tipo' in requisicao):
            pet.tipo = requisicao ['tipo']
        if ('raca' in requisicao):
            pet.raca = requisicao ['raca']
        if ('data_nascimento' in requisicao):
            pet.data_nascimento = requisicao ['data_nascimento']
        if ('id_clientes' in requisicao):
            pet.id_clientes = requisicao ['id_clientes']
        if ('idade' in requisicao):
            pet.idade = requisicao ['idade']

        mybd.session.add(pet)
        mybd.session.commit()
        return gera_resposta (200, pet.to_jason(), 'Pet atualizado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta (400, {}, 'Erro ao atualizar')
#----------------------------------------------------------------------------------------------------

# ----------------------------RESPOSTA PADRAO--------------------------------------------------------
def gera_resposta (status, conteudo, mensagem = False):
    body = {}
    body ['Lista de Clientes'] = conteudo
    if (mensagem):
        body ['mensagem'] = mensagem
    return Response (json.dumps(body), status = status, mimetype = 'application/json')
app.run (port = 5000, host = 'localhost', debug = True)

