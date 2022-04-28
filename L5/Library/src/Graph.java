
public interface Graph {

    void addEdge(String src, String dest, int weight);

    String SSSP(String sourceNode);

    String MST();

    String printGraph();

}
