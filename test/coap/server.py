from coapthon.server.coap import CoAP
from son import Son

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('son/', Son())

def main():
    server = CoAPServer("0.0.0.0", 5683)
    try:
        print("antes del server")
        server.listen(10)
        print("despues del server")
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == '__main__':
    main()