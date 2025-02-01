import paho.mqtt.client as mqtt

BROKER = 'broker.hivemq.com'
PORT = 1883
CHAT_TOPIC = 'projektProtokoly/chat'
NOTIFICATION_TOPIC = 'projektProtokoly/notifications/#' 

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(CHAT_TOPIC)
    client.subscribe(NOTIFICATION_TOPIC)

def on_message(client, userdata, msg):
    if msg.topic.startswith('projektProtokoly/notifications/'):
        handle_notification(msg)
    elif msg.topic == CHAT_TOPIC:
        handle_chat_message(msg)

def handle_notification(msg):
    print(f"Notification: {msg.payload.decode()}")

def handle_chat_message(msg):
    print(f"Chat message: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()