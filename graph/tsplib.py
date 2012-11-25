# -*- coding: utf-8 -*-
#
# Author: Marcelo Costa Toyama - mctoyama@gmail.com
#
# License GPL v 3.0
#
# Description:
# TSPLIB problems
# 

# TSPLIB
# http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/

import re
import math
from graph.distance_matrix import *

# -------------------------------------------------------------------------
# TSP LIB distance matrix - 
#
# -------------------------------------------------------------------------
class TSPLIB_matrix(Distance_matrix):
    """Traveling Salesman problem matrix"""

    def __init__(self, p_filename):
        """Construct matrix from file"""

        self._matrix = list()

        self._NAME = ""
        self._COMMENT = ""
        self._TYPE = ""
        self._EDGE_WEIGHT_TYPE = ""
        self._DIMENSION = ""
        self._NODE_COORD_SECTION = False

        self._coord = {}

        # reading TSPLIB file
        v_fd = open(p_filename, "r")

        for v_line in v_fd:

            v_pr_line = v_line.split(":")

            # removendo espaços duplos
            v_match = re.search("  ", v_pr_line[0])
            while v_match:
                v_match = re.search("  ", v_pr_line[0])
                v_pr_line[0] = v_pr_line[0].replace("  ", " ")

            # removendo \s\n - > ""
            v_match = re.search(" \n", v_pr_line[0])
            while v_match:
                v_match = re.search(" \n", v_pr_line[0])
                v_pr_line[0] = v_pr_line[0].replace(" \n", "")

            # removendo \n
            v_match = re.search("\n", v_pr_line[0])
            while v_match:
                v_match = re.search("\n", v_pr_line[0])
                v_pr_line[0] = v_pr_line[0].replace("\n", "")
                
            if not self._NODE_COORD_SECTION:            

                if re.search("^NAME", v_pr_line[0]):
                    self._NAME = v_pr_line[1]
                elif re.search("^COMMENT", v_pr_line[0]):
                    self._COMMENT = v_pr_line[1]
                elif re.search("^TYPE", v_pr_line[0]):
                    if not re.search("TSP", v_pr_line[1]):
                        raise Exception("ERROR: NOT A TSP PROBLEM")
                    else:
                        self._TYPE = v_pr_line[1]
                elif re.search("EDGE_WEIGHT_TYPE", v_pr_line[0]) :
                    if not re.search("EUC_2D", v_pr_line[1]):
                        raise Exception("ERROR: NOT A EUC_2D TYPE")
                    else:
                        self._EDGE_WEIGHT_TYPE = v_pr_line[1]
                elif re.search("^DIMENSION", v_pr_line[0]):
                    self._DIMENSION = v_pr_line[1]
                elif re.search("^NODE_COORD_SECTION", v_pr_line[0]):
                    self._NODE_COORD_SECTION = True

            else:
                if re.search("^EOF", v_line):
                    break

                v_line_node = v_line
                
                # cleaning double \s\s -> \s
                v_match = re.search("  ", v_line_node)
                while v_match:
                    v_match = re.search("  ", v_line_node)
                    v_line_node = v_line_node.replace("  ", " ")

                # cleaning double \s\n -> \s
                v_match = re.search(" \n", v_line_node)
                while v_match:
                    v_match = re.search(" \n", v_line_node)
                    v_line_node = v_line_node.replace(" \n", "")

                # cleaning double \n -> \s
                v_match = re.search("\n", v_line_node)
                while v_match:
                    v_match = re.search("\n", v_line_node)
                    v_line_node = v_line_node.replace("\n", "")

                v_pr_line = v_line_node.split(" ")

                # registering node                
                v_node = int(v_pr_line[-3]) - 1
                v_x = float(v_pr_line[-2])
                v_y = float(v_pr_line[-1])

                self._coord[v_node] = (v_x,v_y)

        v_fd.close()

        # creating distance matrix
        for v_row in range( len( self._coord ) ):

            v_line_tsp = list()

            for v_column in range( len( self._coord ) ):
                v_line_tsp.append(0.0)

            self._matrix.append(v_line_tsp)

        for v_i, (v_xi, v_yi) in self._coord.items():
            for v_j, (v_xj, v_yj) in self._coord.items():
                dx = v_xi - v_xj
                dy = v_yi - v_yj
                dij = math.sqrt( dx*dx + dy*dy )
                dij = float( dij )
                self._matrix[v_i][v_j] = dij

                if v_i != v_j and dij == 0:
                    self._matrix[v_i][v_j] = 0.001

# -------------------------------------------------------------------------        
# TSPLIB tour
# -------------------------------------------------------------------------
class TSPLIB_tour:
    """Represents a TSPLIB tour"""

    def __init__(self, p_filename):
        """It reads a TSPLIB opt.tour"""

        self._path = list()

        v_fd = open(p_filename, "r")
        v_tour_section = False

        for v_line in v_fd:

            if re.search("^EOF", v_line):
                break
            
            if re.search("^TOUR_SECTION", v_line):
                v_tour_section = True
                continue

            if v_tour_section:
                v_value = int( v_line )
                if v_value > 0:
                    v_value -= 1
                    self._path.append( v_value )
            
        v_fd.close()

    def path(self):
        return( self._path )


