import asyncio
import paho.mqtt.client as mqtt
import logging

from config import MQTT_BROKER_IP, MQTT_BROKER_PORT, MQTT_TOPICS

logger = logging.getLogger(__name__)

class MqttClient:
    def __init__(self, message_queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
        logger.info("Initializing MQTT client")
        self.broker_ip = MQTT_BROKER_IP
        self.broker_port = MQTT_BROKER_PORT
        self.topics = MQTT_TOPICS
        self.client = mqtt.Client()
        self.message_queue = message_queue
        self.loop = loop

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        logger.info(f"Connecting to MQTT broker at {self.broker_ip}:{self.broker_port}")
        self.client.connect(self.broker_ip, self.broker_port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected with result code {rc}")
        for topic in self.topics:
            logger.info(f"Subscribing to topic: {topic}")
            self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        logger.debug(f"Received message on topic {msg.topic}")
        # 将消息放入 asyncio 队列中
        asyncio.run_coroutine_threadsafe(self.message_queue.put(msg), self.loop)
