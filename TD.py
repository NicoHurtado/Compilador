import pandas as pd
from Grammar import *



def es_recursiva_izquierda(G):
    for no_terminal in G.noterminals:
        for produccion in G.producciones[no_terminal]:
            if produccion.startswith(no_terminal):
                return True
    return False

def es_LL1(tabla):
    for no_terminal in tabla:
        for terminal in tabla[no_terminal]:
            producciones = tabla[no_terminal][terminal]
            if len(producciones) > 1:
                print(f"Conflicto en la casilla {no_terminal} - {terminal}")
                return False
    return True




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


def actualizar_tabla(tabla, noterminales, first, follow):
    for no_terminal in noterminales:
        if 'Ɛ' in first[no_terminal]:
            for terminal in follow[no_terminal]:
                tabla[no_terminal][terminal].append('Ɛ')
    return tabla


def Duplicados(dict):
    for i in dict:
        dict[i] = list(set(dict[i]))
    return dict


def QuitarEpsilon(diccionario):
    claves_epsilon = [clave for clave, valor in diccionario.items() if clave == 'Ɛ']

    for clave in claves_epsilon:
        diccionario.pop(clave)

    for valor in diccionario.values():
        if isinstance(valor, dict):
            QuitarEpsilon(valor)

    return diccionario



def verificar_cadena(tabla, G, cadena):
    cadena += '$'
    pila = ['$'] 
    pila.append(G.inicial) 

    simbolo_cadena = cadena[0]
    while len(pila) > 0 :
        print(f'pila: {pila}, simbolo_cadena: {simbolo_cadena}')
        simbolo_pila = pila.pop()
        simbolo_cadena = cadena[0]
        if simbolo_pila in G.terminals or simbolo_pila == '$':
            if simbolo_pila == simbolo_cadena and simbolo_cadena == '$':
                return True
            elif simbolo_pila == simbolo_cadena:
                cadena = cadena[1:]
                simbolo_cadena = cadena[0]
            else:
                return False
        else:
            if simbolo_cadena in tabla[simbolo_pila] and len(tabla[simbolo_pila][simbolo_cadena]) > 0:
                produccion = tabla[simbolo_pila][simbolo_cadena][0]
                if produccion != 'Ɛ':
                    for simbolo in reversed(produccion):
                        pila.append(simbolo)
            else:
                return False
    return True





def analizar(txt):
    noterminals, terminals, inicial, producciones = read(txt)

    print("\n")

    print("Simbolo inicial: ", inicial)
    print(f"NO Terminales: {noterminals}")
    print(f"Terminales: {terminals}")
    print(f"Producciones: {producciones}\n")
    print("--" * 20 + "\n")

    G = gramatica(noterminals, terminals, inicial, producciones)

    FIRST_SET = FIRST(G)
    FOLLOW_SET = FOLLOW(G)
    FIRST_SET = Duplicados(FIRST_SET)
    FOLLOW_SET = Duplicados(FOLLOW_SET)

    print(f"FIRST: {FIRST_SET}\n")
    print("--" * 20 + "\n")
    print(f"FOLLOW: {FOLLOW_SET}\n")

    if es_recursiva_izquierda(G):
        print("esta gramatica es recursiva por izquierda")
    else:
        print("--" * 8 + " Tabla de analisis sintactico " + "--" * 8 + "\n")

        tabla = Tabla(terminals, noterminals, producciones)
        tabla = actualizar_tabla(tabla, noterminals, FIRST_SET, FOLLOW_SET)
        tabla = QuitarEpsilon(tabla)
        df = pd.DataFrame(tabla)
        df = df.transpose()
        print(df)

        seguir = True
        while seguir:
            if es_LL1(tabla):
                cadena_para_V = input("Ingrese su cadena: ")
                if verificar_cadena(tabla, G, cadena_para_V):
                     print("Esta cadena es válida.")
                else:
                     print("Esta cadena es inválida.")
            else:
                print("esta gramatica no es LL1")
            seguir = False




if __name__ == '__main__':
    print('--' * 10 + 'Test 1' + '--' * 10 + '\n')
    analizar('input3.txt')
    print('\n')
    
# input -> LL1
# input2 -> NO LL1
# input3 -> LL1
# input4 -> LL1 (Recursiva por izquierda)