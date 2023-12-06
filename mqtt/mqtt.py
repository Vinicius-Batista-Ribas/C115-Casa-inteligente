import paho.mqtt.client as mqtt
import random
import time

# Configurações do broker MQTT (HiveMQ)
broker_address = "broker.hivemq.com"
port = 1883
temperatura_topic = "meu/topico/temperatura"
umidade_ar_topic = "meu/topico/umidadeAr"
umidade_terra_topic = "meu/topico/umidadeTerra"
refrigerador_topic = "meu/topico/refrigerador"
aquecedor_topic = "meu/topico/aquecedor"
irrigador_topic = "meu/topico/irrigador"
umidificador_topic = "meu/topico/umidificador"
ligado = "Ligado"
desligado = "Desligado"





# Callback quando a conexão com o broker é estabelecida
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao Broker com código de retorno: {rc}")
    # Inscreva-se nos tópicos ao conectar
    client.subscribe(umidade_ar_topic)
    client.subscribe(temperatura_topic)
    client.subscribe(umidade_terra_topic)
    client.subscribe(aquecedor_topic)
    client.subscribe(refrigerador_topic)
    client.subscribe(irrigador_topic)
    client.subscribe(umidificador_topic)


# Callback quando uma mensagem é recebida do broker
def on_message(client, userdata, msg):

    if msg.topic == temperatura_topic:
        temperatura = float(msg.payload.decode('utf-8'))
        print(f"Recebido o tópico {msg.topic} com umidade do ar: {temperatura_topic}%")
       

    elif msg.topic == umidade_ar_topic:
        umidade_ar = float(msg.payload.decode('utf-8'))
        print(f"Recebido o tópico {msg.topic} com umidade do ar: {umidade_ar}%")

    elif msg.topic == umidade_terra_topic:
        umidade_terra = float(msg.payload.decode('utf-8'))
        print(f"Recebido o tópico {msg.topic} com umidade da terra: {umidade_terra}%")

# Criar um cliente MQTT
client = mqtt.Client()

# Configurar as funções de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker
client.connect(broker_address, port, 60)


estado_lampada = False
# Loop principal
while True:
   
    # Gerar valores simulados
    temperatura_simulada = round(random.uniform(0, 50), 2)
    umidade_ar_simulada = round(random.uniform(20, 70), 2)
    umidade_terra_simulada = round(random.uniform(10, 80), 2)

    temperatura = int(temperatura_simulada)

    if temperatura > 28:
        client.publish(refrigerador_topic, ligado)
        client.publish(aquecedor_topic, desligado)
    elif 14 <= temperatura <= 28:
        client.publish(refrigerador_topic, desligado)
        client.publish(aquecedor_topic, desligado)
    elif temperatura < 14:
        client.publish(refrigerador_topic, desligado)
        client.publish(aquecedor_topic, ligado)

    umidade = int(umidade_ar_simulada)

    if umidade < 30:
        client.publish(umidificador_topic, ligado + ". \nnível de umidade prejudicial.\nLembre-se de beber água!!!")
    elif 30 <= umidade < 40:
        client.publish(umidificador_topic, ligado)
    elif umidade >= 40:
        client.publish(umidificador_topic, desligado)
    irrigador = int(umidade_terra_simulada)


    if irrigador <= 20:
        client.publish(irrigador_topic, ligado)
    if 40 <= irrigador <= 55:
        client.publish(irrigador_topic, desligado)

    # Publicar os valores simulados nos respectivos tópicos
    client.publish(temperatura_topic, str(temperatura_simulada))
    print("Temperatura sendo atualizada")
    client.publish(umidade_ar_topic, str(umidade_ar_simulada))
    print("Umidade do ar sendo atualizada")
    client.publish(umidade_terra_topic, str(umidade_terra_simulada))
    print("Umidade da terra sendo atualizada")

    # Aguardar alguns segundos antes de gerar os próximos valores
    time.sleep(15)
