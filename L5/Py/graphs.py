from py4j.java_gateway import *


def start():
    try:
        print('running jvm in the background...')
        subprocess.Popen(["java", "GraphEP"])
        print('successs')
    except:
        print('error')


def newGraph():
    gateway = JavaGateway()
    graph = gateway.entry_point
    # gateway.help(graph)
    # gateway.close()
    return graph


def closeGraph(graph):
    return None


def help():
    gateway = JavaGateway()
    gateway.help(gateway.entry_point)


def addNode(graph, data):
    graph.addNode(data)


def addEdge(graph, src, dest, weight):
    graph.addEdge(src, dest, weight)


def stop():
    gt = JavaGateway()
    gt.close()
    gt.shutdown()
    print('done')
