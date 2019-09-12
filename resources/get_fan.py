from coapthon.resources.resource import Resource

class GetFan(Resource):
    def __init__(self, name="get_fan"):
        super(GetFan, self).__init__(name)
        self.payload = "Get Fan Resource"

    def render_GET(self, request):
        return self