metadata = {
	"name": "nodo",
	"description": "",
	"resources": [
		{
			"tag": "a",
			"name": "a",
			"description": " a",
			"type": "a",
			"unit": "a"
		},
		{
			"tag": " b",
			"name": "b",
			"description": "b",
			"type": " b",
			"unit": "  b"
		}
	]
}

for key, value in metadata.items(): 
    if isinstance(value, list):
        for v in value:
            for key2, value2 in v.items():
                index = value.index(v)
                metadata[key][index][key2] = value2.strip() 
    else:
        metadata[key] = value.strip()

print(metadata)