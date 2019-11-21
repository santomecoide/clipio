import sys
import time
from urllib.parse import urlparse
from abc import ABC, abstractmethod

from paho.mqtt import client as mqtt
from coapthon.client.helperclient import HelperClient
from tinydb import TinyDB, Query
import clipio.constants as CON

class ComparatorAction(ABC):
    def __init__(self, eca_id, settings):
        self.__settings = settings
        self.__mqtt = settings['mqtt_listener']
        
        eca_db = TinyDB("ecadb.json")
        eca = eca_db.search(Query().id == eca_id)[0]
        base = eca["actions"][eca["name"]]
        
        self.__event_data = base["input"]["properties"]["event"]
        self.__condition_data = base["input"]["properties"]["condition"]
        self.__action_data = base["output"]
        self.__triggered = False
        
        eca_db.close()
        super().__init__()

    def __py_type(self, type_):
        for accepted_type in CON.ACCEPTED_TYPES:
            if accepted_type['name'] == type_:
                return accepted_type['py_type']
        return None
    
    def __fix_path(self, path):
        if path[0] == "/":
            path = path[1:]
        return path

    def __get_event_href(self, protocol):
        for form in self.__event_data["forms"]:
            if form["protocol"] == protocol:
                return form["href"]
        return False

    def __get_action_href(self, protocol):
        for form in self.__action_data["forms"]:
            if form["protocol"] == protocol:
                return form["href"] 
        return False

    def __set_coap_listener(self, href):
        url_components = urlparse(href)
        hostname = url_components.hostname
        port = url_components.port
        path = self.__fix_path(url_components.path)

        server = (hostname, int(port))
        coap_client = HelperClient(server)

        break_ = False
        while not self.__triggered and not break_:            
            switcher = {
                "string": self.__string_switch,
                "number": self.__number_switch,
                "integer": self.__integer_switch,
                "boolean": self.__boolean_switch
            }
            function = switcher.get(
                self.__event_data["type"], 
                lambda:"Invalid"
            )

            try:
                response = coap_client.get(path)
                payload = self.__py_type(self.__event_data["type"])(response.payload)
                function(
                    payload,
                    self.__condition_data["properties"]["value"]["const"]
                )
            except:
                break_ = True
            
            if not break_:
                for i in range(self.__settings['coap_request_delay_time']):
                    components_db = TinyDB("generated/components.json")
                    table_eca = components_db.table('eca')
                    enabled = table_eca.all()[0]['enabled']
                    components_db.close()
                    if i > 0 and not enabled:
                        break_ = True
                        break
                    time.sleep(1)

        coap_client.close()

    def __on_message(self, client, userdata, msg):
        switcher = {
            "string": self.__string_switch,
            "number": self.__number_switch,
            "integer": self.__integer_switch,
            "boolean": self.__boolean_switch
        }
        function = switcher.get(
            self.__event_data["type"], 
            lambda:"Invalid"
        )

        try:
            payload = self.__py_type(self.__event_data["type"])(msg.payload)
            function(
                payload,
                self.__condition_data["properties"]["value"]["const"]
            )
        except:
            pass

    def __on_connect(self, client, userdata, flags, rc):
        href = self.__get_event_href("mqtt")
        url_components = urlparse(href)
        path = self.__fix_path(url_components.path)
        
        client.subscribe(path)

    def __set_mqtt_listener(self, href):
        client = mqtt.Client()
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message

        user = self.__mqtt['user'].strip()
        password = self.__mqtt['password'].strip()
        if user and password:
            client.username_pw_set(user, password)

        url_components = urlparse(href)
        port = url_components.port
        hostname = url_components.hostname

        client.connect(hostname, port)

        client.loop_start()
        while not self.__triggered:
            components_db = TinyDB("generated/components.json")
            table_eca = components_db.table('eca')
            enabled = table_eca.all()[0]['enabled']
            components_db.close()
            if not enabled:
                break
        client.loop_stop()

    @abstractmethod
    def __string_switch(self, input_var, condition_const):
        pass

    @abstractmethod
    def __number_switch(self, input_var, condition_const):
        pass

    @abstractmethod
    def __integer_switch(self, input_var, condition_const):
        pass

    @abstractmethod
    def __boolean_switch(self, input_var, condition_const):
        pass

    def __trigger_action(self):
        const = self.__action_data["const"]
        href = self.__get_action_href("coap")
        
        url_components = urlparse(href)
        hostname = url_components.hostname
        port = url_components.port
        path = self.__fix_path(url_components.path)

        server = (hostname, int(port))
        coap_client = HelperClient(server)
        coap_client.put(path, str(const))
        
        self.__triggered = True

    def set_listener(self):
        if self.__mqtt['enable']:
            href = self.__get_event_href("mqtt")
            if not href:
                href = self.__get_event_href("coap")
            self.__set_mqtt_listener(href)
        else:       
            href = self.__get_event_href("coap")
            self.__set_coap_listener(href)