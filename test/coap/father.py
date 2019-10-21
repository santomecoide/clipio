from abc import abstractmethod
from coapthon.resources.resource import Resource

class Father(Resource):
    def __init__(self, name):
        super(Father, self).__init__(name)

    @abstractmethod
    def render_GET(self, request):
        print("---------")
        print("padre")
        print("padre")