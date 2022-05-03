# import graphs
from MyGraph import MyGraph

g1 = MyGraph()
g2 = MyGraph()

g1.addNode('A')
g1.addNode('B')
g1.addNode('C')
g1.addNode('D')

g1.addEdge('A', 'B', 100)
g1.addEdge('A', 'C', 200)
g1.addEdge('B', 'C', 50)

g1.print()

# g1.removeEdge('A','B')
g1.removeNode('C')

g1.print()


g1.MST()
g1.SSSP('A')


g2.addNode('A')
g2.addNode('B')
g2.addNode('C')

g2.addEdge('A', 'C', 100)
g2.addEdge('B', 'C', 200)
g2.addEdge('B', 'A', 50)
g2.addEdge('C', 'A', 10)
g2.addEdge('C', 'B', 1)


g2.print()

g2.MST()
g2.SSSP('C')


