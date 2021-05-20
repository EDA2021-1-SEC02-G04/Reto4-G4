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
                    'paths': None
                    }

        analyzer['landing_points'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=comparelanding_points)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
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
def addlanding_point(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], stopid):
            gr.insertVertex(analyzer['connections'], stopid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def loadlanding_points(analyzer,landing_point):
    mapa_vertices=analyzer["landing_points"]
    if not m.contains(mapa_vertices,landing_point["landing_point_id"]):
        m.put(mapa_vertices,landing_point["landing_point_id"],landing_point)

def loadconnections(analyzer,connection):
    grafo=analyzer["connections"]
    
    if not gr.containsVertex(grafo,(connection["\ufefforigin"],connection["cable_id"])):
        gr.insertVertex(grafo,(connection["\ufefforigin"],connection["cable_id"]))
    if not gr.containsVertex(grafo,(connection["destination"],connection["cable_id"])):
        gr.insertVertex(grafo,(connection["destination"],connection["cable_id"]))
    gr.addEdge(grafo,(connection["\ufefforigin"],connection["cable_id"]),(connection["destination"],connection["cable_id"]),connection["cable_length"])

# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
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