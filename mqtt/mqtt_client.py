import asyncio
import paho.mqtt.client as mqtt
from datetime import datetime

# Import configuration
from config import MQTT_BROKER_IP
from config import MQTT_BROKER_PORT
from config import MQTT_TOPICS

class MqttClient:
    def __init__(self):
        self.broker_ip = MQTT_BROKER_IP
        self.broker_port = MQTT_BROKER_PORT
        self.topics = MQTT_TOPICS
        self.client = mqtt.Client()
        self.msg = None

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.broker_ip, self.broker_port,60)
        self.client.loop_start()


    def on_connect(self,client,userdata,flags, rc):
        print("Connected with result code" + str(rc))
        for topic in self.topics:
            self.client.subscribe(topic)

    def on_message(self,client,userdata, msg):
        #打印时间
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print(f'Received message from {msg.topic}: {msg.payload.decode()} at {current_time}')
    
        self.msg = msg   