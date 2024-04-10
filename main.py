import random
import time
import psutil 
from paho.mqtt import client as mqtt_client

broker = "192.168.2.2"
port = 1883
# client_id = f'python-mqtt-{random.randint(0, 1000)}'
client_id = f"base_topic"
username = "mqtt"
password = "mqtt354"
base_topic = "pc"

disks = ["C:", "D:", "E:"]

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
    
        cpu = psutil.cpu_percent()
        print(f"Процессор: {cpu}")
        
        mem = psutil.virtual_memory()
        mem_free = int(mem.available)
        mem_use = int(mem.used)
        mem_percent = float(mem.percent)
        print(f"Оперативка занята: {mem.percent}% ")
        
        client.publish(f"{base_topic}/cpu", f"{cpu}")
        client.publish(f"{base_topic}/mem", f"{mem_percent}")
        
        for disk in disks:
            try:
                sd = psutil.disk_usage(disk)
                sd_used = round((int(sd.used)/1074000000), 2)
                sd_free = round((int(sd.free)/1074000000), 2)
                sd_state = "ON"
            except Exception as e:
                print("Error getting information for disk {disk} {}".format(e))
                sd_used = 'ERR'
                sd_free = 'ERR'
                sd_state = "OFF"
        
            client.publish(f"{base_topic}/disk/{disk}", f"{sd}")
            client.publish(f"{base_topic}/disk/{disk}/used", f"{sd_used}")
            client.publish(f"{base_topic}/disk/{disk}/free", f"{sd_free}")
            client.publish(f"{base_topic}/disk/{disk}/state", f"{sd_state}")
        
        
        print(f"")
        time.sleep(15)
        
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
