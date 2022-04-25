package Graphs;

public interface Graph {

    void addEdge(Node src, Node dest, int weight);

    void SSSP(Node sourceNode);

    void MST();

    void printGraph();

}
