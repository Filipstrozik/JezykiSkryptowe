
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.PriorityQueue;


public class GraphList implements Graph {

    int vertices;
    ArrayList<LinkedList<Edge>> adjacencylist;
    ArrayList<Node> nodeList;


    static class ResultSet {
        int parent;
        int weight;
    }

    public GraphList() {
        this.vertices = 0;
        this.adjacencylist = new ArrayList<>();
        this.nodeList = new ArrayList<>();
    }

    public Node getNode(String data) {
        return new Node(data);
    }

    public void addNode(String data) {
        if (getIndexOfNode(data) == -1) {
            this.nodeList.add(new Node(data));
            this.adjacencylist.add(new LinkedList<>());
            this.vertices += 1;
        }
    }

    //TODO: eraseNode(String data) -> musisz usunac tez wszytskie krawedzie ktore maja go za dest
    //TODO: oprcz tego że usuwasz Linked Liste
    //TODO: zatem też usuwanie krawędzi eraseEdge(String src, String dest)
    public void removeEdge(String src, String dest) {
        if (hasEdge(src, dest)) {
            int idSource = getIndexOfNode(src);
            int idEdge = 0;
            LinkedList<Edge> list = adjacencylist.get(idSource);
            for (Edge edge : list) {
                if (edge.dest.data.equals(dest)) {
                    idEdge = list.indexOf(edge);
                    break;
                }
            }
            list.remove(idEdge);
        }
    }


    public void removeNode(String data) {
        int idToRemove = getIndexOfNode(data);
        if (idToRemove != -1){
            for (LinkedList<Edge> lista : adjacencylist) {
                for (Edge edge : lista) {
                    if(edge.dest.data.equals(data)){
                        removeEdge(edge.src.data, edge.dest.data);
                        break;
                    }
                }
            }
            adjacencylist.remove(idToRemove);
            nodeList.remove(idToRemove);
            vertices--;
        }

    }

    private Integer getIndexOfNode(String nodeData) {
        int id = 0;
        for (Node node : nodeList) {
            if (node.data.equals(nodeData)) {
                return id;
            }
            id += 1;
        }
        return -1;
    }

    @Override
    public void addEdge(String source, String destination, int weight) {
        Edge edge = new Edge(nodeList.get(getIndexOfNode(source)), nodeList.get(getIndexOfNode(destination)), weight);
        adjacencylist.get(getIndexOfNode(source)).addFirst(edge);
//        edge = new Edge(destination, source, weight);
//        adjacencylist[destination].addFirst(edge); //for undirected graph
    }


    public boolean hasEdge(String source, String destination) {
        int idSource = getIndexOfNode(source);
        LinkedList<Edge> list = adjacencylist.get(idSource);
        for (Edge edge : list) {
            if (edge.dest.data.equals(destination)) {
                return true;
            }
        }
        return false;
    }

    public Integer getEdgeWeight(String source, String destination) {
        int idSource = getIndexOfNode(source);
        LinkedList<Edge> list = adjacencylist.get(idSource);
        for (Edge edge : list) {
            if (edge.dest.data.equals(destination)) {
                return edge.weight;
            }
        }
        return null;
    }

    public void setEdgeWeight(String source, String destination, int nWeight) {
        if (getIndexOfNode(source) != -1) {
            LinkedList<Edge> list = adjacencylist.get(getIndexOfNode(source));
            for (Edge edge : list) {
                if (edge.dest.data.equals(destination)) {
                    edge.changeWeight(nWeight);
                }
            }
        }
    }


    @Override
    public String printGraph() {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < vertices; i++) {
            LinkedList<Edge> list = adjacencylist.get(i);
            result.append(nodeList.get(i)).append(": ");
            for (Edge edge : list) {
                result.append(" -> [").append(edge.dest).append(",").append(edge.weight).append("]");
            }
            result.append("\n");
        }
        return result.toString();
    }

    @Override
    //this Dijkstra algorithm uses additional class Pair< , > which is implemented in javafx.util but i made an additional class
    // in order to omit problems with importing Pair form javafx
    public String SSSP(String sourceNode) {
        int sourceVertex = getIndexOfNode(sourceNode);


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
        return printDijkstra(dist, sourceVertex);
    }

    public String printDijkstra(int[] distance, int sourceVertex) {
        StringBuilder result = new StringBuilder();
        result.append("Dijkstra Algorithm: (Adjacency List + Priority Queue) :\n");
        for (int i = 0; i < vertices; i++) {
            result.append("Source Vertex: ").append(nodeList.get(sourceVertex)).append(" to vertex ").append(nodeList.get(i)).append(" distance: ").append(distance[i]).append("\n");
        }
        return result.toString();
    }

    @Override
    public String MST() {
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
        return printMST(resultSet);
    }

    private String printMST(ResultSet[] resultSet) {
        int total_min_weight = 0;
        StringBuilder result = new StringBuilder();
        result.append("Minimum Spanning Tree (Prim's Algorithm) : \n");
        for (int i = 1; i < vertices; i++) {
            result.append("Edge: ").append(nodeList.get(i)).append(" - ").append(nodeList.get(resultSet[i].parent)).append(" key: ").append(resultSet[i].weight).append("\n");
            total_min_weight += resultSet[i].weight;
        }
        result.append("Total minimum key: ").append(total_min_weight).append("\n");
        return result.toString();
    }

    @Override
    public String toString() {
        return "GraphList{" +
                "\nvertices=" + vertices +
                ",\nadjacencylist=" + adjacencylist +
                ",\nnodeList=" + nodeList +
                '}';
    }
}
