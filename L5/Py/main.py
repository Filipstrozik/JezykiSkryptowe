import os
import subprocess
import asyncio

from py4j.java_gateway import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('przed odpaleniu jvm')
    # subprocess.run('java GraphList')
    print('po odpaleniu jvm')

    port = launch_gateway()
    gateway = JavaGateway()

    # gateway = JavaGateway(
    #     gateway_parameters=GatewayParameters(port=port),
    #     callback_server_parameters=CallbackServerParameters(port=0))

    graph = gateway.entry_point
    gateway.help(graph)
    #
    # a = graph.getNode('A')
    #
    # b = graph.getNode('B')
    # c = graph.getNode('C')
    #
    # graph.addNode(a)
    # graph.addNode(b)
    # graph.addNode(c)
    # graph.addEdge(a, b, 2)
    # graph.addEdge(a, c, 100)
    # graph.addEdge(b, c, 5)
    # graph.printGraph()
    #
    # graph.SSSP(a)
    #
    # print(graph.MST())
    #
    # print('koniec')
    gateway.close()
    gateway.shutdown()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
