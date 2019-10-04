import sys
import time
from urllib.parse import urlparse
from abc import ABC, abstractmethod

from paho.mqtt import client as mqtt
from coapthon.client.helperclient import HelperClient
from tinydb import TinyDB, Query

class ComparatorAction(ABC):
    def __init__(self, eca_id):
        eca_db = TinyDB("ecadb.json")
        eca = eca_db.search(Query().id == eca_id)[0]
        base = eca["actions"][eca["name"]]
        
        self.__event_data = base["input"]["properties"]["event"]
        self.__condition_data = base["input"]["properties"]["condition"]
        self.__action_data = base["output"]
        self.__triggered = False
        
        eca_db.close()
        super().__init__()

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
        netloc = url_components.netloc
        port = url_components.port
        path = self.__fix_path(url_components.path)

        server = (netloc.split(":")[0], int(port))
        coap_client = HelperClient(server)

        while not self.__triggered:
            response = coap_client.get(path)
            switcher = {
                "string": self.string_switch,
                "number": self.number_switch,
                "integer": self.integer_switch,
                "boolean": self.boolean_switch
            }
            function = switcher.get(
                self.__event_data["type"], 
                lambda:"Invalid"
            )
            function(
                response.payload,
                self.__condition_data["properties"]["value"]["const"]
            )
            time.sleep(60)

    def __on_message(self, client, userdata, msg):
        switcher = {
            "string": self.string_switch,
            "number": self.number_switch,
            "integer": self.integer_switch,
            "boolean": self.boolean_switch
        }
        function = switcher.get(
            self.__event_data["type"], 
            lambda:"Invalid"
        )
        function(
            msg.payload,
            self.__condition_data["properties"]["value"]["const"]
        )

    def __on_connect(self, client, userdata, flags, rc):
        href = self.__get_event_href("mqtt")
        url_components = urlparse(href)
        path = self.__fix_path(url_components.path)
        
        client.subscribe(path)

    def __set_mqtt_listener(self, href):
        client = mqtt.Client()
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message

        url_components = urlparse(href)
        port = url_components.port
        server = url_components.netloc.split(":")[0]

        client.connect(server, port, 60)

        client.loop_start()
        while not self.__triggered:
            pass
        client.loop_stop()

    @abstractmethod
    def string_switch(self, input_var, condition_const):
        pass

    @abstractmethod
    def number_switch(self, input_var, condition_const):
        pass

    @abstractmethod
    def integer_switch(self, input_var, condition_const):
        pass

    @abstractmethod
    def boolean_switch(self, input_var, condition_const):
        pass

    def trigger_action(self):
        const = self.__action_data["const"]
        href = self.__get_action_href("coap")
        
        url_components = urlparse(href)
        netloc = url_components.netloc
        port = url_components.port
        path = self.__fix_path(url_components.path)

        server = (netloc.split(":")[0], int(port))
        coap_client = HelperClient(server)
        coap_client.put(path, str(const))
        
        self.__triggered = True

    def set_listener(self):
        href = self.__get_event_href("mqtt")
        if href is False:
            href = self.__get_event_href("coap")
            self.__set_coap_listener(href)
        else:       
            self.__set_mqtt_listener(href)