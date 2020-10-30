from coapthon.client.helperclient import HelperClient

host = "192.168.0.18"
port = 5683
path ="luz"

client = HelperClient(server=(host, port))
#response = client.get(path)
client.put(path, "100")
#print(response.pretty_print())
client.stop()