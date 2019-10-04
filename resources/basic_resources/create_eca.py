from datetime import datetime
import ast

from tinydb import TinyDB, Query
from coapthon.resources.resource import Resource

class CreateEca(Resource):
    def __init__(self, name="create_eca"):
        super(CreateEca, self).__init__(name)
        self.payload = "Create Eca Resource"

    def render_POST(self, request):
        eca_db = TinyDB("ecadb.json")
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