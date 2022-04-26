
public interface Graph {

    void addEdge(String src, String dest, int weight);

    void SSSP(Node sourceNode);

    String MST();

    void printGraph();

}
