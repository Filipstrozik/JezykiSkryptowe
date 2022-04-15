import java.util.ArrayList;
import java.util.Comparator;
import java.util.Scanner;

public class aggregate {
    static public String aggregate_function = "";
    static public ArrayList<String> lines;

    public static void main(String[] args) {
        if(args.length == 0)
            System.exit(1);
        aggregate_function = args[0];
        lines = readInput();
        switch (aggregate_function) {
            case "/min" -> System.out.println(a_min());
            case "/max" -> System.out.println(a_max());
            case "/sum" -> System.out.println(a_sum());
            case "/avg" -> System.out.println(a_avg());
            case "/count" -> System.out.println(a_count());
            case "/median" -> System.out.println(a_median());
            case "/var" -> System.out.println(a_var());
        }
    }

    public static ArrayList<String> readInput() {
        Scanner sc = new Scanner(System.in);
        ArrayList<String> lines = new ArrayList<>();

        while (sc.hasNextLine()) {
            lines.add(sc.nextLine());
        }
        return lines;
    }

    public static double a_var() {
        double avg = a_avg();
        double sum = 0.0;
        int cnt = 0;
        for (String line : lines) {
            sum += Math.pow((Double.parseDouble(line) - avg), 2);
            cnt++;
        }
        return sum / cnt;
    }

    public static double a_median() {
        lines.sort(Comparator.comparing(String::valueOf));
        if (lines.size() % 2 == 0) {
            int i = lines.size() / 2;
            double a = Double.parseDouble(lines.get(i));
            double b = Double.parseDouble(lines.get(i + 1));
            return ((a + b) / 2.0);
        } else {
            return Double.parseDouble(lines.get(lines.size() / 2));
        }
    }

    public static double a_count() {
        return lines.size();
    }

    public static double a_avg() {
        double sum = 0.0;
        int cnt = 0;
        for (String line : lines) {
            try {
                sum += Double.parseDouble(line);
            } catch (Exception e) {
                e.printStackTrace();
            }
            cnt++;
        }
        return sum / cnt;
    }

    public static double a_sum() {
        double sum = 0.0;
        for (String line : lines) {
            sum += Double.parseDouble(line);
        }
        return sum;
    }

    public static double a_max() {
        double max = Double.parseDouble(lines.get(0));
        for (String line : lines) {
            max = Math.max(max, Double.parseDouble(line));
        }
        return max;
    }

    public static double a_min() {
        double min = Double.parseDouble(lines.get(0));
        for (String line : lines) {
            min = Math.min(min, Double.parseDouble(line));
        }
        return min;
    }

}
