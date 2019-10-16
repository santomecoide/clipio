from coapthon.client.helperclient import HelperClient

payload = {
    "name": "Nombre del ECA",
    "description": "Descripcion del ECA",
    "event": {
        "type": "integer",
        "unit": "°C",
        "mqtt_href": "mqtt://iot.eclipse.org:1883/90072060600/ejemplo",
        "coap_href": "coap://192.168.0.25:5683/temperature/get"
    },
    "condition": {
        "operator": ">",
        "value": 10 
    },
    "action": {
        "type": "boolean",
        "value": 1,
        "coap_href": "coap://192.168.0.25:5683/heater/set"
    }
}

payload2 = {
    "id": 1,
    "state": 1
}

server = ("192.168.0.25", 5683)
client = HelperClient(server)
response = client.post("eca/create", str(payload))
print(response)