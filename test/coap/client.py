from coapthon.client.helperclient import HelperClient

host = "192.168.1.51"
port = 5683
path ="metadata"

client = HelperClient(server=(host, port))
response = client.get(path)
#client.put(path, "0")
print(response.pretty_print())
client.stop()