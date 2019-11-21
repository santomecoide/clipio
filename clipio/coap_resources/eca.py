from datetime import datetime
import ast

from tinydb import TinyDB, Query
from coapthon.resources.resource import Resource
from clipio import constants as CON

class Eca(Resource):
    def __init__(self):
        super(Eca, self).__init__("eca")

    def __update_state(self, state):
        def transform(doc):
            doc["properties"]["state"]["const"] = state
            doc["modified"] = str(datetime.now())
        return transform

    def render_PUT(self, request):
        eca_db = TinyDB(CON.ECA_DB_PATH)
        
        data = ast.literal_eval(request.payload)
        eca_db.update(
            self.__update_state(data["state"]), 
            Query().id == data["id"]
        )
        
        eca_db.close()
        return self
    
    def render_POST(self, request):
        eca_db = TinyDB(CON.ECA_DB_PATH)
        data = ast.literal_eval(request.payload)
        event = {
            "type": data["event"]["type"],
            "unit": data["event"]["unit"],
            "forms": [
                {
                    "op": "readproperty",
                    "protocol": "mqtt",
                    "href": data["event"]["mqtt_href"]
                },
                {
                    "op": "readproperty",
                    "protocol": "coap",
                    "href": data["event"]["coap_href"],
                    "methodName": "GET"
                }
            ]
        }
        condition = {
            "type": "object",
            "properties": {
                "operator": {
                    "type": "string",
                    "const": data["condition"]["operator"]
                },
                "value": {
                    "const": data["condition"]["value"],
                }
            }
        }
        action = {
            "type": data["action"]["type"],
            "const": data["action"]["value"],
            "forms": [
                {
                    "op": "writeproperty",
                    "protocol": "coap",
                    "href": data["action"]["coap_href"],
                    "methodName": "PUT"
                }
            ]
        }
        eca_id = eca_db.insert({
            "id": 0,
            "name": data["name"],
            "description": data["description"],
            "created": str(datetime.now()),
            "modified": str(datetime.now()),
            "properties": {
                "state": {
                    "type": "boolean",
                    "const": 0
                }
            },
            "actions": {
                data["name"]: {
                    "input": {
                        "type": "object",
                        "properties": {
                            "event": event,
                            "condition": condition
                        }
                    },
                    "output": action
                }
            }
        })

        eca_db.update({"id": eca_id}, Query()["id"] == 0)
        eca_db.close()

        return self