import json
from coapthon.resources.resource import Resource

class GetMetadata(Resource):
    def __init__(self, name="get_metadata"):
        super(GetMetadata, self).__init__(name)
        self.payload = "Get Metadata Resource"

    def render_GET(self, request):
        with open('metadata.json') as myfile:
            data = json.load(myfile)
            self.payload = str(data)
            return self