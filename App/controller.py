"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
from App import model
import csv
import time
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadlanding_points(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = cf.data_dir + "landing_points.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8-sig"),
                                delimiter=",")
    primero=True
    for landing_point in input_file:
        if primero==True:
            primer_landing=landing_point
            primero=False
        model.loadlanding_points_distancia(analyzer,landing_point)
        model.loadlanding_points_internet(analyzer,landing_point)
    return  primer_landing
        
        
    
    return analyzer
def loadconnections(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = cf.data_dir + "connections.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8-sig"),
                                delimiter=",")
    
    for connection in input_file:
    
        model.loadconnections_distancia(analyzer,connection)
        model.loadconnections_internet(analyzer,connection)
    return analyzer


def fusion(analyzer):
    model.fusion_distancia(analyzer)
    model.fusion_internet(analyzer)


def load_capitales(analyzer):
    servicesfile = cf.data_dir + "countries.csv"
    input_file = csv.DictReader(open(servicesfile, encoding='utf-8'),
                                delimiter=",")
    for capital in input_file:
        model.addcapital_distancia(analyzer,capital)
        model.addcapital_internet(analyzer,capital)
        ultimo=capital
    return ultimo



# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalPoints(analyzer):

    return model.totalPoints(analyzer)


def totalConnections(analyzer):

    return model.totalConnections(analyzer)

def totalPaises(analyzer):

    return model.totalPaises(analyzer)

def connectedComponents(analyzer,verta,vertb):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta=model.connectedComponents(analyzer,verta,vertb)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return (respuesta,delta_time,delta_memory)

def mas_conectados(analyzer):
    delta_time = -1.0
    delta_memory = -1.0
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta=model.mas_conectados(analyzer)
    stop_memory = getMemory()
    stop_time = getTime()
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return (respuesta,delta_time,delta_memory)

def distancia_minima_paises(analyzer,pais1,pais2):
    delta_time = -1.0
    delta_memory = -1.0
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta=model.distancia_minima_paises(analyzer,pais1,pais2)
    stop_memory = getMemory()
    stop_time = getTime()
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return (respuesta,delta_time,delta_memory)
    

def MST(analyzer):
    delta_time = -1.0
    delta_memory = -1.0
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta=model.model.MST(analyzer)
    stop_memory = getMemory()
    stop_time = getTime()
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return (respuesta,delta_time,delta_memory)


def error_en_vertice(analyzer,vertice):
    delta_time = -1.0
    delta_memory = -1.0
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta=model.model.MST(analyzer)
    stop_memory = getMemory()
    stop_time = getTime()
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return (respuesta,delta_time,delta_memory)

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
