package Graphs;

public interface Graph {

    void addEdge(int src, int dest, int weight);

    void SSSP(int sourceVertex);

    void MST();

    void printGraph();

}
