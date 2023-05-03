class gramatica:

    def __init__(self, noterminals, terminals, inicial, producciones):
        self.noterminals = noterminals
        self.terminals = terminals
        self.inicial = inicial
        self.producciones = producciones

    

def read(file):

    noterminals = []
    terminals = []
    inicial = ''
    producciones = {}

    with open(file, 'r') as file:
        contenido = file.read()
        inicial = contenido[0]

    for i in contenido.split():
        if i.isupper():
            noterminals.append(i)
        elif i.islower():
            terminals.append(i)

    NonSet = set(noterminals)
    TermSet = set(terminals)
    
    noterminals = list(NonSet)
    terminals = list(TermSet)

    for i in terminals:
        if i == 'epsilon':
            terminals.remove(i)

    for i in contenido.split('\n'):
        if '-' in i:
            no_terminal, produccion = i.split('-')
            producciones[no_terminal.strip()] = [p.replace(' ', '') for p in produccion.split('|')]

    return noterminals, terminals, inicial, producciones

a = [1,2,3]

def main():

    noterminal, terminals, inicial, producciones = read('input.txt')

    print("Simbolo inicial: ", inicial)
    print(f'NO Terminales: {noterminal}')
    print(f'Terminales: {terminals}')
    print(f'Producciones: {producciones}')

    G = gramatica(noterminal, terminals, inicial, producciones)

if __name__ == '__main__':
    main()