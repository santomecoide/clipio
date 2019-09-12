import os
from threading import Thread

from tinydb import TinyDB

from comparator_greater import Greater 
from comparator_less import Less
from comparator_grater_or_equal import GreaterOrEqual
from comparator_less_or_equal import LessOrEqual
from comparator_equal import Equal
from comparator_not_equal import NotEqual

eca_taken = [0]

def greater(eca_id):
    gt = Greater(eca_id)
    gt.set_listener()

def less(eca_id):
    ls = Less(eca_id)
    ls.set_listener()

def greater_or_equal(eca_id):
    gteq = GreaterOrEqual(eca_id)
    gteq.set_listener()

def less_or_equal(eca_id):
    lseq = LessOrEqual(eca_id)
    lseq.set_listener()

def equal(eca_id):
    eq = Equal(eca_id)
    eq.set_listener()

def not_equal(eca_id):
    neq = NotEqual(eca_id)
    neq.set_listener()

def holder(eca):
    print(eca["name"] + " inicio")

    base = eca["actions"][eca["name"]]
    condition = base["input"]["properties"]["condition"]
    
    switcher = {
        ">": greater,
        "<": less,
        ">=": greater_or_equal,
        "<=": less_or_equal,
        "==": equal,
        "!=": not_equal,
    }
    function = switcher.get(
        condition["properties"]["operator"]["const"], 
        lambda:"Invalid"
    )
    function(eca["id"])

    print(eca["name"] + " fin")
    
def main():
    while True:
        eca_db = TinyDB("ecadb.json")
        eca_db.all()
        
        for eca in eca_db.all():
            if eca["id"] not in eca_taken:
                holder_thread = Thread(target=holder, args=(eca, ))
                holder_thread.start()
                eca_taken.append(eca["id"])
        
        eca_db.close()

if __name__ == "__main__":
    main()