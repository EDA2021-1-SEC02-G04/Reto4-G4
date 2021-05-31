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


import sys
import config
import threading
from App import controller
from DISClib.ADT import stack
assert config



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
    
    primero=controller.loadlanding_points(cont)
    controller.loadconnections(cont)
    controller.fusion(cont)
    ultimo=controller.load_capitales(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalPoints(cont)
    numpaises = controller.totalPaises(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('Numero de paises: ' + str(numpaises))
    print('\n===Primer landing point===')
    print('Identificador: '+str(primero['landing_point_id'])+str(primero['id']))
    print('Nombre: '+str(primero['name']))
    print('Latitud: '+str(primero['latitude']))
    print('Longitud: '+str(primero['longitude']))
    print('\n===Ultimo pais===')
    print('Nombre: '+str(ultimo['CountryName']))
    print('Población: '+str(ultimo['Population']))
    print('Usuarios de Internet: '+str(ultimo['Internet users']))
def optionThree(cont):
    pass
    


def optionFour(cont, initialStation):
    pass
def optionFive(cont, destStation):
    pass


def optionSix(cont, destStation):
    pass


def optionSeven(cont):
    pass


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
