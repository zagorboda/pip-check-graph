import subprocess


class AdjNode:
    def __init__(self, value):
        self.vertex = value
        self.next = None


class Graph:
    def __init__(self, num):
        self.V = num
        # dict_init = [None] * self.V
        # self.graph = dict.fromkeys(dict_init)
        self.graph = [None] * self.V

    # Add edges
    def add_edge(self, s, d):
        node = AdjNode(d)
        node.next = self.graph[s]
        self.graph[s] = node

        node = AdjNode(s)
        node.next = self.graph[d]
        self.graph[d] = node

    # Print the graph
    def print_agraph(self):
        for i in range(self.V):
            print("Vertex " + str(i) + ":", end="")
            temp = self.graph[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")


process = subprocess.run(['pip3', 'list'],
                         # capture_output=True,
                         check=True,
                         timeout=60,
                         stdout=subprocess.PIPE).stdout

dependencies = {}
# i = 0
for line in filter(lambda x: x, process.decode("utf-8").split('\n')[2:]):
    # i += 1
    # if i == 10:
    #     break
    package = line.split()[0]
    package_process = subprocess.run(['pip3', 'show', line.split()[0]],
                             # capture_output=True,
                             check=True,
                             timeout=60,
                             stdout=subprocess.PIPE).stdout
    print(package_process)
    dep_list = package_process.split(b'\n')[-3:-1]
    requires = list(filter(lambda x: x, dep_list[0].split(b': ')[1].split(b', ')))
    required_by = list(filter(lambda x: x, dep_list[1].split(b': ')[1].split(b', ')))
    dependencies[package] = {'required_by': '', 'requires': ''}

    dependencies[package]['required_by'] = [x.decode('utf-8') for x in required_by]
    dependencies[package]['requires'] = [x.decode('utf-8') for x in requires]

dependencies = {k: v for k, v in sorted(dependencies.items(), key=lambda item: len(item[1]))}

print(type(dependencies.items()))

V = len(dependencies)

graph = Graph(V)

edges_list = []

import networkx as nx
G = nx.DiGraph()

for key, value in dependencies.items():
    _required_by, _requires = value['required_by'], value['requires']
    # for vertex in _required_by:
    #     graph.add_edge(key, vertex)
    G.add_node(key)
    for item in _required_by:
        edges_list.append((key, item))
        G.add_edge(item, key)
    print('    {}'.format(' ,'.join(_required_by)))
    print('  /')
    print(key)
    print('  \\')
    print('    {}'.format(' ,'.join(_requires)))
    print('\n')

# graph = Graph(5)
#
# graph.add_edge(0, 1)
# graph.add_edge(0, 2)
# graph.add_edge(0, 3)
# graph.add_edge(1, 2)
#
# graph.print_agraph()
#
# from collections import defaultdict
#
# class Graph:
#
#     # Constructor
#     def __init__(self):
#
#         # default dictionary to store graph
#         self.graph = defaultdict(list)
#
#     # function to add an edge to graph
#     def addEdge(self, u, v):
#         self.graph[u].append(v)
#
#     # A function used by DFS
#     def DFSUtil(self, v, visited):
#
#         # Mark the current node as visited and print it
#         visited.add(v)
#         print(v)
#
#         # Recur for all the vertices adjacent to
#         # this vertex
#         for neighbour in self.graph[v]:
#             if neighbour not in visited:
#                 self.DFSUtil(neighbour, visited)
#
#     # The function to do DFS traversal. It uses
#     # recursive DFSUtil()
#
#     def DFS(self):
#
#         # Create a set to store all visited vertices
#         visited = set()
#
#         # Call the recursive helper function to print
#         # DFS traversal starting from all vertices one
#         # by one
#         for vertex in list(self.graph):
#             if vertex not in visited:
#                 self.DFSUtil(vertex, visited)
#
#
# # Driver code
# # Create a graph given in the above diagram
# g = Graph()
# g.addEdge(0, 1)
# g.addEdge(0, 2)
# g.addEdge(1, 2)
# g.addEdge(2, 0)
# g.addEdge(2, 3)
# g.addEdge(3, 3)
#
# g.DFS()

test_1 = [("root", "a"), ("a", "b"), ("a", "e"), ("b", "c"), ("b", "d"), ("d", "e")]
print(edges_list)
print(test_1)

# import networkx as nx
#
# graph = nx.DiGraph()
# graph.add_edges_from(edges_list)
# # print(graph.in_edges('alembic'))
# print(graph.in_edges('idna')) # => [('a', 'e'), ('d', 'e')]




import matplotlib.pyplot as plt


# G.add_node("alembic")
# G.add_node("anyio")
# G.add_node("appdirs")
# G.add_node("Flask-Migrate")
# G.add_node("jupyter-server")
# G.add_node("virtualenv")
# # G.add_node("G")
# G.add_edge("Flask-Migrate","alembic")
# G.add_edge("jupyter-server","jupyter-server")
# G.add_edge("jupyter-server","appdirs")
# G.add_edge("C","F")
# G.add_edge("D","E")
# G.add_edge("F","G")

print(G.nodes())
print(G.edges())

pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edge_color='r', arrows = True)

# pos = nx.circular_layout(G)
# edges = G.edges()
#
# nx.draw(G, pos)

# ax = plt.gca()
# ax.set_axis_off()
plt.show()