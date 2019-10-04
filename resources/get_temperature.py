import random
from coapthon.resources.resource import Resource

class GetTemperature(Resource):
    def __init__(self, name="get_temperature"):
        super(GetTemperature, self).__init__(name)
        self.payload = "Get Temperature Resource"

    def render_GET(self, request):
        self.payload = str(random.randint(1,20))
        return self