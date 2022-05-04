
from MyGraph import MyGraph

g1 = MyGraph()
g2 = MyGraph()

g2.addNode('A')
g2.addNode('B')
g2.addNode('C')

g2.addEdge('A', 'C', 11)
g2.addEdge('B', 'C', 200)
g2.addEdge('B', 'A', 50)
g2.addEdge('C', 'A', 10)
g2.addEdge('C', 'B', 1)

g2.print()

g2.setNodeLabel('A', 'X')

g2.print()

g2.MST('C')
g2.SSSP('B')

g2.DFS('C')
g2.BFS('C')

g1.addNode('A')
g1.addNode('B')
g1.addNode('C')
g1.addNode('D')

g1.addEdge('A', 'B', 100)
g1.addEdge('A', 'C', 200)
g1.addEdge('B', 'C', 50)

g1.print()
g1.DFS('A')

g1.removeEdge('A', 'B')
g1.removeNode('C')

g1.print()

g1.addNode('C')
g1.addEdge('A', 'B', 10)
g1.addEdge('B', 'D', 100)
g1.addEdge('D', 'C', 1000)
g1.addEdge('C', 'A', 10000)

g1.addEdge('A', 'C', 5)
g1.addEdge('C', 'D', 50)
g1.addEdge('D', 'B', 500)
g1.addEdge('B', 'A', 5000)

g1.print()

g1.MST('A')
g1.SSSP('A')
