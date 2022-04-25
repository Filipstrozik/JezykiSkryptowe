package Graphs;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.PriorityQueue;

public class GraphList implements Graph{

    int vertices;
    ArrayList<LinkedList<Edge>> adjacencylist;
    ArrayList<Node> nodeList;


    static class ResultSet {
        int parent;
        int weight;
    }


    public GraphList(){
        this.vertices = 0;
        this.adjacencylist = new ArrayList<>();
        this.nodeList = new ArrayList<>();
    }

    public void addNode(Node node){
        this.nodeList.add(node);
        this.adjacencylist.add(new LinkedList<>());
        this.vertices+=1;
    }

    @Override
    public void addEdge(Node source, Node destination, int weight) {
        int idSource = nodeList.indexOf(source);
        Edge edge = new Edge(source, destination, weight);
        adjacencylist.get(idSource).addFirst(edge);
//        edge = new Edge(destination, source, weight);
//        adjacencylist[destination].addFirst(edge); //for undirected graph
    }


    public boolean hasEdge(Node source, Node destination) {
        int idSource = nodeList.indexOf(source);
        LinkedList<Edge> list = adjacencylist.get(idSource);
        for (Edge edge : list) {
            if (edge.dest == destination) { // TODO chyba equals
                return true;
            }
        }
        return false;
    }

    public Integer getEdgeValue(Node source, Node destination) {
        int idSource = nodeList.indexOf(source);
        LinkedList<Edge> list = adjacencylist.get(idSource);
        for (Edge edge : list) {
            if (edge.dest == destination) {
                return edge.weight;
            }
        }
        return null;
    }


    @Override
    public void printGraph() {
        for (int i = 0; i < vertices; i++) {
            LinkedList<Edge> list = adjacencylist.get(i);
            System.out.print(nodeList.get(i) + ": ");
            for (Edge edge : list) {
                System.out.print(" -> [" + edge.dest + "," + edge.weight + "]");
            }
            System.out.println();
        }
    }

    @Override //this Dijkstra algorithm uses additional class Pair< , > which is implemented in javafx.util but i made an additional class
    // in order to omit problems with importing Pair form javafx
    public void SSSP(Node sourceNode) {
        int sourceVertex = nodeList.indexOf(sourceNode);


        boolean[] spt = new boolean[vertices];
        int[] dist = new int[vertices];
        int INFINITY = Integer.MAX_VALUE;

        //set distances to infinity
        for (int i = 0; i < vertices; i++) {
            dist[i] = INFINITY;
        }

        // set up a prioryty queue, override comparator to sort it by the keys values.
        PriorityQueue<Pair<Integer, Integer>> pq = new PriorityQueue<Pair<Integer, Integer>>(vertices, (o1, o2) -> {
            int key1 = o1.getKey();
            int key2 = o2.getKey();
            return key1 - key2;
        });

        //set source vertex distance to 0
        dist[sourceVertex] = 0;
        Pair<Integer, Integer> p0 = new Pair<>(dist[sourceVertex], sourceVertex);
        // put it to queue
        pq.offer(p0);

        while (!pq.isEmpty()) {
            //extract the min
            Pair<Integer, Integer> extractedPair = pq.poll();

            int extractedVertex = extractedPair.getValue();
            if (!spt[extractedVertex]) {
                spt[extractedVertex] = true;

                LinkedList<Edge> listOfEdges = adjacencylist.get(extractedVertex);

                //iterate through all the adjacent vertices and update the keys
                for (Edge edge : listOfEdges) {
                    int destination = nodeList.indexOf(edge.dest);
                    //if edge destination is not present in mst -> check if distance needs an update (total weight) if current val < total weight -> update
                    if (!spt[destination]) {
                        int newKey = dist[extractedVertex] + edge.weight;
                        int currentKey = dist[destination];
                        if (currentKey > newKey) {
                            Pair<Integer, Integer> p = new Pair<>(newKey, destination);
                            pq.offer(p);
                            dist[destination] = newKey;
                        }
                    }
                }
            }
        }
        printDijkstra(dist, sourceVertex);
    }

    public void printDijkstra(int[] distance, int sourceVertex) {
        System.out.println("Dijkstra Algorithm: (Adjacency List + Priority Queue)");
        for (int i = 0; i < vertices; i++) {
            System.out.println("Source Vertex: " + nodeList.get(sourceVertex) + " to vertex " + nodeList.get(i) +
                    " distance: " + distance[i]);
        }
    }

    @Override
    public void MST() {
        boolean[] mst = new boolean[vertices];
        ResultSet[] resultSet = new ResultSet[vertices];
        int[] key = new int[vertices];

        //Initialize all the keys to infinity and
        //initialize resultSet for all the vertices
        for (int i = 0; i < vertices; i++) {
            key[i] = Integer.MAX_VALUE;
            resultSet[i] = new ResultSet();
        }

        PriorityQueue<Pair<Integer, Integer>> pq = new PriorityQueue<>(vertices, (o1, o2) -> {
            int key1 = o1.getKey();
            int key2 = o2.getKey();
            return key1 - key2;
        });

        //create the pair for for the first index, 0 key 0 index
        key[0] = 0;
        Pair<Integer, Integer> p0 = new Pair<>(key[0], 0);

        pq.offer(p0);

        resultSet[0] = new ResultSet();
        resultSet[0].parent = -1;


        while (!pq.isEmpty()) {
            //extract the min pair
            Pair<Integer, Integer> extractedPair = pq.poll();

            int extractedVertex = extractedPair.getValue();
            mst[extractedVertex] = true;

            LinkedList<Edge> list = adjacencylist.get(extractedVertex);
            //iterate through all the adjacent vertices and update the keys
            for (Edge edge : list) {

                //only if edge destination is not present in mst
                if (!mst[nodeList.indexOf(edge.dest)]) {
                    int destination = nodeList.indexOf(edge.dest);
                    int newKey = edge.weight;
                    //check it current weight < existing weight, if yes, update it
                    if (key[destination] > newKey) {
                        //add it to the priority queue
                        Pair<Integer, Integer> p = new Pair<>(newKey, destination);
                        pq.offer(p);
                        //update the resultSet for destination vertex
                        resultSet[destination].parent = extractedVertex;
                        resultSet[destination].weight = newKey;
                        //update the key
                        key[destination] = newKey;
                    }
                }
            }
        }
        printMST(resultSet);
    }

    private void printMST(ResultSet[] resultSet) {
        int total_min_weight = 0;
        System.out.println("Minimum Spanning Tree (Prim's Algorithm) : ");
        for (int i = 1; i < vertices; i++) {
            System.out.println("Edge: " + nodeList.get(i) + " - " + nodeList.get(resultSet[i].parent) +
                    " key: " + resultSet[i].weight);
            total_min_weight += resultSet[i].weight;
        }
        System.out.println("Total minimum key: " + total_min_weight);
    }
}
