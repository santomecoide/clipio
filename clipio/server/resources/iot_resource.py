from coapthon.resources.resource import Resource

class IotResource(Resource):
    def __init__(self, name): 
        super(IotResource, self).__init__(name)

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        return self