# -*- coding: utf-8 -*-
#
# Author: Marcelo Costa Toyama - mctoyama@gmail.com
#
# License GPL v 3.0
#
# Description:
# distance matrix representing a graph

# -------------------------------------------------------------------------
# Distance Matrix
# -------------------------------------------------------------------------
class Distance_matrix:
    """Distance matrix - representing a graph"""
    def __init___(self):
        self._matrix = [[0]]

    def len(self):
        """Return matrix size"""

        v_row_size = len(self._matrix)

        for i in self._matrix:
            if v_row_size != len(i):
                raise Exception("TSP matrix must be a square matrix!")

        return( v_row_size )

    def distance(self, p_a, p_b):
        """calculate the distance between two cities"""
        return( self._matrix[p_a][p_b] )

    def path_len(self, p_path):
        """Return path length"""

        v_a = p_path[0]
        v_b = p_path[0]
        v_len = 0

        for v_index in range(len(p_path)):
            if p_path[v_index] >= self.len():
                raise Exception("Invalid matrix index!")

        for v_index in range(1, len(p_path)):
            v_a = v_b
            v_b = p_path[v_index]
            v_len = v_len + self._matrix[v_a][v_b]

        v_len = v_len + self._matrix[p_path[-1]][p_path[0]]

        return v_len

    def all_nodes(self):
        """Return a list of all matrix indexes"""

        v_ret = list()

        for i in range(self.len()):
            v_ret.append(i)

        return( v_ret )

    def get(self, p_a, p_b):
        """Returns the distance from city p_a and p_b"""
        return( self._matrix[p_a][p_b] )

    def biggest_edge(self):

        v_ret = -1
        
        for v_a in range(self.len()):
            for v_b in range(self.len()):
                if v_ret < self._matrix[v_a][v_b]:
                    v_ret = self._matrix[v_a][v_b]
        
        return( v_ret )

