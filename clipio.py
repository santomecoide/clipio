import sys
import os
import json

def print_help():
    print("type:")
    print("clipio.py [command] [file] [options]")

def fixPath(path):
    if path[-1:] != chr(47) and path[-1:] != chr(92): 
        path = path + chr(92) 
    return path

def gen_metadata(path):
    path = fixPath(path)
    with open(path + 'metadata.json') as metadata_file:
        data = json.load(metadata_file)
        print(data["name"])

def gen_user_metadata(path, name):
    path = fixPath(path)
    
    metadata_file = open(path + 'src/metadata.json',"w+")
    metadata_file.write('{\n')
    metadata_file.write('\t"name": "' + name + '",\n')
    metadata_file.write('\t"description": "",\n')
    metadata_file.write('\t"resources": [\n')
    metadata_file.write('\t\t{\n')
    metadata_file.write('\t\t\t"name": "",\n')
    metadata_file.write('\t\t\t"description": ""\n')
    metadata_file.write('\t\t},\n')
    metadata_file.write('\t\t{\n')
    metadata_file.write('\t\t\t"name": "",\n')
    metadata_file.write('\t\t\t"description": ""\n')
    metadata_file.write('\t\t}\n')
    metadata_file.write('\t]\n')
    metadata_file.write('}\n')
    metadata_file.close()

def gen_project(name, path):    
    path = fixPath(path)
    
    try: os.mkdir(path)
    except FileExistsError: pass

    try: os.mkdir(path + "src")
    except FileExistsError: pass

    gen_user_metadata(path, name)

try:
    command = sys.argv[1]
    
    if command == "new":
        gen_project(sys.argv[2], sys.argv[3])
    
    if command == "generate":
        file_name = sys.argv[2]
        if file_name == "metadata":
            gen_metadata(sys.argv[3])

    if command == "help":
        print_help()

except IndexError:
    print_help()

        