import time
import threading
from paho.mqtt import client as mqtt
from tinydb import TinyDB, Query
from clipio.utils.value_helper import ValueHelper

class MqttClient():
    def __init__(self, settings):
        self.__metadata = settings.METADATA
        self.__run_flag = False         

    def __push(self, resource):
        value_helper = ValueHelper(resource['tag'], resource['type'])
        mqtt = resource['mqtt']
        qos = mqtt['qos']
        topic = self.__metadata['name'] + "/" + resource['tag']
        
        client = mqtt.Client()
        user = mqtt['user'].strip()
        password = mqtt['password'].strip()
        if user and password:
            client.username_pw_set(user, password)
        client.connect(mqtt['host'], mqtt['port'])
        client.reconnect()
        
        client.loop_start()
        while self.__run_flag:
            try:
                payload = value_helper.value
                client.publish(topic, payload, qos)
            except:
                print("can not publish")
            
            for i in range(mqtt['delay_time']):
                if i > 0 and not self.__run_flag:
                    break
                time.sleep(1)
        client.loop_stop()
        
    def __run(self):
        self.__run_flag = True

        for resource in self.__metadata['resources']:
            if resource['mqtt']['enabled']:
                push_thread = threading.Thread(
                    target=self.__push,
                    args=(resource,))
                push_thread.start() 

        print("Mqtt client end")
        
    def run(self):
        run_ = False
        for resource in self.__metadata['resources']:
            if resource['mqtt']['enabled']:
                run_ = True
                break
        
        if run_:
            run_thread = threading.Thread(target=self.__run)
            run_thread.start()

            print("mqtt client init")

    def stop(self):
        run_ = False
        for resource in self.__metadata['resources']:
            if resource['mqtt']['enabled']:
                run_ = True
                break
        
        if run_:  
            self.__run_flag = False
            print("stopping mqtt client...")