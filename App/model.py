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

from math import trunc
import config
from DISClib.ADT.graph import gr, vertices
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Utils import error as error
from DISClib.DataStructures import mapentry as me
from DISClib import haversine as hs
from DISClib.Algorithms.Sorting import mergesort as ms
import math
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
                    'paises':None,
                    'components':None,
                    'traduccion':None
                    }

        analyzer['landing_points'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=comparelanding_points)
        analyzer['traduccion'] = m.newMap(numelements=14000,
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
    landing_point["conexiones"]=lt.newList()
    landing_point["vecinos"]=lt.newList()
    mapa_vertices=analyzer["landing_points"]
    if not m.contains(mapa_vertices,landing_point["landing_point_id"]):
        m.put(mapa_vertices,landing_point["landing_point_id"],landing_point)
    nombre=landing_point["name"].split(',')[0]
    if not m.contains(analyzer['traduccion'],landing_point["name"]):
        m.put(analyzer['traduccion'],nombre,landing_point["landing_point_id"])

def loadconnections_distancia(analyzer,connection):
    grafo=analyzer["connections_distancia"]
    mapa=analyzer["landing_points"]
    peso=0
    if not gr.containsVertex(grafo,(connection["origin"],connection["cable_id"])):
        gr.insertVertex(grafo,(connection["origin"],connection["cable_id"]))
        pareja1=m.get(mapa,connection["origin"])
        valor1=me.getValue(pareja1)
        lt.addLast(valor1["conexiones"],{'vertice':(connection["origin"],connection["cable_id"]),"capacityTBPS":connection["capacityTBPS"]})
        lt.addLast(valor1["vecinos"],(connection["destination"],connection["cable_id"],connection['cable_length'][:-3].replace(',','')))
    if not gr.containsVertex(grafo,(connection["destination"],connection["cable_id"])):
        gr.insertVertex(grafo,(connection["destination"],connection["cable_id"]))
        pareja2=m.get(mapa,connection["destination"])
        valor2=me.getValue(pareja2)
        lt.addLast(valor2["conexiones"],{'vertice':(connection["destination"],connection["cable_id"]),"capacityTBPS":connection["capacityTBPS"]})
        lt.addLast(valor2["vecinos"],(connection["origin"],connection["cable_id"],connection['cable_length'][:-3].replace(',','')))
    if connection["cable_length"]!='n.a.':
        peso=float(connection["cable_length"][:-3].replace(',',''))
    else:
        par1=m.get(mapa,connection["origin"])
        lat1=me.getValue(par1)['latitude']
        lon1=me.getValue(par1)['longitude']
        par2=m.get(mapa,connection["destination"])
        lat2=me.getValue(par2)['latitude']
        lon2=me.getValue(par2)['longitude']
        peso=hs.haversine((float(lat1),float(lon1)),((float(lat2),float(lon2))))
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
    gr.insertVertex(grafo,(capital['CapitalName'],'capital'))
    for punto in lt.iterator(lista_landing):
        en_pais=False
        try:
            pais=punto['name'].split(',')[1].strip()
        except:
            pais=0
        if pais==capital['CountryName']:
            en_pais=True
            dist=hs.haversine((float(capital['CapitalLatitude']),float(capital['CapitalLongitude'])),(float(punto['latitude']),float(punto['longitude'])))
            gr.addEdge(grafo,(capital['CapitalName'],'capital'),lt.getElement(punto['conexiones'],1)['vertice'],dist)
            gr.addEdge(grafo,lt.getElement(punto['conexiones'],1)['vertice'],(capital['CapitalName'],'capital'),dist)
    if en_pais==False:
        menor=None
        dist=None
        for punto in lt.iterator(lista_landing):
            
            distancia=hs.haversine((float(capital['CapitalLatitude']),float(capital['CapitalLongitude'])),(float(punto['latitude']),float(punto['longitude'])))
            
            if dist==None or distancia<dist :
                dist=distancia
                menor=punto
        gr.addEdge(grafo,(capital['CapitalName'],'capital'),lt.getElement(menor['conexiones'],1)['vertice'],dist)
        gr.addEdge(grafo,lt.getElement(menor['conexiones'],1)['vertice'],(capital['CapitalName'],'capital'),dist)






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


def connectedComponents(analyzer,verta,vertb):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections_distancia'])
    id_a=traduccion(verta,analyzer)
    id_b=traduccion(vertb,analyzer)
    pareja1=m.get(analyzer['landing_points'],id_a)
    cableid1=lt.getElement(me.getValue(pareja1)['conexiones'],1)['vertice'][1]
    pareja2=m.get(analyzer['landing_points'],id_b)
    cableid2=lt.getElement(me.getValue(pareja2)['conexiones'],1)['vertice'][1]
    vertice1=(id_a,cableid1)
    vertice2=(id_b,cableid2)
    conectados=scc.stronglyConnected(analyzer['components'], vertice1, vertice2)
    return (scc.connectedComponents(analyzer['components']),conectados)


def traduccion(name,analyzer):
    x=m.get(analyzer["traduccion"],name)
    return me.getValue(x)

def pais_capital(analyzer,pais):
    x=m.get(analyzer["paises"],pais)
    return me.getValue(x)

def mas_conectados(analyzer):
    lista=lt.newList()
    maximo=0
    for landing_point in lt.iterator(m.valueSet(analyzer['landing_points'])):
        cantidad_vecinos=lt.size(landing_point['conexiones'])
        if cantidad_vecinos==maximo:
            lt.addLast(lista,landing_point)
        elif cantidad_vecinos>maximo:
            lista=lt.newList()
            lt.addLast(lista,landing_point)
            maximo=cantidad_vecinos
    return (maximo,lista)

def distancia_minima_paises(analyzer,pais1,pais2):
    capital1=pais_capital(analyzer,pais1)
    capital2=pais_capital(analyzer,pais2)
    vertice1=(capital1,'capital')
    vertice2=(capital2,'capital')
    analyzer['MST_Dij'] = djk.Dijkstra(analyzer['connections_distancia'],vertice1)
    distancia_minima=djk.distTo(analyzer['MST_Dij'],vertice2)
    camino=djk.pathTo(analyzer['MST_Dij'],vertice2)
    camino_final=lt.newList()
    for conexion in lt.iterator(camino):
        try:
            int(conexion['vertexA'][0])
            verticea=conexion['vertexA'][0]
            pareja1=m.get(analyzer['landing_points'],verticea)
            nombrea=me.getValue(pareja1)['name'].split(',')[0]
        except:
            nombrea=conexion['vertexA'][0]

        try:
            int(conexion['vertexB'][0])
            verticeb=conexion['vertexB'][0]
            pareja2=m.get(analyzer['landing_points'],verticeb)
            nombreb=me.getValue(pareja2)['name'].split(',')[0]
        except:
            nombreb=conexion['vertexB'][0]


        conexion=(nombrea,nombreb,conexion['weight'])
        lt.addLast(camino_final,conexion)
    return distancia_minima,camino_final

def MST(analyzer):
    analyzer['MST']=prim.PrimMST(analyzer['connections_distancia'])
    suma=0
    contador=0
    for i in lt.iterator(m.valueSet(analyzer['MST']['distTo'])):
        suma+=i
        contador+=1
    analyzer['Dij']=djk.Dijkstra(analyzer['connections_distancia'],lt.getElement(gr.vertices(analyzer['connections_distancia']),5))
    maximo=None
    distancia=0
    for vertice in lt.iterator(gr.vertices(analyzer['connections_distancia'])):
        camino=djk.pathTo(analyzer['Dij'],vertice)
        if camino!=None:
            if st.size(camino)>distancia and distancia!=math.inf:
                maximo=camino
                distancia=st.size(camino)
    camino_final=lt.newList()
    for conexion in lt.iterator(camino):
        try:
            int(conexion['vertexA'][0])
            verticea=conexion['vertexA'][0]
            pareja1=m.get(analyzer['landing_points'],verticea)
            nombrea=me.getValue(pareja1)['name'].split(',')[0]
        except:
            nombrea=conexion['vertexA'][0]

        try:
            int(conexion['vertexB'][0])
            verticeb=conexion['vertexB'][0]
            pareja2=m.get(analyzer['landing_points'],verticeb)
            nombreb=me.getValue(pareja2)['name'].split(',')[0]
        except:
            nombreb=conexion['vertexB'][0]


        conexion=(nombrea,nombreb,conexion['weight'])
        lt.addLast(camino_final,conexion)
    return (contador,suma,camino_final)


def error_en_vertice(analyzer,vertice):
    id_a=traduccion(vertice,analyzer)
    pareja=m.get(analyzer['landing_points'],id_a)
    valor=me.getValue(pareja)
    vecinos=valor['vecinos']
    mapa=m.newMap()
    for vecino in lt.iterator(vecinos):
        landing_point=vecino[0]
        pareja2=m.get(analyzer['landing_points'],landing_point)
        valor2=me.getValue(pareja2)
        pais=valor2['name'].split(',')[1].strip()
        if not m.contains(mapa,pais):
            m.put(mapa,pais,(pais,vecino[2]))
    lista=m.valueSet(mapa)
    numero_afectados=lt.size(lista)
    ordenados=ms.sort(lista,cmpkm)
    return(numero_afectados,ordenados)

        

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
def cmpkm(lp1, lp2):
    
    if (float(lp1[1]) > float(lp2[1])):
        return True
    else:
        return False
# Funciones de ordenamiento