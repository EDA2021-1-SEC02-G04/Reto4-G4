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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config
from DISClib.ADT.graph import addEdge, gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import mapentry as me
from DISClib import haversine as hs
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'landing_points': None,
                    'connections': None,
                    'components': None,
                    'paths': None,
                    'paises':None
                    }

        analyzer['landing_points'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=comparelanding_points)

        analyzer['connections_distancia'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=comparevertices)
        analyzer['connections_internet'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=comparevertices)
        analyzer['paises'] = m.newMap(numelements=400,
                                     maptype='PROBING',
                                     comparefunction=comparelanding_points)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

"""
def addStopConnection(analyzer, service):
    """"""
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """"""
    try:
        addlanding_point(analyzer, origin)
        addConnection(analyzer, origin, destination, distance)
        addRouteStop(analyzer, service)
        addRouteStop(analyzer, lastservice)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')
"""


def loadlanding_points_distancia(analyzer,landing_point):
    lista=lt.newList(datastructure='ARRAY_LIST')
    landing_point["conexiones"]=lista
    mapa_vertices=analyzer["landing_points"]
    if not m.contains(mapa_vertices,landing_point["landing_point_id"]):
        m.put(mapa_vertices,landing_point["landing_point_id"],landing_point)

def loadconnections_distancia(analyzer,connection):
    grafo=analyzer["connections_distancia"]
    mapa=analyzer["landing_points"]
    peso=0
    if not gr.containsVertex(grafo,(connection["origin"],connection["cable_id"])):
        gr.insertVertex(grafo,(connection["origin"],connection["cable_id"]))
        pareja1=m.get(mapa,connection["origin"])
        valor1=me.getValue(pareja1)
        lt.addLast(valor1["conexiones"],{'vertice':(connection["origin"],connection["cable_id"]),"capacityTBPS":connection["capacityTBPS"]})
    if not gr.containsVertex(grafo,(connection["destination"],connection["cable_id"])):
        gr.insertVertex(grafo,(connection["destination"],connection["cable_id"]))
        pareja2=m.get(mapa,connection["destination"])
        valor2=me.getValue(pareja2)
        lt.addLast(valor2["conexiones"],{'vertice':(connection["destination"],connection["cable_id"]),"capacityTBPS":connection["capacityTBPS"]})
        if connection["cable_length"]!='n.a.':
            peso=float(connection["cable_length"][:-3].replace(',',''))
    gr.addEdge(grafo,(connection["origin"],connection["cable_id"]),(connection["destination"],connection["cable_id"]),peso)
    gr.addEdge(grafo,(connection["destination"],connection["cable_id"]),(connection["origin"],connection["cable_id"]),peso)

def fusion_distancia(analyzer):
    lstpoints = m.valueSet(analyzer['landing_points'])
    for key in lt.iterator(lstpoints):
        punto=key["conexiones"]
        for subvertice1 in lt.iterator(punto):
            for subvertice2 in lt.iterator(punto):
                if subvertice1 != subvertice2:
                    gr.addEdge(analyzer["connections_distancia"],subvertice1['vertice'],subvertice2['vertice'],0.1)


def addcapital_distancia(analyzer,capital):    
    grafo=analyzer["connections_distancia"]
    lista_landing=m.valueSet(analyzer["landing_points"])
    m.put(analyzer['paises'],capital['CountryName'],capital['CapitalName'])
    if capital['CapitalLatitude']!='':
        menor=None
        dist=None
        for punto in lt.iterator(lista_landing):
            distancia=hs.haversine((float(capital['CapitalLatitude']),float(capital['CapitalLongitude'])),(float(punto['latitude']),float(punto['longitude'])))
            if dist==None or distancia<dist :
                dist=distancia
                menor=punto
        gr.insertVertex(grafo,(capital['CapitalName'],'capital'))
        gr.addEdge(grafo,(capital['CapitalName'],'capital'),lt.getElement(menor['conexiones'],1)['vertice'],dist)






def loadlanding_points_internet(analyzer,landing_point):
    lista=lt.newList(datastructure='ARRAY_LIST')
    landing_point["conexiones_internet"]=lista
    mapa_vertices=analyzer["landing_points"]
    if not m.contains(mapa_vertices,landing_point["landing_point_id"]):
        m.put(mapa_vertices,landing_point["landing_point_id"],landing_point)

def loadconnections_internet(analyzer,connection):
    grafo=analyzer["connections_internet"]
    mapa=analyzer["landing_points"]
    peso=0
    if not gr.containsVertex(grafo,(connection["origin"],connection["cable_id"])):
        gr.insertVertex(grafo,(connection["origin"],connection["cable_id"]))
        pareja1=m.get(mapa,connection["origin"])
        valor1=me.getValue(pareja1)
        lt.addLast(valor1["conexiones"],{'vertice':(connection["origin"],connection["cable_id"]),"capacityTBPS":connection["capacityTBPS"]})
    if not gr.containsVertex(grafo,(connection["destination"],connection["cable_id"])):
        gr.insertVertex(grafo,(connection["destination"],connection["cable_id"]))
        pareja2=m.get(mapa,connection["destination"])
        valor2=me.getValue(pareja2)
        lt.addLast(valor2["conexiones"],{'vertice':(connection["destination"],connection["cable_id"]),"capacityTBPS":connection["capacityTBPS"]})
        peso=float(connection["capacityTBPS"])
    gr.addEdge(grafo,(connection["origin"],connection["cable_id"]),(connection["destination"],connection["cable_id"]),peso)
    gr.addEdge(grafo,(connection["destination"],connection["cable_id"]),(connection["origin"],connection["cable_id"]),peso)

def fusion_internet(analyzer):
    lstpoints = m.valueSet(analyzer['landing_points'])
    for key in lt.iterator(lstpoints):
        punto=key["conexiones"]
        for subvertice1 in lt.iterator(punto):
            for subvertice2 in lt.iterator(punto):
                if subvertice1 != subvertice2:
                    gr.addEdge(analyzer["connections_internet"],subvertice1['vertice'],subvertice2['vertice'],0.1)


def addcapital_internet(analyzer,capital):    
    grafo=analyzer["connections_internet"]
    lista_landing=m.valueSet(analyzer["landing_points"])
    if capital['CapitalLatitude']!='':
        menor=None
        dist=None
        for punto in lt.iterator(lista_landing):
            distancia=hs.haversine((float(capital['CapitalLatitude']),float(capital['CapitalLongitude'])),(float(punto['latitude']),float(punto['longitude'])))
            if dist==None or distancia<dist :
                dist=distancia
                menor=punto
        internet=minimo_internet(menor)
        gr.insertVertex(grafo,(capital['CapitalName'],'capital'))
        gr.addEdge(grafo,(capital['CapitalName'],'capital'),lt.getElement(menor['conexiones'],1)['vertice'],internet)

def minimo_internet(landing_point):
    minimo=None
    for vertice in lt.iterator(landing_point['conexiones']):
        internet=vertice["capacityTBPS"]
        if minimo==None or internet<minimo :
            minimo=internet
    return minimo
    
# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta
def totalPoints(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections_distancia'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections_distancia'])

def totalPaises(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return m.size(analyzer['paises'])

# Funciones utilizadas para comparar elementos dentro de una lista


def comparelanding_points(landing_point1, landing_point2):
    """
    Compara dos estaciones
    """
    
    if (landing_point1 == landing_point2["key"]):
        return 0
    elif (landing_point1 > landing_point2["key"]):
        return 1
    else:
        return -1

def comparevertices(vertice1, vertice2):
    """
    Compara dos estaciones
    """
    if (vertice1 == vertice2["key"]):
        return 0
    else:
        return -1

# Funciones de ordenamiento