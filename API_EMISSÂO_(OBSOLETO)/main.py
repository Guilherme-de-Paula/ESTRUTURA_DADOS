from datetime import datetime, timezone
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json
import paho.mqtt.client as mqtt

app = Flask ('coleta_dados')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://projeto3:senai%40134@projetointegrador-grupo4.mysql.database.azure.com/db_projetointegrador'
mybd = SQLAlchemy (app)

# ********************* CONEXÃO SENSORES *********************************
# pip install paho-mqtt

mqtt_data = {}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("projeto_integrado/SENAI134/Cienciadedados/grupo1")

def on_message(client, userdata, msg):
    global mqtt_data
 # Decodifica a mensagem recebida de bytes para string
    payload = msg.payload.decode('utf-8')
   
    # Converte a string JSON em um dicionário Python
    mqtt_data = json.loads(payload)
   
    # Imprime a mensagem recebida
    print(f"Received message: {mqtt_data}")

    # Adiciona o contexto da aplicação para a manipulação do banco de dados
    with app.app_context():
        try:
            temperatura = mqtt_data.get('temperature')
            pressao = mqtt_data.get('pressure')
            altitude = mqtt_data.get('altitude')
            umidade = mqtt_data.get('humidity')
            #poeira_1 = mqtt_data.get('particula1')
            #poeira_2 = mqtt_data.get('particula2')
            co2 = mqtt_data.get('co2')
            timestamp_unix = mqtt_data.get('timestamp')

            if timestamp_unix is None:
                print("Timestamp não encontrado no payload")
                return

            # Converte timestamp Unix para datetime
            try:
                timestamp = datetime.fromtimestamp(int(timestamp_unix), tz=timezone.utc)
            except (ValueError, TypeError) as e:
                print(f"Erro ao converter timestamp: {str(e)}")
                return

            # Cria o objeto Registro com os dados
            new_data = Litoral(
                temperatura=temperatura,
                pressao=pressao,
                altitude=altitude,
                umidade=umidade,
                #poeira_1=poeira_1,
                #poeira_2=poeira_2,
                co2=co2,
                tempo_registro=timestamp
            )

            # Adiciona o novo registro ao banco de dados
            mybd.session.add(new_data)
            mybd.session.commit()
            print("Dados inseridos no banco de dados com sucesso")

        except Exception as e:
            print(f"Erro ao processar os dados do MQTT: {str(e)}")
            mybd.session.rollback()

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("test.mosquitto.org", 1883, 60)

def start_mqtt():
    mqtt_client.loop_start()

#-----------------------------------------------------------------------------------------------------------


class Litoral (mybd.Model):
    __tablename__ = 'tb_litoral'
    id = mybd.Column (mybd.Integer, primary_key = True)
    localizacao = mybd.Column (mybd.String (255))
    dia_hora = mybd.Column (mybd.String (255))
    co2 = mybd.Column (mybd.Float (20,2))
    poeira_1 = mybd.Column (mybd.Float (20,2))
    poeira_2 = mybd.Column (mybd.Float (20,2))
    pressao = mybd.Column (mybd.Float (20,2))
    umidade = mybd.Column (mybd.Float (20,2))
    temperatura = mybd.Column (mybd.Float (20,2))
    altitude = mybd.Column (mybd.Float (20,2))

    def to_json (self):
        return {
            'id': self.id,
            'localizacao': self.localizacao,
            'dia_hora': self.dia_hora,
            'co2': float(self.co2),
            'poeira_1': float(self.poeira_1),
            'poeira_2': float(self.poeira_2),
            'pressao': float(self.pressao),
            'umidade': float(self.umidade),
            'temperatura': float(self.temperatura),
            'altitude': float(self.altitude)
        }
    
# -------------------------------------------------------------------------------
                            # METODO GET
@app.route('/litoral', methods = ['GET'])
def selecionar_litoral():
    litoral_selecionado = Litoral.query.all()
    litoral_json = [litorais.to_json()
                    for litorais in litoral_selecionado]
    return gera_resposta (200, 'litoral', litoral_json)

@app.route('/litoral/<id_pam>', methods = ['GET'])
def selecionar_litoral_id(id_pam):
    litoral_selecionado = Litoral.query.filter_by(id = id_pam).first()
    litoral_json = litoral_selecionado.to_json()
    return gera_resposta (200, litoral_json, 'Dados Encontrado!')

# -------------------------------------------------------------------------------

                            # METODO POST
@app.route('/litoral', methods = ['POST'])
def criar_litoral():
    requisicao = request.get_json()

    try:
        litoral = Litoral (
            id = requisicao['id'],
            localizacao = requisicao['localizacao'],
            dia_hora = requisicao['dia_hora'],
            co2 = requisicao['co2'],
            poeira_1 = requisicao['poeira_1'],
            poeira_2 = requisicao['poeira_2'],
            pressao = requisicao['pressao'],
            umidade = requisicao['umidade'],
            temperatura = requisicao['temperatura'],
            altitude = requisicao['altitude']
        )

        mybd.session.add(litoral)
        mybd.session.commit()

        return gera_resposta (201, litoral.to_json(), 'Criado com Sucesso!')
    
    except Exception as e:
        print ('Erro', e)

        return gera_resposta (400, {}, 'Erro ao cadastrar!')
    
# ---------------------------------------------------------------------------------
                         # METODO DELETE
@app.route('/litoral/<id_pam>', methods = ['DELETE'])
def deletar_litoral(id_pam):
    litoral = Litoral.query.filter_by(id = id_pam).first()

    try:
        mybd.session.delete(litoral)
        mybd.session.commit()

        return gera_resposta (200, litoral.to_json(), 'Deletado com sucesso!')
    
    except Exception as e:
        print ('Erro', e)
        return gera_resposta (400, {}, 'Erro ao deletar!')
    
# -----------------------------------------------------------------------------------
                           # METODO PUT
@app.route('/litoral/<id_pam>', methods = ['PUT'])
def atualizar_litoral(id_pam):
    litoral = Litoral.query.filter_by(id = id_pam).first()
    requisicao = request.get_json()

    try:
        if ('localizacao' in requisicao):
            litoral.localizacao = requisicao ['localizacao']
        if ('dia_hora' in requisicao):
            litoral.dia_hora = requisicao ['dia_hora']
        if ('co2' in requisicao):
            litoral.co2 = requisicao ['co2']
        if ('poeira_1' in requisicao):
            litoral.poeira_1 = requisicao ['poeira_1']
        if ('poeira_2' in requisicao):
            litoral.poeira_2 = requisicao ['poeira_2']
        if ('pressao' in requisicao):
            litoral.pressao = requisicao ['pressao']
        if ('umidade' in requisicao):
            litoral.umidade = requisicao ['umidade']
        if ('temperatura' in requisicao):
            litoral.temperatura = requisicao ['temperatura']
        if ('altitude' in requisicao):
            litoral.altitude = requisicao ['altitude']

        mybd.session.add(litoral)
        mybd.session.commit()

        return gera_resposta (200, litoral.to_json(), 'Dados atualizado com sucesso!')
    
    except Exception as e:
        print ('Erro', e)
        return gera_resposta (400, {}, 'Erro ao atualizar')




# ----------------------------------------------------------------------------------------
                       # tb_adicional

class Adicional (mybd.Model):
    __tablename__ = 'tb_adicional'
    id_adicional = mybd.Column (mybd.Integer, primary_key = True)
    qualidade_ar = mybd.Column (mybd.Float (20,2))
    densidade_ar = mybd.Column (mybd.Float (20,2))
    velocidade_vento = mybd.Column (mybd.Float (20,2))
    previsao_chuva = mybd.Column (mybd.Float (20,2))
    id = mybd.Column (mybd.Integer, mybd.ForeignKey ('tb_litoral.id'), nullable = False)

    def to_json (self):
        return {
            'id_adicional': self.id_adicional,
            'qualidade_ar': float(self.qualidade_ar),
            'densidade_ar': float(self.densidade_ar),
            'velocidade_vento': float(self.velocidade_vento),
            'previsao_chuva': float(self.previsao_chuva),
            'id': self.id
        }
#--------------------------------------------------------------------------------------

# GET ADICIONAL
@app.route('/adicional', methods = ['GET'])
def selecionar_adicional ():
    adicional_selecionado = Adicional.query.all()
    adicional_json = [adicional.to_json()
                      for adicional in adicional_selecionado]
    return gera_resposta (200, 'adicional', adicional_json)
#---------------------------------------------------------------------------------------

# POST ADICIONAL
@app.route('/adicional', methods = ['POST'])
def criar_adicional():
    requisicao = request.get_json()

    try:
        adicional = Adicional (
            id_adicional = requisicao['id_adicional'],
            qualidade_ar = requisicao ['qualidade_ar'],
            densidade_ar = requisicao ['densidade_ar'],
            velocidade_vento = requisicao ['velocidade_vento'],
            previsao_chuva = requisicao ['previsao_chuva'],
            id = requisicao ['id']
        )

        mybd.session.add(adicional)
        mybd.session.commit()
        return gera_resposta (201, adicional.to_json(), 'Criado com sucesso!')
    
    except Exception as e:
        print ('Erro', e)
        return gera_resposta (400, {}, 'Erro ao cadastrar!')
#----------------------------------------------------------------------------------------    

# DELETE ADICIONAL
@app.route('/adicional/<id_adicional_pam>', methods = ['DELETE'])
def deletar_adicional (id_adicional_pam):
    adicional = Adicional.query.filter_by(id_adicional = id_adicional_pam).first()

    try:
        mybd.session.delete(adicional)
        mybd.session.commit()
        return gera_resposta (200, adicional.to_json(), 'Deletado com sucesso!')
    
    except Exception as e:
        print ('Erro', e)
        return gera_resposta (400, {}, 'Erro ao deletar')
#--------------------------------------------------------------------------------------------- 
  
# PUT ADICIONAL 
@app.route('/adicional/<id_adicional_pam>', methods = ['PUT'])
def atualizar_adicional(id_adicional_pam):
    adicional = Adicional.query.filter_by(id_adicional = id_adicional_pam).first()
    requisicao = request.get_json()

    try:
        if ('qualidade_ar' in requisicao):
            adicional.qualidade_ar = requisicao ['qualidade_ar']
        if ('densidade_ar' in requisicao):
            adicional.densidade_ar = requisicao ['densidade_ar']
        if ('velocidade_vento' in requisicao):
            adicional.velocidade_vento = requisicao ['velocidade_vento']
        if ('previsao_chuva' in requisicao):
            adicional.previsao_chuva = requisicao ['previsao_chuva']
        if ('id' in requisicao):
            adicional.id = requisicao ['id']

        mybd.session.add(adicional)
        mybd.session.commit()
        return gera_resposta (200, adicional.to_json(), 'Dado atualizado com sucesso!')
    
    except Exception as e:
        print ('Erro', e)
        return gera_resposta (400, {}, 'Erro ao atualizar')
#--------------------------------------------------------------------------------

    
# ------------------- GERA RESPOSTA ------------------------------------------
def gera_resposta(status, conteudo, mensagem = False):
    body = {}
    body ['Dados Coletados'] = conteudo
    if (mensagem):
        body ['mensagem'] = mensagem

    return Response (json.dumps(body), status = status, mimetype = 'application/json')
app.run (port = 5000, host = 'localhost', debug = True)
