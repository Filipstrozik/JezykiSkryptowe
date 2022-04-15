import java.util.ArrayList;

public class Max implements AggregateStrategy{


    @Override
    public double compute(ArrayList<String> lines) {
        double max = Double.parseDouble(lines.get(0));
        for (String line : lines) {
            max = Math.max(max, Double.parseDouble(line));
        }
        return max;
    }
}
