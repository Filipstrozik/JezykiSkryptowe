package Graphs;

public class Node {

    String data;

    Node(String data){
        this.data = data;
    }

    void changeData(String data){
        this.data = data;
    }

    @Override
    public String toString() {
        return "Node(" + data + ')';
    }
}
