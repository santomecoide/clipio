from random import random

def busy():
    value = int(random()*100)
    print(value)
    if value > 80:
        return False
    return True

while busy(): pass