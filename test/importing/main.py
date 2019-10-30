a_mod = __import__('a', fromlist=['ASS'])
a_klass = getattr(a_mod, 'ASS')

b_mod = __import__('b', fromlist=['BSS'])
b_klass = getattr(b_mod, 'BSS')

try:
    c_mod = __import__('c', fromlist=['CSS'])
    c_klass = getattr(c_mod, 'CSS')
except ModuleNotFoundError:
    print("c no existe")


ass = a_klass()
bss = b_klass() 

ass.saludar()
bss.saludar()