from abc import abstractmethod
from coapthon.resources.resource import Resource

class IotResource(Resource):
    def __init__(self, name):
        super(IotResource, self).__init__(name)

    @abstractmethod
    def render_GET(self, request):
        pass

    @abstractmethod
    def render_PUT(self, request):
        pass
    