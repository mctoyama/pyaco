# -*- coding: utf-8 -*-
#
# Author: Marcelo Costa Toyama - mctoyama@gmail.com
#
# License GPL v 3.0
#
# Description:
# Ant Colony optimization for TSP PROBLEMS
#

# each ant starts the trail in a distinct city
#
# update pheromone only the best path

# TSPLIB
# http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/


import math
from graph.distance_matrix import *
from graph.tsplib import *

# -------------------------------------------------------------------------
# class greed
# -------------------------------------------------------------------------
class Greed:
    """Greed algorithm"""

    def __init__(self, p_distance_matrix):
        """Constructor:
            - p_distance_matrix: distance matrix for nodes in the graph"""
        self._matrix = p_distance_matrix
        self._agents = self._matrix.all_nodes()
        self._best_path = list()
        self._best_path_len = -1

    def run(self):
        """Run the greed algorithm"""

        v_all_paths = {}
        v_best_path = list()
        v_best_path_len = -1

        for v_agent in self._agents:

            v_path = list()
            v_path.append(v_agent)

            v_cities = self._matrix.all_nodes()
            v_cities.remove( v_agent )
            v_cities.sort()

            v_end = False

            while not v_end:

                v_from = v_path[-1]
                v_next_city = -1
                v_next_dist = -1
                v_dist_array = {}

                for i in v_cities:
                    v_dist_array[i] = self._matrix.get(v_from, i)

                for v_city, v_dist in v_dist_array.items():
                    if v_next_dist == -1:
                        v_next_dist = v_dist
                        v_next_city = v_city
                    elif v_next_dist > v_dist:
                        v_next_dist = v_dist
                        v_next_city = v_city

                v_path.append(v_next_city)
                v_cities.remove( v_next_city)

                if len(v_cities) == 0:
                    v_end = True

            v_all_paths[v_agent] = v_path

        for v_city, v_path in v_all_paths.items():
            if v_best_path_len == -1:
                v_best_path = v_path
                v_best_path_len = self._matrix.path_len( v_best_path )
            elif v_best_path_len > self._matrix.path_len( v_path ):
                v_best_path = v_path
                v_best_path_len = self._matrix.path_len( v_best_path )

        return( v_best_path )

if __name__ == "__main__":

    # TSP LIB problem
    tsp_matrix = TSPLIB_matrix("berlin52.tsp")

    g = Greed( tsp_matrix )

    ret = g.run()

    print("greed path: ", ret)
    print("greed length: ", tsp_matrix.path_len( ret ))

