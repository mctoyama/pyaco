# -*- coding: utf-8 -*-
#
# Author: Marcelo Costa Toyama - mctoyama@gmail.com
#
# License GPL v 3.0
#
# Description:
# Ant colony system

# each ant starts the trail in a distinct city
#
# all ants updates the pheromone
# An ant only searchs in the n - nearest neighbors
# this list of closest member is called - v_candidate_set

# The examples are from TSPLIB
# http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/

import random
import math
import re
from graph.distance_matrix import *
from graph.tsplib import *

# -------------------------------------------------------------------------
# Pheromone matrix
# -------------------------------------------------------------------------
class Pheromone_matrix:
    def __init__(self, p_tsp_matrix, p_Q, p_evap):
        """Creating pheromone matrix and initializing variables:
           - p_tsp_matrix - Traveling Salesman problem matrix
           - p_Q - amount of pheromony put on each iteraction for each ant
           - p_evap = evaporation factor
        """

        self._tsp_matrix = p_tsp_matrix

        self._len = p_tsp_matrix.len()

        self._pheromone_matrix = list()

        for i in range(self._len):

            v_row_tmp = list()

            for j in range(self._len):
                v_row_tmp.append(1.0)

            self._pheromone_matrix.append(v_row_tmp)

        self._Q = p_Q
        self._evap = p_evap

    def deposit_pheromone(self, p_path):
        """Deposits pheromone in the trail"""

        v_delta = self._Q / self._tsp_matrix.path_len( p_path )

        v_a = p_path[0]
        v_b = p_path[0]

        for v_index in range(len(p_path)):
            if p_path[v_index] >= self._len:
                raise Exception("Invalid matrix index!")

        for v_index in range(1, len(p_path)):
            v_a = v_b
            v_b = p_path[v_index]
            self._pheromone_matrix[v_a][v_b] = self._pheromone_matrix[v_a][v_b] + v_delta

        # closing the tsp cicle
        self._pheromone_matrix[p_path[-1]][p_path[0]] = self._pheromone_matrix[p_path[-1]][p_path[0]] + v_delta

    def evaporate(self):
        """Evaporat the pheromone"""
        for i in range(self._len):
            for j in range(self._len):
                self._pheromone_matrix[i][j] = (1.0 - self._evap) * self._pheromone_matrix[i][j]

    def get(self,p_a, p_b):
        """returns the pheromene from trail p_a to p_b"""
        return( self._pheromone_matrix[p_a][p_b] )

    def __repr__(self):
        v_str = ""
        for i in range(len(self._pheromone_matrix)):
            v_str = v_str + repr(self._pheromone_matrix[i]) + "\n"
        return( v_str )

# -------------------------------------------------------------------------
# ant colony
# -------------------------------------------------------------------------
class Colony:
    """Ant Colony class"""
    def __init__(self, p_distance_matrix, p_alfa, p_beta, p_deposit_ph, p_evap_ph, p_neighbor_size):
        """Constructor for ant colony"""
        self._matrix = p_distance_matrix
        self._ph_matrix = Pheromone_matrix( self._matrix, p_deposit_ph, p_evap_ph)
        self._ants = self._matrix.all_nodes()
        self._best_global_path = list()
        self._alfa = p_alfa
        self._beta = p_beta
        self._best_path = list()
        self._best_path_len = float("Inf")
        self._count_stable = 0
        self._neighbor_size = p_neighbor_size

        random.seed(None)

    def path_len(self, p_path):
        return self._matrix.path_len( p_path )

    def iter(self):
        """Ant colony optimization iteration"""

        # There is the same number of cities and ants.
        # Each ant start its trail in a different city

        # all paths - each ant builds a path
        v_all_paths = {}

        # For each ant
        for v_ant in self._ants:

            #starting city
            v_path = list()
            v_path.append(v_ant)

            # all others cities
            v_cities = self._matrix.all_nodes()
            v_cities.remove( v_ant )

            v_end = False

            # creating a path in the graph
            while not v_end:

                v_from = v_path[-1]

                #candidate set with n nearest cities
                v_candidate_set = list()

                for v_c in v_cities:
                    v_candidate_set.append( (v_c, self._matrix.get(v_from, v_c)) )

                v_candidate_set.sort( key = lambda pair: pair[1] )

                if len(v_candidate_set) > self._neighbor_size:
                    v_candidate_set = v_candidate_set[:self._neighbor_size]

                v_candidate_set = list( map( lambda pair: pair[0], v_candidate_set) )

                # each city probability
                v_prob = {}

                for i in v_candidate_set:
                    v_prob[i] = 0.0

                v_sum = 0.0

                for v_next_city in v_candidate_set:
                    v_ph = self._ph_matrix.get(v_from, v_next_city)
                    v_dist = 1.0 / self._matrix.get(v_from, v_next_city)
                    v_sum = v_sum + (v_ph ** self._alfa)*(v_dist ** self._beta)

                for v_next_city in v_candidate_set:
                    v_ph = self._ph_matrix.get(v_from, v_next_city)
                    v_dist = 1.0 / self._matrix.get(v_from, v_next_city)
                    v_value = (v_ph ** self._alfa)*(v_dist ** self._beta) / v_sum
                    v_prob[v_next_city] = v_value

                v_circle = 0.0
                v_rand = random.random()

                for v_next_city, v_city_prob in v_prob.items():

                    v_circle = v_circle + v_city_prob

                    if v_rand <= v_circle:
                        v_path.append(v_next_city)
                        v_cities.remove( v_next_city )
                        break

                if len(v_cities) == 0:
                    v_end = True

            # adding path for this particulary ant
            v_all_paths[v_ant] = v_path

        #evaporating pheromone
        self._ph_matrix.evaporate()

        #stagnation flag
        v_flag = False

        #searching for best path
        for v_ant, v_path in v_all_paths.items():

            if self._best_path_len >= self._matrix.path_len( v_path ):
                self._best_path = v_path
                self._best_path_len = self._matrix.path_len( v_path )
                v_flag = True

        # if stagnation self._count_stable += 1
        if v_flag:
            self._count_stable = 0
        else:
            self._count_stable += 1

        #updating pheromone
        for v_ant, v_path in v_all_paths.items():
            self._ph_matrix.deposit_pheromone(v_path)

    def run(self, p_max_iter, p_stable):
        """ Runs the algoritm
            - p_max_iter: maximum number of iterations
            - p_stable: terminates the algorithm after x iterations without improvement"""

        for i in range(p_max_iter):

            self.iter()

            print( "iteration: ", i)
            print( "len: ", self._matrix.path_len( self._best_path ) )

            if self._count_stable == p_stable:
                break

        return( self._best_path )

    def run_from(self, p_path, p_max_iter, p_stable):
        """ Runs the algoritm
            - p_path: starting path
            - p_max_iter: maximum number of iterations
            - p_stable: terminates the algorithm after p_stable iterations without improvement"""

        self._best_path = p_path
        self._best_path_len = self._matrix.path_len( self._best_path )

        for i in range(p_max_iter):

            self.iter()

            print( "iteration: ", i)
            print( "len: ", self._matrix.path_len( self._best_path ) )

            if self._count_stable == p_stable:
                break

        return( self._best_path )

# module debug
if __name__ == "__main__":

    # TSP LIB problem
    tsp_matrix = TSPLIB_matrix("a280.tsp")

    #optimal path
    opt_path = TSPLIB_tour("a280.opt.tour")
    p = opt_path.path()
    print("opt path: ", p)
    print("opt length: ", tsp_matrix.path_len(p))
    print("------------------------------------------------------------------------")

    raw_input("Press <ENTER> to start")

    # heuristic amount of pheromone deposited in the trail
    v_q = tsp_matrix.len() * tsp_matrix.biggest_edge()

    # creating the problem
    #def __init__(self, p_distance_matrix, p_alfa, p_beta, p_deposit_ph, p_evap_ph, p_neighbor_size):
    col = Colony(tsp_matrix, 1,1,v_q,0.6,20)

    # running the algorithm
    ret = col.run(100,100)

    # collecting results
    print("path: ", ret)
    print("length: ", tsp_matrix.path_len(ret))
    print("------------------------------------------------------------------------")



