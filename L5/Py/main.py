from py4j.java_gateway import JavaGateway

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gateway = JavaGateway()
    graph = gateway.entry_point
    gateway.help(graph)

    a = graph.getNode('A')

    b = graph.getNode('B')
    c = graph.getNode('C')

    graph.addNode(a)
    graph.addNode(b)
    graph.addNode(c)
    graph.addEdge(a, b, 2)
    graph.addEdge(a, c, 100)
    graph.addEdge(b, c, 5)
    graph.printGraph()

    graph.SSSP(a)

    print(graph.MST())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
