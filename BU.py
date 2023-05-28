from collections import deque
from Grammar import *


no_terminales, terminales, simbolo_inicial, producciones = read('input4.txt')
G = gramatica(no_terminales, terminales, simbolo_inicial, producciones)

follow = FOLLOW(G)

if "Ɛ" in terminales:
    terminales.remove("Ɛ")



class Item:
    def __init__(self, symbol, production, dot_position):
        self.symbol = symbol
        self.production = tuple(production)
        self.dot_position = dot_position

    def __eq__(self, other):
        return self.symbol == other.symbol and \
            self.production == other.production and \
            self.dot_position == other.dot_position

    def __hash__(self):
        return hash((self.symbol, self.production, self.dot_position))


def closure(I):
    closure_set = set(I)
    queue = deque(I)
    while queue:
        item = queue.popleft()
        dot_pos = item.dot_position
        if dot_pos < len(item.production) and item.production[dot_pos] in producciones:
            for production in producciones[item.production[dot_pos]]:
                new_item = Item(item.production[dot_pos], production, 0)
                if new_item not in closure_set:
                    closure_set.add(new_item)
                    queue.append(new_item)
    return closure_set


def goto(I, X):
    goto_set = set()
    for item in I:
        dot_pos = item.dot_position
        if dot_pos < len(item.production) and item.production[dot_pos] == X:
            new_item = Item(item.symbol, item.production, dot_pos + 1)
            goto_set.add(new_item)
    return closure(goto_set)


def build_parsing_table():
    parsing_table = {}
    item_sets = []

   
    start_production = list(producciones[simbolo_inicial])[0]
    start_item = Item(simbolo_inicial + "'", [simbolo_inicial], 0)
    initial_set = closure([start_item])

    item_sets.append(initial_set)

    queue = deque([initial_set])
    while queue:
        current_set = queue.popleft()
        for symbol in terminales + no_terminales:
            goto_set = goto(current_set, symbol)
            if goto_set and goto_set not in item_sets:
                item_sets.append(goto_set)
                queue.append(goto_set)

    for i, item_set in enumerate(item_sets):
        action = {}
        goto_dict = {}
        for item in item_set:
            dot_pos = item.dot_position
            production = item.production

            if dot_pos == len(production):
                if item.symbol == simbolo_inicial + "'":
                    action['$'] = 'ACCEPT'
                else:
                    if item.symbol in no_terminales:
                        for j, prod in enumerate(producciones[item.symbol]):
                            if production == tuple(prod.split()):
                                for follow_symbol in follow[item.symbol]:
                                    if follow_symbol in action:
                                        continue
                                    action[follow_symbol] = f'R{j + 1}'
                                break
                    else:
                        for terminal in terminales:
                            if terminal in action:
                                continue
                            if terminal in follow[item.symbol]:
                                action[terminal] = f'R{j + 1}'

            elif dot_pos < len(production) and production[dot_pos] in terminales:
                action[production[dot_pos]] = f'S{item_sets.index(goto(item_set, production[dot_pos]))}'
            elif dot_pos < len(production) and production[dot_pos] in no_terminales:
                goto_dict[production[dot_pos]] = item_sets.index(goto(item_set, production[dot_pos]))

        parsing_table[i] = {
            'action': action,
            'goto': goto_dict
        }


    return parsing_table, item_sets

terminales.append('$')

def print_parsing_table(parsing_table):
    header = ['Estado'] + terminales + no_terminales
    table = [header]

    for state, actions in parsing_table.items():
        row = [str(state)]
        for terminal in terminales:
            row.append(actions['action'].get(terminal, ''))
        for non_terminal in no_terminales:
            row.append(actions['goto'].get(non_terminal, ''))
        table.append(row)

    column_widths = [max(len(str(row[i])) for row in table) for i in range(len(table[0]))]
    table_format = '|'.join('{{:{}}}'.format(width) for width in column_widths)

    print(table_format.format(*table[0]))
    print('-' * sum(column_widths) + '---------')

    for row in table[1:]:
        print(table_format.format(*row))

def verificar_cadena(cadena):
    stack = [0] 
    input_tokens = list(cadena) + ['$']  
    index = 0  

    while True:
        state = stack[-1]  
        token = input_tokens[index] 

        if token not in parsing_table[state]['action']:
            return False  

        action = parsing_table[state]['action'][token]

        if action.startswith('S'):
            next_state = int(action[1:])
            stack.append(token)
            stack.append(next_state)
            index += 1
        elif action.startswith('R'):
            
            production_index = int(action[1:]) - 1
            production = producciones[no_terminales[production_index]]
            for _ in range(2 * len(production[1].split())):
                stack.pop() 
            prev_state = stack[-1]  
            stack.append(production[0])  
            stack.append(parsing_table[prev_state]['goto'][production[0]])
        elif action == 'ACCEPT':
            return True  
        
        return False


if __name__ == '__main__':

    print("Gramática:")
    print('Simbolo Inicial: '+ G.inicial)
    print('No Terminales: '+ str(G.noterminals))
    print('Terminales: '+ str(G.terminals))
    print('Producciones: '+ str(G.producciones))

    parsing_table, item_sets = build_parsing_table()

    print("\nConjuntos de items")
    for i, item_set in enumerate(item_sets):
        print(f"\nITEM {i}:")
        for item in item_set:
            print(
                f"  {item.symbol} -> {' '.join(item.production[:item.dot_position])} . {' '.join(item.production[item.dot_position:])}")
            
    print("\n--------------------------------------------------\n")


    print("Tabla de análisis sintáctico:")
    print_parsing_table(parsing_table)




