from coapthon.server.coap import CoAP
import resources

class CoapServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast)
        self.add_resource('metadata/get', resources.GetMetadata())
        self.add_resource('eca/create', resources.CreateEca())
        self.add_resource('eca/state/update', resources.UpdateEcaState())
        self.add_resource('context/query', resources.ContextQuery())

        #estos recursos deben ser creados segun las propiedades de los metadatos
        self.add_resource(
            'temperature/get', resources.GetTemperature()
        )
        self.add_resource(
            'temperature/set', resources.SetTemperature()
        )
        self.add_resource(
            'heater/get', resources.GetHeater()
        )
        self.add_resource(
            'heater/set', resources.SetHeater()
        )
        self.add_resource(
            'fan/get', resources.GetFan()
        )
        self.add_resource(
            'fan/set', resources.SetFan()
        )

        print("CoAP Server start on " + host + ":" + str(port))

def main():
    ip = "192.168.0.25"
    port = 5683

    server = CoapServer(ip, port)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == "__main__":
    main()