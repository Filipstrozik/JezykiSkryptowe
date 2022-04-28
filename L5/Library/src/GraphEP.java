import py4j.GatewayServer;
public class GraphEP {
    private GraphList graph;

    public GraphEP() {
        graph = new GraphList();
    }

    public GraphList getGraph() {
        return graph;
    }

    public GraphList getNewGraph() {
        return new GraphList();
    }

    public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(new GraphEP());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }
}
