from coapthon.resources.resource import Resource

class SetHeater(Resource):
    def __init__(self, name="set_heater"):
        super(SetHeater, self).__init__(name)
        self.payload = "Set Heater Resource"

    def render_PUT(self, request):
        return self