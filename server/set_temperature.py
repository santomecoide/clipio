from coapthon.resources.resource import Resource

class SetTemperature(Resource):
    def __init__(self, name="set_temperature"):
        super(SetTemperature, self).__init__(name)
        self.payload = "Set Temperature Resource"

    def render_PUT(self, request):
        return self