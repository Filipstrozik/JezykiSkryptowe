package Graphs;

public class Main {

    public static void main(String[] args) {
        GraphList graph2 = new GraphList(6);
        graph2.addEdge(0, 1, 4);
        graph2.addEdge(0, 2, 3);
        graph2.addEdge(1, 2, 1);
        graph2.addEdge(1, 3, 2);
        graph2.addEdge(2, 3, 4);
        graph2.addEdge(3, 4, 2);
        graph2.addEdge(4, 5, 6);
        graph2.printGraph();
        System.out.println();
        graph2.SSSP(5);
        System.out.println();
        graph2.MST();
    }
}
