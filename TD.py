import pandas as pd

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

    with open(file, 'r', encoding='utf-8') as file:
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

    if 'Ɛ' not in terminals:
        terminals.append('Ɛ')

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

def FOLLOW(G):
    follows = {}
    for nonterminal in G.noterminals:
        follows[nonterminal] = []
    follows[G.inicial].append('$')
    for nonterminal in G.noterminals:
        for production in G.producciones[nonterminal]:
            for i in range(len(production)):
                if production[i] in G.noterminals:
                    if i == len(production) - 1:
                        follows[production[i]].extend(follows[nonterminal])
                    else:
                        if production[i+1] in G.terminals:
                            follows[production[i]].append(production[i+1])
                        else:
                            follows[production[i]].extend(FIRST(G, production[i+1], G.producciones[production[i+1]]))
                            if 'Ɛ' in follows[production[i]]:
                                follows[production[i]].remove('Ɛ')
                                follows[production[i]].extend(follows[nonterminal])
    return follows

def Tabla(terminales, noterminales, producciones):
    tabla = {}
    for no_terminal in noterminales:
        tabla[no_terminal] = {}
        for terminal in terminales:
            tabla[no_terminal][terminal] = []
        tabla[no_terminal]['$'] = []
    for no_terminal, produccion in producciones.items():
        for prod in produccion:
            primerSimbolo = prod[0]
            if primerSimbolo in terminales:
                tabla[no_terminal][primerSimbolo].append(prod)
            elif primerSimbolo in noterminales:
                primeros = PrimeroDeCadaProduccion(terminales, noterminales, producciones, prod)
                for simbolo in primeros:
                    tabla[no_terminal][simbolo].append(prod)
                if 'Ɛ' in primeros:
                    for simbolo in tabla[no_terminal]['$']:
                        tabla[no_terminal][simbolo].append(prod)
    return tabla

def PrimeroDeCadaProduccion(terminales, no_terminales, producciones, produccion):
    primeros = set()
    primer_simbolo = produccion[0]
    if primer_simbolo in terminales:
        primeros.add(primer_simbolo)
    elif primer_simbolo in no_terminales:
        for prod in producciones[primer_simbolo]:
            if prod == 'Ɛ':
                if len(produccion) == 1:
                    primeros.add('Ɛ')
                else:
                    for simbolo in PrimeroDeCadaProduccion(terminales, no_terminales, producciones, produccion[1:]):
                        primeros.add(simbolo)
            else:
                for simbolo in PrimeroDeCadaProduccion(terminales, no_terminales, producciones, prod):
                    primeros.add(simbolo)
    
    return primeros


def Duplicados(dict):
    for i in dict:
        dict[i] = list(set(dict[i]))
    return dict

def main():

    noterminals, terminals, inicial, producciones = read('input.txt')

    print('--'*10 + 'Proyecto Compiladores' + '--'*10 + '\n')

    print("Simbolo inicial: ", inicial)
    print(f'NO Terminales: {noterminals}')
    print(f'Terminales: {terminals}')
    print(f'Producciones: {producciones}\n')
    print('--'*20+'\n')

    G = gramatica(noterminals, terminals, inicial, producciones)

    FIRST_SET = {}

    for i in noterminals:
        FIRST_SET[i] = []

    FIRST(G, G.inicial, G.producciones[G.inicial], FIRST_SET)
    FOLLOW_SET = FOLLOW(G)
    FIRST_SET = Duplicados(FIRST_SET)
    FOLLOW_SET = Duplicados(FOLLOW_SET)
    

    print(f'FIRST: {FIRST_SET}\n')
    print('--'*20+'\n')
    print(f'FOLLOW: {FOLLOW_SET}\n')

    print('--'*8 + ' Tabla de analisis sintactico ' + '--'*8 + '\n')
    tabla = Tabla(terminals, noterminals, producciones)
    df = pd.DataFrame(tabla)
    df = df.transpose() 
    print(df)


if __name__ == '__main__':
    main()