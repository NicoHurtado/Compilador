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
        elif i.islower() or i in ['[', ']', '+', '*', '(', ')', '=', '?']:
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


def FIRST(G):
    FIRST_SET = {}
    for nonterminal in G.noterminals:
        FIRST_SET[nonterminal] = set()
    update_terminals(G)

    flag = True
    while flag:
        flag = False
        for nonterminal in G.noterminals:
            for production in G.producciones[nonterminal]:
                counter = 0
                while counter < len(production):
                    element = production[counter]
                    if element in G.terminals:
                        if element not in FIRST_SET[nonterminal]:
                            FIRST_SET[nonterminal].add(element)
                            flag = True
                        break
                    elif element in G.noterminals:
                        if 'Ɛ' not in FIRST_SET[element]:
                            if not (FIRST_SET[element] - {'Ɛ'}).issubset(FIRST_SET[nonterminal]):
                                FIRST_SET[nonterminal].update(FIRST_SET[element] - {'Ɛ'})
                                flag = True
                            break
                        else:
                            if counter == len(production) - 1 and 'Ɛ' in FIRST_SET[element]:
                                FIRST_SET[nonterminal].add('Ɛ')
                                flag = True
                            elif not (FIRST_SET[element] - {'Ɛ'}).issubset(FIRST_SET[nonterminal]):
                                FIRST_SET[nonterminal].update(FIRST_SET[element] - {'Ɛ'})
                                flag = True
                    else:
                        break
                    counter += 1

                if counter == len(production) and 'Ɛ' in FIRST_SET[element]:
                    FIRST_SET[nonterminal].add('Ɛ')
                    flag = True

    # Asegurarse de que 'Ɛ' se incluya en el conjunto FIRST del símbolo inicial
    if 'Ɛ' in FIRST_SET[G.inicial]:
        FIRST_SET[G.inicial].add('Ɛ')

    for terminal in G.terminals:
        FIRST_SET[terminal] = {terminal}
    FIRST_SET['Ɛ'] = {'Ɛ'}
    for nonterminal in G.noterminals:
        for production in G.producciones[nonterminal]:
            if production == 'Ɛ':
                FIRST_SET[nonterminal].add(production)

    return FIRST_SET


def FOLLOW(G):
    follows = {}
    for nonterminal in G.noterminals:
        follows[nonterminal] = set()
    follows[G.inicial].add('$')
    first_set = FIRST(G)
    while True:
        updated = False
        for nonterminal in G.noterminals:
            for production in G.producciones[nonterminal]:
                for i in range(len(production)):
                    if production[i] in G.noterminals:
                        if i == len(production) - 1:
                            new_follows = follows[nonterminal] - follows[production[i]]
                            if new_follows:
                                follows[production[i]].update(new_follows)
                                updated = True
                        else:
                            if production[i + 1] in G.terminals:
                                if production[i + 1] not in follows[production[i]]:
                                    follows[production[i]].add(production[i + 1])
                                    updated = True
                            else:
                                new_follows = first_set[production[i + 1]] - {'Ɛ'} - follows[production[i]]
                                if new_follows:
                                    follows[production[i]].update(new_follows)
                                    updated = True
                                if 'Ɛ' in first_set[production[i + 1]]:
                                    j = i + 2
                                    while j < len(production) and 'Ɛ' in first_set[production[j]]:
                                        j += 1
                                    if j == len(production):
                                        new_follows = follows[nonterminal] - follows[production[i]]
                                        if new_follows:
                                            follows[production[i]].update(new_follows)
                                            updated = True
        if not updated:
            break
    return {k: list(v) for k, v in follows.items()}


def update_terminals(G):
    terminals = set()
    for noterminal in G.noterminals:
        for production in G.producciones[noterminal]:
            for symbol in production:
                if symbol not in G.noterminals and symbol != 'Ɛ':
                    terminals.add(symbol)
    G.terminals = list(terminals)