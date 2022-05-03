from py4j.java_gateway import *


class MyGraph:

    def __init__(self):
        try:
            self.graph = JavaGateway().entry_point.getNewGraph()
        except:
            subprocess.Popen(["java", "GraphEP"])
            self.graph = JavaGateway().entry_point.getNewGraph()

    def addNode(self, data):
        self.graph.addNode(data)

    def removeNode(self, data):
        self.graph.removeNode(data)

    def addEdge(self, src, dest, weight):
        self.graph.addEdge(src, dest, weight)

    def removeEdge(self, src, dest):
        self.graph.removeEdge(src, dest)

    def getEdgeWeight(self, src, dest):
        return self.graph.getEdgeWeight(src, dest)

    def setEdgeWeight(self, src, dest, weight):
        self.graph.setEdgeWeight(src, dest, weight)

    def getHelp(self):
        JavaGateway().help(JavaGateway().entry_point)

    def SSSP(self, src):
        print(self.graph.SSSP(src))

    def MST(self):
        print(self.graph.MST())

    def print(self):
        print(self.graph.printGraph())

    def __del__(self):
        JavaGateway().close()
        JavaGateway().shutdown()
        pass
