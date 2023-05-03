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

    for i in noterminals:
        if i == 'Ɛ':
            noterminals.remove(i)

    for i in contenido.split('\n'):
        if '-' in i:
            no_terminal, produccion = i.split('-')
            producciones[no_terminal.strip()] = [p.replace(' ', '') for p in produccion.split('|')]

    return noterminals, terminals, inicial, producciones

def FIRST(G, symbol, P, FIRST_SET):
    for production in P:
        counter = 0
        for element in production:
            if element in G.terminals:
                FIRST_SET[symbol].append(element)
                break
            if element in G.noterminals:
                counter += 1
                if FIRST(G, element, G.producciones[element], FIRST_SET):
                    FIRST_SET[symbol].extend(FIRST_SET[element])
                    FIRST_SET[symbol].remove('Ɛ')
                else:
                    FIRST_SET[symbol].extend(FIRST_SET[element])
                    break

                if counter == len(production):
                    if 'Ɛ' in FIRST_SET[element]:
                        FIRST_SET[symbol].append('Ɛ')

def main():

    noterminals, terminals, inicial, producciones = read('input.txt')

    print("Simbolo inicial: ", inicial)
    print(f'NO Terminales: {noterminals}')
    print(f'Terminales: {terminals}')
    print(f'Producciones: {producciones}')
    print('--'*10)

    G = gramatica(noterminals, terminals, inicial, producciones)

    FIRST_SET = {}

    for i in noterminals:
        FIRST_SET[i] = []

    FIRST(G, G.inicial, G.producciones[G.inicial], FIRST_SET)
    print(f'FIRST: {FIRST_SET}')

if __name__ == '__main__':
    main()