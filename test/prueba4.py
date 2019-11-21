from urllib.parse import urlparse
a = "mqtt://domain:port/project_name/topoic"
url_components = urlparse(a)

path = url_components.path.split("/")

print(url_components.hostname)