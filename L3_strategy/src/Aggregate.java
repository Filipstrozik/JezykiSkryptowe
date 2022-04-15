import java.util.ArrayList;
import java.util.Scanner;

public class Aggregate {
    public static AggregateStrategy strategy;

    public static void main(String[] args) {
        if(args.length == 0)
            System.exit(1);
        String aggregate_function = args[0];
        switch (aggregate_function) {
            case "/min" -> strategy = new Min();
            case "/max" -> strategy = new Max();
            case "/sum" -> strategy = new Sum();
            case "/avg" -> strategy = new Avg();
            case "/count" -> strategy = new Count();
            case "/median" -> strategy = new Median();
            case "/var" -> strategy = new Variance();
        }
        System.out.println(strategy.compute(readInput()));
    }

    public static ArrayList<String> readInput() {
        Scanner sc = new Scanner(System.in);
        ArrayList<String> lines = new ArrayList<>();

        while (sc.hasNextLine()) {
            lines.add(sc.nextLine());
        }
        return lines;
    }
}
