InicialSymbol = ''
Terminals = []
NONTerminals = []
Productions = []


with open('input.txt', 'r') as file:
    contenido = file.read()
    InicialSymbol = contenido[0]
    
    for i in contenido.split():
        if i.isupper():
            NONTerminals.append(i)
        elif i.islower():
            Terminals.append(i)

    NonSet = set(NONTerminals)
    TermSet = set(Terminals)
    
    NONterminal = list(NonSet)
    Terminals = list(TermSet)
    for i in Terminals:
        if i == 'epsilon':
            Terminals.remove(i)
    
    for i in contenido.split('\n'):
        if i != '':
            Productions.append(i)

    
print("Simbolo inicial: ", InicialSymbol)
print(f'NO Terminales: {NONterminal}')
print(f'Terminales: {Terminals}')
print(f'Producciones: {Productions}')

