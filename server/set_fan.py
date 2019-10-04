from coapthon.resources.resource import Resource

class SetFan(Resource):
    def __init__(self, name="set_fan"):
        super(SetFan, self).__init__(name)
        self.payload = "Set Fan Resource"

    def render_PUT(self, request):
        return self