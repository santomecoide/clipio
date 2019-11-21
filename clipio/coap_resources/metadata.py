import json
from coapthon.resources.resource import Resource
from clipio import constants as CON

class Metadata(Resource):
    def __init__(self):
        super(Metadata, self).__init__("metadata")

    def __fix(self, data):
        fix_data = data.replace("'", '"')
        return fix_data

    def render_GET(self, request):
        with open(CON.METADATA_PATH) as fp:
            data = json.load(fp)
            self.payload = self.__fix(str(data))
            return self