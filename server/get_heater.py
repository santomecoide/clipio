from coapthon.resources.resource import Resource

class GetHeater(Resource):
    def __init__(self, name="get_heater"):
        super(GetHeater, self).__init__(name)
        self.payload = "Get Heater Resource"

    def render_GET(self, request):
        return self