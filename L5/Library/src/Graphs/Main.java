package Graphs;

public class Main {

    public static void main(String[] args) {
        GraphList g = new GraphList();
        Node a = new Node("A");
        Node b = new Node("B");
        Node c = new Node("C");
        g.addNode(a);
        g.addNode(b);
        g.addNode(c);
        g.addEdge(a,b,2);
        g.addEdge(a,c,100);
        g.addEdge(b,c,5);
        g.printGraph();

        System.out.println();
        g.SSSP(a);
        System.out.println();
        g.MST();
    }
}
