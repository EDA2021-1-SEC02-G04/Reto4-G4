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
from DISClib.ADT import list as lt
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
def optionThree(cont,verta,vertb):
    ans=controller.connectedComponents(cont,verta,vertb)
    respuesta=ans[0]
    print('\nEl numero de clusters es: ' + str(respuesta[0]))
    if respuesta[1]==True:
        print('Los vértices '+ verta +' y '+vertb+ ' están conectados')
    else:
        print('Los vértices '+ verta +' y '+vertb+ ' no están conectados')

    print("Tiempo [ms]: ", f"{ans[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{ans[2]:.3f}")
    
def optionFour(cont):
    ans=controller.mas_conectados(cont)
    respuesta=ans[0]
    print('El mayor número de conexiones es: ' + str(respuesta[0]))
    for landing_point in lt.iterator(respuesta[1]):
        nombre=landing_point['name'].split(',')[0]
        pais=landing_point['name'].split(',')[1]
        print('\nNombre: '+ nombre)
        print('Pais: '+ pais)
        print('Identificador: '+ landing_point['landing_point_id'])
    print("Tiempo [ms]: ", f"{ans[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{ans[2]:.3f}")

def optionFive(cont, pais1,pais2):
    respuesta=controller.distancia_minima_paises(cont,pais1,pais2)
    print('La distancia total entre '+pais1+' y '+pais2+' es '+ str(respuesta[0]))
    for landing_point in lt.iterator(respuesta[1]):
        print(landing_point[0] +' - '+landing_point[1]+' con distancia '+ str(landing_point[2]))
    print("Tiempo [ms]: ", f"{ans[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{ans[2]:.3f}")

def optionSix(cont):
    ans=controller.MST(cont)
    respuesta=ans[0]
    print('El número de vértices en el MST es: '+ str(respuesta[0]))
    print('El peso total es: '+ str(round(respuesta[1],2))+ 'km')
    print("Tiempo [ms]: ", f"{ans[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{ans[2]:.3f}")

def optionSeven(cont,vert):
    ans=controller.error_en_vertice(cont,vert)
    respuesta=ans[0]
    print('Numero de paises afectados: '+ str(respuesta[0]))
    print('Paises afectados:')
    for pais in lt.iterator(respuesta[1]):
        print(pais[0])
    print("Tiempo [ms]: ", f"{ans[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{ans[2]:.3f}")
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
            verta=input('Seleccione el vertice 1: ')
            vertb=input('Seleccione el vertice 2: ')
            optionThree(cont,verta,vertb)

        elif int(inputs[0]) == 4:
            optionFour(cont)

        elif int(inputs[0]) == 5:
            pais1=input('Seleccione el pais 1: ')
            pais2=input('Seleccione el pais 2: ')
            optionFive(cont,pais1,pais2)

        elif int(inputs[0]) == 6:
            optionSix(cont)

        elif int(inputs[0]) == 7:
            vert=input('Seleccione el vertice: ')
            optionSeven(cont,vert)

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
