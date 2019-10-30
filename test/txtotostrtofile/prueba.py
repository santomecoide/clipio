text = open('text.txt',"r")
data = text.read()
text.close()

format_data = data.format("Algo", "algo", "algo")

to_file = open('file.py',"w+")
to_file.write(format_data)
to_file.close()