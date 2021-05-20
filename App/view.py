"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Catalogo")
    print("2- Cargar información")
    print("3- Calcular componentes conectados")
    print("4- Landing points con más cables")
    print("5- Ruta minima entre dos paises")
    print("6- Red de expansión con mínima distancia")
    print("7- Analizar fallo en un landing point")
    print("0- Salir")
    print("*******************************************")


def optionTwo(cont):
    print("\nCargando datos ....")
    controller.loadServices(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))


def optionThree(cont):



def optionFour(cont, initialStation):

def optionFive(cont, destStation):



def optionSix(cont, destStation):



def optionSeven(cont):



"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            cont = controller.init()

        elif int(inputs[0]) == 2:
            optionTwo(cont)

        elif int(inputs[0]) == 3:
            optionThree(cont)

        elif int(inputs[0]) == 4:
            msg = "Estación Base: BusStopCode-ServiceNo (Ej: 75009-10): "
            initialStation = input(msg)
            optionFour(cont, initialStation)

        elif int(inputs[0]) == 5:
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionFive(cont, destStation)

        elif int(inputs[0]) == 6:
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionSix(cont, destStation)

        elif int(inputs[0]) == 7:
            optionSeven(cont)

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
