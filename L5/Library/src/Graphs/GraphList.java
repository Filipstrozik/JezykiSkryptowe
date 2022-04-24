package Graphs;

import java.util.Comparator;
import java.util.LinkedList; //TODO przerobic na arraylisty
import java.util.PriorityQueue;

public class GraphList implements Graph{

    int vertices;
    LinkedList<Edge>[] adjacencylist;


//    class Edge {
//        int src, dest, weight;
//
//        Edge(int src, int dest, int weight) {
//            this.src = src;
//            this.dest = dest;
//            this.weight = weight;
//        }
//    }

    static class ResultSet {
        int parent;
        int weight;
    }

    //Constructor
    public GraphList(int vertices) { //only undirected and weighted graphs
        this.vertices = vertices;
        adjacencylist = new LinkedList[vertices];
        //initialize adjacency lists for all the vertices
        for (int i = 0; i < vertices; i++) {
            adjacencylist[i] = new LinkedList<Edge>();
        }
    }

    @Override
    public void addEdge(int source, int destination, int weight) {
        Edge edge = new Edge(source, destination, weight);
        adjacencylist[source].addFirst(edge);
//        edge = new Edge(destination, source, weight);
//        adjacencylist[destination].addFirst(edge); //for undirected graph
    }


    public void addEdge(Edge ed) {
        adjacencylist[ed.src].addFirst(ed);
//        edge = new Edge(destination, source, weight);
//        adjacencylist[destination].addFirst(edge); //for undirected graph
    }

    public boolean hasEdge(int source, int destination) {
        LinkedList<Edge> list = adjacencylist[source];
        for(int i = 0; i<list.size();i++){
            if(list.get(i).dest== destination){
                return true;
            }
        }
        return false;
    }

    public Integer getEdgeValue(int source, int destination) {
        LinkedList<Edge> list = adjacencylist[source];
        for(int i = 0; i<list.size();i++){
            if(list.get(i).dest== destination){
                return list.get(i).weight;
            }
        }
        return null;
    }


    @Override
    public void printGraph() {
        for (int i = 0; i < vertices; i++) {
            LinkedList<Edge> list = adjacencylist[i];
            System.out.print(i + ": ");
            for (int j = 0; j < list.size(); j++) {
                System.out.print(" -> [" + list.get(j).dest + "," + list.get(j).weight + "]");
            }
            System.out.println();
        }
    }

    @Override //this Dijkstra algorithm uses additional class Pair< , > which is implemented in javafx.util but i made an additional class
    // in order to omit problems with importing Pair form javafx
    public void SSSP(int sourceVertex) {
        boolean[] spt = new boolean[vertices];
        int dist[] = new int[vertices];
        int INFINITY = Integer.MAX_VALUE;

        //set distances to infinity
        for (int i = 0; i < vertices; i++) {
            dist[i] = INFINITY;
        }

        // set up a prioryty queue, override comparator to sort it by the keys values.
        PriorityQueue<Pair<Integer, Integer>> pq = new PriorityQueue<Pair<Integer, Integer>>(vertices, new Comparator<Pair<Integer, Integer>>() {
            @Override
            public int compare(Pair<Integer, Integer> o1, Pair<Integer, Integer> o2) {
                int key1 = o1.getKey();
                int key2 = o2.getKey();
                return key1 - key2;
            }
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

                LinkedList<Edge> listOfEdges = adjacencylist[extractedVertex];

                //iterate through all the adjacent vertices and update the keys
                for (int i = 0; i < listOfEdges.size(); i++) {
                    Edge edge = listOfEdges.get(i);
                    int destination = edge.dest;
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
            System.out.println("Source Vertex: " + sourceVertex + " to vertex " + +i +
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

        PriorityQueue<Pair<Integer, Integer>> pq = new PriorityQueue<>(vertices, new Comparator<>() {
            @Override
            public int compare(Pair<Integer, Integer> o1, Pair<Integer, Integer> o2) {
                int key1 = o1.getKey();
                int key2 = o2.getKey();
                return key1 - key2;
            }
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

            LinkedList<Edge> list = adjacencylist[extractedVertex];
            //iterate through all the adjacent vertices and update the keys
            for (int i = 0; i < list.size(); i++) {

                Edge edge = list.get(i);
                //only if edge destination is not present in mst
                if (!mst[edge.dest]) {
                    int destination = edge.dest;
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
            System.out.println("Edge: " + i + " - " + resultSet[i].parent +
                    " key: " + resultSet[i].weight);
            total_min_weight += resultSet[i].weight;
        }
        System.out.println("Total minimum key: " + total_min_weight);
    }
}
