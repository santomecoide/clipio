import os
__path = os.path.dirname(os.path.abspath(__file__))

__iot_resource_file = open(__path + '/iot_resource.txt','r')
iot_resource_seed = __iot_resource_file.read()
__iot_resource_file.close()

__app_resource_file = open(__path + '/app_resource.txt','r')
app_resource_seed = __app_resource_file.read()
__app_resource_file.close()