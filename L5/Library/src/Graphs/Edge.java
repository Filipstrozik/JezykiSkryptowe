package Graphs;

public class Edge {
    Node src, dest;
    int weight;

    public Edge(Node src, Node dest, int weight) {
        this.src = src;
        this.dest = dest;
        this.weight = weight;
    }

    void changeWeight(int weight){
        this.weight = weight;
    }
}
