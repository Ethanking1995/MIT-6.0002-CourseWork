# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
# Answer:The nodes represent the buildings on the MIT campus and the edges represent the paths between them.
#Distances are represented in the third and fourth columns on each line of the MIT_map.txt file., the weight of each edge
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map

    """
    print("Loading map from file...")
    file=open(map_filename)
    y=[]
    for line in file:
        y.append(line.split(' '))
    file.close()
    #initialize a list to store a list of relevant data for each weighted edge. First two elements 
    #of the inner lists are nodes and the remaining two are ints
    edges=[]
    for weightedge in y:
        j=[]
        for x in weightedge:
            if weightedge.index(x)==1 or weightedge.index(x)==0:
                y=Node(x)
                j.append(y)
            else:
                j.append(int(x))
        edges.append(j)
    #initliaze a Digraph representing the campus map
    Map=Digraph()
    #Add each edge in edges to the map, checking to see if both nodes are in the map first. If they are,
    #then we add the edge. Else, we add the relevant nodes and then add the edge
    for edge in edges:
        if Map.has_node(edge[0]) and Map.has_node(edge[1]):
            e=WeightedEdge(edge[0],edge[1],edge[2],edge[3])
            Map.add_edge(e)
        elif not Map.has_node(edge[0]) or not Map.has_node(edge[1]):
            if Map.has_node(edge[0]):
                Map.add_node(edge[1])
                e=WeightedEdge(edge[0],edge[1],edge[2],edge[3])
                Map.add_edge(e)
            elif Map.has_node(edge[1]):
                Map.add_node(edge[0])
                e=WeightedEdge(edge[0],edge[1],edge[2],edge[3])
                Map.add_edge(e)
            else:
                Map.add_node(edge[0])
                Map.add_node(edge[1])
                e=WeightedEdge(edge[0],edge[1],edge[2],edge[3])
                Map.add_edge(e)

        

    return Map
    
    # TODO
    

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

#print('testing load map.. expecting: \n a->b (10,9) \n a->c (12,2) \n b->c (1,1)')
#print('got:')
print(load_map('mit_map.txt'))

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?

#
# Answer: We want to find the shortest path from node A to node B, defining shortest to be the path with the 
#least distance amongst all possible paths from A to B. The constraint is that we can't exceed the maximum outdoor distance.

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # TODO
    path=path+[start]
    if start not in digraph.nodes:
        raise ValueError('Node not in graph')
    if start==end:
        return path
    else:
        #iterate through each edge of the startng node
        for node in digraph.get_edges_for_node(start):
            #prevent infinite cycle
            if node.dest not in path:
                newPath=get_best_path(digraph,node,end,path,max_dist_outdoors,best_dist,best_path)
                if newPath != None:
                    #initialize distance varaibles
                    total_dist=0
                    outdoor_dist=0
                    for i in range(len(newPath-1)):
                        for edge in digraph.edges[newPath[i]]:
                            if edge.dest==path[i+1]:
                                total_dist+=edge.get_total_distance()
                                outdoor_dist+=edge.get_outdoor_distance()
                    #if outdoor and total distance fit the constraints and the total distance
                    #is less than the current best distance, swap values for best path and best distance
                    if outdoor_dist<=max_dist_outdoors and total_dist<=best_dist:
                        best_dist=total_dist
                        best_path=newPath
    
    return best_path


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    start=Node(start)
    end=Node(end)
    best_path=get_best_path(digraph,start,end,[],max_total_dist,max_dist_outdoors,None)
    if best_path==None:
        raise ValueError('NO best path exists')
    return [node.get_name() for node in best_path]
    

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
