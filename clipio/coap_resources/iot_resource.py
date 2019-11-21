from coapthon.resources.resource import Resource
from clipio.utils.value_helper import ValueHelper

class IotResource(Resource):
    def __init__(self, tag, type_):
        super(IotResource, self).__init__(tag)
        self.__value_helper = ValueHelper(tag, type_)
    
    def render_GET(self, request):
        self.payload = str(self.__value_helper.value)
        return self

    def render_PUT(self, request):
        self.__value_helper.value = request.payload
        return self