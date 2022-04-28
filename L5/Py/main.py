import os
import string
import subprocess
import asyncio
import time
from threading import Thread

from py4j.java_gateway import *


def runGraphList():
    try:
        print('running jvm in the background...')
        subprocess.Popen(["java", "GraphList"])
        print('udalo sie')
    except:
        print('nie udalo sie')


def test():
    port = launch_gateway()
    gateway = JavaGateway()

    graph = gateway.entry_point
    gateway.help(graph)

    test1(graph)

    print('koniec')
    gateway.close()
    gateway.shutdown()


def test1(graph):
    a: string = 'A'
    b: string = 'B'
    graph.addNode(a)
    graph.addNode(b)
    graph.addNode('C')
    graph.addEdge(a, b, 2)
    # graph.addEdge('A', 'C', 100)
    # graph.addEdge('B', 'C', 5)
    graph.printGraph()


def newNode(graph, name):
    node = graph.getNode(name)
    graph.addNode(node)
    return graph


if __name__ == '__main__':
    Thread(target=runGraphList()).start()
    Thread(target=test()).start()
