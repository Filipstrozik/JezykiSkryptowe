import java.util.ArrayList;

public class Min implements AggregateStrategy{

    @Override
    public double compute(ArrayList<String> lines) {
        double min = Double.parseDouble(lines.get(0));
        for (String line : lines) {
            min = Math.min(min, Double.parseDouble(line));
        }
        return min;
    }
}
